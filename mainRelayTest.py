import requests
import time

def main():
    # Step 1: connect to relay
    resp = requests.post("http://localhost:3000/connect", json={
        "username": "peeepoo_man",
        "password": "Raeh147611"
    })
    print("Connect response:", resp.text)

    # Step 2: wait for login (Showdown handshake)
    print("Waiting for login to complete...")
    time.sleep(5)  # Wait 5 seconds

    # Step 3: send the challenge
    resp = requests.post("http://localhost:3000/send", json={
        #"message": "/pm OOmeNN hi from peeepoo_man!"
        #"message": "/challenge OOmeNN, gen9vgc2025regj"
        "message": "/cmd userdetails peeepoo_man"
    })
    print("Challenge response:", resp.text)

if __name__ == "__main__":
    main()
