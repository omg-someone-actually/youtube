from os import system
from threading import Thread
from time import sleep
from shutil import disk_usage

def start():
  system('cd flask; export FLASK_APP=app; export FLASK_ENV=devolpment; flask run -h 0.0.0.0')

def clear_files():
  system('rm flask/static/*')
  print('Cleared Videos!')

def check_file_space():
  while True:
    total, used, free = disk_usage(__file__)
    print(total, used, free*0.000001)
    if (free*0.000001) >= 800:
      clear_files()
    sleep(1)

if __name__ == '__main__':
  clear_files()
  Thread(target=check_file_space).start()
  start()