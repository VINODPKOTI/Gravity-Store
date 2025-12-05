import os
import shutil

def clean_project(directory):
    # Remove __MACOSX directory
    macosx_path = os.path.join(directory, '__MACOSX')
    if os.path.exists(macosx_path):
        print(f"Removing {macosx_path}")
        try:
            shutil.rmtree(macosx_path)
            print("Removed __MACOSX")
        except Exception as e:
            print(f"Error removing __MACOSX: {e}")

    # Remove ._ files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('._'):
                path = os.path.join(root, file)
                try:
                    os.remove(path)
                    print(f"Removed {path}")
                except Exception as e:
                    print(f"Error removing {path}: {e}")

clean_project('.')
