import subprocess, sys, json
import os

acc = sys.argv[1]
with open('accounts.json', 'r') as f:
    accounts = json.load(f)
if (acc not in accounts.keys()):
    print("No such account name")
    exit(0)
key = accounts[acc]
path = f"links/{acc}.txt"
if not os.path.exists(path):
    open(path, "w")
for i in range(3):
    command = f"D:/ProgrammFiles/nodejs/node.exe D:/Projects/js/getlinks.js {acc} {key} {path} \"cf noncf\""
    print("CMD:", command)
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(f"initiating for {acc}", line.decode("utf-8"), end="")
    with open(path, "r") as f:
        links = f.readlines()
        if (len(links) != 6):
            print("Error: not enough links")
            continue
    break