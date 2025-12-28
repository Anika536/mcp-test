# 📦 Repository Structure & File Guide

Complete breakdown of every file in the MCP Test Server repository and what it does.

## Directory Tree

```
mcp-test/
│
├── 📄 README.md                    # Main repository documentation
├── 📄 QUICK_START.md              # ⚡ START HERE - Scanner in 10 minutes
├── 📄 SCANNER_GUIDE.md            # Detailed scanner detection guide
├── 📄 SCANNER_CHECKLIST.md        # Verification and troubleshooting
├── 📄 LICENSE                      # MIT License
├── 📄 pyproject.toml              # Python project configuration
├── 📄 package.json                # NPM metadata
├── 📄 requirements.txt            # Python dependencies
│
├── 🔧 Core Server Files
│   └── 📄 server.py               # Main MCP server implementation
│
├── 🔍 Scanner Detection Files
│   ├── 📄 mcp.json                # Claude Desktop MCP config
│   ├── 📄 mcp.yaml                # YAML format MCP config
│   ├── 📄 mcp-config.json         # Example client configuration
│   └── .mcp/
│       ├── 📄 config.json         # Hidden config for scanner
│       └── 📄 mcp.json            # MCP metadata
│
├── 🚀 Setup Scripts
│   ├── 📄 setup-github.ps1        # PowerShell setup script (Windows)
│   └── 📄 setup-github.sh         # Bash setup script (Unix/Mac)
│
├── 📚 Examples & Testing
│   ├── examples/
│   │   ├── 📄 README.md
│   │   ├── 📄 test_client.py     # Interactive testing client
│   │   └── 📄 scanner_test.py    # Automated scanner validation
│   └── tests/
│       ├── 📄 __init__.py
│       └── 📄 test_server.py     # Unit tests
│
└── 📝 Configuration & Ignore
    ├── 📄 .gitignore             # Git ignore rules
    └── 📄 .gitattributes         # Git attributes

Total: 25+ files | Size: ~500KB
```

## File Descriptions

### 📖 Documentation Files

#### README.md
**Purpose:** Main repository documentation  
**Used By:** GitHub, developers  
**Contains:** Features, installation, usage, API reference  
**Size:** ~5 KB

#### QUICK_START.md ⚡ **READ THIS FIRST**
**Purpose:** Get scanner working in 10 minutes  
**Used By:** First-time users  
**Contains:** Step-by-step instructions, troubleshooting  
**Size:** ~3 KB

#### SCANNER_GUIDE.md
**Purpose:** Detailed scanner detection information  
**Used By:** Scanner developers, verification  
**Contains:** Detection patterns, expected results, advanced testing  
**Size:** ~4 KB

#### SCANNER_CHECKLIST.md
**Purpose:** Verification and troubleshooting guide  
**Used By:** Quality assurance, problem-solving  
**Contains:** Pre/post-push checklist, error fixes, validation  
**Size:** ~6 KB

### 🔧 Core Server Files

#### server.py
**Purpose:** Main MCP server implementation  
**Language:** Python  
**Features:**
- 6 diverse tools (echo, add_numbers, format_json, etc.)
- 4 resources (text, JSON, markdown, config)
- 2 prompts for testing
- ~600 lines of code

**Key Classes:**
```python
server = Server("mcp-test-server")

@server.list_tools()        # List available tools
@server.call_tool()         # Handle tool calls
@server.list_resources()    # List resources
@server.read_resource()     # Read resource content
@server.list_prompts()      # List prompts
@server.get_prompt()        # Get prompt content
```

### 🔍 Scanner Detection Files

These files are specifically created for scanner detection:

#### mcp.json
**Purpose:** Claude Desktop style MCP configuration  
**Detected By:** Scanner (pattern: `filename:mcp.json`)  
**Format:** JSON  
**Contains:** 3 server definitions with commands
```json
{
  "mcpServers": {
    "mcp-test-server": {...},
    "mcp-test-python": {...},
    "mcp-test-uv": {...}
  }
}
```

#### mcp.yaml
**Purpose:** YAML format MCP configuration  
**Detected By:** Scanner (pattern: `filename:mcp.yaml`)  
**Format:** YAML  
**Contains:** Server definitions in YAML format

#### .mcp/config.json
**Purpose:** Hidden directory configuration  
**Detected By:** Scanner (pattern: `path:.mcp`)  
**Format:** JSON  
**Contains:** Alternative config format for scanners

#### .mcp/mcp.json
**Purpose:** MCP metadata in hidden directory  
**Format:** JSON  
**Contains:** Version, description, provider info

