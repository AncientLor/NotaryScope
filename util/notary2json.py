import json
import sys
import time
import requests
import zipfile
import io
from pathlib import Path
from hashlib import file_digest
import shutil


WORKDIR: Path = Path(__file__).parent     # Script Directory -> /FULL/PATH/NotaryScope/util
PROOT: Path = WORKDIR.parent              # Project Root -> /FULL/PATH/NotaryScope
BACKUPDIR: Path = Path(f"{PROOT}/backup")
TEMPDIR: Path = Path(f"{PROOT}/tmp")
LOGDIR: Path = Path(f"{PROOT}/log")
LOGFILE: Path = Path(f"{PROOT}/log/update.log")
ACTIVE_NOTARY_MASTER_FILE: Path = Path(f"{PROOT}/notaries.json")
ACTIVE_NOTARY_LIST_URL: str = 'https://notary.cdn.sos.ca.gov/export/active-notary.zip'


###########################
#### Logging Utilities ####
###########################

# Append Message to Logfile
def add_log(msg: str, first: bool = False)->None:
    ts: str = time.strftime("%m/%d/%y %H:%M:%S")
    with open(LOGFILE, "a") as log:
        if first:
            log.write(f"\n\n---------- [{ts}] --------\n\n")
        else:
            log.write(f"{ts} {msg}\n")
        
# Date for Logfiles
def filedate()->str:
    return time.strftime("%m%d%y")


##################################################
#### Download Today's Active Notaries Archive ####
##################################################

# Download Current "Active Notary" Archive
def get_active_notary_archive()->bytes:

    r: requests.Response = requests.request("GET", ACTIVE_NOTARY_LIST_URL)

    # Exit if Status Code != 200
    if r.status_code != 200:
        add_log(f"[ERROR] Status Code: {r.status_code} Error Message: {r.content}")
        sys.exit(1)

    return r.content


###################################
#### Extract Text From Archive ####
###################################

def extract_notary_list(zip_bytes: bytes)->Path:

    target_file: str = 'active-notary.txt'
    output_file: Path = Path(f"{TEMPDIR}/active-notary_{filedate()}.txt")

    # Create Handle for Zip Archive
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        
        # Exit if Target File Not Found
        if target_file not in zf.namelist():
            add_log(f"[ERROR] File {target_file} not found.")
            sys.exit(1)

        # Extract Target from Archive
        with open(output_file, 'wb') as outfile:
            outfile.write(zf.read(target_file))
    
    add_log(f"[OK] Extracted {target_file} from \"active-notary.zip\" to {output_file}")
        
    return output_file


#################################
#### Active Notaries to JSON ####
#################################

def convert_text_to_json(input_text: Path, output_json: Path)->None:
    
    with open(input_text, 'r', encoding='utf-8') as instream:
        lines: list[str] = instream.readlines()

    # Extract Header Fields from First Line
    headers: list[str] = lines[0].strip().split('\t')

    # Convert Following Lines to Dictionary
    entries: list[dict] = []
    
    for line in lines[1:]:    
        fields: list[str] = line.strip().split('\t')
        
        # Ensure Fields/Headers Align
        if len(fields) == len(headers):
            entry: dict = dict(zip(headers, fields))
            entries.append(entry)
        
        else:
            add_log(f"[WARNING] Skipping malformed line: {line}")

    # Apply Camel Case Format to Business Names
    for e in entries:
        camel_case_list: list = []
        business_name: list[str] = e['Business Name'].split(' ')
        
        if business_name != '': 
            for name in business_name:
                if name == "UPS":
                    camel_case_list.append(name)

                else:
                    camel_case_list.append(name.capitalize())
            
            camel_case_text: str = ' '.join(camel_case_list)
            e['Business Name'] = camel_case_text

    # Write to JSON File
    with open(output_json, 'w', encoding='utf-8') as outfile:
        json.dump(entries, outfile, indent=2)

    add_log(f"[OK] Conversion complete. {len(entries)} entries written to {output_json}")


###################################
#### Backup Active Notaries DB ####
###################################

# Create Backup of Current Active Notaries DB 
def backup_master_notary_file()->None:

    #  Return if Nothing to Backup
    if not Path.exists(ACTIVE_NOTARY_MASTER_FILE):
        add_log(f"\"{ACTIVE_NOTARY_MASTER_FILE}\" does not exist. Skipping.")
        return
    
    backup_file: Path = Path(f"{BACKUPDIR}/notaries-{filedate()}.json") 
    
    try:
        shutil.copyfile(ACTIVE_NOTARY_MASTER_FILE, backup_file)
    
    except PermissionError:
        add_log(f"[ERROR] Unable to backup '{ACTIVE_NOTARY_MASTER_FILE}' to '{backup_file}'. Permission denied.")
    
    except Exception as e:
        add_log(f"[ERROR] Unable to backup '{ACTIVE_NOTARY_MASTER_FILE}' to '{backup_file}'. Error: {e}")
    
    #with open(ACTIVE_NOTARY_MASTER_FILE, 'r', encoding='utf-8') as m:
    #    with open(backup_file, 'w', encoding='utf-8') as b:
    #        b.write(m.read())
    
    # Integrity Check
    with open(ACTIVE_NOTARY_MASTER_FILE, 'rb') as master:
        master_checksum: str = file_digest(master, 'sha1').hexdigest()
    
    with open(backup_file, 'rb') as backup:
        backup_checksum: str = file_digest(backup, 'sha1').hexdigest()
    
    if master_checksum != backup_checksum:
        add_log(f"[ERROR] Active Notary Backup Failed.\nChecksum Mismatch.")
        add_log(f"[ERROR] Master: {master_checksum}\nBackup: {backup_checksum}")
        sys.exit(2)
    
    add_log(f"[OK] Active Notary File Successfully Backed Up")


###################################
#### Update Active Notaries DB ####
###################################

def update_master_notary_file(json_file: Path)->None:

    try:
        shutil.copyfile(json_file, ACTIVE_NOTARY_MASTER_FILE)

    except PermissionError:
        add_log(f"[ERROR] Unable to copy '{json_file}' to '{ACTIVE_NOTARY_MASTER_FILE}'. Permission denied.")
    
    except Exception as e:
        add_log(f"[ERROR] Unable to copy '{json_file}' to '{ACTIVE_NOTARY_MASTER_FILE}'. Error: {e}")

    
    #with open(ACTIVE_NOTARY_MASTER_FILE, 'w', encoding='utf-8') as master:
    #    with open(json_file, 'r', encoding='utf-8') as new:
    #        master.write(new.read())


#############################
#### Clear TMP Directory ####
#############################

def purge_temp_dir()->None:
    try:
        shutil.rmtree(TEMPDIR)
        add_log(f"[OK] Directory '{TEMPDIR}' and its contents have been removed successfully.")
    
    except FileNotFoundError:
        add_log(f"[ERROR] Directory '{TEMPDIR}' not found.")
    
    except PermissionError:
        add_log(f"[ERROR] Permission denied to remove '{TEMPDIR}'.")
    
    except Exception as e:
        add_log(f"[ERROR] An unexpected error occurred: {e}")

####################
#### Main Entry ####
####################

if __name__ == "__main__":

    # Create Directories if Not Present
    BACKUPDIR.mkdir(exist_ok=True)
    TEMPDIR.mkdir(exist_ok=True)
    LOGDIR.mkdir(exist_ok=True)
    
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
    
    sys.exit(0)
