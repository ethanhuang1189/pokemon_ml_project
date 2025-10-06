import express from "express";
import fetch from "node-fetch";
import WebSocket from "ws";

const app = express();
app.use(express.json());

let ws = null;
let loggedIn = false;
let usernameCache = "";
let challstrCache = "";

// --- CONNECT ENDPOINT ---
app.post("/connect", async (req, res) => {
  const { username, password } = req.body;
  usernameCache = username;
  loggedIn = false;

  const server = "wss://sim3.psim.us/showdown/websocket";
  ws = new WebSocket(server);

  ws.on("open", () => {
    console.log("🌐 Connected to Showdown server...");
    res.send("Connecting to Showdown...");
  });

  ws.on("message", async (msg) => {
    const message = msg.toString();
    console.log("[Showdown]", message);

    // Login challenge step
    if (message.startsWith("|challstr|")) {
      challstrCache = message.split("|")[2] + "|" + message.split("|")[3];
      console.log("🔑 Got challstr, logging in...");

      const loginRes = await fetch("https://play.pokemonshowdown.com/action.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          act: "login",
          name: username,
          pass: password,
          challstr: challstrCache,
        }),
      });

      const text = await loginRes.text();
      const jsonText = text.startsWith("]") ? text.slice(1) : text;
      const data = JSON.parse(jsonText);

      if (data.assertion) {
        ws.send(`|/trn ${username},0,${data.assertion}`);
        loggedIn = true;
        console.log(`✅ Logged in as ${username}`);
      } else {
        console.error("❌ Login failed:", data);
      }
    }
  });

  ws.on("close", () => {
    loggedIn = false;
    console.log("⚠️ Disconnected from Showdown.");
  });

  ws.on("error", (err) => console.error("❌ WebSocket error:", err));
});

// --- SEND ENDPOINT ---
app.post("/send", (req, res) => {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    return res.status(400).send("Not connected to Showdown");
  }

  if (!loggedIn) {
    return res.status(400).send("Not logged in yet");
  }

  const { message } = req.body;
  ws.send(message);
  console.log("➡️ Sent:", message);
  res.send("Message sent to Showdown");
});

// --- START SERVER ---
const PORT = 3000;
app.listen(PORT, () => console.log(`Relay running on http://localhost:${PORT}`));
