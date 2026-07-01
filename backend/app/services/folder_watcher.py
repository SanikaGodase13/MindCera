import time
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app.database.db import SessionLocal
from app.models.monitored_folder import MonitoredFolder
from app.services.folder_processor import FolderProcessor


class FolderHandler(FileSystemEventHandler):

    def __init__(self, folder_id):

        self.folder_id = folder_id

        self.processor = FolderProcessor()

        # Prevent duplicate processing
        self.processed_files = set()

    def process_event(self, event):

        if event.is_directory:
            return

        file_path = event.src_path

        # Only supported file types
        if not file_path.lower().endswith(
            (".txt", ".docx", ".pdf")
        ):
            return

        # Ignore Word temp files
        if os.path.basename(file_path).startswith("~$"):
            return

        # Duplicate protection
        if file_path in self.processed_files:
            return

        self.processed_files.add(file_path)

        print(
            f"NEW FILE DETECTED: {file_path}"
        )

        time.sleep(2)

        db = SessionLocal()

        try:

            folder = (
                db.query(MonitoredFolder)
                .filter(
                    MonitoredFolder.id == self.folder_id
                )
                .first()
            )

            if not folder:
                return

            self.processor.process_file(
                folder,
                file_path,
                db
            )

            print(
                f"FILE ANALYZED: {file_path}"
            )

        except Exception as e:

            print(
                f"Watcher Error: {e}"
            )

        finally:

            db.close()

    def on_created(self, event):
        self.process_event(event)

    def on_modified(self, event):
        self.process_event(event)


class FolderWatcher:

    def __init__(self):

        self.observer = Observer()

    def start(
        self,
        folder_id,
        folder_path
    ):

        handler = FolderHandler(folder_id)

        self.observer.schedule(
            handler,
            folder_path,
            recursive=False
        )

        self.observer.start()

        print(
            f"Watching: {folder_path}"
        )

    def stop(self):

        self.observer.stop()
        self.observer.join()