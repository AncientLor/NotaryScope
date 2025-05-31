from constants import TEMPDIR, ACTIVE_NOTARY_LIST_URL
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from log_util import add_log, filedate
from requests import Response, request

##################################################
#### Download Today's Active Notaries Archive ####
##################################################

# Download Current "Active Notary" Archive
def get_active_notary_archive()->bytes:

    r: Response = request("GET", ACTIVE_NOTARY_LIST_URL)

    # Exit if Status Code != 200
    if r.status_code != 200:
        add_log(f"[ERROR] Status Code: {r.status_code} Error Message: {r.content}")
        exit(1)

    return r.content


###################################
#### Extract Text From Archive ####
###################################

def extract_notary_list(zip_bytes: bytes)->Path:

    target_file: str = 'active-notary.txt'
    output_file: Path = Path(f"{TEMPDIR}/active-notary_{filedate()}.txt")

    # Create Handle for Zip Archive
    with ZipFile(BytesIO(zip_bytes)) as zf:
        
        # Exit if Target File Not Found
        if target_file not in zf.namelist():
            add_log(f"[ERROR] File {target_file} not found.")
            exit(1)

        # Extract Target from Archive
        with open(output_file, 'wb') as outfile:
            outfile.write(zf.read(target_file))
    
    add_log(f"[OK] Extracted {target_file} from \"active-notary.zip\" to {output_file}")
        
    return output_file