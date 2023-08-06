#!/usr/bin/python3
import os
import subprocess
import email.charset
import locale
from subprocess import (Popen,PIPE)
from email.message import Message

# tag::main[]
# ## DIESEN TEIL BITTE ANPASSEN ####
from_email = "it-admin@Recplastgmbh.de"
to_email = "it-admin@Recplastgmbh.de"
# ##################################

# Variablen fuer Tests
MAIL_BINARY = "/usr/bin/mail"
SENDMAIL_BINARY = "/usr/sbin/sendmail"
subject = "Unattended-Upgrades Test Mail"
body = "Wenn diese E-Mail ankommt, funktioniert die E-Mail-Funktion auch fuer Unattended-Upgrades! :)"

# Funktion fuer das Versenden ueber /usr/bin/mail
def _send_mail_using_mailx(from_address, to_address, subject, body):
    encoded_body = body.encode(locale.getpreferredencoding(False), errors="replace")
    mail = subprocess.Popen(
        [MAIL_BINARY, "-r", from_address, "-s", subject, to_address],
        stdin=subprocess.PIPE, universal_newlines=False)
    mail.stdin.write(encoded_body)
    mail.stdin.close()
    ret = mail.wait()
    return ret

# Funktion fuer das Versenden ueber /usr/sbin/sendmail
def _send_mail_using_sendmail(from_address, to_address, subject, body):
    msg = Message()
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Auto-Submitted'] = "auto-generated"
    charset = email.charset.Charset("utf-8")
    charset.body_encoding = email.charset.QP  # type: ignore
    msg.set_payload(body, charset)
    sendmail = subprocess.Popen(
        [SENDMAIL_BINARY, "-oi", "-t"],
        stdin=subprocess.PIPE, universal_newlines=True)
    sendmail.stdin.write(msg.as_string())
    sendmail.stdin.close()
    ret = sendmail.wait()
    return ret

# Versendet die Test E-Mail ueber '/usr/sbin/sendmail' oder '/usr/bin/mail'
if os.path.exists(SENDMAIL_BINARY):
    print("Sende E-Mail mit 'sendmail' Programm")
    ret = _send_mail_using_sendmail(from_email, to_email, subject, body)
elif os.path.exists(MAIL_BINARY):
    print("Sende E-Mail mit 'mail' Programm")
    ret = _send_mail_using_mailx(from_email, to_email, subject, body)

# Ausgabe je nach Ergebnis
if ret == 0:
    print("E-Mail erfolgreich versand.")
else:
    print("E-Mail konnte nicht versendet werden.")
# end::main[]