import os
import tkinter as tk

def show_musicNote_played_window():
    log_path = "music/log/last_index.txt"
    bound_index = 30
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                last_index = int(f.read().strip())
            except ValueError:
                last_index = -1
    else:
        last_index = -1
        with open(log_path, "w") as f:
            f.write(str(last_index))

    window = tk.Tk()
    window.title("楽曲リスト")

    list_frame = tk.Frame(window)
    list_frame.pack(padx=10, pady=10)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(
        list_frame, 
        width=70, height=20, font=("Consolas", 24),
        yscrollcommand=scrollbar.set
    )
    listbox.pack(side="left", fill="both")

    scrollbar.config(command=listbox.yview)

    for i in range(bound_index):  # 常に0〜29を確認
        time_path = f"music/played/{i}/save_time.txt"
        if os.path.exists(time_path):
            with open(time_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                time = lines[0].strip() if len(lines) > 0 else "no time"
                level_str = lines[1].strip() if len(lines) > 1 else "0"
                try:
                    level = int(level_str)
                except ValueError:
                    level = 0
                level_set = "◇◇◇"
                level_set = level_set[:level -1] + "◆" + level_set[level -1:]
                listbox.insert(tk.END, f"No.{i:2d} | {time} | Level: {level_set}")

    result = {'selected_index': None}

    button_frame = tk.Frame(window)
    button_frame.pack(pady=(0, 30), fill="x")

    def on_back():
        result["selected_index"] = False
        window.destroy()

    back_button = tk.Button(button_frame, text="戻る", command=on_back)
    back_button.pack(side="left", padx=20)

    def on_play():
        selected = listbox.curselection()
        if not selected:
            print("何も選択されていません")
            return
        
        selected_text = listbox.get(selected[0])
        if selected_text.startswith("No."):
            try:
                index = int(selected_text.split("|")[0].strip()[3:])
                result['selected_index'] = f"music/played/{index}/"
                window.destroy()
            except ValueError:
                print("index を抽出できませんでした")
        else:
            print("有効な行ではありません")

    play_button = tk.Button(button_frame, text="遊ぶ", command=on_play)
    play_button.pack(side="right", padx=20)

    window.mainloop()
    return result["selected_index"]

print(show_musicNote_played_window())