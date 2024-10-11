from tkinter import Tk
from tkinter import LEFT
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from tkinter import END


class WindowLogin(Tk):
    """登录窗口"""

    def __init__(self):
        """初始化登录窗口"""
        super(WindowLogin, self).__init__()

        # 设置窗口属性
        self.window_init()

        # 填充控件
        self.add_widgets()

        # 事件触发
        self.on_login_click(lambda: print(self.get_user_info()))
        self.on_reset_click(lambda: self.clear())

    def window_init(self):
        """初始化窗口属性"""
        # 设置窗口标题
        self.title("登录窗口")

        # 设置窗口不能被拉伸
        self.resizable(False, False)

        # 设置窗口大小和位置
        wind_width = 255
        wind_height = 95

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        pos_x = (screen_width - wind_width) / 2
        pos_y = (screen_height - wind_height) / 2

        self.geometry('%dx%d+%d+%d' % (wind_width, wind_height, pos_x, pos_y))

    def add_widgets(self):
        """添加控件到窗口里"""
        # 用户名
        username = Label(self, text="账 号:")
        username.grid(row=0, column=0, padx=10, pady=5)

        username_entry = Entry(self, name="username_entry")
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        username_entry['width'] = 25

        # 密码
        password = Label(self, text="密 码")
        password.grid(row=1, column=0, padx=10, pady=5)

        password_entry = Entry(self, name="password_entry")
        password_entry.grid(row=1, column=1, padx=10, pady=5)
        password_entry.config(show="#")  # 隐藏密码
        password_entry['width'] = 25

        # 按钮区
        # 创建Frame
        button_frame = Frame(self, name="button_frame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=1)
        # 登录
        login_bt = Button(button_frame, name="login_button", text=" 登录 ")
        login_bt.pack(side=LEFT, padx=10, fill="x", expand=True)
        # 重置
        reset_bt = Button(button_frame, name="reset_button", text=" 重置 ")
        reset_bt.pack(side=LEFT, padx=10, fill="x", expand=True)

    def get_user_info(self):
        """获取用户账号"""
        return self.children["username_entry"].get(), self.children["password_entry"].get()

    def clear(self):
        """清空账号和密码"""
        self.children["username_entry"].delete(0, END)
        self.children["password_entry"].delete(0, END)

    def on_login_click(self, command):
        """登录按钮的响应"""
        login_bt = self.children['button_frame'].children['login_button']
        login_bt['command'] = command

    def on_reset_click(self, command):
        """重置按钮的响应"""
        reset_bt = self.children['button_frame'].children['reset_button']
        reset_bt['command'] = command

    def on_window_close(self, command):
        """关闭窗口的响应注册"""
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == '__main__':
    wind_login = WindowLogin()
    wind_login.mainloop()
