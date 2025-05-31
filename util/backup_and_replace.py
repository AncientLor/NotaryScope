from constants import ACTIVE_NOTARY_MASTER_FILE, BACKUPDIR
from log_util import *
from pathlib import Path
from hashlib import file_digest
from shutil import copyfile

###################################
#### Backup Active Notaries DB ####
###################################

# Create Backup of Current Active Notaries DB 
def backup_master_notary_file()->None:

    #  Return if Nothing to Backup
    if not Path.exists(ACTIVE_NOTARY_MASTER_FILE):
        add_log(f"\"{ACTIVE_NOTARY_MASTER_FILE}\" does not exist. Skipping.")
        return
    
    # Remove Previous Backups
    for file in BACKUPDIR.iterdir():
        file.unlink()
        add_log(f"[OK] Removed Backup File: {file}")

    backup_file: Path = Path(f"{BACKUPDIR}/notaries-{filedate()}.json") 
    
    try:
        copyfile(ACTIVE_NOTARY_MASTER_FILE, backup_file)
    
    except PermissionError:
        add_log(f"[ERROR] Unable to backup '{ACTIVE_NOTARY_MASTER_FILE}' to '{backup_file}'. Permission denied.")
    
    except Exception as e:
        add_log(f"[ERROR] Unable to backup '{ACTIVE_NOTARY_MASTER_FILE}' to '{backup_file}'. Error: {e}")
    
    # Integrity Check
    with open(ACTIVE_NOTARY_MASTER_FILE, 'rb') as master:
        master_checksum: str = file_digest(master, 'sha1').hexdigest()
    
    with open(backup_file, 'rb') as backup:
        backup_checksum: str = file_digest(backup, 'sha1').hexdigest()
    
    if master_checksum != backup_checksum:
        add_log(f"[ERROR] Active Notary Backup Failed.\nChecksum Mismatch.")
        add_log(f"[ERROR] Master: {master_checksum}\nBackup: {backup_checksum}")
        exit(2)
    
    add_log(f"[OK] Active Notary File Successfully Backed Up")


###################################
#### Update Active Notaries DB ####
###################################

def update_master_notary_file(json_file: Path)->None:

    try:
        copyfile(json_file, ACTIVE_NOTARY_MASTER_FILE)

    except PermissionError:
        add_log(f"[ERROR] Unable to copy '{json_file}' to '{ACTIVE_NOTARY_MASTER_FILE}'. Permission denied.")
    
    except Exception as e:
        add_log(f"[ERROR] Unable to copy '{json_file}' to '{ACTIVE_NOTARY_MASTER_FILE}'. Error: {e}")