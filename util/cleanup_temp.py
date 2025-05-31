from constants import TEMPDIR
from log_util import add_log
from shutil import rmtree

#############################
#### Clear TMP Directory ####
#############################

def purge_temp_dir()->None:
    try:
        rmtree(TEMPDIR)
        add_log(f"[OK] Directory '{TEMPDIR}' and its contents have been removed successfully.")
    
    except FileNotFoundError:
        add_log(f"[ERROR] Directory '{TEMPDIR}' not found.")
    
    except PermissionError:
        add_log(f"[ERROR] Permission denied to remove '{TEMPDIR}'.")
    
    except Exception as e:
        add_log(f"[ERROR] An unexpected error occurred: {e}")