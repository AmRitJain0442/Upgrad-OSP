# 🔑 Gemini API Setup Guide

## Quick Setup (2 minutes)

### Step 1: Get Your FREE API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX`)

### Step 2: Create .env File

**Option A: Copy from example**
```bash
cd ai-learning-platform
copy .env.example .env
```

**Option B: Create manually**

Create a file named `.env` in the `ai-learning-platform` folder with this content:

```
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX
```

Replace `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX` with your actual API key.

### Step 3: Install Dependencies & Run

```bash
pip install -r requirements.txt
cd backend
python app.py
```

You should see:
```
✓ Gemini API key loaded successfully
 * Running on http://127.0.0.1:5000
```

---

## ✅ Verification

If the API key is configured correctly, you'll see:
```
✓ Gemini API key loaded successfully
```

If NOT configured, you'll see:
```
WARNING: GEMINI_API_KEY not found in .env file!
Please create a .env file...
```

---

## 📁 File Structure

```
ai-learning-platform/
├── .env                  ← YOUR API KEY (create this)
├── .env.example          ← Template (don't edit)
├── backend/
│   └── app.py           ← Loads API key from .env
├── requirements.txt
└── README.md
```

---

## 🔒 Security Notes

### ✅ DO:
- Keep `.env` file LOCAL only
- Never commit `.env` to Git (already in .gitignore)
- Keep your API key private

### ❌ DON'T:
- Share your `.env` file
- Post API key on GitHub, Discord, etc.
- Commit `.env` to version control

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution 1: Check file location**
```
.env file must be in: ai-learning-platform/.env
NOT in: ai-learning-platform/backend/.env
```

**Solution 2: Check file name**
- File must be named `.env` (with the dot at the start)
- NOT `env.txt` or `.env.txt`
- On Windows, make sure "Hide extensions" is off

**Solution 3: Check file content**
```
GEMINI_API_KEY=your_key_here
```
- No spaces around `=`
- No quotes needed
- Make sure you pasted your actual key

### Issue: "API key is invalid"

**Solution:**
1. Go back to https://makersuite.google.com/app/apikey
2. Create a NEW API key
3. Update your `.env` file with the new key
4. Restart the server

### Issue: File not found on Windows

Use Command Prompt or PowerShell to create:

**PowerShell:**
```powershell
cd ai-learning-platform
New-Item -Path . -Name ".env" -ItemType "file"
notepad .env
```

**CMD:**
```cmd
cd ai-learning-platform
echo GEMINI_API_KEY=your_key_here > .env
```

Then edit the file and paste your actual key.

---

## 📝 Example .env File

```env
# Get your key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ123456

# Optional: Custom secret key for Flask sessions
SECRET_KEY=my-super-secret-key-change-this
```

---

## 🎯 Testing Your Setup

### Test 1: Check API Key is Loaded

```bash
cd backend
python app.py
```

Look for: `✓ Gemini API key loaded successfully`

### Test 2: Upload and Summarize

1. Open http://localhost:5000
2. Click "Launch" on Submodule 1
3. Upload a document (PDF, DOCX, or TXT)
4. Type a prompt: "Summarize this document"
5. Click "Generate Summary"

If it works → ✅ API configured correctly!

If error → Check troubleshooting above

---

## 💡 Pro Tips

### Tip 1: Multiple Environments

For development vs production:

**.env.development**
```
GEMINI_API_KEY=dev_key_here
```

**.env.production**
```
GEMINI_API_KEY=prod_key_here
```

### Tip 2: Check API Usage

Monitor your API usage at:
https://makersuite.google.com/app/apikey

Free tier includes:
- 60 requests per minute
- Sufficient for learning and testing

### Tip 3: Backup Your Key

Save your API key somewhere safe (password manager) in case you need to recreate the .env file.

---

## 🆘 Still Having Issues?

1. **Check the file exists:**
   ```bash
   dir .env    # Windows CMD
   ls -la .env # PowerShell/Mac/Linux
   ```

2. **Check the content:**
   ```bash
   type .env   # Windows CMD
   cat .env    # PowerShell/Mac/Linux
   ```

3. **Restart the server:**
   - Stop the server (Ctrl+C)
   - Run `python app.py` again

4. **Check requirements:**
   ```bash
   pip list | findstr dotenv
   ```
   Should show: `python-dotenv`

---

**You're all set!** 🚀

Your API key is now securely stored in `.env` and the platform will load it automatically.
