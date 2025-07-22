'''
ファイル名：main.py
バージョン：V1.0
作成者：宗近知生
更新日：2025.07.15
機能要約：このファイルは，全ての画面の遷移と引数の値を決定して管理すること
'''
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 例: patch フォルダの絶対パス
sys.path.insert(0, BASE_DIR)

from config import run_config_screen
from home import run_home_screen
from error import show_error_screen
from correct import show_correct_screen
from music_details import run_music_details_screen
from lifecycle import LifecycleManager
from uistate import UIStateManager
from demo import playscreen_main
from save import run_save_screen
from saved_music import run_saved_music_screen
from make_music.make_music import make_music
from make_note.generate_chart_main import generate_chart_main
from submit_music_unplayed_path import submit_music_unplayed_path
from submit_music_played_path import submit_music_played_path
from save_musicNote_played import save_musicNote_played
from save_music_unplayed import save_music_unplayed
from save_note_unplayed import save_note_unplayed
from audiomanager import AudioManager

import pygame
import sys


def dispatch_event():
    '''
    関数名：dipatch_event
    作成者：宗近知生
    更新日：2025.07.15
    機能要約：この関数は，whileループの中で画面遷移の引数に応じて異なる関数を起動する
    '''
    
    #初期化
    print("pygame.font initialized?", pygame.font.get_init())

    pygame.init() 
    pygame.mixer.init() 

    lifecycle = LifecycleManager()

    # インスタンスの初期化
    lifecycle.initialize_system()
    # AudioManagerの取得
    audio_manager = lifecycle.get_audio_manager()
    ui_state_manager = UIStateManager(lifecycle,audio_manager)

    initial_state = {"screen": "main"}
    ui_state_manager.set_state(initial_state)

    #ゲーム起動時のループ
    while True:
        current_state = ui_state_manager.get_current_state()
        next_screen = current_state.get("screen", "main")
        
        #ホーム画面の遷移
        if next_screen == "main":
            result = run_home_screen(audio_manager)
            if result == "config_screen":
                ui_state_manager.set_state({"screen": "config"})

            elif result == "saved_music_screen":
                ui_state_manager.set_state({"screen": "saved"})

            elif isinstance(result, str) and result.startswith("level_start_"):
                level = result.replace("level_start_", "")
                level_num = int(level)
                play_path = submit_music_unplayed_path(level_num)
                                
                if play_path != False:
                    ui_state_manager.set_state({"screen": "play"})#play
                else:
                    print("ここにQuit操作を追加(play)")
                    lifecycle.shutdown_system()
                    break
                    
            elif result is None:
                break

            else:
                print("ここにQuit操作を追加(home)")
                lifecycle.shutdown_system()
                break

        #設定画面の遷移
        elif next_screen == "config":
            result = run_config_screen(audio_manager)
            if result == "home_screen":
                ui_state_manager.set_state({"screen": "main"})
            
            else:
                print("ここにQuit操作を追加(config)")
                lifecycle.shutdown_system()
                break

        #プレイ中の設定画面の遷移
        elif next_screen == "config_on_play":
            result = run_config_screen(audio_manager)
            if result == "home_screen":
                ui_state_manager.set_state({"screen": "play"})

            else:
                print("ここにQuit操作を追加(pconfig)")
                lifecycle.shutdown_system()
                break

        #保存楽曲を選択する画面の遷移
        elif next_screen == "saved":
            result = run_saved_music_screen(audio_manager,30)
            if result == "home_screen":
                ui_state_manager.set_state({"screen": "main"})                
            elif isinstance(result,dict): #ここからsavedはまだ dictは草
                filepath = result["filepath"]
                index = os.path.basename(os.path.dirname(filepath))
                index_int = int(index)
                play_path = submit_music_played_path(index_int)
                if play_path != False:
                    ui_state_manager.set_state({"screen": "play"})
                else:
                    print("ここにQuit操作を追加(play)")
                    lifecycle.shutdown_system()
                    break
            else:
                print("ここにQuit操作を追加(saved)")
                lifecycle.shutdown_system()
                break

        #プレイ画面の遷移
        elif next_screen == "play": #早く返り値知りたい
                result = playscreen_main(audio_manager,play_path)
                #print("result : "+result)
                if result == "CONFIG_REQUEST":
                    ui_state_manager.set_state({"screen": "config_on_play"})
                elif result == "SUCCESS":
                    if play_path.startswith("music/unplayed"):
                        ui_state_manager.set_state({"screen": "save_quest"})
                    elif play_path.startswith("music/played"):
                        ui_state_manager.set_state({"screen": "main"})
                    else:
                        print("ここにQuit操作を追加(play)")
                        lifecycle.shutdown_system()
                        break
                else:
                    print("ここにQuit操作を追加(play)")
                    lifecycle.shutdown_system()
                    break

        #保存意思の確認画面の遷移
        elif next_screen == "save_quest":
            result = run_save_screen()
            if result == False:#no
                ui_state_manager.set_state({"screen": "detail"})
            elif result == True:#yes
                isSuccess_save = save_musicNote_played(level_num)
                if isSuccess_save == True:
                    ui_state_manager.set_state({"screen": "save_success"})
                elif isSuccess_save == False:
                    ui_state_manager.set_state({"screen": "save_fail"})
                else:
                    print("ここにQuit操作を追加(isSuccess)")
                    lifecycle.shutdown_system()
                    break
            else:
                print("ここにQuit操作を追加(save_quest)")
                lifecycle.shutdown_system()
                break

        #保存成功の遷移
        elif next_screen == "save_success":
            isSuccess = show_correct_screen("Correct", "楽曲の保存に成功しました", audio_manager) # audio_managerを渡す
            if isSuccess == "Exit":
                ui_state_manager.set_state({"screen": "detail"})
            else:
                print("ここにQuit操作を追加(save_success)")
                lifecycle.shutdown_system()
                break

        #保存失敗の遷移
        elif next_screen == "save_fail":
            isFail = show_error_screen("Error", "楽曲の保存に失敗しました", audio_manager) # audio_managerを渡す
            if isFail == "Exit":
                ui_state_manager.set_state({"screen": "detail"})
            else:
                print("ここにQuit操作を追加(save_fail)")
                lifecycle.shutdown_system()
                break

        #楽曲詳細入力の遷移
        elif next_screen == "detail":
            prompt = run_music_details_screen(audio_manager) #test_audio_manager
            if isinstance(prompt,dict):
                ui_state_manager.set_state({"screen": "music_gen"})
            else:
                print("ここにQuit操作を追加(detail)")
                lifecycle.shutdown_system()
                break

        #楽曲生成の遷移
        elif next_screen == "music_gen":
            make_music(prompt,"tmp/music.wav",audio_manager)#MakeMusic
            ui_state_manager.set_state({"screen": "note_gen"})

        #譜面生成の遷移
        elif next_screen == "note_gen":
            difficulty_level = "level_start_"+level
            result = generate_chart_main(difficulty_level, audio_manager)
           
            if result:
                isSuccessMusic = save_music_unplayed(level_num)
                isSuccessNote  = save_note_unplayed(level_num)
                
                if isSuccessMusic == True and isSuccessNote == True:
                    ui_state_manager.set_state({"screen": "save_success_played"})
                
                elif isSuccessMusic == False or isSuccessNote == False:
                    ui_state_manager.set_state({"screen": "save_fail_played"})
                else:
                    print("ここにQuit操作を追加(save(note,music))")
                    lifecycle.shutdown_system()
                    break
            else:
                print("ここにQuit操作を追加(note_gen)")
                lifecycle.shutdown_system()
                break
        
        #既プレイ楽曲の保存成功　遷移
        elif next_screen == "save_success_played":
            isSuccess = show_correct_screen("Correct", "楽曲の保存に成功しました", audio_manager) # audio_managerを渡す
            if isSuccess == "Exit":
                ui_state_manager.set_state({"screen": "main"})
            else:
                print("ここにQuit操作を追加(save_success_played)")
                lifecycle.shutdown_system()
                break
            
        #既プレイ楽曲の保存失敗　遷移
        elif next_screen == "save_fail_played":
            isFail = show_error_screen("Error", "楽曲の保存に失敗しました", audio_manager) # audio_managerを渡す
            if isFail == "Exit":
                ui_state_manager.set_state({"screen": "main"})
            else:
                print("ここにQuit操作を追加(save_fail_played)")
                lifecycle.shutdown_system()
                break

        else:
            print(f"不明な画面状態: {next_screen}")
            lifecycle.shutdown_system()
            break

if __name__ == "__main__":
    dispatch_event()