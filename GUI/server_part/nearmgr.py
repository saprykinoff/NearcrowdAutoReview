import sys
import os
import time
os.chdir("/var/www/nearmgr")

def guarantee(id):
    if (not os.path.exists(f"ids/{id}")):
        os.mkdir(f"ids/{id}")
        with open(f"ids/{id}/exp.txt", 'w') as f:
            print(0, file=f)

def get_remain(id):
    if (not os.path.exists(f"ids/{id}")):
        return 0
    with open(f"ids/{id}/exp.txt", 'r') as f:
        remain = max(0, int(f.read()) - int(time.time()))
        return remain

def increase_exp(id, hours):
    guarantee(id)
    tm = int(time.time())
    with open(f"ids/{id}/exp.txt", 'r') as f:
        tm = max(tm, int(f.read()))
    tm += int(hours) * 60 * 60
    with open(f"ids/{id}/exp.txt", 'w') as f:
        print(tm, file=f)

def set_exp(id, hours):
    guarantee(id)
    tm = int(time.time())
    tm += int(hours) * 60 * 60
    with open(f"ids/{id}/exp.txt", 'w') as f:
        print(tm, file=f)


_, func, *params = sys.argv
if (func == "get"):
    print(get_remain(*params))
if (func == "inc"):
    increase_exp(*params)
if (func == "set"):
    set_exp(*params)
if (func == "help"):
    print("""
    get id
    inc id hours
    set id hours
    """)
