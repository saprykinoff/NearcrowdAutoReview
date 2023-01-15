from threading import Thread
import time
from farmer import Farmer
import json

with open('accounts.json', 'r') as f:
    accounts = json.load(f)
active = [
    "acc",
    "acc",
    "acc",
    "acc",
    "acc",
    "acc",
    "acc",
    "acc"
]
farmers = dict()
for acc in active:
    if (acc not in accounts.keys()):
        print("cant find account", acc)
        exit(0)
    farmers[acc] = Farmer(acc)

def update_status():
    while 1:

        status = dict()
        for acc in active:
            status[acc] = farmers[acc].status()
        with open("status.json", "w") as f:
            json.dump(status, f, ensure_ascii=False, indent=4)
        print(status)
        time.sleep(0)


for acc in active:
    t = Thread(target=farmers[acc].run)
    t.start()
    pass

t2 = Thread(target=update_status)
t2.start()
