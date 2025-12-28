# GitHub Repository Best Practices for MCP Scanner Detection

## Repository Settings Recommendations

### Public vs Private
- **Recommended:** Public repository (easiest scanner detection)
- **Why:** Public repos are searchable by default
- **For private repos:** Token must have repository access

### Repository Description
Add in GitHub Settings:

```
Comprehensive MCP server for testing and validating MCP scanners. 
Includes 6 tools, 4 resources, 2 prompts, and scanner detection files.
```

### Repository Topics
Add in GitHub Settings → Topics:
- `mcp`
- `model-context-protocol`
- `testing`
- `scanner`
- `anthropic`

### README Frontmatter
At the top of your README, add:

```markdown
# MCP Test Server

[![Scanner Compatible](https://img.shields.io/badge/Scanner-Compatible-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)]()

> Comprehensive MCP server for testing MCP scanners and validating MCP implementations
```

## File Visibility on GitHub

### Ensure Files Are Visible

**Files that MUST be visible:**
1. ✅ `mcp.json` - in root
2. ✅ `mcp.yaml` - in root  
3. ✅ `package.json` - in root
4. ✅ `requirements.txt` - in root

**Verify visibility:**
1. Go to your repo on GitHub
2. Click "Code" tab
3. Scroll down file list - should see all config files
4. Click on `.mcp` folder - should see config.json inside

### Handle .gitignore Correctly

**WARNING:** Make sure `.mcp/` directory is NOT in `.gitignore`

**Check:**
```bash
cat .gitignore | grep mcp
# Should return nothing (empty)
```

**If you see `.mcp`, remove it:**
```bash
# Edit .gitignore and remove any line with ".mcp"
git add .gitignore
git commit -m "Remove .mcp from gitignore for scanner detection"
git push
```

## Optimizing for Scanner Detection

### 1. File Naming Conventions
Use standard MCP naming:
- ✅ `mcp.json` (not `mcp-config.json`)
- ✅ `mcp.yaml` (not `mcp-configuration.yaml`)
- ✅ `.mcp/config.json` (standard hidden directory)

### 2. JSON Format
Ensure valid JSON in all `.json` files:
```bash
# Validate with jq (if installed)
jq . mcp.json

# Or use online: https://jsonlint.com
```

### 3. UTF-8 Encoding
Files should be UTF-8 encoded:
```bash
# Check file encoding
file -i mcp.json
# Should show: UTF-8 Unicode text
```

### 4. mcpServers Key
Ensure `mcpServers` (not `mcpservers` or `MCP_SERVERS`):
```json
{
  "mcpServers": {        // ← Exact case matters
    "server-name": {...}
  }
}
```

## GitHub Search Verification

Before running the scanner, verify GitHub's search can find your files:

### Search Test 1: MCP Files
```
On GitHub, press "/" and search:
repo:YOUR-USERNAME/YOUR-REPO filename:mcp.json

Should find: mcp.json, mcp.yaml
```

### Search Test 2: mcpServers
```
repo:YOUR-USERNAME/YOUR-REPO mcpServers

Should find: mcp.json, mcp.yaml
```

### Search Test 3: Dependencies
```
repo:YOUR-USERNAME/YOUR-REPO @modelcontextprotocol filename:package.json

Should find: package.json
```

## Waiting for GitHub Indexing

### Timeline
- **Immediately:** Files visible on GitHub web UI
- **5-10 minutes:** Code search index starts updating
- **15-30 minutes:** Full search indexing complete
- **30+ minutes:** Cache clearing, full visibility

### How to Check Indexing Status
1. Wait 5-10 minutes after pushing
2. Go to your repo
3. Use GitHub search (press `/`)
4. Search for `filename:mcp.json`
5. If found = indexed and ready for scanner

### If Not Indexed After 30 Minutes
1. Check file is actually committed: `git log --oneline`
2. Verify file is not in `.gitignore`
3. Check file encoding is UTF-8
4. Try a different search: `mcpServers` or `@modelcontextprotocol`

## Branch & Tag Strategy

### Main Branch
- Scanner looks for config on default branch
- Default is usually `main` (modern standard)
- Rename if needed: `git branch -M main`

### Tags (Optional)
Add a release tag for versions:
```bash
git tag -a v0.1.0 -m "Initial MCP test server"
git push origin v0.1.0
```

## Collaboration & Access

### For Organization Repositories
If part of an organization:

1. **Org Visibility Settings**
   - Settings → Visibility → Ensure code search enabled
   - Settings → Access → Token should have `read:org` access

2. **Repository Permissions**
   - User should have `read` access minimum
   - Token should have `repo` scope

3. **Branch Protection (Optional)**
   - Won't affect scanner, but good practice
   - Can enable PR reviews before merge

## Visibility Checklist

- [ ] Repository is public OR token has access
- [ ] Files visible in GitHub web UI
- [ ] Files are UTF-8 encoded
- [ ] `.mcp/` directory NOT in `.gitignore`
- [ ] No syntax errors in JSON/YAML
- [ ] `mcpServers` key present with correct case
- [ ] Branch is `main` or default branch set correctly
- [ ] GitHub search finds `filename:mcp.json` within 15 minutes

## Scanner-Optimized Settings

### Recommended GitHub Settings

**Settings → General:**
- ✅ Make public (for scanner discoverability)
- ✅ Disable Wiki if not used
- ✅ Disable Projects if not used
- ✅ Disable Discussions if not needed

**Settings → Code & automation → Code security:**
- ✅ Enable CodeQL analysis (optional, good practice)
- ✅ Enable Secret scanning (optional, good practice)

**Settings → Collaborators:**
- ✅ Public repos: Anyone can view code
- ✅ Private repos: Share with scanner user/org

## Troubleshooting GitHub-Related Issues

### Issue: Scanner Can't Find Repository
**Solution:**
1. Verify repo is public
2. Wait 15 minutes for indexing
3. Check GitHub search manually
4. Verify token has `repo` scope

### Issue: Scanner Finds Some Files But Not Others
**Solution:**
1. Verify all files committed: `git status`
2. Check no files are ignored: `cat .gitignore | grep -E '(mcp|package|requirements)'`
3. Wait for full indexing
4. Verify file encoding

### Issue: Scanner Token Can't Access Organization
**Solution:**
1. Regenerate token with `read:org` scope
2. Verify token not expired
3. Check user is member of organization
4. Try with user account first (not org)

## Analytics & Monitoring

### GitHub Insights
Monitor scanner activity:
1. Go to Insights → Traffic
2. Track referrer statistics
3. See if scanner is accessing your repo

### Search Analytics
See which searches find your files:
1. Insights → Traffic → Referrers
2. Look for search queries

## Keeping Repository Updated

After successful scanner detection:

### Add to Scanner Registry
1. Document your MCP server
2. Submit PR to scanner's known MCPs list
3. Include: name, description, risk level, provider

### Maintain Scanner Compatibility
- Keep configuration files updated
- Update descriptions as needed
- Test with scanner periodically
- Report any detection issues

---

## Quick Summary

✅ **For Best Scanner Detection:**
1. Make repository public
2. Wait 15 minutes after pushing
3. Use standard file names (`mcp.json`, not `mcp-config.json`)
4. Ensure valid JSON/YAML
5. Keep `.mcp/` directory visible (not in `.gitignore`)
6. Generate token with `repo` + `read:org` scopes
7. Verify GitHub search finds your files before scanning

---

See [QUICK_START.md](QUICK_START.md) for step-by-step scanner setup instructions.
