from pathlib import Path

WORKDIR: Path = Path(__file__).parent.parent     # Script Directory -> /FULL/PATH/NotaryScope/util
PROOT: Path = WORKDIR.parent                    # Project Root -> /FULL/PATH/NotaryScope
BACKUPDIR: Path = Path(f"{PROOT}/backup")
TEMPDIR: Path = Path(f"{PROOT}/tmp")
LOGDIR: Path = Path(f"{PROOT}/log")
LOGFILE: Path = Path(f"{LOGDIR}/update.log")
DBDIR: Path = Path(f"{PROOT}/db")
CHECKSUM: Path = Path(f"{DBDIR}/zip_hash.sha256")
ACTIVE_NOTARY_MASTER_FILE: Path = Path(f"{DBDIR}/notaries.json")
ACTIVE_NOTARY_LIST_URL: str = 'https://notary.cdn.sos.ca.gov/export/active-notary.zip'