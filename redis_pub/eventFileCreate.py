import logging
import sys
import pub

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
            pub.pubToRedis(event.src_path)

def main(argv=None):
    path = "/var/awesome-transform"

    observer = Observer()
    event_handler = MyEventHandler(observer)

    observer.schedule(event_handler,path,recursive=False)
    observer.start()
    observer.join()

    return 0

if __name__ == '__main__' :
    sys.exit(main(sys.argv))