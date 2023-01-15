import dearpygui.dearpygui as dpg

from time import sleep


def long_async_preparer(data, sender):
    floaty = get_value("Async Input Data")
    dpg.asyarun_async_function(long_callback, floaty, return_handler=long_async_return)


def long_callback(sender, data):
    sleep(3)
    return data * 2


def long_async_return(sender, data):
    log_debug(data)


def long_callback2(sender, data):
    sleep(3)
    log_debug(data * 2)

show_logger()
add_text(
    "input a number and see the logger window for the output of the long callback that would normally freeze the GUI")
add_input_float("Async Input Data", default_value=1.0)
add_button("long Function", callback=long_callback2, callback_data=get_value("Async Input Data"), tip="This is the long callback that will freeze the gui")
add_button("long Asynchronous Function", callback=long_async_preparer, tip="this will not a freeze the GUI")

start_dearpygui()