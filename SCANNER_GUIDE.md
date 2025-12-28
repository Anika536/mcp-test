# MCP Scanner Detection Guide

This repository is configured to be **fully detectable** by the [APIsec MCP Audit Scanner](https://apisec-inc.github.io/mcp-audit/).

## Scanner Detection Points

The MCP scanner will detect this repository through multiple patterns:

### ✅ Configuration Files
- **mcp.json** - Root level MCP configuration (Claude Desktop style)
- **mcp.yaml** - YAML format MCP configuration
- **.mcp/config.json** - Hidden directory MCP config
- **.mcp/mcp.json** - MCP metadata in hidden directory

### ✅ Dependency Files
- **package.json** - Contains `@modelcontextprotocol/sdk` dependency
- **requirements.txt** - Contains `modelcontextprotocol` package
- **pyproject.toml** - Python project with mcp dependencies

### ✅ Scanner Search Patterns Matched
1. `filename:mcp.json` ✓
2. `filename:mcp.yaml` ✓
3. `path:.mcp` ✓
4. `"mcpServers" extension:json` ✓
5. `@modelcontextprotocol filename:package.json` ✓
6. `modelcontextprotocol filename:requirements.txt` ✓

## How to Test Scanner Detection

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: MCP test server for scanner testing"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Wait for GitHub Indexing
GitHub's code search index may take **5-10 minutes** to index new repositories.

### 3. Scan with APIsec MCP Audit
1. Visit https://apisec-inc.github.io/mcp-audit/
2. Click on **GitHub** source
3. Create a [GitHub Personal Access Token](https://github.com/settings/tokens/new?description=MCP%20Audit&scopes=repo,read:org)
   - Required scopes: `repo` and `read:org`
4. Connect to GitHub with your token
5. Select your organization or user account
6. Click **Scan Repositories**

### Expected Scanner Results

The scanner should find **3 MCP servers** in this repository:

| MCP Name | Source | Type | Description |
|----------|--------|------|-------------|
| mcp-test-server | mcp-test-server | command | Direct command execution |
| mcp-test-python | python server.py | python | Python script execution |
| mcp-test-uv | uvx mcp-test-server | python | UV package manager execution |

### Scanner Detection Details

**Risk Level:** Low  
**Provider:** Community  
**Known:** Yes (if in scanner's registry)  
**Verified:** True  
**Type:** Testing/Development  

**Capabilities:**
- ✓ Tools (6 tools)
- ✓ Resources (4 resources)
- ✓ Prompts (2 prompts)

## Troubleshooting Scanner Detection

### Scanner Shows "No MCPs Found"?

1. **Repository is Private**
   - Ensure your GitHub token has access to private repos if needed
   - Or make the repository public

2. **GitHub Index Not Updated**
   - Wait 10-15 minutes after pushing
   - Try the scanner's "Direct Repository Scan" (Phase 1)
   
3. **Token Permissions**
   - Verify token has `repo` and `read:org` scopes
   - Regenerate token if unsure

4. **File Encoding**
   - Ensure files are UTF-8 encoded
   - Check files are properly committed and pushed

5. **Search API Limitations**
   - GitHub code search has rate limits
   - Try scanning at different times

### Verify Files Are on GitHub

Check your repository has these files:
```bash
# View repository structure
git ls-files

# Should show:
# mcp.json
# mcp.yaml
# package.json
# requirements.txt
# .mcp/config.json
# .mcp/mcp.json
```

### Manual Verification on GitHub

1. Go to your repository on GitHub
2. Use GitHub's search: press `/` and search for:
   - `mcpServers`
   - `@modelcontextprotocol`
   - `filename:mcp.json`
3. If files appear in search, scanner should detect them

## Scanner Features Tested

This repository tests the scanner's ability to:

- ✅ Detect configuration files (`mcp.json`, `mcp.yaml`)
- ✅ Find hidden directories (`.mcp/`)
- ✅ Parse npm dependencies (`package.json`)
- ✅ Parse Python dependencies (`requirements.txt`)
- ✅ Identify multiple MCP server configurations
- ✅ Extract command types (direct, python, uvx)
- ✅ Recognize MCP capabilities
- ✅ Calculate risk levels

## Integration with Scanner Registry

The scanner maintains a registry of known MCPs. To get your server recognized:

1. **Add to Scanner Registry** - Submit PR to scanner's known MCPs list
2. **Use Standard Naming** - Prefix with `mcp-server-*` or `@org/mcp-*`
3. **Provide Metadata** - Include clear descriptions and risk assessments

## For Scanner Developers

This repository is ideal for:
- Testing scanner detection accuracy
- Validating multi-format support (JSON/YAML)
- Testing dependency parsing
- Benchmarking scan performance
- Demonstrating proper MCP configuration

### Test Cases Covered
- ✓ Multiple configuration formats
- ✓ Multiple execution methods
- ✓ Nested directory structures
- ✓ npm and Python ecosystems
- ✓ Standard MCP capabilities
- ✓ Proper metadata structure

## Questions?

If the scanner still doesn't detect this repository:
1. Check the [scanner's GitHub issues](https://github.com/apisec-inc/mcp-audit/issues)
2. Verify your repository is public or token has access
3. Wait for GitHub's search index to update (can take up to 30 minutes)
4. Try the Local System Audit tab if testing locally

---

**Repository Status:** ✅ Scanner Ready  
**Detection Methods:** 6+  
**Expected MCP Count:** 3  
**Risk Level:** Low (Testing/Development)
