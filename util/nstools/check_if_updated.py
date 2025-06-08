from .constants import CHECKSUM
from .log_util import add_log
from pathlib import Path
from hashlib import sha256

def compare_archive_hashes(zip_bytes: bytes)->None:
    # Check for Updated Archive by Comparing SHA256 Hashes
    new_hash: str = sha256(zip_bytes).hexdigest()
    
    # If No Checksum File or Value, Create/Write New SHA256 Hash
    if not Path.exists(CHECKSUM) or CHECKSUM == "":
        with open(CHECKSUM, "w") as chk:
            chk.write(new_hash)
        add_log(f"[OK] Updated Checksum File: \"{CHECKSUM}\".\nNew Hash: {new_hash}")
        
    
    # Update Checksum if Hashes Differ, Exit if Not 
    with open(CHECKSUM, 'r') as chk:
        old_hash: str = chk.read()
    if new_hash != old_hash:
        with open(CHECKSUM, 'w') as chk:
            chk.write(new_hash)
        add_log(f"[OK] Updated Checksum File: \"{CHECKSUM}\".\nOld Hash: {old_hash}\nNew Hash: {new_hash}")
    else:
        add_log(f"[OK] Archive Has Not Been Modified Since Last Update. Exiting...")
        exit(0)