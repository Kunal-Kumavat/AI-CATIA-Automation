import psutil

def check_catia_status():
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'] and 'CNEXT.exe' in process.info['name']:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False