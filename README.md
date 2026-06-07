<!-- mcp-name: io.github.CSOAI-ORG/mcp-spec-compliance-mcp -->
[![MCP Scorecard: 93/100](https://img.shields.io/badge/proofof.ai-93%2F100-5b21b6)](https://proofof.ai/scorecard/mcp-spec-compliance-mcp.html)

mcp-name: io.github.CSOAI-ORG/mcp-spec-compliance-mcp

# MCP Spec Compliance MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Compliant-22c55e)](https://councilof.ai)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Install-3775a9)](https://pypi.org/project/mcp_spec_compliance_mcp/)

> MCP Spec Compliance MCP - audits any MCP server

MCP Spec Compliance MCP - audits any MCP server.json against the official spec. HMAC-signed conformity reports. MIT. By MEOK AI Labs.

---

## 🚀 Quick Start

```bash
# Install via pip
pip install mcp_spec_compliance_mcp

# Or install via Smithery
npx -y @smithery/cli@latest install mcp-spec-compliance-mcp --client claude
```

## ✨ Features

- MCP protocol compliant
- Easy installation
- Well-documented API
- Production-ready
- Active maintenance

## 📖 Documentation

- [Full Documentation](https://docs.meok.ai/mcp-spec-compliance-mcp)
- [API Reference](https://api.meok.ai)
- [EU AI Act Compliance Guide](https://councilof.ai/compliance)

## 🛡️ Compliance

This MCP server is built with **EU AI Act compliance** built-in:

- ✅ Article 9 — Risk Management System
- ✅ Article 13 — Transparency & Instructions for Use
- ✅ Article 15 — Bias Detection & Testing
- ✅ Article 26 — FRIA Support (where applicable)
- ✅ Article 50 — AI Content Watermarking (where applicable)

Need help getting compliant? **[Book a free 15-min diagnostic →](https://cal.com/csoai/august-audit)**

## 🏢 Enterprise

Need custom development, SLA guarantees, or white-label deployment?

- **Pro:** $99/mo — Full MCP suite + EU AI Act tracking
- **Enterprise:** $499/mo — Custom dev + SLA + Dedicated support

[View Pricing →](https://councilof.ai/pricing) | [Contact Sales →](mailto:sales@csoai.org)

## 🤝 Part of the MEOK Ecosystem

This server is part of the **[MEOK AI Labs](https://meok.ai)** ecosystem — 300+ MCP servers for sovereign AI governance.

| Domain | Purpose |
|--------|---------|
| [councilof.ai](https://councilof.ai) | EU AI Act compliance marketplace |
| [safetyof.ai](https://safetyof.ai) | AI safety & monitoring |
| [meok.ai](https://meok.ai) | Sovereign AI platform |
| [cobolbridge.ai](https://cobolbridge.ai) | Legacy modernization |

## 📜 License

MIT © [CSOAI-ORG](https://github.com/CSOAI-ORG)

---

<p align="center">
  <sub>Built with 💜 by <a href="https://meok.ai">MEOK AI Labs</a> · UK Companies House 16939677</sub>
</p>
<!-- BUY-LADDER:END -->


## Configuration

Add to your `claude_desktop_config.json` (Claude Desktop) or your MCP client config:

```json
{
  "mcpServers": {
    "mcp-spec-compliance-mcp": {
      "command": "uvx",
      "args": ["mcp-spec-compliance-mcp"]
    }
  }
}
```

Or: `pip install mcp-spec-compliance-mcp` then run the `mcp-spec-compliance-mcp` command (stdio transport).

## Examples

Once configured, ask your assistant, for example:
- "Use `audit_server_json` to …"
- "Use `check_required_fields` to …"
- "Use `check_naming_conventions` to …"
