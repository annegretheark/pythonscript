import imaplib
import email
import re
import getpass
from email.header import decode_header
from urllib.parse import urlparse
from email.header import decode_header
from urllib.parse import urlparse
password = getpass.getpass("Skriv inn passord: ")

mail = imaplib.IMAP4_SSL("e-postserver")
mail.login("brukernavn", password)

status, mailboxes = mail.list()

for mbox in mailboxes:
    print(mbox.decode())
