import tkinter


def test():
    windows = tkinter.Tk()
    windows.title("登录界面")

    login_bt = tkinter.Button(windows, name="login", text='登录')
    login_bt.grid(row=0, column=1)

    reset_login = tkinter.Button(windows, name="reset", text='重置')
    reset_login.grid(row=1, column=1)

    windows.mainloop()


test()
