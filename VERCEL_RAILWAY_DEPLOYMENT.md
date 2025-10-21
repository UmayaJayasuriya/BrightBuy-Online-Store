# 🚀 Vercel + Railway Deployment Guide

## Overview

- **Frontend**: Deploy to Vercel (React)
- **Backend**: Deploy to Railway (FastAPI + MySQL)

---

## ✅ Step 1: Deploy Frontend to Vercel

### Prerequisites

- GitHub account
- Vercel account (sign up free at vercel.com)

### Steps:

1. **Push your code to GitHub**

   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Go to Vercel Dashboard**

   - Visit: https://vercel.com/dashboard
   - Click "New Project"
   - Click "Import Git Repository"
   - Select your `BrightBuy-Online-Store` repo

3. **Configure Project Settings**

   - **Root Directory**: Leave empty (Vercel will auto-detect)
   - **Framework Preset**: React
   - **Build Command**: `npm run build` (in frontend folder)
   - **Output Directory**: `frontend/build`
   - **Install Command**: `npm install` (in frontend folder)

4. **Set Environment Variables**

   - Click "Environment Variables"
   - Add variable:
     - **Name**: `REACT_APP_API_URL`
     - **Value**: `http://localhost:8020` (for now, we'll update after Railway deployment)
   - Click "Add"

5. **Deploy**
   - Click "Deploy"
   - Wait 3-5 minutes for deployment
   - Your frontend will be live! ✅

---

## ✅ Step 2: Deploy Backend to Railway

### Prerequisites

- Vercel deployment complete (get the URL)
- GitHub account
- Railway account (sign up free at railway.app)

### Steps:

1. **Go to Railway Dashboard**

   - Visit: https://railway.app
   - Click "New Project"
   - Click "Deploy from GitHub repo"
   - Select your `BrightBuy-Online-Store` repo

2. **Create MySQL Database**

   - In Railway dashboard, click "New"
   - Click "Database"
   - Click "MySQL"
   - Wait for creation (2-3 minutes)

3. **Configure Backend Service**

   - Click "New"
   - Click "GitHub Repo"
   - Select your repo again
   - Railway will auto-detect it's a Python project

4. **Set Environment Variables**

   - In Railway, go to your backend service
   - Click "Variables"
   - Add these variables:
     ```
     DB_HOST=mysql (Railway automatically sets this)
     DB_USER=root
     DB_PASSWORD=[copy from MySQL service variables]
     DB_NAME=brightbuy
     DB_PORT=3306
     ```

5. **Add Build & Start Commands**

   - In "Settings" tab:
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8020`
     - **Python Version**: 3.11

6. **Deploy**
   - Railway will auto-deploy
   - Get your backend URL from Railway dashboard
   - It will look like: `https://yourapp-production.up.railway.app`

---

## 🔄 Step 3: Connect Frontend to Backend

### Update API URL:

1. **Go back to Vercel Dashboard**
2. **Select your frontend project**
3. **Go to Settings → Environment Variables**
4. **Update `REACT_APP_API_URL`**:

   ```
   Name: REACT_APP_API_URL
   Value: https://yourapp-production.up.railway.app
   ```

5. **Redeploy Frontend**:
   - Go to Deployments
   - Click the latest deployment
   - Click "..." menu → "Redeploy"

---

## 🗄️ Step 4: Set Up Database (Important!)

### Import Your Database Schema:

1. **Get Railway MySQL Credentials**:

   - In Railway dashboard, click MySQL database
   - Click "Connect" tab
   - Copy connection string

2. **Import Your Database**:

   ```bash
   # Option 1: Using MySQL Workbench
   # Connect using Railway credentials
   # File → Import SQL Dump → Select your database file

   # Option 2: Using command line
   mysql -h [host] -u [user] -p [password] [database] < database_backup.sql
   ```

3. **Verify Connection**:
   - Visit: `https://yourapp-production.up.railway.app/docs`
   - You should see Swagger API docs
   - If you see errors, check database connection

---

## ✅ Testing Your Deployment

### Test Frontend:

```
https://yourproject.vercel.app
```

### Test Backend API:

```
https://yourapp-production.up.railway.app/docs
```

### Test API Connection:

1. Open frontend at vercel.app URL
2. Try to login
3. If it works, everything is connected! ✅

---

## 🔐 Important Notes

1. **CORS Settings**: Update your FastAPI CORS to include Vercel domain:

   ```python
   # In backend/app/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourproject.vercel.app", "http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Database Backup**: Always keep a backup of your database

3. **Environment Secrets**: Never commit `.env` files with real passwords

---

## 🚀 Your Live URLs

Once deployed:

- **Frontend**: `https://yourproject.vercel.app`
- **Backend**: `https://yourapp-production.up.railway.app`
- **API Docs**: `https://yourapp-production.up.railway.app/docs`

---

## 🐛 Troubleshooting

### "Cannot connect to database"

- Check Railway MySQL credentials
- Verify database is running
- Check DB environment variables

### "Frontend won't load"

- Clear browser cache
- Check REACT_APP_API_URL is set correctly
- Verify Vercel build logs

### "API calls failing"

- Check CORS settings in FastAPI
- Verify API URL is correct in frontend
- Check Railway backend is running

### "Port already in use"

- Railway automatically assigns ports
- Check Railway deployment logs

---

## 📊 Cost Breakdown (Free Tier)

| Service         | Cost                                              |
| --------------- | ------------------------------------------------- |
| Vercel Frontend | FREE                                              |
| Railway Backend | $5 credit/month (usually FREE for small projects) |
| Railway MySQL   | Included                                          |
| **Total**       | **FREE**                                          |

---

## 🎯 Next Steps

1. ✅ Deploy frontend to Vercel
2. ✅ Deploy backend to Railway
3. ✅ Set up MySQL database
4. ✅ Connect frontend to backend
5. ✅ Test everything
6. ✅ Share your live URLs!

Good luck! 🚀
