import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk


class App:
    def __init__(self):
        self.MainFrame()

    def MainFrame(self):
        self.root = tk.Tk()
        self.root.geometry('480x640')
        self.root.title('Text Reader')
        main_frame = tk.Frame(self.root, bg='#4e89ae')

        info_frame = tk.Frame(main_frame, bg='#8d93ab', height=40)
        self.file_listBox = ttk.Combobox(
            info_frame, state='readonly', postcommand=self.SelectedText)
        folder_button = tk.Button(
            info_frame, bg='#f1f3f8', width=3, relief='flat', bd=4, font=('Century Gothic', 8), text='Open', command=self.OpenDir)

        footer_frame = tk.Frame(main_frame, bg='#8d93ab', height=40)

        next_button = tk.Button(
            footer_frame, bg='#f1f3f8', width=3, text='>', relief='flat', font=('Century Gothic', 8), command=lambda: self.MoveFiles(True))
        last_button = tk.Button(
            footer_frame, bg='#f1f3f8', width=3, text='<', relief='flat', command=lambda: self.MoveFiles(False))

        text_scroll = tk.Scrollbar(main_frame)
        self.text_box = tk.Text(main_frame, fg='#f1f3f8', relief='flat', state='disabled',
                                bg='#393b44', wrap=tk.WORD, font=('Century Gothic', 12), yscrollcommand=text_scroll.set)
        text_scroll.config(command=self.text_box.yview)

        self.file_listBox.bind('<<ComboboxSelected>>', self.SelectedText)
        self.root.bind_all('<Key>', self.shortCut)

        main_frame.pack(fill='both', expand=1)
        info_frame.pack(side='top', fill='x')
        folder_button.pack(side='left', padx=5, pady=5)
        self.file_listBox.pack(pady=10, padx=40, fill='x')
        footer_frame.pack(side='bottom', fill='x')
        next_button.pack(side='right', padx=5, pady=5)
        last_button.pack(side='left', padx=5, pady=5)
        text_scroll.pack(side='right', fill='y')
        self.text_box.pack(side='top', fill='both', expand=1)

        self.root.mainloop()

    def shortCut(self, key):
        keyPress = key.keycode
        if keyPress == 37 or keyPress == 65:
            self.MoveFiles(False)
        if keyPress == 39 or keyPress == 68:
            self.MoveFiles(True)

    def MoveFiles(self, modifier):
        current_num = self.file_listBox.current()
        max_num = len(self.file_listBox['values'])
        if current_num == -1:
            return
        if modifier:
            Posmod = current_num + 1
            if Posmod <= max_num:
                self.file_listBox.current(Posmod)
        else:
            Negmod = current_num - 1
            if Negmod >= 0:
                self.file_listBox.current(Negmod)
        self.SelectedText()

    def SelectedText(self, event=None):
        try:
            comboVal = str(self.file_listBox.get())
            f = open(f"{self.fileDir}/{comboVal}", 'r', encoding='utf-8')
            f_text = str(f.read())
            self.text_box.config(state='normal')
            self.text_box.delete(1.0, 'end')
            self.text_box.insert(1.0, f_text)
            self.text_box.config(state='disabled')
            self.root.update()
        except Exception:
            return

    def OpenDir(self):
        self.fileDir = fd.askdirectory()
        file_list = []
        for df in os.listdir(str(self.fileDir)):
            path = os.path.join(str(self.fileDir), df)
            if os.path.isdir(path):
                continue
            file_list.append(df)
        self.file_listBox['values'] = file_list
        self.file_listBox.current(0)
        self.SelectedText()


s = App()
