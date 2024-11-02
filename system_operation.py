import sys
import os
import datetime
import threading
#image=PIL.Image.open('etr.png')
def on_ckicked(icon,item):
    pass
    #ui.show()
    #app.exec()
#icon=pystray.Icon('Name',image, menu=pystray.Menu(pystray.MenuItem('Open',on_ckicked)))

def get_user_list():
    #keki=os.system("net user")
    good_users_view=[]
    pre_users_str = os.popen('wmic useraccount get name,status').read()
    arr_trash=pre_users_str.split('\n')
    for i in range(len(arr_trash)):
        if (' OK ' in arr_trash[i]):
            slice_username = arr_trash[i].index(' ')
            good_users_view.append(arr_trash[i][:slice_username])
    print(good_users_view)
    return good_users_view

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_exe_path():
    if getattr(sys, 'frozen', False):
        # Код выполняется в режиме frozen (exe)
        exe_dir = os.path.dirname(sys.executable)
        exe_name = os.path.basename(sys.executable)
    else:
        # Код выполняется в режиме скрипта (.py)
        exe_dir = os.path.dirname(os.path.abspath(__file__))
        exe_name = os.path.basename(sys.argv[0])  # или можно использовать os.path.basename(__file__)

    full_path = os.path.join(exe_dir, exe_name)
    return full_path
def get_db_path(db_name):
    if getattr(sys, 'frozen', False):
        # Код выполняется в режиме frozen (exe)
        exe_dir = os.path.dirname(sys.executable)

    else:
        # Код выполняется в режиме скрипта (.py)
        exe_dir = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(exe_dir, db_name)
    return full_path
def get_current_user():
    return os.getlogin()

def time_work():
    dt_now = datetime.datetime.now()
    print()
def get_today_weekday():
    '''возвращает номер текущего дня недели'''
    today_weekday=datetime.datetime.today().weekday()
    return today_weekday
    #print(arr_trash)
#ter = get_user_list()
def get_today_date():
    current_date = datetime.date.today()
    return current_date
def get_now_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


# def start_timer():
#     timer_thread = threading.Timer(7, timer_expired)# todo изменить н анеобходимое количество секунд
#     timer_thread.start()
#     return timer_thread
    #действия с бд

   # users_can=os.system('')

    #print(type(responce))
    # path="C:/Users"
    # directory = os.listdir(path)
    # print(directory)
    # users_list=psutil.users()
    # #print(users_list)
    # username = os.getlogin()
    # print(username)
    # return users_list


def shutdown_system():
    os.system("logoff")