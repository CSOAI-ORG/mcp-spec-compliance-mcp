# MCP Spec Compliance MCP

> ## 🧱 Part of the MEOK Governance Substrate (£499/mo)
> See [meok.ai/docs](https://meok.ai/docs) and [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry).

# Audit any MCP server.json against the official Model Context Protocol spec

<!-- mcp-name: io.github.CSOAI-ORG/mcp-spec-compliance-mcp -->

[![PyPI](https://img.shields.io/pypi/v/mcp-spec-compliance-mcp)](https://pypi.org/project/mcp-spec-compliance-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What this does

Lints any `server.json` against the official MCP spec — required field gate, semver, slug pattern, recommended fields, deprecated patterns, naming conventions. Returns a numeric conformity score 0–100 and an HMAC-signed report you can publish next to your registry submission.

The meta-viral move: every MCP author wants to know if their server passes audit **before** pushing to the official registry.

## Tools

| Tool | Purpose |
|---|---|
| `audit_server_json(server_json, spec_version?)` | Full audit with score + errors + warnings |
| `check_required_fields(server_json, spec_version?)` | Fast gate — required fields only |
| `check_naming_conventions(server_json, tool_names?)` | Slug + semver + tool-name lint |
| `list_spec_versions()` | Supported spec revisions |
| `generate_passing_template(org, slug)` | Minimal-passing server.json template |
| `sign_conformity_report(audit_result)` | HMAC-signed publishable cert |

## Why this exists

The official MCP Registry rejects submissions with missing required fields. Many submissions fail because authors don't realise `$schema` is required as of 2025-12-11. This MCP catches that before you push.

## Sister MCPs

- `agent-replay-debugger-mcp` — debug your own MCP runs
- `oasf-agent-directory-mcp` — once you pass spec compliance, publish to the Cisco AGNTCY directory too
- `agent-prompt-injection-firewall-mcp` — scan your tool inputs against OWASP LLM01

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Pricing

| Option | Price |
|---|---|
| Self-host MIT | £0 |
| Universal PAYG | £29/mo + £0.0002/call |
| Governance Substrate | £499/mo |
| A2A Substrate | £999/mo |
| Defence | £4,990/mo |

Buy: https://meok.ai/governance

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677).

<!-- BUY-LADDER:START -->

## 💸 Try MEOK in 30 seconds — instant buy ladder

| Tier | Price | What you get | Stripe |
|---|---|---|---|
| Smoke test | **£1** | Signed sample MCP-Hardening report + Article 50 PDF | <https://buy.stripe.com/dRmcN75ScdQS7oh1Uc8k90U> |
| Quick Kit | **£9** | EU AI Act Article 50 implementation guide (C2PA + EU-Icon) | <https://buy.stripe.com/cNi00la8s1460ZT0Q88k90V> |
| Founder Call | **£29** | 30-min 1-on-1 with the founder | <https://buy.stripe.com/8x228ta8s6oqbExaqI8k90W> |

> Refundable. UK Stripe — VAT-clean. Builds on the 81-MCP MEOK fleet.
> Verify any signed report at <https://meok.ai/verify>.

<!-- BUY-LADDER:END -->

