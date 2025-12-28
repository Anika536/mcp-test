# MCP Scanner Detection Checklist

Use this checklist to verify your repository is properly configured for MCP scanner detection.

## Pre-Push Checklist

### Required Files
- [ ] `mcp.json` exists in root directory
- [ ] `mcp.yaml` exists in root directory  
- [ ] `package.json` exists with `@modelcontextprotocol/sdk` dependency
- [ ] `requirements.txt` exists with `modelcontextprotocol` package
- [ ] `.mcp/config.json` exists
- [ ] `.mcp/mcp.json` exists

### File Content Verification
- [ ] `mcp.json` contains `mcpServers` key
- [ ] Each server config has `command` field
- [ ] `package.json` has valid JSON syntax
- [ ] `requirements.txt` lists MCP packages
- [ ] Files are UTF-8 encoded

### Git Repository
- [ ] Git repository initialized (`git init`)
- [ ] All files committed (`git add . && git commit`)
- [ ] Branch renamed to `main` (`git branch -M main`)
- [ ] GitHub remote added (`git remote add origin <url>`)
- [ ] Changes pushed to GitHub (`git push -u origin main`)

## Post-Push Checklist

### GitHub Verification (5-10 minutes after push)
- [ ] Repository is public OR token has access to private repos
- [ ] Files visible on GitHub web interface
- [ ] Navigate to repository → Code tab → verify files exist:
  - [ ] `mcp.json` visible
  - [ ] `mcp.yaml` visible
  - [ ] `package.json` visible
  - [ ] `.mcp/` directory visible

### GitHub Search Test
- [ ] Go to your repository on GitHub
- [ ] Press `/` to open search
- [ ] Search for `mcpServers` - should find matches
- [ ] Search for `@modelcontextprotocol` - should find matches
- [ ] Search for `filename:mcp.json` - should find file

### Scanner Token Setup
- [ ] Created GitHub Personal Access Token
- [ ] Token has `repo` scope enabled
- [ ] Token has `read:org` scope enabled
- [ ] Token saved securely

### Scanner Test (10-15 minutes after push)
- [ ] Visit https://apisec-inc.github.io/mcp-audit/
- [ ] Click "GitHub" source tile
- [ ] Paste GitHub token
- [ ] Click "Connect to GitHub"
- [ ] Select your organization/user from dropdown
- [ ] Click "Scan Repositories"
- [ ] Wait for scan to complete

## Expected Results

### Scanner Should Find:
- **Total MCPs:** 3
- **Known MCPs:** 3 (or 0 if not in scanner registry yet)
- **Unknown MCPs:** 0 (or 3 if not in scanner registry yet)
- **Repositories Scanned:** 1

### MCP Servers Detected:
1. **mcp-test-server**
   - Source: `mcp-test-server`
   - Type: `command`
   - Risk: Low

2. **mcp-test-python**
   - Source: `python server.py`
   - Type: `python`
   - Risk: Low

3. **mcp-test-uv**
   - Source: `uvx mcp-test-server`
   - Type: `python`
   - Risk: Low

### Files Detected In:
- [ ] `mcp.json`
- [ ] `mcp.yaml`
- [ ] `.mcp/config.json`

### Dependencies Detected:
- [ ] `@modelcontextprotocol/sdk` from `package.json`
- [ ] `modelcontextprotocol` from `requirements.txt`

## Troubleshooting

### ❌ "No MCPs Found"

**Likely Causes:**
1. GitHub search index not updated yet
   - ✅ Wait 15-30 minutes, try again
   
2. Repository is private and token doesn't have access
   - ✅ Make repository public OR
   - ✅ Regenerate token with correct scopes

3. Files not committed/pushed
   - ✅ Run `git status` to check
   - ✅ Commit and push any changes

4. File syntax errors
   - ✅ Validate JSON files at jsonlint.com
   - ✅ Check for typos in `mcpServers` key

### ❌ Token Connection Failed

**Likely Causes:**
1. Incorrect token format
   - ✅ Token should start with `ghp_`
   - ✅ Regenerate if unsure

2. Missing scopes
   - ✅ Token needs `repo` and `read:org`
   - ✅ Create new token with correct scopes

3. Token expired
   - ✅ Check token expiration date
   - ✅ Create new token if expired

### ❌ Scanner Finds 0 MCPs but Files Exist

**Likely Causes:**
1. GitHub search API rate limit
   - ✅ Wait 1 hour, try again
   
2. Repository too new
   - ✅ GitHub needs time to index (up to 30 min)
   
3. Organization visibility settings
   - ✅ Check org settings allow code search
   
4. Files in gitignore
   - ✅ Ensure `.mcp/` not in `.gitignore`
   - ✅ Check files are actually committed

## Quick Verification Commands

```bash
# Verify files are committed
git ls-files | grep -E '(mcp\.json|mcp\.yaml|package\.json|requirements\.txt|\.mcp)'

# Check git status
git status

# Verify remote
git remote -v

# Check current branch
git branch --show-current

# View last commit
git log -1 --oneline
```

## Success Indicators

✅ **Scanner successfully detected your MCP servers when:**
- Scan completes without errors
- Results section appears (not "No MCPs Found")
- At least 3 MCP servers listed
- File paths point to your repository
- Risk levels displayed

## Next Steps After Successful Scan

1. **Export Results**
   - Click "Export JSON" for detailed analysis
   - Click "Export CSV" for spreadsheet
   - Click "Export Markdown" for documentation

2. **Verify Detection Patterns**
   - Check which files scanner found MCPs in
   - Verify all configuration files detected
   - Confirm dependency detection working

3. **Test with Updates**
   - Modify `mcp.json` to add another server
   - Push changes
   - Rescan to verify updates detected

---

**Status:** [ ] All checks passed  
**Date Tested:** _____________  
**Scanner Version:** _____________  
**MCPs Found:** _____________  
**Notes:** _____________________________________________
