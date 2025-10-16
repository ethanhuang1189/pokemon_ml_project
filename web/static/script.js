// Global state
let selectedBot = null;
let selectedOpponent = null;
let currentBattleId = null;
let eventSource = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadBots();
    refreshHistory();
});

// Load available bots
async function loadBots() {
    try {
        const response = await fetch('/api/bots');
        const bots = await response.json();

        const botGrid = document.getElementById('botGrid');
        botGrid.innerHTML = '';

        bots.forEach(bot => {
            const botCard = document.createElement('div');
            botCard.className = 'bot-card';
            botCard.innerHTML = `
                <h3>${bot.name}</h3>
                <p>${bot.description}</p>
            `;
            botCard.onclick = () => selectBot(bot, botCard);
            botGrid.appendChild(botCard);
        });
    } catch (error) {
        console.error('Error loading bots:', error);
        alert('Failed to load bots. Please refresh the page.');
    }
}

// Load opponent bots
async function loadOpponents() {
    try {
        const response = await fetch('/api/opponents');
        const opponents = await response.json();

        const opponentGrid = document.getElementById('opponentGrid');
        opponentGrid.innerHTML = '';

        opponents.forEach(opponent => {
            const opponentCard = document.createElement('div');
            opponentCard.className = 'bot-card';
            opponentCard.innerHTML = `
                <h3>${opponent.name}</h3>
                <p>${opponent.description}</p>
            `;
            opponentCard.onclick = () => selectOpponent(opponent, opponentCard);
            opponentGrid.appendChild(opponentCard);
        });
    } catch (error) {
        console.error('Error loading opponents:', error);
        alert('Failed to load opponents. Please refresh the page.');
    }
}

// Select a bot
function selectBot(bot, cardElement) {
    // Remove previous selection
    document.querySelectorAll('#botGrid .bot-card').forEach(card => {
        card.classList.remove('selected');
    });

    // Mark as selected
    cardElement.classList.add('selected');
    selectedBot = bot;

    // Show opponent selection
    document.getElementById('opponentSelection').style.display = 'block';
    loadOpponents();
}

// Select an opponent
function selectOpponent(opponent, cardElement) {
    // Remove previous selection
    document.querySelectorAll('#opponentGrid .bot-card').forEach(card => {
        card.classList.remove('selected');
    });

    // Mark as selected
    cardElement.classList.add('selected');
    selectedOpponent = opponent;

    // Show battle configuration
    document.getElementById('selectedBotName').textContent = selectedBot.name;
    document.getElementById('selectedOpponentName').textContent = opponent.name;
    document.getElementById('battleConfig').style.display = 'block';
}

// Cancel battle configuration
function cancelBattle() {
    selectedBot = null;
    selectedOpponent = null;
    document.querySelectorAll('.bot-card').forEach(card => {
        card.classList.remove('selected');
    });
    document.getElementById('botSelection').style.display = 'block';
    document.getElementById('opponentSelection').style.display = 'none';
    document.getElementById('battleConfig').style.display = 'none';
}

// Start a battle
async function startBattle() {
    if (!selectedBot) {
        alert('Please select a bot first!');
        return;
    }

    if (!selectedOpponent) {
        alert('Please select an opponent bot!');
        return;
    }

    const numBattles = parseInt(document.getElementById('numBattles').value);

    try {
        const requestBody = {
            bot_type: selectedBot.id,
            opponent_type: selectedOpponent.id,
            n_battles: numBattles
        };

        // Start the battle
        const response = await fetch('/api/battle/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();

        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }

        currentBattleId = data.battle_id;

        // Update UI
        document.getElementById('battleBotName').textContent = selectedBot.name;
        document.getElementById('battleOpponent').textContent = selectedOpponent.name;
        document.getElementById('battleTotal').textContent = numBattles;
        document.getElementById('battleStatus').textContent = 'Initializing...';

        // Show progress sections
        document.getElementById('botSelection').style.display = 'none';
        document.getElementById('opponentSelection').style.display = 'none';
        document.getElementById('battleConfig').style.display = 'none';
        document.getElementById('battleProgress').style.display = 'block';
        document.getElementById('battleViewer').style.display = 'none';

        // Start listening to battle events
        listenToBattleEvents(data.battle_id);

    } catch (error) {
        console.error('Error starting battle:', error);
        alert('Failed to start battle. Please try again.');
    }
}

