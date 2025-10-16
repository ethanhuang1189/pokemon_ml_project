# Testing the Live Battle Viewer

## Step-by-Step Test

### 1. Start Both Servers

**Run:** `start_with_showdown.bat`

You should see TWO windows open:
- Window 1: Pokemon Showdown (shows "Worker 1 now listening on 0.0.0.0:8000")
- Window 2: Flask server (shows "Running on http://127.0.0.1:5000")

### 2. Verify Showdown is Running

Open in browser: **http://localhost:8000**

You should see the Pokemon Showdown homepage with:
- Login button
- Format selection
- Battle buttons

If you don't see this, Showdown isn't running properly.

### 3. Open Web Interface

Open in browser: **http://localhost:5000**

Look at the top - you should see:
- **Green dot**: "Live Viewing Mode: ON (Showdown Connected)"
- **Red dot**: "Simple Mode (Showdown not detected)"

If you see green, you're ready for live viewing!

### 4. Start a Battle

1. Click a bot (e.g., "Custom Strategy Bot")
2. Click opponent bot (e.g., "Random Bot")
3. Set battles to 1
4. Click "Start Battle"

### 5. Watch for the Button

In the "Battle in Progress" section, look for:

**"Watch Live: [Open in Showdown]"** button

This should appear within 2-5 seconds after battle starts.

### 6. Click the Button

Click "Open in Showdown" - it will open a new tab with the battle!

You should see:
- Pokemon sprites on both sides
- Move selection buttons
- Battle log
- HP bars

## Troubleshooting

### "Watch Live" button never appears

**Check Flask console output** for battle URLs like:
```
Battle URL: http://localhost:8000/battle-gen8randombattle-12345
```

If you see these URLs, the battle is working but the frontend isn't detecting it.

**Manual test:**
1. Copy the battle URL from Flask console
2. Paste it in your browser
3. You should see the battle

### Showdown shows "Room not found"

This means the battle finished before you opened the link. Try:
- Set battles to 5 or 10 (gives you more time)
- Click the link faster
- Battles might be too quick - this is normal for some matchups

### No battle URLs in Flask console

The bots aren't connecting to Showdown. Check:

1. **Showdown is running with `--no-security`:**
   ```bash
   node pokemon-showdown start --no-security
   ```

2. **Port 8000 is available:**
   ```bash
   # On Windows
   netstat -ano | findstr :8000
   ```

3. **Check app.py configuration:**
   Should have:
   ```python
   LOCAL_SERVER = ServerConfiguration(
       "ws://localhost:8000/showdown/websocket",
       "http://localhost:8000/action.php?"
   )
   ```

### Battles work but I don't see graphics

Check browser console (F12) for errors.

The link format should be:
```
http://localhost:8000/battle-gen8randombattle-XXXXXX
```

## Expected Behavior

**With Showdown Running:**
- Green status indicator
- "Watch Live" button appears
- Click button → see graphical battle
- Battle log shows moves in real-time

**Without Showdown:**
- Red status indicator
- No "Watch Live" button
- Battles still run (internally)
- See text logs only

## Debug Mode

To see more details, open browser console (F12) and watch for:
- Battle events being received
- Battle URL updates
- Any JavaScript errors

## Quick Test Commands

```bash
# Test 1: Is Showdown running?
curl http://localhost:8000

# Test 2: Is Flask running?
curl http://localhost:5000

# Test 3: Can bots connect?
# Start a battle and check Flask terminal for:
# "Connecting bots..."
# "Battle started..."
```

## Success Checklist

- [ ] Showdown server starts without errors
- [ ] Flask server starts without errors
- [ ] Web page loads at localhost:5000
- [ ] Green status indicator shows
- [ ] Can select bots
- [ ] Battle starts
- [ ] "Watch Live" button appears
- [ ] Clicking button opens Showdown battle
- [ ] Can see Pokemon fighting

If all checked, you're good to go!
