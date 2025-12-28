#!/bin/bash
# Quick setup script for pushing to GitHub

echo "🚀 MCP Test Server - GitHub Setup"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git repository already exists"
fi

# Check for remote
if ! git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "📝 Please enter your GitHub repository URL:"
    echo "   (e.g., https://github.com/username/mcp-test.git)"
    read -p "Repository URL: " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✓ Remote 'origin' added"
    else
        echo "⚠️  No URL provided. You'll need to add remote manually:"
        echo "   git remote add origin <your-repo-url>"
    fi
else
    echo "✓ Remote 'origin' already configured: $(git remote get-url origin)"
fi

# Check for changes to commit
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "📝 Staging all files..."
    git add .
    echo "✓ Files staged"
    
    echo ""
    echo "💾 Committing changes..."
    git commit -m "Initial commit: MCP test server for scanner testing"
    echo "✓ Changes committed"
else
    echo "✓ No changes to commit"
fi

# Check current branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo ""
    echo "🔀 Renaming branch to 'main'..."
    git branch -M main
    echo "✓ Branch renamed to main"
fi

echo ""
echo "📤 Ready to push? Run:"
echo "   git push -u origin main"
echo ""
echo "⏱️  After pushing, wait 5-10 minutes for GitHub to index your repository"
echo "🔍 Then test with: https://apisec-inc.github.io/mcp-audit/"
echo ""
echo "📖 See SCANNER_GUIDE.md for detailed testing instructions"
