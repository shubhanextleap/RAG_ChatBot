# Streamlit Cloud Deployment - Troubleshooting Guide

## 🔴 Error: "Error installing requirements"

This error means Streamlit Cloud couldn't install your Python dependencies. Here's how to fix it:

---

## 🔍 STEP 1: Check Your requirements.txt

Your requirements.txt MUST include:

```txt
streamlit>=1.0.0
flask>=2.0.0
flask-cors>=3.0.0
python-dotenv>=0.19.0
langchain>=0.0.200
langchain-community>=0.0.1
langchain-groq>=0.1.0
groq>=0.0.1
chromadb>=0.3.21
sentence-transformers>=2.2.0
requests>=2.28.0
pydantic>=2.0.0
```

✅ I've already updated your `requirements.txt` with these!

---

## 🔧 STEP 2: Fix Installation Issues

### Option A: Use requirements-minimal.txt
If you get timeout errors, Streamlit Cloud has trouble installing all dependencies.

**Solution:**
1. In Streamlit Cloud deployment settings
2. Change main file to: `app.py`
3. Delete `requirements.txt` from deployment (but keep locally)
4. Upload `requirements-minimal.txt` as `requirements.txt`

### Option B: Clear Streamlit Cloud Cache
1. Go to your app settings
2. Click "Reboot App"
3. This forces a clean reinstall

### Option C: Redeploy from GitHub
1. Push latest requirements.txt to GitHub:
```bash
git add requirements.txt requirements-minimal.txt
git commit -m "Fix requirements for Streamlit Cloud"
git push origin main
```

2. In Streamlit Cloud:
   - Click your app
   - Scroll to "Advanced Settings"
   - Click "Reboot app" or "Redeploy"

---

## 📋 STEP 3: Check Main File Configuration

Streamlit Cloud needs to know which file to run.

**In Streamlit Cloud Settings:**
1. Click your app name
2. Look for "App file" or "Main file"
3. Ensure it's set to: `app.py`

**NOT:** `streamlit_app.py` or `main.py`

---

## ⏱️ STEP 4: Installation Timeout

If installation keeps timing out (>15 minutes):

**Problem:** Some packages take too long to compile on Streamlit Cloud servers

**Solution 1 - Simplify Requirements:**
```txt
streamlit==1.28.1
python-dotenv==1.0.0
langchain==0.0.300
groq==0.4.1
chromadb==0.4.0
```

**Solution 2 - Install Pre-compiled Wheels:**
Streamlit Cloud sometimes needs binary wheels instead of source builds.

Check if your package is on: https://pypi.org/ (look for "Wheels" section)

---

## 🔴 COMMON ERRORS AND FIXES

### Error: "No module named 'langchain'"

**Cause:** Package wasn't installed correctly

**Fix:**
```txt
# Make sure this is in requirements.txt:
langchain>=0.0.200
langchain-community>=0.0.1
langchain-groq>=0.1.0
```

---

### Error: "Could not find a version that satisfies"

**Cause:** Version conflict between packages

**Fix:** Use flexible version constraints:
```txt
# WRONG (too specific):
langchain==0.0.123

# RIGHT (more flexible):
langchain>=0.0.200
```

---

### Error: "Build failed for chromadb"

**Cause:** ChromaDB needs to be compiled, which sometimes fails

**Fix Option 1:** Use pre-built version:
```txt
chromadb>=0.4.0
```

**Fix Option 2:** Skip Chroma initially and test basic deployment:
```txt
# Comment out chromadb for now
# chromadb>=0.4.0
```

---

### Error: "Timeout while installing"

**Cause:** Installation taking too long (>15 minutes)

**Fix:**
1. Reduce number of packages
2. Use `requirements-minimal.txt`
3. Remove version pins (use `>=` instead of `==`)

---

## ✅ STEP 5: Test Deployment

After fixing requirements, test in Streamlit Cloud:

### Quick Test
1. Go to your Streamlit Cloud app URL
2. If it loads, check logs for runtime errors
3. Ask a test question

