# Quick setup script for pushing to GitHub (PowerShell)

Write-Host "🚀 MCP Test Server - GitHub Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already exists" -ForegroundColor Green
}

# Check for remote
$remoteExists = $false
try {
    git remote get-url origin 2>$null
    $remoteExists = $LASTEXITCODE -eq 0
} catch {
    $remoteExists = $false
}

if (-not $remoteExists) {
    Write-Host ""
    Write-Host "📝 Please enter your GitHub repository URL:" -ForegroundColor Yellow
    Write-Host "   (e.g., https://github.com/username/mcp-test.git)" -ForegroundColor Gray
    $repoUrl = Read-Host "Repository URL"
    
    if ($repoUrl) {
        git remote add origin $repoUrl
        Write-Host "✓ Remote 'origin' added" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No URL provided. You'll need to add remote manually:" -ForegroundColor Yellow
        Write-Host "   git remote add origin <your-repo-url>" -ForegroundColor Gray
    }
} else {
    $originUrl = git remote get-url origin
    Write-Host "✓ Remote 'origin' already configured: $originUrl" -ForegroundColor Green
}

# Check for changes to commit
$hasChanges = (git status --porcelain) -ne $null

if ($hasChanges) {
    Write-Host ""
    Write-Host "📝 Staging all files..." -ForegroundColor Yellow
    git add .
    Write-Host "✓ Files staged" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "💾 Committing changes..." -ForegroundColor Yellow
    git commit -m "Initial commit: MCP test server for scanner testing"
    Write-Host "✓ Changes committed" -ForegroundColor Green
} else {
    Write-Host "✓ No changes to commit" -ForegroundColor Green
}

# Check current branch
$currentBranch = git branch --show-current

if ($currentBranch -ne "main") {
    Write-Host ""
    Write-Host "🔀 Renaming branch to 'main'..." -ForegroundColor Yellow
    git branch -M main
    Write-Host "✓ Branch renamed to main" -ForegroundColor Green
}

Write-Host ""
Write-Host "📤 Ready to push? Run:" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "⏱️  After pushing, wait 5-10 minutes for GitHub to index your repository" -ForegroundColor Yellow
Write-Host "🔍 Then test with: https://apisec-inc.github.io/mcp-audit/" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 See SCANNER_GUIDE.md for detailed testing instructions" -ForegroundColor Gray
