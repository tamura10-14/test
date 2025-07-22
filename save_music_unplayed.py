'''
ファイル名：save_music_unplayed.py
バージョン：V1.0
作成者：宗近知生
更新日：2025.07.15
機能要約：このファイルは，tmp/にあるmusic.wavを引数indexに応じたパスにコピーする
'''
import shutil
import os

def save_music_unplayed(index: int) -> bool:
    '''
    関数名：save_music_unplayed
    作成者：宗近知生
    更新日：2025.07.15
    機能要約：この関数は，tmp/にあるmusic.wavを引数indexに応じたパスにコピーする
    '''
    
    if index not in (1, 2, 3, 4):
        print(f"エラー: index は 1〜4 の間で指定してください（指定された index: {index}）")
        return False

    input_path = "tmp/" + "music.wav"
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