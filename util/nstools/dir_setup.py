from .constants import BACKUPDIR, TEMPDIR, LOGDIR, DBDIR

# Create Directories if Not Present
def setup_dirs(): 
  BACKUPDIR.mkdir(exist_ok=True)
  TEMPDIR.mkdir(exist_ok=True)
  LOGDIR.mkdir(exist_ok=True)
  DBDIR.mkdir(exist_ok=True)