// Listen to battle events using Server-Sent Events
function listenToBattleEvents(battleId) {
    if (eventSource) {
        eventSource.close();
    }

    eventSource = new EventSource(`/api/battle/${battleId}/events`);

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleBattleEvent(data);
    };

    eventSource.onerror = (error) => {
        console.error('EventSource error:', error);
        eventSource.close();
    };
}

// Handle battle events
function handleBattleEvent(event) {
    switch (event.type) {
        case 'battle_start':
            document.getElementById('battleStatus').textContent = 'Battle in progress...';
            break;
        case 'battle_url':
            // Load battle in iframe
            const iframe = document.getElementById('battleIframe');
            iframe.src = event.data.url;
            document.getElementById('battleViewer').style.display = 'block';

            // Set up replay link (replace /battle- with /replay-)
            const replayUrl = event.data.url.replace('/battle-', '/replay-');
            const replayLink = document.getElementById('replayLink');
            replayLink.href = replayUrl;
            document.getElementById('replayLinkContainer').style.display = 'block';
            break;
        case 'battle_end':
            document.getElementById('battleStatus').textContent = 'Battle completed!';
            document.getElementById('battleWins').textContent = event.data.wins;
            document.getElementById('battleLosses').textContent = event.data.losses;
            battleCompleted();
            break;
        case 'error':
            document.getElementById('battleStatus').textContent = 'Error occurred';
            battleCompleted();
            break;
        case 'done':
            battleCompleted();
            break;
    }
}

// Update battle stats
function updateBattleStats(data) {
    document.getElementById('battleWins').textContent = data.wins;
    document.getElementById('battleLosses').textContent = data.finished - data.wins;
    document.getElementById('battleFinished').textContent = data.finished;
}

// Format status for display
function formatStatus(status) {
    const statusMap = {
        'info': 'Initializing...',
        'battle_start': 'Battle Started',
        'progress': 'Battling...',
        'battle_end': 'Completed',
        'error': 'Error',
        'done': 'Completed'
    };
    return statusMap[status] || status;
}

// Battle completed
function battleCompleted() {
    if (eventSource) {
        eventSource.close();
        eventSource = null;
    }

    // Refresh history
    refreshHistory();
}

// Reset UI for new battle
function resetUI() {
    selectedBot = null;
    selectedOpponent = null;
    currentBattleId = null;

    document.getElementById('botSelection').style.display = 'block';
    document.getElementById('opponentSelection').style.display = 'none';
    document.getElementById('battleConfig').style.display = 'none';
    document.getElementById('battleProgress').style.display = 'none';
    document.getElementById('battleViewer').style.display = 'none';
    document.getElementById('replayLinkContainer').style.display = 'none';

    // Clear iframe and replay link
    document.getElementById('battleIframe').src = '';
    document.getElementById('replayLink').href = '#';

    document.querySelectorAll('.bot-card').forEach(card => {
        card.classList.remove('selected');
    });

    document.getElementById('numBattles').value = '1';

    loadBots();
    refreshHistory();
}

// Refresh battle history
async function refreshHistory() {
    try {
        const response = await fetch('/api/battles');
        const battles = await response.json();

        const historyContainer = document.getElementById('historyContainer');

        if (battles.length === 0) {
            historyContainer.innerHTML = '<p class="no-battles">No battles yet</p>';
            return;
        }

        historyContainer.innerHTML = '';

        const botNames = {
            'random': 'Random Bot',
            'maxdamage': 'Max Damage Bot',
            'custom': 'Custom Strategy Bot'
        };

        battles.slice().reverse().forEach(battle => {
            const historyItem = document.createElement('div');
            historyItem.className = `history-item ${battle.status}`;

            const bot1Name = botNames[battle.bot_type] || 'Unknown Bot';
            const bot2Name = botNames[battle.opponent_type] || 'Unknown Bot';

            let winnerText = '';
            if (battle.status === 'completed' && battle.winner) {
                const winnerName = botNames[battle.winner] || 'Unknown';
                winnerText = `<br><small style="color: #4aff88;">${winnerName} Wins!</small>`;
            }

            historyItem.innerHTML = `
                <div>
                    <strong>${bot1Name}</strong> vs <strong>${bot2Name}</strong>
                    ${winnerText}
                </div>
                <div style="text-align: right;">
                    <strong>${battle.bot_wins}/${battle.bot_finished}</strong>
                    <br>
                    <small>wins</small>
                </div>
            `;

            historyContainer.appendChild(historyItem);
        });
    } catch (error) {
        console.error('Error refreshing history:', error);
    }
}
