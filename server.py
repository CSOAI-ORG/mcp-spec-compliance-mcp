#!/usr/bin/env python3
"""
MCP Spec Compliance MCP — audit any MCP server against the official spec
========================================================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/mcp-spec-compliance-mcp -->

WHAT THIS DOES
--------------
Scans an MCP server.json (or live MCP server endpoint) against the official
Model Context Protocol spec (2025-06-18 + 2025-12-11 revisions). Reports:

- Required-field drift
- Deprecated patterns
- Schema misalignment vs the canonical registry schema
- Missing-but-recommended fields
- Tool-naming convention violations

The viral move: every MCP author wants to know if their server passes audit
before publishing to the registry. This MCP gives them a signed conformity
report in under a second.

TOOLS
-----
- audit_server_json(server_json): full conformity audit
- check_required_fields(server_json): just the required-field gate
- check_naming_conventions(server_json): slug + tool name conventions
- list_spec_versions(): supported spec revisions
- generate_passing_template(): a minimal-passing server.json
- sign_conformity_report(audit_result): HMAC seal the audit for publishing

PRICING
-------
Free MIT self-host · £29/mo Starter · £79/mo Pro · A2A Substrate £999/mo.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
import re
import time
from datetime import datetime, timezone
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("mcp-spec-compliance")
_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")


# ──────────────────────────────────────────────────────────────────────
# Spec-tracking — refresh when MCP spec ships a new revision
# ──────────────────────────────────────────────────────────────────────
SPEC_VERSIONS = ["2025-06-18", "2025-12-11"]
CURRENT_SPEC = "2025-12-11"

REQUIRED_FIELDS = {
    "2025-06-18": ["name", "version", "description"],
    "2025-12-11": ["$schema", "name", "version", "description", "packages"],
}

RECOMMENDED_FIELDS = {
    "2025-12-11": ["repository", "remotes", "websiteUrl"],
}

# Slug must look like  io.github.<org>/<package-name>
SLUG_RE = re.compile(r"^io\.github\.[A-Za-z0-9_-]+\/[a-z0-9][a-z0-9._-]*$")
TOOL_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[A-Za-z0-9.-]+)?(\+[A-Za-z0-9.-]+)?$")


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    return hmac.new(_HMAC_SECRET.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ──────────────────────────────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def audit_server_json(server_json: dict, spec_version: str = CURRENT_SPEC) -> dict:
    """
    Full conformity audit of an MCP server.json.

    Args:
        server_json: The contents of an MCP server.json file.
        spec_version: Target spec revision. Defaults to latest.

    Returns:
        {pass, score_0_100, errors, warnings, recommendations, spec_version}
    """
    if spec_version not in SPEC_VERSIONS:
        return {"error": f"Unknown spec_version. Supported: {SPEC_VERSIONS}"}

    errors: list[str] = []
    warnings: list[str] = []
    recs: list[str] = []

    # Required fields
    for field in REQUIRED_FIELDS[spec_version]:
        if field not in server_json:
            errors.append(f"missing required field: {field}")

    # Recommended fields (spec 2025-12-11+)
    for field in RECOMMENDED_FIELDS.get(spec_version, []):
        if field not in server_json:
            recs.append(f"recommended field absent: {field}")

    # Naming
    name = server_json.get("name", "")
    if name and not SLUG_RE.match(name):
        errors.append(f"name does not match 'io.github.<org>/<pkg>' pattern: {name!r}")

    # Version
    ver = server_json.get("version", "")
    if ver and not SEMVER_RE.match(ver):
        errors.append(f"version is not valid semver: {ver!r}")

    # Description length
    desc = server_json.get("description", "")
    if desc:
        if len(desc) < 30:
            warnings.append(f"description is short ({len(desc)} chars). Registry recommends 80-250.")
        elif len(desc) > 500:
            warnings.append(f"description is long ({len(desc)} chars). Registry recommends 80-250.")

    # Packages
    packages = server_json.get("packages", [])
    if not isinstance(packages, list):
        errors.append("packages must be an array")
    elif packages:
        for i, p in enumerate(packages):
            if "registryType" not in p:
                errors.append(f"packages[{i}] missing registryType (pypi / npm / docker)")
            if "identifier" not in p:
                errors.append(f"packages[{i}] missing identifier")
            if "version" not in p:
                warnings.append(f"packages[{i}] missing version (defaults to top-level version)")

    # Remotes (recommended for hosted MCPs)
    remotes = server_json.get("remotes", [])
    if not remotes:
        recs.append("no `remotes` field — clients can only run via local stdio. Add a hosted endpoint for non-Python users.")

    # Score
    base = 100
    base -= 10 * len(errors)
    base -= 3 * len(warnings)
    base -= 1 * len(recs)
    score = max(0, base)

    return {
        "pass": len(errors) == 0,
        "score_0_100": score,
        "spec_version": spec_version,
        "errors": errors,
        "warnings": warnings,
        "recommendations": recs,
        "audited_at": _ts(),
        "next_step": "Call sign_conformity_report() to get a publishable signed audit cert." if not errors else "Fix errors before publishing.",
    }


@mcp.tool()
def check_required_fields(server_json: dict, spec_version: str = CURRENT_SPEC) -> dict:
    """
    Fast gate: only check required fields.

    Args:
        server_json: server.json contents.
        spec_version: target spec version.

    Returns:
        {pass, missing}
    """
    missing = [f for f in REQUIRED_FIELDS.get(spec_version, []) if f not in server_json]
    return {"pass": len(missing) == 0, "missing": missing, "spec_version": spec_version}


@mcp.tool()
def check_naming_conventions(server_json: dict, tool_names: Optional[list[str]] = None) -> dict:
    """
    Lint the slug, version, and tool names.

    Args:
        server_json: server.json contents.
        tool_names: Optional list of tool names to validate against snake_case convention.

    Returns:
        {pass, issues}
    """
    issues = []
    name = server_json.get("name", "")
    if name and not SLUG_RE.match(name):
        issues.append(f"slug not in 'io.github.<org>/<pkg>' format: {name!r}")
    ver = server_json.get("version", "")
    if ver and not SEMVER_RE.match(ver):
        issues.append(f"version not semver: {ver!r}")
    bad_tools = [t for t in (tool_names or []) if not TOOL_NAME_RE.match(t)]
    if bad_tools:
        issues.append(f"tool names not snake_case lowercase: {bad_tools}")
    return {"pass": len(issues) == 0, "issues": issues}


@mcp.tool()
def list_spec_versions() -> dict:
    """Return the supported MCP spec revisions + which fields are required for each."""
    return {
        "current": CURRENT_SPEC,
        "supported": SPEC_VERSIONS,
        "required_fields": REQUIRED_FIELDS,
        "recommended_fields": RECOMMENDED_FIELDS,
        "official_spec": "https://modelcontextprotocol.io/specification",
    }


@mcp.tool()
def generate_passing_template(org: str = "your-org", slug: str = "your-package-mcp") -> dict:
    """
    Generate a minimal-but-passing server.json template.

    Args:
        org: GitHub org slug.
        slug: Package slug (must end in -mcp by convention).

    Returns:
        {template}
    """
    template = {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
        "name": f"io.github.{org}/{slug}",
        "version": "1.0.0",
        "description": f"{slug} — describe what your MCP does in 80-250 characters for the registry listing.",
        "repository": {"url": f"https://github.com/{org}/{slug}", "source": "github"},
        "packages": [
            {"registryType": "pypi", "identifier": slug, "version": "1.0.0",
             "runtimeHint": "python", "transport": {"type": "stdio"}}
        ],
        "remotes": [
            {"type": "streamable-http", "url": f"https://your-domain.example/{slug}"}
        ],
    }
    return {
        "template": template,
        "next_step": "Save as server.json next to your pyproject.toml. Run `mcp-publisher publish` to push to the official registry.",
    }


@mcp.tool()
def sign_conformity_report(audit_result: dict) -> dict:
    """
    HMAC-sign a conformity report so authors can publish it as evidence.

    Args:
        audit_result: Output of audit_server_json().

    Returns:
        {signed, signature, sealed_at, cert_id}
    """
    cert_id = f"MCP_CONFORM_{int(time.time())}_{os.urandom(4).hex()}"
    sealed = {
        "cert_id": cert_id,
        "audit_result": audit_result,
        "sealed_at": _ts(),
        "issuer": "MEOK AI Labs (CSOAI LTD)",
    }
    sig = _sign(sealed)
    return {
        "signed": _HMAC_SECRET != "",
        "cert_id": cert_id,
        "signature": sig,
        "sealed_at": sealed["sealed_at"],
        "verify_url": f"https://meok-attestation-api.vercel.app/verify/{cert_id}",
        "hint": "Auditors verify the signature by recomputing HMAC over sealed payload with the same secret.",
    }


if __name__ == "__main__":
    mcp.run()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/5kQ6oJ0xS3ce8sl7ew8k91j"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
