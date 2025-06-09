$DIRNAME = $pwd.ToString().Substring(2).Split('\')[-1]

if ($DIRNAME -ne 'deploy')
{
	Write-Host -Object "Make sure this script is run from -> /NotaryScope/util/deploy";
	exit(1);
}

Set-Location -Path '../..';

git checkout main;

python "util/main.py";
git add "web/db/notaries.json";
git add "web/db/zip_hash.sha256";

npx "@tailwindcss/cli" -i 'util/deploy/css/input.css' -o 'web/css/main.css';
git add "web/css/main.css";

git commit -m "Listing Update";
git push origin main;
