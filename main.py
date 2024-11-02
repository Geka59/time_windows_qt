from user_interface import UserInterface





def main():
    ui=UserInterface()
    ui.ui_start()
if __name__== '__main__':
    main()






#key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Run")
# winreg.SetValueEx(key,'new_var',0,winreg.REG_SZ,'1100110')
# nyvalue=winreg.QueryValueEx(key,"Steam")
# if key:
#     winreg.CloseKey(key)
#
# print(nyvalue)