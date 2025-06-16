from show_save_success import show_save_success
from show_save_fail import show_save_fail

def get_save_state(save_state:bool):

    if ( save_state == True):
        return show_save_success()
    elif ( save_state == False ):
        return show_save_fail()

print(get_save_state(False))