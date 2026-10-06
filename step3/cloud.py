import json


NUM_SERVERS = 5
SERVER_PATH = "./servers/server"

def save_shares(website: str, username: str, shares: list[tuple[int, int]]) -> bool:
    shares_written = 0
    for i in range(NUM_SERVERS):
        path = f"{SERVER_PATH}{i + 1}.json"
        data = {}
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except:
            pass

        if username not in data:
            data[username] = {}
        data[username][website] = shares[i]

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            shares_written += 1  
    return shares_written == NUM_SERVERS

def get_shares(website: str, username: str) -> list[tuple[int, int]]:
    shares = []
    for i in range(NUM_SERVERS):
        path = f"{SERVER_PATH}{i + 1}.json"
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if username in data and website in data[username]:
                    share = data[username][website]
                    shares.append(tuple(share))
        except:
            pass
    return shares
