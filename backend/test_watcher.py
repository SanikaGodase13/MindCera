from app.services.folder_watcher import FolderWatcher
import time

watcher = FolderWatcher()

watcher.start(
    r"D:\MindCeraJournal"
)

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    watcher.stop()