#### package.json
**Purpose:** NPM project metadata  
**Detected By:** Scanner (pattern: `@modelcontextprotocol filename:package.json`)  
**Contains:**
- `@modelcontextprotocol/sdk` dependency
- Project metadata
- Scripts for testing

#### requirements.txt
**Purpose:** Python dependencies list  
**Detected By:** Scanner (pattern: `modelcontextprotocol filename:requirements.txt`)  
**Contains:**
- `mcp>=0.9.0`
- `modelcontextprotocol>=0.9.0`

#### mcp-config.json
**Purpose:** Example client configuration  
**Used By:** Documentation, client setup  
**Shows:** How to configure clients to use the server

### 🚀 Setup Scripts

#### setup-github.ps1
**Purpose:** Automate GitHub setup (Windows)  
**Language:** PowerShell  
**Does:**
1. Initialize git repository
2. Add GitHub remote
3. Commit and push files
4. Rename branch to main

**Usage:**
```powershell
.\setup-github.ps1
```

#### setup-github.sh
**Purpose:** Automate GitHub setup (Unix/Mac)  
**Language:** Bash  
**Same functionality as PowerShell version

**Usage:**
```bash
bash setup-github.sh
```

### 📚 Testing & Examples

#### examples/test_client.py
**Purpose:** Interactive testing client  
**Demonstrates:**
- Connecting to MCP server
- Calling each tool
- Reading resources
- Listing prompts

**Run:**
```bash
python examples/test_client.py
```

#### examples/scanner_test.py
**Purpose:** Automated scanner validation  
**Tests:**
- Tool discovery (6 tools)
- Resource discovery (4 resources)
- Prompt discovery (2 prompts)
- Schema parsing
- Risk identification

**Run:**
```bash
python examples/scanner_test.py
```

**Output:** `scanner_test_results.json`

#### tests/test_server.py
**Purpose:** Unit tests using pytest  
**Tests:**
- Tool listing
- Tool execution
- Resource reading
- Prompt discovery

**Run:**
```bash
pytest tests/test_server.py -v
```

### 📋 Project Configuration Files

#### pyproject.toml
**Purpose:** Python project configuration  
**Contains:**
- Build system requirements
- Project metadata
- Dependencies (mcp>=0.9.0)
- Optional dev dependencies (pytest, pytest-asyncio)
- Entry point (mcp-test-server command)

#### LICENSE
**Type:** MIT License  
**Purpose:** Open source licensing  
**Allows:** Free use, modification, distribution

#### .gitignore
**Purpose:** Exclude files from git tracking  
**Excludes:**
- Python: `__pycache__/`, `*.pyc`, venv, .pytest_cache
- IDEs: `.vscode/`, `.idea/`
- OS: `.DS_Store`, `Thumbs.db`
- Project: `*.db`, test outputs

## File Relationships

### For Scanner Detection:

```
Scanner Scans GitHub
    ↓
Finds patterns:
    ├── filename:mcp.json          → mcp.json ✓
    ├── filename:mcp.yaml          → mcp.yaml ✓
    ├── path:.mcp                  → .mcp/config.json ✓
    ├── "mcpServers" extension:json → mcp.json ✓
    ├── @modelcontextprotocol ...  → package.json ✓
    └── modelcontextprotocol ...   → requirements.txt ✓
```

### For Testing MCP Server:

```
user/developer
    ↓
pip install .  (installs from pyproject.toml)
    ↓
mcp-test-server  (runs server.py entry point)
    ↓
python examples/test_client.py  (tests functionality)
    ↓
python examples/scanner_test.py  (validates scanning)
```

## Size & Complexity

| Aspect | Details |
|--------|---------|
| Total Files | 25+ |
| Total Size | ~500 KB |
| Python Code | ~800 lines (server.py + examples + tests) |
| Configuration | ~200 lines (JSON, YAML, TOML) |
| Documentation | ~20 KB (guides, checklists, README) |
| Largest File | server.py (~400 lines) |

## Import Dependencies

```python
# server.py requires:
from mcp.server import Server
from mcp.types import (Tool, TextContent, Resource, 
                       ImageContent, EmbeddedResource, ...)
import asyncio
import sys
import json
from datetime import datetime

# examples/test_client.py requires:
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# tests/test_server.py requires:
import pytest
import asyncio
```

## Key Statistics

- **Detection Methods:** 6+ patterns detected
- **MCP Servers:** 3 server definitions
- **Tools:** 6 different tools
- **Resources:** 4 resource types
- **Prompts:** 2 example prompts
- **Configuration Formats:** 3 (JSON, YAML, hidden)
- **Languages Supported:** Python, YAML, JSON
- **Test Coverage:** Tools, resources, prompts, scanning

---

**Pro Tip:** Start with QUICK_START.md, then reference this guide for details about specific files.
