# janniebuchthorborg.dk

Statisk hjemmeside for Jannie Buch Thorborg. Erstatter den gamle Aida-side hos one.com.
Udgiv ALDRIG fra Aida-editoren igen – den overskriver siden.

## Ret tekst
1. Ret teksterne i `build.py`.
2. Kør `python3 build.py` – den færdige side lægges i `dist/`.
3. Commit og push til `main`.
4. Læg de ændrede filer fra `dist/` op på webhotellet (one.com File Manager, mappen httpd.www for janniebuchthorborg.dk).

Statistik: Cloudflare Web Analytics (ingen cookies, intet cookie-banner).
Aidas filer gemmes på webhotellet i `/_aida-backup/` (spærret for besøgende).

Portrætbillederne (assets/img/jannie-*.jpg) er hentet fra Jannies Instagram og ligger kun på serveren, ikke i repoet. Upload dist/ overskriver dem ikke.
