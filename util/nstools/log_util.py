from .constants import LOGFILE
from time import strftime

# Append Message to Logfile
def add_log(msg: str, first: bool = False)->None:
    ts: str = strftime("%m/%d/%y %H:%M:%S")
    with open(LOGFILE, "a") as log:
        if first:
            log.write(f"\n\n---------- [{ts}] --------\n\n")
        else:
            log.write(f"{ts} {msg}\n")
        
# Date for Logfiles
def filedate()->str:
    return strftime("%m%d%y")