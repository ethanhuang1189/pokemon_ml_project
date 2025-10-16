# Debug Challenge Issues

## Quick Diagnostic

### Test 1: Is Showdown Running?

```bash
# Open browser to:
http://localhost:8000

# You should see Showdown homepage
# If not, Showdown isn't running
```

### Test 2: Can you login?

1. Go to http://localhost:8000
2. Click "Choose name"
3. Type any name (e.g., "TestUser")
4. Does it let you in?

If NO: Showdown server has authentication issues

### Test 3: Test Challenge Directly

```bash
# In project root directory:
python test_challenge.py

# Follow prompts:
# 1. It will ask for your username
# 2. Type the EXACT username you're logged in as on Showdown
# 3. Wait for challenge notification
```

This will tell us if Bot_Naila can send challenges at all.

## Common Issues

### Issue 1: Username Case Sensitivity

**Problem:** Showdown usernames are case-sensitive!

**Solution:**
- If you logged in as "MyUser", bot must challenge "MyUser" (not "myuser")
- Exact match required

### Issue 2: User Not Actually Logged In

**Problem:** Showdown session expired or not connected

**Solution:**
1. Refresh Showdown page
2. Re-login
3. Look for your username in top-right corner
4. Should say "You are: [YourName]"

### Issue 3: Local vs Official Server

**Problem:** Bot connects to wrong server

**Check web/app.py line 29-32:**
```python
LOCAL_SERVER = ServerConfiguration(
    "ws://localhost:8000/showdown/websocket",
    "http://localhost:8000/action.php?"
)
```

Should be **localhost:8000** for local server.

### Issue 4: Bot Not Actually Challenging

**Check Flask console output for:**
- "Sending challenge to [username]..."
- "Challenge sent!"
- Or any error messages

### Issue 5: Notification Settings

**On Showdown:**
1. Click your username (top-right)
2. Go to "Options"
3. Check "Notifications" section
4. Make sure challenges are enabled

## Step-by-Step Debug

### 1. Verify Server Setup

```bash
# Terminal 1: Start Showdown
cd showdown-relay/pokemon-showdown
node pokemon-showdown start --no-security

# Should see:
# "Worker 1 now listening on 0.0.0.0:8000"
```

### 2. Verify Bot Can Connect

```bash
# Terminal 2: Run test
python test_challenge.py

# You should see:
# ✓ Bot_Naila created
# ✓ Challenge sent!
```

### 3. Check Showdown UI

After bot sends challenge, in Showdown you should see:
- Top-right: Red notification badge with "1"
- Or: Pop-up notification
- Or: In Home tab, "Bot_Naila challenged you!"

### 4. Check Web Dashboard

In the web interface (localhost:5000), event log should show:
```
[Time] Creating random bot as Bot_Naila...
[Time] Bot Bot_Naila (random) is ready!
[Time] Waiting 10 seconds for you to log into Showdown...
[Time] Sending challenge to YourUsername...
[Time] Challenge sent! Check Showdown for notification from Bot_Naila
```

If you DON'T see "Challenge sent!", there's an error.

## Try These

### Option 1: Increase Wait Time

Edit `web/app.py` line 231:
```python
await asyncio.sleep(10)  # Change to 20 or 30
```

Gives you more time to log in.

### Option 2: Manual Challenge Test

1. Login to Showdown as yourself (e.g., "Player1")
2. Open browser console (F12)
3. Type in console:
```javascript
app.send('/challenge Player1, gen8randombattle')
```

See if you get your own challenge - tests notification system.

### Option 3: Check Username Format

Bot_Naila might need different username format. Try:
- Lowercase: "myusername"
- CamelCase: "MyUsername"
- With spaces: "My Username" (usually doesn't work)

### Option 4: Watch Flask Terminal

When you start battle, watch Flask terminal for:
```
Bot_Naila connecting...
Challenge sent to: [username]
Error (if any)
```

## Still Not Working?

### Collect Debug Info:

1. **Flask terminal output** (copy entire output)
2. **Showdown username** (exact spelling)
3. **Browser console** (F12, any errors?)
4. **test_challenge.py output** (what did it say?)

### Then check:

1. Is username spelled EXACTLY the same?
2. Are you on the Home tab in Showdown?
3. Did 10+ seconds pass after clicking "Start Battle"?
4. Is Bot_Naila online? (check user list on Showdown)

## Quick Fix Attempts

### Attempt 1: Fresh Start
1. Stop both servers (Ctrl+C)
2. Restart: `start_with_showdown.bat`
3. Wait for both to fully start
4. Try again

### Attempt 2: Different Username
1. Use very simple username: "test123"
2. No spaces, no special characters
3. All lowercase

### Attempt 3: Accept Manually
Sometimes challenges appear but notifications don't. Check:
- Home tab on Showdown
- Look for text "Bot_Naila challenged you to gen8randombattle"
- Click Accept button

Let me know what you find!
