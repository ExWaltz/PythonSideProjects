import tkinter as tk
import codecs
import requests
import webbrowser as wb
import YT_Search as yt
from io import BytesIO
from PIL import Image, ImageTk


class Window:
    def __init__(self):
        self.color_pallet = ["#ed6663", "#b52b65", "#3c2c3e", "#59405c"]
        self.root = tk.Tk()
        self.root.title('Youtube Search')
        self.root.geometry('750x500')
        self.root.iconbitmap('icon.ico')
        self.isnew = True
        self.vid_frame_list = []
        
        self.vid_Link_list = []
        self.Pimg = []
        self.chnl_link = []
        self.Vimg1 = []
        self.each_vid_link = []
        self.MakeWindow()

    def getInfo(self):
        self.open_vid_file = codecs.open('search.log', 'r', 'utf-8')
        self.open_chnl_file = codecs.open('searchChnl.log', 'r', 'utf-8')
        self.chnl_val_list = self.open_chnl_file.read()
        self.chnl_val_list = str(self.chnl_val_list).splitlines(0)
        self.vid_val_list = self.open_vid_file.read()
        self.vid_val_list = str(self.vid_val_list).splitlines(0)
        self.CloseAllFiles()

    def CloseAllFiles(self):
        self.open_vid_file.close()
        self.open_chnl_file.close()

    def OpenLink(self, link):
        wb.open(str(link))

    def ResultsInfo(self, RES_TEXT, RES_IMG, RES_LINK, vidNUM):
        self.vid_frame = tk.Frame(
            self.results_frame, bd=3, bg=self.color_pallet[3])
        self.vid_Link = tk.Button(self.vid_frame, text=RES_TEXT, font=('Arial bold', 10), width=700, wraplength=300,
                                  bg=self.color_pallet[2], fg=self.color_pallet[0], relief=tk.FLAT, image=RES_IMG, compound=tk.LEFT, anchor=tk.W, justify=tk.LEFT, command=lambda: self.OpenLink(RES_LINK))
        self.vid_frame_list.append(self.vid_frame)
        self.vid_Link_list.append(self.vid_Link)
        self.vid_frame_list[vidNUM].pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.vid_Link_list[vidNUM].pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        self.root.update()

    def CloseResults(self):
        for eachvids in self.vid_frame_list:
            eachvids.pack_forget()
            for eachvidlink in self.vid_Link_list:
                eachvidlink.pack_forget()
        self.vid_frame_list.clear()
        self.vid_Link_list.clear()
        self.Pimg.clear()
        self.chnl_link.clear()
        self.Vimg1.clear()
        self.each_vid_link.clear()

    def ShowVidResults(self):
        for each_vid in range(len(self.vid_val_list)):
            vid_part = str(self.vid_val_list[each_vid]).split(":`~|")
            vid_info_text = f"{vid_part[2]}\n{vid_part[5]}\n{vid_part[6]}\n{vid_part[7]}"
            response1 = requests.get(f"http://{str(vid_part[3])}")
            img_obj1 = Image.open(BytesIO(response1.content))
            self.Vimg1.append(ImageTk.PhotoImage(img_obj1))
            self.each_vid_link.append((vid_part[4]))
            self.ResultsInfo(
                vid_info_text, self.Vimg1[each_vid], self.each_vid_link[each_vid], each_vid + len(self.chnl_val_list))
        self.isnew = False

    def ShowChnlResults(self):
        print('showing')
        for each_chnl in range(len(self.chnl_val_list)):
            chnl_part = str(self.chnl_val_list[each_chnl]).split(":`~|")
            response = requests.get(f"http://{str(chnl_part[1])}")
            img_obj = Image.open(BytesIO(response.content))
            self.Pimg.append(ImageTk.PhotoImage(img_obj))
            self.chnl_link.append(chnl_part[2])
            self.ResultsInfo(chnl_part[0], self.Pimg[each_chnl],
                             self.chnl_link[each_chnl], each_chnl)
            self.root.update()
        self.ShowVidResults()

    def SearchYoutube(self):
        try:
            search_hold_val = str(self.search_entry.get())
            yt.YoutubeSearch(search_hold_val)
            if not self.isnew:
                self.CloseResults()
            self.getInfo()
            self.ShowChnlResults()
        except Exception:
            raise Exception

    def MakeEntryFrame(self):
        search_frame = tk.Frame(self.main_frame, bg=self.color_pallet[3], bd=5)
        self.search_entry = tk.Entry(search_frame, font=(
            'Arial bold', 19), relief=tk.FLAT, bg=self.color_pallet[2], fg=self.color_pallet[0])
        search_button = tk.Button(search_frame, text="Search", font=('Arial bold', 10), width=15, bd=4,
                                  bg=self.color_pallet[0], fg=self.color_pallet[2], relief=tk.FLAT, command=self.SearchYoutube)
        # Deploy EntryFrame
        search_frame.pack(side=tk.TOP, fill=tk.X)
        search_button.pack(side=tk.RIGHT)
        self.search_entry.pack(side=tk.TOP, fill=tk.X)

    def ScrollCanvas(self, event):
        self.main_canvas.yview_scroll(-1 * int(event.delta / 120), 'units')

    def MakeWindow(self):
        self.main_frame = tk.Frame(self.root, bg=self.color_pallet[3])
        self.main_canvas = tk.Canvas(
            self.main_frame, height=700, width=500, bg=self.color_pallet[3], highlightthickness=0)
        self.results_scrollbar = tk.Scrollbar(
            self.main_frame, orient="vertical", command=self.main_canvas.yview)
        self.results_frame = tk.Frame(
            self.main_canvas, bg=self.color_pallet[3])
        self.results_scrollbar.bind("<Configure>", lambda e: self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.bind_all('<MouseWheel>', self.ScrollCanvas)
        self.main_canvas.create_window(
            (0, 0), window=self.results_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.MakeEntryFrame()
        self.results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.root.mainloop()


if __name__ == '__main__':
    Window()
