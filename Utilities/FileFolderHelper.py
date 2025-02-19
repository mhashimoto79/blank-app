import os
import glob

def clear_folder(folder_path:str):
    files = glob.glob(f'{folder_path}\*')
    for f in files:
        os.remove(f)