import threading
import time

import win10toast as win10toast
from pygame import mixer


# toast_not.on_destroy(hwnd=toast_not.hwnd, msg='Looking for next...',)

def notify_w_job(fl_article):
    """Notifyes in logs, """
    sound_thread = threading.Thread(target=notify_sound)

    def job_windows():
        toast_not = win10toast.ToastNotifier()
        toast_not.show_toast(f'{fl_article.source}', f'{fl_article}',
                             duration=5, threaded=False)
    alert_box_thread = threading.Thread(target=job_windows)
    print(fl_article)# logging system
    sound_thread.start()
    alert_box_thread.start()
    sound_thread.join()
    alert_box_thread.join()




# file = ''
# notify_sound = vlc.MediaPlayer('file:///C:/Users/Acer/PycharmProjects/fl_tb_n_scrawler/Minion-elo.mp3')
# notify_sound.play()
def notify_sound(sound_file='Minion-elo.mp3'):
    mixer.init()
    mixer.music.load(sound_file)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)
# file = 'Minion-elo.mp3'
# playsound.playsound(file, True)
# webbrowser.open('Minion-elo.mp3')

