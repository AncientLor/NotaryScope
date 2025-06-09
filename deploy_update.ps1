git checkout main;
python "./main.py";
git add "../web/db/notaries.json";
git add "../web/db/zip_hash.sha256";
git commit -m "Listing Update";
git push origin main;