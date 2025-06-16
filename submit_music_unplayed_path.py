import os

def submit_music_unplayed_path(index: int):
    if index not in (1, 2, 3, 4):
        print(f"エラー: index は 1〜4 の間で指定してください（指定された index: {index}）")
        return False

    unplayed_path = f"music/unplayed/{index}/music.wav"

    if not os.path.exists(unplayed_path):
        print(f"エラー: 指定されたファイルが存在しません（{unplayed_path}）")
        return False

    return unplayed_path

#print(submit_music_unplayed_path(1))
