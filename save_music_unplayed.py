import shutil
import os

def save_music_unplayed(index: int, type: str) -> bool:

    if index not in (1, 2, 3, 4):
        print(f"エラー: index は 1〜4 の間で指定してください（指定された index: {index}）")
        return False

    if type not in ("music", "note"):
        print(f"エラー: 無効なタイプです（{type}）")
        return False


    if type == "music":
        ext = ".wav"
    elif type == "note":
        ext = ".txt"
    else:
        print(f"エラー: 無効なタイプです（{type}）")
        return False

    input_path = "tmp/" + type + ext
    filename = os.path.basename(input_path)
    output_path = f"music/unplayed/{index}/{filename}"

    if not os.path.exists(input_path):
        print(f"エラー: 入力ファイルが存在しません（{input_path}）")
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        shutil.copy2(input_path, output_path)
        return True
    except Exception as e:
        return False