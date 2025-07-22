'''
ファイル名：submit_music_unplayed_path.py
バージョン：V1.0
作成者：宗近知生
更新日：2025.07.15
機能要約：このファイルは，引数indexに応じnote.jsonとmusic.wavを含むディレクトリのパスを作成する
'''
import os

def submit_music_unplayed_path(index: int) ->str|bool:
    '''
    関数名：submit_music_unplayed_path
    作成者：宗近知生
    更新日：2025.07.15
    機能要約：この関数は，引数indexに応じてnote.jsonとmusic.wavを含むディレクトリの相対パスを返す
    　　　　　なおエラー時はFalseを返す
    '''

    if index not in (1, 2, 3, 4):
        print(f"エラー: index は 1〜4 の間で指定してください（指定された index: {index}）")
        return False

    unplayed_path = f"music/unplayed/{index}"

    if not os.path.exists(unplayed_path):
        print(f"エラー: 指定されたディレクトリが存在しません（{unplayed_path}）")
        return False

    music_path = os.path.join(unplayed_path, "music.wav")
    note_path = os.path.join(unplayed_path, "note.json")

    if not os.path.exists(music_path):
        print(f"エラー: {music_path} が存在しません")
        return False
    if not os.path.exists(note_path):
        print(f"エラー: {note_path} が存在しません")
        return False

    return unplayed_path