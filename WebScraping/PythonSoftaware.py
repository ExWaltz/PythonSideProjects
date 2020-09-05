import tkinter as tk


color_pallet = ["#6A605C", "#9B5094",
                "#9A94BC", "#8FB8DE", "#CDF7F6", "#eDF7F6"]


def main():
    root = tk.Tk(screenName="Top Search")
    root.geometry("500x490")
    main_background_frame = tk.Frame(
        root, width=500, height=500)
    main_title = tk.Label(main_background_frame, text="Top Search",
                          bg=color_pallet[1], fg=color_pallet[4])
    main_search_entry = tk.StringVar()
    main_search = tk.Entry(
        main_background_frame, textvariable=main_search_entry, bg=color_pallet[2], fg=color_pallet[0])
    main_search_button = tk.Button(main_background_frame, text="Search", relief=tk.FLAT,
                                   bg=color_pallet[3], fg=color_pallet[0])
    main_background_frame.place(width=500, height=500)
    main_search.place(relwidth=0.8, relheight=0.1, rely=0.04)
    main_search_button.place(relwidth=0.2, relheight=0.1, rely=0.04, relx=0.8)
    main_title.place(relwidth=1, relheight=0.04)
    root.mainloop()


if __name__ == '__main__':
    main()
