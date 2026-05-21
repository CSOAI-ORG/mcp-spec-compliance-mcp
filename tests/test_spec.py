"""Smoke tests for mcp-spec-compliance-mcp."""
import sys, os, inspect, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    audit_server_json,
    check_required_fields,
    check_naming_conventions,
    list_spec_versions,
    generate_passing_template,
    sign_conformity_report,
)


def test_audit_passes_clean_server_json():
    sj = {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
        "name": "io.github.example/example-mcp",
        "version": "1.0.0",
        "description": "An example MCP server that does some example things and demonstrates a real description length suitable for the registry.",
        "repository": {"url": "https://github.com/example/example-mcp", "source": "github"},
        "packages": [
            {"registryType": "pypi", "identifier": "example-mcp", "version": "1.0.0",
             "runtimeHint": "python", "transport": {"type": "stdio"}}
        ],
        "remotes": [{"type": "streamable-http", "url": "https://example.com/v1/mcp"}],
    }
    r = audit_server_json(sj)
    assert r["pass"] is True
    assert r["score_0_100"] >= 95


def test_audit_catches_missing_required():
    r = audit_server_json({"name": "io.github.x/y-mcp"})
    assert r["pass"] is False
    assert len(r["errors"]) >= 2  # missing description + version + packages


def test_audit_catches_bad_slug():
    sj = {
        "$schema": "x",
        "name": "not-a-registry-slug",
        "version": "1.0.0",
        "description": "x" * 120,
        "packages": [{"registryType": "pypi", "identifier": "y", "version": "1.0.0"}],
    }
    r = audit_server_json(sj)
    assert any("io.github" in e for e in r["errors"])


def test_audit_catches_bad_version():
    sj = {
        "$schema": "x",
        "name": "io.github.x/y-mcp",
        "version": "not-semver",
        "description": "x" * 120,
        "packages": [{"registryType": "pypi", "identifier": "y", "version": "1.0.0"}],
    }
    r = audit_server_json(sj)
    assert any("semver" in e for e in r["errors"])


def test_audit_warns_short_description():
    sj = {
        "$schema": "x",
        "name": "io.github.x/y-mcp",
        "version": "1.0.0",
        "description": "short",
        "packages": [{"registryType": "pypi", "identifier": "y", "version": "1.0.0"}],
    }
    r = audit_server_json(sj)
    assert any("description is short" in w for w in r["warnings"])


def test_check_required_fields_returns_missing():
    r = check_required_fields({"name": "x"})
    assert r["pass"] is False
    assert "version" in r["missing"]
    assert "description" in r["missing"]


def test_check_naming_lints_slug_and_tools():
    sj = {"name": "wrong-slug", "version": "1.x"}
    r = check_naming_conventions(sj, tool_names=["GoodName", "ok_name"])
    assert r["pass"] is False
    assert any("slug" in i for i in r["issues"])
    assert any("snake_case" in i for i in r["issues"])


def test_list_spec_versions_has_current():
    r = list_spec_versions()
    assert r["current"] == "2025-12-11"
    assert "2025-12-11" in r["supported"]


def test_generate_passing_template_passes_its_own_audit():
    t = generate_passing_template("acme", "acme-test-mcp")
    audit = audit_server_json(t["template"])
    assert audit["pass"] is True


def test_sign_conformity_report_emits_cert():
    audit = {"pass": True, "score_0_100": 100, "errors": [], "warnings": []}
    r = sign_conformity_report(audit)
    assert r["cert_id"].startswith("MCP_CONFORM_")
    assert "verify_url" in r


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    p = f = 0
    for fn in fns:
        try:
            fn(); print(f"OK {fn.__name__}"); p += 1
        except Exception as e:
            print(f"X  {fn.__name__}: {type(e).__name__}: {e}"); traceback.print_exc(); f += 1
    print(f"\n{p} passed, {f} failed")
