from constants import TEMPDIR
from log_util import add_log, filedate
from get_notary_list import get_active_notary_archive, extract_notary_list
from backup_and_replace import backup_master_notary_file, update_master_notary_file
from cleanup_temp import purge_temp_dir
from notary_to_json import convert_text_to_json
from dir_setup import setup_dirs
from pathlib import Path
from sys import exit


####################
#### Main Entry ####
####################

if __name__ == "__main__":

    # Check/Create Project Directories
    setup_dirs()
    
    # Log Session Header
    add_log('', first=True)

    # Download Current Active Notary Archive
    zip_bytes: bytes = get_active_notary_archive()

    # Extract Text File from Archive
    active_notary_text_file: Path = extract_notary_list(zip_bytes)
    
    # Active Notary JSON Output File
    active_notary_json_file: Path = Path(f"{TEMPDIR}/notaries_{filedate()}.json")

    # Convert Text File to JSON Format
    convert_text_to_json(active_notary_text_file, active_notary_json_file)
    
    # Backup & Update Active Notary File
    backup_master_notary_file()
    update_master_notary_file(active_notary_json_file)

    # Cleanup Temp Directory
    purge_temp_dir()
    
    # Log Success
    add_log(f"[OK] Active Notary Listing Successfully Updated.")
    
    exit(0)
