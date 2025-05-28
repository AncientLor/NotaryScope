import json
import sys
import time
import requests
import zipfile
import io
from pathlib import Path
from hashlib import file_digest

WORKDIR: Path = Path(__file__).parent     # Script Directory -> /FULL/PATH/NotaryScope/util
PROOT: Path = WORKDIR.parent              # Project Root -> /FULL/PATH/NotaryScope
BACKUPDIR: Path = Path(f"{PROOT}/backup")
TEMPDIR: Path = Path(f"{PROOT}/tmp")
LOGFILE: Path = Path(f"{PROOT}/log/update.log")
ACTIVE_NOTARY_MASTER_FILE: Path = Path(f"{PROOT}/notaries.json")
ACTIVE_NOTARY_LIST_URL: str = 'https://notary.cdn.sos.ca.gov/export/active-notary.zip'


# Append Message to Logfile
def add_log(msg: str)->None:
    ts: str = time.strftime("[%m/%d/%y %H:%M:%S]")
    with open(LOGFILE, "a") as log:
        log.write(f"{ts} {msg}\n")


# Date for Logfiles
def filedate()->str:
    return time.strftime("%m%d%y")


# Download Current "Active Notary" Archive
def get_active_notary_list()->bytes:

    r: requests.Response = requests.request("GET", ACTIVE_NOTARY_LIST_URL)

    # Exit if Status Code != 200
    if r.status_code != 200:
        msg: str = f"[ERROR] Status Code: {r.status_code} Error Message: {r.content}"
        add_log(msg)
        sys.exit(1)

    return r.content


# Extract Active Notary Text File from ZIP Archive
def extract_notary_list(zip_bytes: bytes)->bytes:

    target_file: str = 'active-notary.txt'
    output_file: Path = Path(f"{TEMPDIR}/active-notary_{filedate()}.txt")

    # Create Handle for Zip Archive
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        
        # Exit if Target File Not Found
        if target_file not in zf.namelist():
            msg: str = f"[ERROR] File {target_file} not found."
            add_log(msg)
            sys.exit(1)

        # Extract Target from Archive
        text_bytes: bytes = zf.read(target_file)
        with open(output_file, 'wb') as outfile:
            outfile.write(text_bytes)
    
    msg: str = f"[OK] Extracted {target_file} from \"active-notary.zip\" to {output_file}"
    add_log(msg)
        
    return output_file


# Convert Active Notary Text File to JSON Format
def convert_text_to_json(input_text, output_json)->list[dict]:
    
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
            msg: str = f"[WARNING] Skipping malformed line: {line}"
            add_log(msg)

    # Write to JSON File
    with open(output_json, 'w', encoding='utf-8') as outfile:
        json.dump(entries, outfile, indent=2)

    msg: str = f"[OK] Conversion complete. {len(entries)} entries written to {output_json}"
    add_log(msg)

    


def backup_master_notary_file()->None:
    
    if not Path.exists(ACTIVE_NOTARY_MASTER_FILE):
        return
    
    backup_file: Path = Path(f"{BACKUPDIR}/notaries-{filedate()}.json") 

    with open(ACTIVE_NOTARY_MASTER_FILE, 'r', encoding='utf-8') as m:
        with open(backup_file, 'w', encoding='utf-8') as b:
            b.write(m.read())
    
    # Integrity Check
    with open(ACTIVE_NOTARY_MASTER_FILE, 'rb') as master:
        master_checksum: str = file_digest(master, 'sha1').hexdigest()
    
    with open(backup_file, 'rb') as backup:
        backup_checksum: str = file_digest(backup, 'sha1').hexdigest()
    
    if master_checksum != backup_checksum:
        msg: str = f"[ERROR] Active Notary Backup Failed.\nChecksum Mismatch."
        add_log(msg)
        msg = f"[ERROR] Master: {master_checksum}\nBackup: {backup_checksum}"
        add_log(msg)
        sys.exit(2)
    
    msg: str = f"[OK] Active Notary File Successfully Backed Up"
    add_log(msg)


def update_master_notary_file(json_file: Path)->None:

    with open(ACTIVE_NOTARY_MASTER_FILE, 'w', encoding='utf-8') as master:
        with open(json_file, 'r', encoding='utf-8') as new:
            master.write(new.read())


if __name__ == "__main__":
    
    # Download Current Active Notary Archive
    zip_bytes: bytes = get_active_notary_list()

    # Extract Text File from Archive
    active_notary_text_file: str = extract_notary_list(zip_bytes)
    
    # Active Notary JSON Output File
    active_notary_json_file: Path = Path(f"{TEMPDIR}/notaries_{filedate()}.json")

    # Convert Text File to JSON Format
    convert_text_to_json(active_notary_text_file, active_notary_json_file)
    
    # Backup & Update Active Notary File
    backup_master_notary_file()
    update_master_notary_file(active_notary_json_file)
    
    # Log Success
    msg: str = f"[OK] Active Notary Listing Successfully Updated."
    add_log(msg)
    
    sys.exit()
