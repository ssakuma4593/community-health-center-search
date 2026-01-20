# GitHub Pages Deployment Guide

## Step 1: Commit and Push Your Changes

```bash
# Make sure you're on the right branch
git checkout feature/github-pages-deployment

# Add all changes
git add -A

# Commit
git commit -m "Add Vite frontend with GitHub Pages deployment support"

# Push to GitHub
git push origin feature/github-pages-deployment
```

## Step 2: Enable GitHub Pages

1. Go to your GitHub repository: `https://github.com/<your-org>/community-health-center-search`
2. Click on **Settings** (top menu)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select **GitHub Actions**
5. Save the changes

## Step 3: Wait for Deployment

1. Go to the **Actions** tab in your repository
2. You should see a workflow run called "Deploy to GitHub Pages"
3. Wait for it to complete (usually 2-3 minutes)
4. Once it's done, you'll see a green checkmark

## Step 4: Access Your Site

Your site will be available at:
```
https://<your-org>.github.io/community-health-center-search/
```

**Note:** Replace `<your-org>` with your GitHub username or organization name.

## Troubleshooting

### Workflow Not Running
- Make sure you pushed to `feature/github-pages-deployment` or `main` branch
- Check the Actions tab for any errors

### Pages Not Showing
- Wait a few minutes after the workflow completes (GitHub Pages can take 1-5 minutes to update)
- Check that Pages source is set to "GitHub Actions" in Settings → Pages
- Verify the workflow completed successfully (green checkmark)

### 404 Error
- Make sure the base path in `vite.config.ts` matches your repository name
- The base path should be `/community-health-center-search/` (with trailing slash)

## Updating Your Site

Every time you push to `main` or `feature/github-pages-deployment`, the site will automatically rebuild and deploy. Just push your changes and wait for the workflow to complete!
