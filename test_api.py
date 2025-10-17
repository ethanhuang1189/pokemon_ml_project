"""Test the Flask API battle endpoint"""
import requests
import json
import time

# Start a battle
print("Starting battle via API...")
response = requests.post('http://localhost:5000/api/battle/start', json={
    'bot_type': 'random',
    'opponent_type': 'maxdamage',
    'n_battles': 1
})

print(f"Response status: {response.status_code}")
data = response.json()
print(f"Response data: {json.dumps(data, indent=2)}")

if 'battle_id' in data:
    battle_id = data['battle_id']
    print(f"\nBattle ID: {battle_id}")

    # Check status multiple times
    for i in range(20):
        time.sleep(1)
        status_response = requests.get(f'http://localhost:5000/api/battle/{battle_id}/status')
        status_data = status_response.json()
        print(f"\n[{i+1}s] Status: {status_data.get('status')}")
        print(f"  Battle URL: {status_data.get('battle_url')}")
        print(f"  Wins: {status_data.get('bot_wins')}")

        if status_data.get('status') in ['completed', 'error']:
            print("\nBattle finished!")
            break
