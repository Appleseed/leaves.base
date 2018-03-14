import logging
import sys
import Publish

"""
Once new file under "/var/awesome-transform" directory is written, "file create" event is triggered and messages are published to redis queue 
"""
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.ERROR)

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    def on_created(self, event):
        print ("e", event)
        if not event.is_directory:
            print ("File created ", event.src_path)
            Publish.publishToRedis(event.src_path)

def main(argv=None):
    path = "/var/awesome"
    # path = 'C:/Users/DELL'

    observer = Observer()
    event_handler = MyEventHandler(observer)

    observer.schedule(event_handler,path,recursive=False)
    observer.start()
    observer.join()

    return 0

if __name__ == '__main__' :
    sys.exit(main(sys.argv))