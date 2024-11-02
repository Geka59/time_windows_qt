import winreg
import sqlite3
from system_operation import get_exe_path,resource_path,get_db_path
path_to_db=get_db_path("data.db")
db_Htime=sqlite3.connect(path_to_db,check_same_thread=False)
#cursor=db_Htime.cursor()



def add_to_autorun():
    #file_path = __file__
    file_path=get_exe_path()
    print(file_path)
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Microsoft\Windows\CurrentVersion\Run', #todo на всех пользлвателей

    access=winreg.KEY_SET_VALUE)
    print(file_path)

    winreg.SetValueEx(key, 'test', 0, winreg.REG_SZ, file_path)
    key.Close()

def db_empty():
    cursor = db_Htime.cursor()
    #cursor.execute("CREATE TABLE IF NOT EXISTS admin (password VARCHAR(30))")
    #db_Htime.commit()
    cursor.execute("SELECT * FROM admin")

    if cursor.fetchall() == []:
        cursor.close()
        return True
    else:
        cursor.close()
        return False


def save_password(passvord):
    cursor = db_Htime.cursor()
    print(passvord)
    cursor.execute("INSERT INTO admin VALUES(?)", [passvord])
    db_Htime.commit()
    cursor.close()

def enabling_limits(limiting_user):
    cursor = db_Htime.cursor()
    cursor.execute("UPDATE temp_limits SET enabled=? WHERE user=?",[1,limiting_user])
    db_Htime.commit()
    cursor.close()
def disable_limits(limiting_user):
    cursor = db_Htime.cursor()
    cursor.execute("UPDATE temp_limits SET enabled=? WHERE user=?",[0,limiting_user])
    db_Htime.commit()
    cursor.close()

def updating_temp_limits(data_limits):
    cursor = db_Htime.cursor()
    weekday_data=data_limits[0]
    user_data = data_limits[1]
    limit_data = data_limits[2]
    cursor.execute("SELECT * FROM temp_limits WHERE weekday=? AND user=?",[weekday_data,user_data])
    if cursor.fetchall()==[]:
        cursor.execute("INSERT INTO temp_limits VALUES(?,?,?,?)", [weekday_data, user_data,limit_data,0]) #todo переделать на апдейт
    else:
        cursor.execute("UPDATE temp_limits SET [limit]=? WHERE weekday=? AND user=?",[limit_data,weekday_data,user_data])
    #cursor.execute("DELETE FROM temp_limits WHERE weekday=? AND user=?",[weekday_data,user_data])
    db_Htime.commit()
    cursor.close()
    #db_Htime.commit()

def creating_limit_record(username,weekday,date):
    '''Создает запсть с датой в бд'''
    cursor = db_Htime.cursor()
    cursor.execute("SELECT * FROM users WHERE weekday=? AND user=?", [weekday, username])
    if cursor.fetchall() == []:
        cursor.execute("INSERT INTO users VALUES(?,?,?,?)",
                       [username, weekday,'00:00', date])
    else:
        cursor.execute("UPDATE users SET data=? WHERE weekday=? AND user=?",
                       [date,weekday,username])
    db_Htime.commit()
    cursor.close()
def updating_limits_record(user,date,time):
    """Функиця обновлення прошедшего времени"""
    cursor = db_Htime.cursor()
    cursor.execute("SELECT * FROM users WHERE user=? AND data=?",[user,date])
    responce=cursor.fetchall()
    new_limit=minus_time(responce[0][2],1)
    #print(responce)
    #print(new_limit)
    cursor.execute("UPDATE users SET [time_passed]=? WHERE data=? AND user=?",[new_limit,date,user])
    db_Htime.commit()
    cursor.close()


def minus_time(time,what_minus):
    '''На самом деле функция добавляет 1 к прошедшеум времени'''

    hours=int(time[:2])
    minutes=int(time[3:])

    if minutes+what_minus>59:
        hours_new=(hours + 1)
        minutes_new = 0
        resp=time_passed_good_looking([hours_new,minutes_new])
        return resp
    else:
        hours_new = hours
        minutes_new = minutes + what_minus
        resp=time_passed_good_looking([hours_new,minutes_new])
        #print(minutes_new)
        return resp

def time_for_life(user,date,balance):
    cursor = db_Htime.cursor()
    responce = balance
    if responce !=[]:
        new_limit_with_plus = plus_time_for_life(responce)
        cursor.execute("UPDATE users SET [time_passed]=? WHERE data=? AND user=?", [new_limit_with_plus, date, user])
        db_Htime.commit()
    cursor.close()

def plus_time_for_life(time):
    '''Функция вычитания 1 минуты из лимита, для возможности выхода'''
    hours = int(time[:2])
    minutes = int(time[3:])
    if hours==0 and minutes==0:
        return '00:00'
    if minutes-1 < 0 and hours>0:
        hours_new=(hours - 1)
        minutes_new = 59 #////////////////////////////////////////////// пофикшенная строчка
        resp=time_passed_good_looking([hours_new,minutes_new])
        return resp
    else:
        hours_new = hours
        minutes_new = minutes -1
        resp=time_passed_good_looking([hours_new,minutes_new])
        #print(minutes_new)
        return resp

def time_passed_good_looking(time_input):# todo not working
    hours=str(time_input[0])
    minutes=str(time_input[1])
    if len(hours)<2:
        hours='0'+hours
    if len(minutes)<2:
        minutes='0'+minutes

    return (hours+':'+minutes)

def get_limiting_today(weekday,username,date):
    '''Получение сегодняшнего прошедшего времени'''
    cursor = db_Htime.cursor()
    cursor.execute("SELECT * FROM users WHERE user=? AND data=?", [username, date])
    responce=cursor.fetchall()
    cursor.close()
    if responce!=[]:
        return responce[0][2]
    else:
        return []
def get_data_temp(data_on_execute):
    cursor = db_Htime.cursor()
    weekday_data = data_on_execute[0]
    user_data = data_on_execute[1]
    cursor.execute("SELECT * FROM temp_limits WHERE weekday=? AND user=?",[weekday_data,user_data])
    ret_resp=cursor.fetchall()
    cursor.close()
    return ret_resp
def get_today_balance(username,weekday_data):
    cursor = db_Htime.cursor()
    cursor.execute("SELECT * FROM temp_limits WHERE weekday=? AND user=?",[weekday_data,username])
    resonce_data=cursor.fetchall()
    ret_data=resonce_data[0][2]
    cursor.close()
    return ret_data
def rewiew_passvord(password):
    cursor = db_Htime.cursor()
    cursor.execute("SELECT * FROM admin")
    arr_pass=cursor.fetchone()
    cursor.close()
    if password in arr_pass:
        return True
    else:
        return False
def creating_tabels():
    cursor = db_Htime.cursor()
    #cursor = db_Htime.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS admin (password VARCHAR(30))")
    db_Htime.commit()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS temp_limits (weekday VRACHAR (15),user VARCHAR (50), [limit] VARCAHR (15), enabled INTEGER (1))")
    db_Htime.commit()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (user VARCHAR (35),weekday VARCHAR (15),time_passed VRACHAR (15),data VARCHAR (15))")
    db_Htime.commit()
    cursor.close()

    #cursor.close()


