import tkinter as tk
import tkinter.font as Font


# def cases():
operators = ["+", "-", "*", "/"]
color_pallet = ["#41444b", "#52575d", "#fddb3a", "#f6f4e6"]
isNew = True


def OperateNum(sent_operator):
    global isNew
    global f_num
    global s_num
    second_num = entry_bar.get()
    if not isNew:
        f_num = float(second_num)
    else:
        s_num = float(second_num)
    s_opt = str(sent_operator)
    entry_bar.delete(0, tk.END)
    for opts in operators:
        if s_opt == "+":
            cal = f_num + s_num
        if s_opt == "-":
            cal = f_num - s_num
        if s_opt == "*":
            cal = f_num * s_num
        if s_opt == "/":
            cal = f_num / s_num
    entry_bar.insert(0, str(cal))
    entry_label.config(text=f"{f_num} {s_opt} {s_num} = \n{cal}")
    isNew = False


def button_press(button_number):
    global f_num
    global s_num
    global usedOperator
    global isNew
    hold_name = str(button_number)
    try:
        for operate in operators:
            if hold_name == operate:
                first_num = entry_bar.get()
                isNew = True
                f_num = float(first_num)
                entry_bar.delete(0, tk.END)
                usedOperator = str(hold_name)
                entry_label.config(text=f"{f_num} {usedOperator}\n")
                return

        if hold_name == "Enter":
            OperateNum(usedOperator)
            return

        if hold_name == "Clear":
            entry_bar.delete(0, tk.END)
            f_num = 0
            s_num = 0
            return

        if isNew:
            current_entry = entry_bar.get()
            entry_bar.delete(0, tk.END)
            entry_bar.insert(0, str(current_entry) + str(button_number))

        else:
            entry_bar.delete(0, tk.END)
            entry_bar.insert(0, str(button_number))
            isNew = True
    except Exception:
        return


def MakeNumPad(root_frame, numText, Incol, Inrow):
    numPad = tk.Button(root_frame, text=numText, width=8, bg=color_pallet[0], fg=color_pallet[2], height=6, relief=tk.FLAT, font=defaultFont, command=lambda: button_press(numText))
    numPad.grid(row=Inrow, column=Incol, padx=5, pady=5)


def Main():
    global defaultFont
    global entry_bar
    global entry_label
    # Main Frame
    root = tk.Tk(className="Calculator")
    root.title("Calculator")
    root.iconbitmap("icon.ico")
    root.resizable(0, 0)
    defaultFont = Font.Font(weight="bold", family='Helvetica')
    main_frame = tk.Frame(root, bg=color_pallet[1])
    main_frame.pack()
    # Entry
    entry_bar = tk.Entry(main_frame, width=20, font=("Century Gothic", 40), relief=tk.FLAT, bg=color_pallet[0], fg=color_pallet[2])
    entry_label = tk.Label(main_frame, text="\n", anchor=tk.E, justify=tk.RIGHT, bg=color_pallet[0], fg=color_pallet[2], relief=tk.FLAT, width=48, font=("Century Gothic", 15))
    entry_bar.grid(row=1, column=0)
    entry_label.grid(row=0, column=0, pady=10, padx=10)
    # Build Buttons
    num_frame = tk.Frame(main_frame, bg=color_pallet[1])
    num_frame.grid(row=2, column=0)
    num_inText = 0
    num_grid_size = 3
    MakeNumPad(num_frame, num_inText, num_grid_size, num_grid_size - 1)
    MakeNumPad(num_frame, ".", num_grid_size + 1, num_grid_size - 1)
    for x in range(num_grid_size):
        for y in range(num_grid_size):
            num_inText += 1
            MakeNumPad(num_frame, num_inText, y, x)
        pass
    # Build Operator Buttons
    num_opt = 0
    for x1 in range(num_grid_size - 1):
        for y1 in range(num_grid_size - 1):
            MakeNumPad(num_frame, operators[num_opt], y1 + num_grid_size, x1)
            num_opt += 1
    # Make Special Buttons
    num_Enter = tk.Button(num_frame, text="Enter", width=8, bg=color_pallet[0], fg=color_pallet[2], relief=tk.FLAT, font=defaultFont, height=14, command=lambda: button_press("Enter"))
    num_Clear = tk.Button(num_frame, text="Clear", width=8, bg=color_pallet[0], fg=color_pallet[2], relief=tk.FLAT, font=defaultFont, height=6, command=lambda: button_press("Clear"))
    num_Enter.grid(row=num_grid_size - num_grid_size, column=num_grid_size + 2, rowspan=2, padx=5, pady=5)
    num_Clear.grid(row=num_grid_size - 1, column=num_grid_size + 2, padx=5, pady=5)
    root.mainloop()


if __name__ == '__main__':
    Main()
