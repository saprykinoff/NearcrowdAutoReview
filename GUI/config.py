import os

version = "0.0.3"

import ctypes
myappid = 'nearmgr.' + version # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
from configparser import ConfigParser
workdir_tmp = os.path.join(os.getenv('APPDATA'), 'Near')
if (not os.path.exists(workdir_tmp)):
    os.mkdir(workdir_tmp)
app_workdir = os.path.join(workdir_tmp, 'AppFiles')
if (not os.path.exists(app_workdir)):
    os.mkdir(app_workdir)
user_workdir = os.path.join(workdir_tmp, 'UserFiles')
if (not os.path.exists(user_workdir)):
    os.mkdir(user_workdir)
user_conf_path = os.path.join(user_workdir, "user_config.ini")
app_conf_path = os.path.join(app_workdir, "app_config.ini")
if (not os.path.exists(user_conf_path)):
    with open(user_conf_path, "w") as f:
        print(
"""[font]
path = ???
size = 30
[common]
safe_time = 3600""", file= f)


if (not os.path.exists(app_conf_path)):
    with open(app_conf_path, "w") as f:
        print(
"""[net]
verification_link = ???
""", file= f)

user_config = ConfigParser()
app_config = ConfigParser()
user_config.read(user_conf_path)
app_config.read(app_conf_path)
font_path =user_config.get("font", "path")
font_size =user_config.getint("font", "size")
verification_link = "45.67.58.175/nearmgr"
safe_time = user_config.getint("common", "safe_time")