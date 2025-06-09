/usr/bin/git checkout main;
/usr/bin/python3 "./main.py";
/usr/bin/git add "../web/db/notaries.json";
/usr/bin/git add "../web/db/zip_hash.sha256";
/usr/bin/git commit -m "Listing Update";
/usr/bin/git push origin main;