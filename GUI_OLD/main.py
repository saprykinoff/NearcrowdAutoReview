from dearpygui import dearpygui as dpg
import threading
import funcs
import datetime
dpg.create_context()
dpg.create_viewport(title='NEAR Farm', width=1200, height=900)
dpg.setup_dearpygui()
accounts = funcs.get_json('accounts.json')
n = len(accounts)
m = 3
def _callback(sender, keyword, user_data):
    acc = user_data
    t = threading.Thread(target=funcs.launch_browser, args=[acc])
    t.start()
with dpg.window(label="NEAR Farm", tag="main"):

    with dpg.table(header_row=False, tag="main_table"):
        for j in range(m):
            dpg.add_table_column()
        i = 0
        for acc in accounts.keys():
            with dpg.table_row(tag=f"main_table[{i}]"):
                dpg.add_text(f"Account: ???", tag=f"main_table[{i}][{0}]")
                dpg.add_text(f"Status: ???", tag=f"main_table[{i}][{1}]")
                dpg.add_button(tag=f"main_table[{i}][{2}]", label="Open browser", callback=_callback, user_data=acc)
            i += 1
    dpg.add_text(tag="time")

deftheme = dpg.get_item_theme("main_table[0][2]")

def set_table():
    status = funcs.get_json('status.json')
    if (status is None):
        return
    dpg.set_value("time", f"Last update: {datetime.datetime.now().strftime('%H:%M:%S')}")
    i = 0
    for acc, stat in status.items():
        dpg.set_value(f"main_table[{i}][{0}]", acc)
        dpg.set_value(f"main_table[{i}][{1}]", stat)

        color = (25, 128, 58)
        if (stat.count(":") == 2):
            dpg.set_item_label(f"main_table[{i}][{2}]", "Open review")
            with dpg.theme() as item_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, color, category=dpg.mvThemeCol_Text)
                    dpg.add_theme_color(dpg.mvThemeCol_Button, color, category=dpg.mvThemeCol_Text)
            dpg.bind_item_theme(f"main_table[{i}][{2}]", item_theme)
        else:
            dpg.bind_item_theme(f"main_table[{i}][{2}]", deftheme)
            dpg.set_item_label(f"main_table[{i}][{2}]", "Open task")

        i += 1
def upd():
    while 1:
        set_table()
t1 = threading.Thread(target=upd)
t1.start()
dpg.set_primary_window("main", True)
dpg.show_viewport()
dpg.start_dearpygui()
# while dpg.is_dearpygui_running():
#     set_table()
#     dpg.render_dearpygui_frame()
dpg.destroy_context()
