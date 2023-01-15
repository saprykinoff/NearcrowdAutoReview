import paramiko
import json, subprocess
import os
data = os.environ['beget_main_data']
host, user, password = data.split(":")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, port=22)
client.exec_command('cd /var/www')
print("Connected")
def get_json(path):
    stdin, stdout, stderr = client.exec_command('cat /var/www/dev/Farm/' + path)

    # stdin = stdin.read().decode('utf-8')
    stdout = stdout.read().decode('utf-8')
    stderr = stderr.read().decode('utf-8')
    data = stdout
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        return None
def launch_browser(acc):
    accounts = get_json('accounts.json')
    if acc not in accounts.keys():
        raise NameError(f"No such account: {acc}")
    key = accounts[acc]
    command = f"node D:/Projects/js/launcher.js {acc} {key}"
    print("CMD:", command)
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(f"initiating for {acc}", line.decode("utf-8"), end="")
    print("Done")
# print(get_json("status.json"))
# launch_browser("kalmykov")