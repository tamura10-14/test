import shutil
import os
from datetime import datetime

def save_musicNote_played(index:int)->bool:

    bound_index = 30

    if index not in (1, 2, 3, 4):
        print(f"エラー: index は 1〜4 の間で指定してください（指定された index: {index}）")
        return False

    src_dir_path = f"music/unplayed/{index}"

    files = ["music.wav","note.txt"]

    if not os.path.exists(src_dir_path):
        print(f"エラー: 元ディレクトリが存在しません ({src_dir_path})")
        return False

    for filename in files:
        if not os.path.exists(os.path.join(src_dir_path, filename)):
            print(f"警告:{filename}は存在しません")
            return False

    log_path = "music/log/last_index.txt"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                last_index = int(f.read().strip())
            except ValueError:
                last_index = -1
    else:
        last_index = -1

    present_index = (last_index + 1) % bound_index
    with open(log_path, "w") as f:
        f.write(str(present_index))

    dest_dir_path = f"music/played/{present_index}"
    os.makedirs(dest_dir_path, exist_ok=True)

    try:
        for filename in files:
            src_file_path = os.path.join(src_dir_path, filename)
            dest_file_path = os.path.join(dest_dir_path, filename)

            if os.path.exists(src_file_path):
                shutil.move(src_file_path, dest_file_path)
            else:
                print(f"警告: {filename} は存在しません")

        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file_path = os.path.join(dest_dir_path, "save_time.txt")

        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(log_time + "\n")
            f.write(str(index))

        return True
    except Exception as e:
        print(f"エラー: ファイル移動中に例外が発生しました: {e}")
        return False

save_musicNote_played(1)