'''
ファイル名：submit_music_played_path.py
バージョン：V1.0
作成者：宗近知生
更新日：2025.07.15
機能要約：このファイルは，引数indexに応じてnote.jsonとmusic.wavを含むディレクトリの相対パスを作成する
'''
import os

def submit_music_played_path(index: int) ->str|bool:
    '''
    関数名：submit_music_played_path
    作成者：宗近知生
    更新日：2025.07.15
    機能要約：この関数は，引数indexに応じてnote.jsonとmusic.wavを含むディレクトリの相対パスを返す
    　　　　　なおエラー時はFalseを返す
    '''
        
    if not (0 <= index <= 29):
        print(f"エラー: index は 0〜29 の間で指定してください（指定された index: {index}）")
        return False

    played_path = f"music/played/{index}"

    if not os.path.exists(played_path):
        print(f"エラー: 指定されたディレクトリが存在しません（{played_path}）")
        return False

    music_path = os.path.join(played_path, "music.wav")
    note_path = os.path.join(played_path, "note.json")

    if not os.path.exists(music_path):
        print(f"エラー: {music_path} が存在しません")
        return False
    if not os.path.exists(note_path):
        print(f"エラー: {note_path} が存在しません")
        return False

    return played_path