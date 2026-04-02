import requests

BASE_URL = "http://localhost:7860"


def reset(task="easy"):
    r = requests.post(f"{BASE_URL}/reset", json={"task": task})
    r.raise_for_status()
    return r.json()


def step(action_type, target):
    r = requests.post(f"{BASE_URL}/step", json={"type": action_type, "target": target})
    r.raise_for_status()
    return r.json()


def get_state():
    r = requests.get(f"{BASE_URL}/state")
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    obs = reset("easy")
    print("Initial observation:")
    print(obs)

    state = get_state()
    attack_ip = state["attack_ip"]
    print("\nAttack IP:", attack_ip)

    print("\nInvestigate step:")
    print(step("investigate", attack_ip))

    print("\nMonitor step:")
    print(step("monitor", attack_ip))

    print("\nBlock step:")
    print(step("block_ip", attack_ip))