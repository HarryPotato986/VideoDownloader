import os
import shutil
from datetime import datetime, timezone, timedelta
from app import app, db, working_folder, Save

def remove_old_data():
    print(f"[{datetime.now()}] Starting working file cleanup.")
    with app.app_context():
        now = datetime.now(timezone.utc)
        threshold = now - timedelta(hours=24)

        old_entries = Save.query.filter(Save.date_created < threshold).all()

        for entry in old_entries:
            dir_path = os.path.join(working_folder, entry.id)

            try:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    print(f"[{datetime.now()}] Deleted folder: {dir_path}")

                db.session.delete(entry)

            except Exception as e:
                print(f"Error cleaning up ID {entry.id}: {e}")

        db.session.commit()


        valid_ids = {res[0] for res in db.session.query(Save.id).all()}

        if not os.path.exists(working_folder):
            return
        
        orphan_count = 0
        for folder_name in os.listdir(working_folder):
            folder_path = os.path.join(working_folder, folder_name)

            if os.path.isdir(folder_path) and folder_name not in valid_ids:
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(folder_path), tz=timezone.utc)
                    if now - mtime > timedelta(hours=1):
                        shutil.rmtree(folder_path)
                        print(f"[{datetime.now()}] Deleted orphaned folder: {folder_name}")
                        orphan_count += 1

                except Exception as e:
                    print(f"Error deleting orphaned folder {folder_name}: {e}")

        if len(old_entries) > 0 or orphan_count > 0:
            print(f"[{datetime.now()}] Successfully removed {len(old_entries)} records and {orphan_count} orphaned folders.")

        print(f"[{datetime.now()}] Cleanup finished.")

if __name__ == "__main__":
    remove_old_data()