#!/bin/bash

echo "Fixing model tracking..."

# Remove from Git cache
git rm -r --cached models/model.joblib 2>/dev/null || true
git rm -r --cached models/feature_names.joblib 2>/dev/null || true
git rm -r --cached models/*.joblib 2>/dev/null || true

# Ensure .gitignore is correct
if ! grep -q "models/\*.joblib" .gitignore; then
    echo "" >> .gitignore
    echo "# DVC-managed model files" >> .gitignore
    echo "models/*.joblib" >> .gitignore
fi

# Check git status
echo ""
echo "Git status:"
git status

# Stage and commit
git add .gitignore
git commit -m "Fix: Stop tracking model files with Git, let DVC manage them"

echo ""
echo "✅ Fixed! Now push to GitHub:"
echo "git push origin main"