### Check Logs
1. In Streamlit Cloud, click your app
2. Click "Manage App" 
3. Go to "Advanced Settings"
4. Click "View Logs"
5. Look for error messages

---

## 🚀 STEP 6: Step-by-Step Redeploy

### Complete Redeployment Process

1. **Update requirements.txt locally:**
   ```bash
   # Make sure you have all dependencies listed
   cat requirements.txt
   ```

2. **Push to GitHub:**
   ```bash
   git add requirements.txt requirements-minimal.txt
   git commit -m "Fix Streamlit Cloud deployment"
   git push origin main
   ```

3. **Clear Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Find your app
   - Click ⋯ → Manage App
   - Click "Settings"
   - Click "Reboot app"

4. **Wait for Redeploy:**
   - Should take 2-5 minutes
   - Watch the status bar

5. **Check App:**
   - Click app name
   - If error persists, check logs

---

## 📊 PRIORITY PACKAGES

Must have (in order of importance):

1. ✅ **streamlit** - Web framework
2. ✅ **langchain** - RAG framework
3. ✅ **groq** - API client
4. ✅ **python-dotenv** - Config loading
5. ✅ **chromadb** - Vector DB
6. ✅ **sentence-transformers** - Embeddings

Optional packages that can be added later:

- flask (for API, not needed for Streamlit)
- flask-cors (for API)
- requests (usually included)

---

## 💡 QUICK FIXES (Try in Order)

### Fix 1: Use Minimal Requirements
Replace `requirements.txt` with `requirements-minimal.txt`:

```bash
mv requirements.txt requirements.txt.backup
mv requirements-minimal.txt requirements.txt
git add requirements.txt
git commit -m "Use minimal requirements"
git push origin main
```

Then redeploy in Streamlit Cloud.

### Fix 2: Check Python Version
Streamlit Cloud uses Python 3.10 or 3.11 by default.

Ensure compatibility by adding:
```txt
# At top of requirements.txt
# Python 3.10+
```

### Fix 3: Use Fixed Versions
```txt
streamlit==1.28.1
langchain==0.1.0
groq==0.4.1
chromadb==0.4.10
sentence-transformers==2.2.2
```

### Fix 4: Skip Large Dependencies
If still failing, comment out these temporarily:
```txt
# Large packages - can cause timeout
# chromadb>=0.4.0
# sentence-transformers>=2.2.0
```

Then re-enable after app is running.

---

## 🔐 SECRETS CONFIGURATION

After fixing requirements, make sure secrets are set:

1. Go to app settings
2. Scroll to "Secrets"
3. Add:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```

---

## 📞 IF STILL NOT WORKING

### Check These Files

Verify in your repo:
- [ ] `requirements.txt` exists and is readable
- [ ] `app.py` exists in root directory
- [ ] `.gitignore` exists
- [ ] No binary files committed
- [ ] File encodings are UTF-8

### Clear Everything

1. Delete app from Streamlit Cloud
2. Delete `.streamlit` cache (run locally):
   ```bash
   rm -rf .streamlit/cache
   ```
3. Push clean repo:
   ```bash
   git add .
   git commit -m "Clean rebuild for Streamlit"
   git push origin main
   ```
4. Redeploy fresh in Streamlit Cloud

### Contact Support

If still failing:
- Check Streamlit forums: https://discuss.streamlit.io/
- Include:
  - Error message from logs
  - Your requirements.txt content
  - Python version info

---

## ✨ EXPECTED BEHAVIOR AFTER FIX

✅ App deploys in 2-5 minutes  
✅ No "Error installing requirements" message  
✅ App loads at your Streamlit URL  
✅ Can ask questions and get responses  
✅ No module import errors  

---

## 📝 Current Status

✅ Updated `requirements.txt` with all dependencies  
✅ Created `requirements-minimal.txt` for fallback  
✅ .streamlit/config.toml configured  
✅ All imports should work  

**Next Steps:**
1. Push to GitHub
2. Go to Streamlit Cloud
3. Redeploy or reboot app
4. Wait 2-5 minutes
5. Check if error is fixed

---

**Your app is ready! Just follow these steps if you see the requirements error.** 🚀
