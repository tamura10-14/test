import os

def show_musicNore_played():
    
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

    for i in range(last_index + 1):
        time_path = f"music/played/{i}/save_time.txt"
        if os.path.exists(time_path):
            with open(time_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                time = lines[0].strip() if len(lines) > 0 else "no time"
                level = lines[1].strip() if len(lines) > 1 else "no level"
            
            print(f"No.{i} | {time} | Level: {level}  仮")
        else:
            print(f"[{i}] save_time.txt が見つかりません")


show_musicNore_played()