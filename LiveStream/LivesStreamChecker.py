import sqlite3
import requests
import webbrowser as wb
import tkinter as tk
from YTLivestream import SearchEvents
from PIL import Image, ImageTk
from io import BytesIO


class Database:
    def __init__(self, dbName):
        self.dbName = dbName
        self.chnlInfo = {}

    def setupDatabase(self):
        self.connectDb = sqlite3.connect(self.dbName)
        self.dbCursor = self.connectDb.cursor()
        return self.dbCursor

    def saveDatabase(self):
        self.connectDb.commit()

    def closeDatabase(self):
        self.connectDb.close()


class App(Database):
    def __init__(self, master):
        super(App, self).__init__("YoutuberInfo.db")
        self.master = master
        self.current_folder = 0
        self._MainFrame()

    def _MainFrame(self):
        self.main_frame = tk.Frame(self.master, bg="#333333")
        self.main_header = tk.Frame(self.main_frame, height=50, bg="#eeeeee")
        # Instantiate Widgets
        self.main_frame.pack(fill="both", expand=1)
        self.main_header.pack(fill="x", padx=10)
        self._makeHeaderButtons()
        self._makeSearchFolder()

    def _makeHeaderButtons(self):
        header_home = tk.Button(
            self.main_header, text="Search", height=2, width=10, relief="solid", borderwidth=1, command=self._SearchFolder)
        header_video = tk.Button(
            self.main_header, text="Videos", height=2, width=10, relief="solid", borderwidth=1, command=self._VideoFolder)
        header_home.pack(side="left", fill="y")
        header_video.pack(side="left", fill="y")

    def _SearchFolder(self):
        self.current_folder = 0
        self.videos_holder.forget()
        self.search_holder.pack(expand=1)
        self.master.update()

    def _VideoFolder(self):
        self.current_folder = 1
        self.search_holder.forget()
        self._makeVideoFolder()
        self.master.update()

    def _makeSearchFolder(self):
        # Hold Main Frame
        self.search_holder = tk.Frame(self.main_frame, bg="#aaaaaa")
        # Logo
        self.main_logo = tk.Text(self.search_holder, borderwidth=0, width=30, wrap="word",
                                 height=2, relief="flat", font=("Century Gothic bold", 26))
        self.main_logo.tag_config("center", justify=tk.CENTER)
        self.main_logo.insert(1.0, "Youtube Event Searcher")
        self.main_logo.config(state="disabled")
        self.main_logo.tag_add("center", 1.0, "end")

        # Search Box
        self.main_text_var = tk.StringVar()
        self.main_search = tk.Entry(
            self.search_holder, textvariable=self.main_text_var, font=("Century Gothic bold", 22))
        self.main_search_button = tk.Button(
            self.search_holder, text="Search", relief="flat", font=("Century Gothic bold", 15), command=self.SearchYoutube)

        # Instantiate widgets
        self.search_holder.pack(expand=1)  # Center Search Frame
        self.main_logo.pack(side="top", fill="x", pady=10)
        self.main_search_button.pack(side="right")
        self.main_search.pack(side="top", fill='x', padx=5)
        self.master.update()

    def _getChnlInfo(self, chnlName):
        self.cursorDataBase.execute(
            """SELECT Channel_Name, Channel_Url, Channel_Img FROM ytData WHERE Channel_Name=:n""", {"n": chnlName})
        chnl_info = self.cursorDataBase.fetchall()
        return chnl_info[0]

    def _makeChannelFrame(self):
        chnl_name_holder = self.resultsName
        chnl_info_list = self._getChnlInfo(chnl_name_holder)
        imgUrl = chnl_info_list[1]
        imgResponse = requests.get(imgUrl).content
        img = Image.open(BytesIO(imgResponse)).resize((100, 100))
        self.chnlInfo[chnl_info_list] = [chnl_info_list[0],
                                         ImageTk.PhotoImage(img), chnl_info_list[2]]
        chnl_frame = tk.Button(self.videos_holder, text=self.chnlInfo[chnl_info_list][0],
                               height=100, image=self.chnlInfo[chnl_info_list][1], anchor=tk.W,
                               justify=tk.LEFT, compound=tk.LEFT)
        chnl_frame.pack(fill="x", side="top")

    def _makeVideoFolder(self):
        videos_Scroll = tk.Scrollbar(self.main_frame)
        self.videos_holder = tk.Text(
            self.main_frame, state="disabled", yscrollcommand=videos_Scroll)
        videos_Scroll.config(command=self.videos_holder.yview)
        videos_Scroll.pack(side="right", fill="y")
        self.videos_holder.pack(side="top", fill="both", expand=1)
        self._makeChannelFrame()

    def SearchYoutube(self):
        searchVal = str(self.main_text_var.get())
        query = SearchEvents()
        self.resultsList = query._RequestWebsite(searchVal)
        if len(self.resultsList) != 0:
            print("Found")
            self.addDatabase()

    def addDatabase(self):
        self.cursorDataBase = self.setupDatabase()
        self.cursorDataBase.execute(
            """SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ytData'""")
        if self.cursorDataBase.fetchone()[0] != 1:
            self.cursorDataBase.execute(
                """CREATE TABLE ytData (
                        Channel_Name text,
                        Channel_Url text,
                        Channel_Img text,
                        Video_Title text PRIMARY KEY,
                        Video_Url text,
                        Video_Date text,
                        Video_Img text
                )""")

        for result in self.resultsList:
            self.resultsName = result[0]
            self.cursorDataBase.execute("""INSERT INTO ytData(Channel_Name, Channel_Img, Channel_Url, Video_Title, Video_Url, Video_Date, Video_Img)
                                            VALUES (:Channel_Name, :Channel_Url, :Channel_Img, :Video_Title, :Video_Url, :Video_Date, :Video_Img)
                                            ON CONFLICT(Video_Title) DO UPDATE SET Channel_Name=excluded.Channel_Name, Channel_Img=excluded.Channel_Img, Channel_Url=excluded.Channel_Url, Video_Title=excluded.Video_Title, Video_Url=excluded.Video_Url, Video_Date=excluded.Video_Date, Video_Img=excluded.Video_Img""",
                                        {"Channel_Name": result[0], "Channel_Url": result[1], "Channel_Img": result[2], "Video_Title": result[3], "Video_Url": result[4], "Video_Date": result[5], "Video_Img": result[6]})
            self.saveDatabase()


def main():
    root = tk.Tk()
    root.title("Youtube Event Searcher")
    root.geometry("700x400")
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
