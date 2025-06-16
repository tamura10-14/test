import tkinter as tk

def show_save_fail():
    window = tk.Tk()
    window.title("通知")
    
    window.update_idletasks()
    width = 900
    height = 600
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)

    label = tk.Label(window, text="楽曲の保存に失敗しました", font=("Consolas", 32))
    label.place(relx=0.5, rely=0.4, anchor="center")

    result = {'state': None}

    def on_back():
        result["state"] = True
        window.destroy()

    back_button = tk.Button(window, text="戻る", font=("Consolas", 16), command=on_back)
    back_button.place(relx=0.5, rely=0.7, anchor="center")

    window.mainloop()
    return result["state"]
