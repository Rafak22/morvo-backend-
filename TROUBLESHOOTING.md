# MORVO Backend Troubleshooting Guide

## 502 Error Resolution Steps

### 1. Check Railway Logs
- Go to your Railway dashboard
- Click on your project
- Go to the "Deployments" tab
- Click on the latest deployment
- Check the logs for any error messages

### 2. Test Endpoints
Try these endpoints in order:

1. **Health Check**: `https://your-app.railway.app/health`
2. **Ping**: `https://your-app.railway.app/ping`
3. **Test**: `https://your-app.railway.app/test`
4. **Debug**: `https://your-app.railway.app/debug`

### 3. Common Issues and Solutions

#### Issue: App not starting
**Solution**: Check if the port is correctly set to `$PORT` environment variable

#### Issue: Import errors
**Solution**: All dependencies are in `requirements.txt` and should install automatically

#### Issue: Supabase connection errors
**Solution**: The app will start even if Supabase is not configured

#### Issue: Environment variables missing
**Solution**: The app has fallbacks for missing environment variables

### 4. Railway Configuration
- Using `railway.json` for configuration
- Removed conflicting `Procfile`
- Added restart policy for better reliability

### 5. Debugging Commands

#### Local Testing
```bash
python startup_test.py
python -c "from main import app; print('App imported successfully')"
```

#### Check Dependencies
```bash
pip list | grep -E "(fastapi|uvicorn|supabase)"
```

### 6. If Still Getting 502 Error

1. **Check Railway Status**: Visit https://status.railway.app/
2. **Verify Domain**: Make sure you're using the correct Railway URL
3. **Check Environment Variables**: Ensure `PORT` is set in Railway
4. **Review Logs**: Look for specific error messages in Railway logs

### 7. Contact Support
If the issue persists, provide:
- Railway deployment logs
- The exact error message
- Steps to reproduce the issue 