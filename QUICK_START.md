# 🚀 Quick Start: Push to GitHub and Test Scanner

Follow these steps to get your MCP test repository scanned in under 10 minutes.

## Step 1: Push to GitHub (2 minutes)

### Option A: Using PowerShell (Windows)
```powershell
# Run the setup script
.\setup-github.ps1

# When prompted, enter your GitHub repo URL:
# https://github.com/YOUR-USERNAME/mcp-test.git

# Then push:
git push -u origin main
```

### Option B: Manual Setup
```bash
# Initialize and commit
git init
git add .
git commit -m "Initial commit: MCP test server for scanner testing"
git branch -M main

# Add your GitHub remote
git remote add origin https://github.com/YOUR-USERNAME/mcp-test.git

# Push
git push -u origin main
```

## Step 2: Create GitHub Token (1 minute)

1. Go to: https://github.com/settings/tokens/new
2. Fill in:
   - **Description:** `MCP Audit Scanner`
   - **Expiration:** 7 days (or longer)
   - **Scopes:** ✅ `repo` and ✅ `read:org`
3. Click "Generate token"
4. **Copy the token** (starts with `ghp_`)

## Step 3: Wait for Indexing (5-10 minutes)

⏱️ GitHub needs time to index your repository for code search.

**While waiting, verify on GitHub:**
1. Go to your repository
2. Check files are visible:
   - ✅ `mcp.json`
   - ✅ `mcp.yaml`
   - ✅ `package.json`
   - ✅ `.mcp/` directory

## Step 4: Run Scanner (2 minutes)

1. **Open scanner:** https://apisec-inc.github.io/mcp-audit/

2. **Connect:**
   - Click **GitHub** tile
   - Paste your token
   - Click **Connect to GitHub**

3. **Scan:**
   - Select your username/organization from dropdown
   - Click **Scan Repositories**
   - Wait for progress bar to complete

## Expected Results

### ✅ Successful Scan Shows:

```
📊 Scan Results
===============
MCPs Found: 3
Repositories: 1
Known MCPs: 3 (or 0 if not in registry)
```

### 📋 MCP Servers Detected:

| MCP Name | Source | File |
|----------|--------|------|
| mcp-test-server | mcp-test-server | mcp.json |
| mcp-test-python | python server.py | mcp.json |
| mcp-test-uv | uvx mcp-test-server | mcp.json |

## Troubleshooting

### ❌ "No MCPs Found"

**Try these in order:**

1. **Wait longer** (up to 30 minutes for GitHub indexing)

2. **Make repository public:**
   ```bash
   # On GitHub: Settings → General → Danger Zone → Change visibility
   ```

3. **Verify files on GitHub:**
   - Visit your repo on GitHub
   - Press `/` and search for `mcpServers`
   - Should find matches in `mcp.json` and `mcp.yaml`

4. **Check token scopes:**
   - Regenerate token with `repo` + `read:org` scopes
   - Try scanner again

5. **Manual GitHub search test:**
   ```
   # In GitHub search bar:
   repo:YOUR-USERNAME/mcp-test mcpServers
   
   # Should return: mcp.json, mcp.yaml
   ```

### ❌ Token Connection Failed

- Verify token starts with `ghp_`
- Create new token with correct scopes
- Check token hasn't expired

### ❌ Scanner Timeout

- Try at a different time (GitHub API rate limits)
- Ensure stable internet connection

## What the Scanner Tests

The scanner validates it can detect:

✅ **Configuration Files:**
- `mcp.json` (Claude Desktop format)
- `mcp.yaml` (YAML format)
- `.mcp/config.json` (hidden directory)

✅ **Dependencies:**
- `@modelcontextprotocol/sdk` in `package.json`
- `modelcontextprotocol` in `requirements.txt`

✅ **Search Patterns:**
- `filename:mcp.json`
- `filename:mcp.yaml`
- `path:.mcp`
- `"mcpServers" extension:json`
- Package dependencies

## Next Steps

### After Successful Detection:

1. **Export results** to analyze detection methods
2. **Read** [SCANNER_GUIDE.md](SCANNER_GUIDE.md) for details
3. **Review** [SCANNER_CHECKLIST.md](SCANNER_CHECKLIST.md) for verification
4. **Test** the actual MCP server functionality:
   ```bash
   pip install .
   python examples/test_client.py
   ```

### To Help Others:

If the scanner successfully found your MCPs, consider:
- Sharing this template
- Contributing detection patterns
- Reporting scanner issues on GitHub

## Quick Reference

| Item | Value |
|------|-------|
| Scanner URL | https://apisec-inc.github.io/mcp-audit/ |
| Token Scopes | `repo`, `read:org` |
| Expected MCPs | 3 |
| Detection Files | 6+ |
| Wait Time | 5-30 minutes |

---

**Need Help?**
- 📖 Detailed guide: [SCANNER_GUIDE.md](SCANNER_GUIDE.md)
- ✅ Verification checklist: [SCANNER_CHECKLIST.md](SCANNER_CHECKLIST.md)
- 🐛 Scanner issues: https://github.com/apisec-inc/mcp-audit/issues
