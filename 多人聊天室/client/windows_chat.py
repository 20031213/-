from tkinter import Toplevel, Text, Button, END
from tkinter.scrolledtext import ScrolledText
from time import localtime, strftime, time


class WindowsChat(Toplevel):
    def __init__(self):
        super(WindowsChat, self).__init__()

        # 设置窗口大小
        self.geometry('%dx%d' % (795, 505))

        # 设置窗口不可修改
        self.resizable(False, False)

        # 添加组件
        self.add_widgets()

        # 动态设置标签
        self.welcome('rq')

    def add_widgets(self):
        """添加组件"""
        # 聊天区
        chat_text_area = ScrolledText(self, width=110, height=30)
        chat_text_area.grid(row=0, column=0, columnspan=2)

        chat_text_area.tag_config('green', foreground='#008800')
        chat_text_area.tag_config('system', foreground='red')
        self.children['chat_text_area'] = chat_text_area

        # 输入区
        chat_input_area = Text(self, name='chat_input_area',
                               width=100, height=7)
        chat_input_area.grid(row=1, column=0)
        # 发送按钮
        send_button = Button(self, name='send_button',
                             width=5, height=2, text='发送')
        send_button.grid(row=1, column=1, pady=10)

    def welcome(self, nickname):
        self.title('欢迎%s' % nickname)

    def on_send_button(self, command):
        """注册事件，当点击发送时消息会发送到服务器并打印"""
        self.children['send_button']['command'] = command

    def get_input_text(self):
        """获取输入框内容"""
        return self.children['chat_input_area'].get(0.0, END)

    def clear_input(self):
        """清空输入框内容"""
        self.children['chat_input_area'].delete(0.0, END)

    def append_text(self, sender, message):
        """添加一条消息到聊天区"""
        send_time = strftime("%Y-%m_%d %H:%M:%S", localtime(time()))
        send_info = '%s:%s' % (sender, send_time)
        self.children['chat_text_area'].insert(END, send_info + '\n', 'green')
        self.children['chat_text_area'].insert(END, '  ' + message + '\n')
        # 向下滚动屏幕
        self.children['chat_text_area'].yview(END)

    def on_window_closed(self, command):
        """注册关闭窗口时执行的指令"""
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == '__main__':
    windowschat = WindowsChat()
    windowschat.mainloop()
