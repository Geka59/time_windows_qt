from PyQt5 import QtWidgets, uic, QtGui, QtCore,QtMultimedia
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QSystemTrayIcon, QMenu, QMessageBox, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

from system_operation import get_user_list,resource_path,get_current_user,get_today_weekday,get_today_date,get_now_time,shutdown_system
from work_rees import db_empty, save_password,rewiew_passvord,enabling_limits,updating_temp_limits,\
    get_data_temp,disable_limits,get_limiting_today,creating_limit_record,get_today_balance,updating_limits_record,add_to_autorun,creating_tabels ,time_for_life
import sys
import os
import ctypes
#from playsound import playsound
import threading
#не пашет регэдие т музыка

class UserInterface():
    def __init__(self):
        self.main_timer = None
        self.app = QtWidgets.QApplication([])
        self.ui = uic.loadUi(resource_path("graphics.ui"))
        self.ui_password = uic.loadUi(resource_path("password.ui"))
        self.app.setQuitOnLastWindowClosed(False)
        self.tray=QtWidgets.QSystemTrayIcon(QtGui.QIcon(resource_path('etr.png')))
        ag = QDesktopWidget().availableGeometry()
        # sg = QDesktopWidget().screenGeometry()
        widget = self.ui.geometry()
        self.mooving_coordinates=[ag.width() - widget.width(),ag.height() - widget.height() - widget.height() // 8]
        self.ui.move(self.mooving_coordinates[0],self.mooving_coordinates[1])
        self.ui_password.pushButton_2.hide()
        self.ui.pushButton_4.hide()
        self.current_user= get_current_user()
        print(self.current_user)
        self.arr_weekdays=['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
        self.admin_mode=False
        creating_tabels()
        self.checking_limit_for_user()
        self.set_text_buuton_limits()
        self.media_player = QMediaPlayer()

        self.ui.comboBox.view().window().setWindowFlags(
            QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.ui.comboBox.view().window().setAttribute(
            QtCore.Qt.WA_TranslucentBackground)


        ### making error message box
        self.err=QMessageBox()
        self.err.setWindowTitle('Ошибка!')
        self.err.setText('Некоторые поля не заполнены')
        self.err.setIcon(QMessageBox.Warning)




    def act(self):#действие при клике на трей
        self.admin_out()
        user=get_current_user()
        self.ui.comboBox.setCurrentText(user)
        self.set_today_weekday_on_ui()
        self.ui.move(self.mooving_coordinates[0],self.mooving_coordinates[1])
        self.ui.show()
        self.new_vizualize()



    def run_as_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def main_timer_left(self):
        self.start_timer()
        print(get_now_time())
        current_username = get_current_user()
        date=get_today_date()
        weekday=self.arr_weekdays[get_today_weekday()]
        updating_limits_record(current_username,date,1)
        time_passed=(get_limiting_today(weekday,current_username,date))
        self.ui.label_5.setText(time_passed)
        balance = get_today_balance(current_username, weekday)
        time_ostalos = self.minus_time(balance, time_passed)
        good_looking_time = self.time_ostalos_good_looking(time_ostalos)
        self.ui.label_2.setText(good_looking_time)
        if time_ostalos[0] < 1 and time_ostalos[1]==10:
            self.plaing_song_10_minutes()

        if time_ostalos[0] < 0 or time_ostalos[1]<0:
            time_for_life(current_username, date, balance)
            shutdown_system()
        if time_ostalos[0] < 1 and time_ostalos[1]==0:
            self.plaing_song_1_minute()
        # в бд дейтвие по добавлению прошедшего времени
        #  отправка на фронт обноаления времени
        #  запуск таймер по новой
        #print(10)

    def start_timer(self):
        #if (self.main_timer==None):
        self.main_timer = threading.Timer(60, self.main_timer_left)
        self.main_timer.start()


    def main_timer_stop(self):
        if self.main_timer!=None:
            self.main_timer.cancel()
            self.main_timer=None


    def plaing_song_10_minutes(self):
        # CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        # filename = os.path.join(CURRENT_DIR, "start_ewent.wav")
        print('10 min')
        path=resource_path("Sound_16367.wav")
        url = QUrl.fromLocalFile(path)
        content = QMediaContent(url)
        self.media_player.setMedia(content)
        self.media_player.play()

        #filename=resource_path("Sound_16367.wav")
        #new_path = filename.replace('\\', '/')
        #threading.Thread(target=playsound, args=(new_path,), daemon=True).start()

    def plaing_song_1_minute(self):
        # CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        # filename = os.path.join(CURRENT_DIR, "start_ewent.wav")
        print('1 min')
        path_file=resource_path("Sound_16368.wav")
        url = QUrl.fromLocalFile(path_file)
        content = QMediaContent(url)
        self.media_player.setMedia(content)
        self.media_player.play()
        #filename = resource_path("Sound_16368.wav")
        #new_path = filename.replace('\\', '/')
        #threading.Thread(target=playsound, args=(new_path,), daemon=True).start()

    def all_limit_ok(self):
        pass

    def first_run(self):
        if self.run_as_admin():
            add_to_autorun()
            self.ui_password.label.setText('Придумайте пароль')
            self.ui_password.show()
        else:
            self.err_timer = threading.Timer(4, self.qt_quit)
            self.err_timer.start()
            self.ui.hide()
            self.ui_password.hide()
            self.err.setText('Запустите приложение от имени администратора!')
            self.err.show()

    def qt_quit(self):
        self.app.quit()

    def save_passvord(self,password):
        if password != '':
            save_password(password)
            self.ui_password.hide()
            self.ui_password.label.setText('Введите пароль для перехода в режим управления')
            #self.ui_start()
            self.ui.show()
            self.tray.show()

    def checking_limit_for_user(self):
        '''Главная функция проверяющая есть ли лимит на текущего пользвателя'''
        current_username=get_current_user()
        weekday=self.arr_weekdays[get_today_weekday()]
        responce=get_data_temp([weekday,current_username])
        #print(responce)
        if ((responce!=[]) and responce[0][3]==1):
            date_now=get_today_date()
            time_left=get_limiting_today(weekday,current_username,date_now)
            if time_left==[]:
                creating_limit_record(current_username,weekday,date_now) #создаем запись в бд
                time_left = get_limiting_today(weekday, current_username, date_now)
            self.ui.label_5.setText(time_left)
            balance=get_today_balance(current_username,weekday)
            time_ostalos=self.minus_time(balance,time_left)
            print(time_ostalos)
            if (time_ostalos[0] > 0 or time_ostalos[1] > 0):
                good_looking_time=self.time_ostalos_good_looking(time_ostalos)
                self.ui.label_2.setText(good_looking_time)
                if self.main_timer==None:
                    self.start_timer()
            else:
                good_looking_time = self.time_ostalos_good_looking(time_ostalos)
                self.ui.label_2.setText(good_looking_time)
                time_for_life(current_username,date_now,balance)
                print('Все шотдовн')
                shutdown_system()
            #self.ui.label_2.setText(responce[0][2]
        else:
            self.ui.label_2.setText('--')
    def time_ostalos_good_looking(self,time_input):
        hours=str(time_input[0])
        minutes=str(time_input[1])
        if len(hours) < 2:
            hours = '0' + hours
        if len(minutes) < 2:
            minutes = '0' + minutes
        return (hours+':'+minutes)

    # def start_timer(self):
    #     if (self.main_timer.is_alive()==False):
    #         self.main_timer.start()


        #self.new_vizualize
        #set_text_buuton_limits
        #set_today_weekday_on_ui
    def minus_time(self,time1,time_left):
        '''вычитание оставшегося времени за баланса'''
        balance_parse=self.parser_time(time1)
        left_parse=self.parser_time(time_left)
        hours = balance_parse[0] - left_parse[0]
        minutes = balance_parse[1] - left_parse[1]
        if minutes < 0:
            hours -= 1
            minutes += 60
        if hours < 0:
            hours =0
            minutes =-1
        return [hours, minutes]

    def admin_enterance(self):
        if (self.ui.pushButton_4.isVisible()):
            self.admin_out()
        else: #это если все оки
            self.ui_password.pushButton_2.show()

            self.ui_password.pushButton.hide()
            self.ui_password.lineEdit.clear()
            self.ui_password.show()

    def password_check(self):
        password=self.ui_password.lineEdit.text()
        print(password)
        if rewiew_passvord(password):
            self.admin_control()

    def admin_control(self):
        style="""
        background-color:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(242, 99, 99, 255), stop:1 rgba(242, 233, 99, 255));
	    border: none;
	    border-radius: 3px;
	    color: #FFF;
	    margin: 1px
                };
        """
        self.admin_mode = True
        self.ui.pushButton_4.show()
        self.ui.checkBox.show()
        self.ui.spinBox.show()
        self.ui.lineEdit.setReadOnly(False)
        self.ui_password.hide()
        self.ui.pushButton.setStyleSheet(style)

    def admin_out(self):
        self.admin_mode=False
        self.ui.pushButton_4.hide()
        self.ui.checkBox.hide()
        self.ui.spinBox.hide()
        self.ui.lineEdit.setReadOnly(True)
        self.checking_limit_for_user()

    def all_form_fill(self):
        '''Стандартная проверка на
        заполненные формы в окне при
        добавлении ограничения '''
        if len(self.ui.lineEdit.text())==5:

            time_on_check=self.parser_time(self.ui.lineEdit.text())
            if time_on_check[0]>24 or time_on_check[1]>59:
                self.err.setText('Недопустимый формат времени')
                self.err.show()
                return False
            return True
        else:
            return False
    def parser_time(self,time):
        '''Парсер для времени на вход принмает срооку вида чч:мм'''
        if len(time)==5:
            all_time = time
            hours =int(time[:2])
            minutes = int(time[3:])
            return [hours,minutes]
        return None
    def changing_lim(self):
        if self.admin_mode==True and self.all_form_fill():
            #self.main_timer_stop()
            arr_data_lim=[]
            arr_data_lim.append(self.ui.label_7.text()) #weekday
            arr_data_lim.append(self.ui.comboBox.currentText()) #user
            arr_data_lim.append(self.ui.lineEdit.text()) #lim
            updating_temp_limits(arr_data_lim)
            self.checking_limit_for_user()
            #self.start_timer()

    def new_vizualize(self):
        '''Функция обновленя данных при перелистынвании'''

        arr_data_on_show = []
        arr_data_on_show.append(self.ui.label_7.text())  # weekday
        arr_data_on_show.append(self.ui.comboBox.currentText())  # user
        data_on_refresh=get_data_temp(arr_data_on_show)# получение данных из бд

        if data_on_refresh!=[]:
            limit=(data_on_refresh)[0][2]
            self.ui.lineEdit.setText(limit)
        else:
            self.ui.lineEdit.setText('00:00')
        #self.ui.lineEdit.setText()
    def enable_limit(self):
        '''Отправляем в бд статус ограничеий'''
        limiting_user=self.ui.comboBox.currentText()
        resp=self.resp_is_enab_limit(limiting_user)# True fasle
        if resp:
            disable_limits(limiting_user)
            self.main_timer_stop()
        else:
            enabling_limits(limiting_user)
        self.set_text_buuton_limits()
        self.checking_limit_for_user()
        #balance_time=self.ui.lineEdit.text()
        #weekday_limit=self.ui.label_7.text()
        #если ограничения на данного пользоваетеля не устновлены
        #print(f'Установим ограничения на {limiting_user} c лимитом в {balance_time} на {weekday_limit}')

    def resp_is_enab_limit(self,username):
        '''Возращает включены ли ограничения на пользователя'''
        weekday = self.arr_weekdays[get_today_weekday()]
        resp = get_data_temp([weekday,username])
        if (resp!=[]) and (resp[0][3]==1):
            return True
        else:
            return False

    def set_text_buuton_limits(self):
        '''Устанавливает актуальное значение на кнопке ограничений
        1-Отключить ограничения
        0-Включить ограничения
        '''
        user=get_current_user()
        if (self.resp_is_enab_limit(user)):
            self.ui.pushButton_4.setText('Отключить ограничения')
        else:
            self.ui.pushButton_4.setText('Включить ограничения')


    def set_today_weekday_on_ui(self):
        weekday=get_today_weekday()
        text_day=self.arr_weekdays[weekday]
        self.ui.label_7.setText(text_day)
    def click_right_weekday(self):

        weekday_from_ui=self.ui.label_7.text()
        index_arr_weekday=self.arr_weekdays.index(weekday_from_ui)
        self.ui.label_7.setText(self.arr_weekdays[index_arr_weekday+1-7*((index_arr_weekday+1)//7)])
        self.new_vizualize()
        self.changing_lim()
    def click_left_weekday(self):
        weekday_from_ui = self.ui.label_7.text()
        index_arr_weekday = self.arr_weekdays.index(weekday_from_ui)
        if (index_arr_weekday - 1)<0:
            new_index=6
        else:
            new_index=index_arr_weekday - 1

        self.ui.label_7.setText(self.arr_weekdays[new_index])
        self.new_vizualize()
        self.changing_lim()
    #def cheking_first_run(self):
     #   if db_empty():
      #      self.first_run()
    def ui_start(self):
        #self.cheking_first_run()
        # #print(ag.width(),widget.width())
        if db_empty():
             self.first_run()
        else:
            self.ui.show()
            self.tray.show()
        self.set_today_weekday_on_ui()

        self.tray.activated.connect(self.act)
        users=get_user_list()
        self.ui.comboBox.addItems(users)
        self.checking_limit_for_user()
        self.set_text_buuton_limits()
        #print(self.ui.isVisible())
        self.new_vizualize()
        self.ui_password.pushButton.clicked.connect(lambda: self.save_passvord(self.ui_password.lineEdit.text()))
        self.ui.pushButton.clicked.connect(self.admin_enterance)
        self.ui.lineEdit.textChanged.connect(self.changing_lim)
        self.ui.pushButton_4.clicked.connect(self.enable_limit)
        self.ui.comboBox.currentIndexChanged.connect(self.new_vizualize)
        self.ui.pushButton_2.clicked.connect(self.click_right_weekday)
        self.ui.pushButton_3.clicked.connect(self.click_left_weekday)
        self.ui_password.pushButton_2.clicked.connect(self.password_check)
        self.app.exec() #todo убрать потом sys


