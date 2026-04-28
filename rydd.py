import imaplib
import getpass
from datetime import datetime, timedelta

BRUKER = "greknuts@online.no"
PASSORD = getpass.getpass("Skriv inn e-post passord: ")
IMAP_SERVER = "imap.online.no"
MAPPE_INN = "INBOX"
MAPPE_UT = "MAS"
MAKS_ANTALL = 200

grense_dato = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")

print("🔌 Kobler til e-post...")
imap = imaplib.IMAP4_SSL(IMAP_SERVER)
imap.login(BRUKER, PASSORD)

status, _ = imap.create(MAPPE_UT)
print("Opprett mappe:", status)

status, _ = imap.select(MAPPE_INN)
print("Åpner INBOX:", status)

status, messages = imap.search(None, f'(BEFORE {grense_dato})')
if status != "OK":
    print("Kunne ikke hente e-postliste.")
    imap.logout()
    raise SystemExit

mail_ids = messages[0].split()
print(f"Fant {len(mail_ids)} e-poster eldre enn en uke.")

# Ta bare de første 200
mail_ids = mail_ids[:MAKS_ANTALL]
print(f"Behandler {len(mail_ids)} e-poster i denne runden.")

flyttet = 0

for mail_id in mail_ids:
    copy_status, _ = imap.copy(mail_id, MAPPE_UT)
    if copy_status == "OK":
        store_status, _ = imap.store(mail_id, "+FLAGS", "\\Deleted")
        if store_status == "OK":
            flyttet += 1

imap.expunge()
imap.logout()

print(f"\n✅ Ferdig. Flyttet {flyttet} e-poster til {MAPPE_UT}.")