# 🚀 Quick Deployment Guide to Streamlit Cloud

## Prerequisites

- GitHub account
- Repository pushed to GitHub (this one!)
- CSV data files in the repository

## Step-by-Step Deployment

### 1. Visit Streamlit Cloud

Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) and click **"Sign up"** or **"Sign in with GitHub"**

### 2. Create New App

1. Click **"New app"** button
2. Select your repository: `DanielArizaGarcia/Data-analysis-for-the-2015-flight-dealys-and-cancelation`
3. Select branch: `main` (or your default branch)
4. Main file path: `app.py`
5. (Optional) Custom subdomain: choose your app name

### 3. Advanced Settings (Optional)

Click **"Advanced settings"** if you need to:
- Set Python version (default: 3.11 is fine)
- Add secrets (not needed for this app)
- Customize app URL

### 4. Deploy

Click **"Deploy!"** and wait for the app to build (usually 2-5 minutes).

## Post-Deployment

### Update README with Live URL

Once deployed, your app will have a URL like:
```
https://your-app-name.streamlit.app
```

Update the README.md file to replace the placeholder with your actual URL.

### Monitoring

- Access your app dashboard at [https://share.streamlit.io/](https://share.streamlit.io/)
- View logs and analytics
- Reboot or delete app if needed

## Automatic Updates

Any `git push` to your `main` branch will automatically trigger a redeploy! 🎉

## Troubleshooting

### Common Issues

1. **"No module named X"**
   - Check that all dependencies are in `requirements.txt`
   - Verify package names are correct

2. **"File not found"**
   - Ensure CSV files are committed to the repository
   - Check file paths are relative (not absolute)

3. **App won't load**
   - Check the logs in the Streamlit Cloud dashboard
   - Verify the app runs locally first: `streamlit run app.py`

### Performance Tips

- Use `@st.cache_data` for expensive operations (already implemented)
- Consider sampling large datasets
- Optimize image sizes if using many images

## Data Files

Make sure these files are in your repository:
- `flights.csv`
- `airlines.csv`
- `airports.csv`

**Note:** GitHub has a 100MB file size limit. If your CSV files are larger:
- Use Git LFS (Large File Storage)
- Or host data externally and load via URL

## Need Help?

- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Contact Support](https://streamlit.io/contact)

---

Happy deploying! 🎈
