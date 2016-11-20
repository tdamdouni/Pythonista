import console, dialogs
import smtplib
import time
import ui

def send_action(sender):
    global sendto, subj, assignment, v
    sendto = v['tofield'].text
    subj = v['subjectfield'].text    
    assignment = v['message'].text
    main()
    
def cancel_action(sender):
    smtpserver.close()
    ui.close_all()

def main():    
    global email_user, sendto, subj, assignment        
    header = 'To: ' + sendto + '\n' + 'From: ' + email_user + '\n' + 'Subject: ' + subj +'\n'
    msg = header + assignment + '\n'
    smtpserver.sendmail(email_user, sendto, msg)
    sent_time = time.strftime("%A, %B %d, %Y at %I:%M:%S %p.", time.localtime())
    console.hud_alert('Your message has been sent successfully on ' + sent_time, 'success', 2.1)
    v['tofield'].text = ''
    v['subjectfield'].text = ''
    v['message'].text = ''

def login():
    global email_user, email_pwd
    fields = [{'key' : 'username', 'type' : 'email', 'value' : 'Enter your username'},
              {'key' : 'password', 'type' : 'password', 'value' : ''}]
    info=dialogs.form_dialog(title='Enter your login credentials', fields=fields)
    if info == None:
        console.hud_alert('Login Cancelled', 'error', 1.5)
    else:
        email_user = info['username']
        email_pwd = info['password']
        setup()

def setup():
    global email_user, email_pwd, v
    v = ui.load_view('myemail')
    send = ui.ButtonItem()
    send.title = 'Send'
    send.action = send_action
    v.right_button_items = [send]
    fromfield = v['fromfield']
    fromfield.text = email_user
    fromfield.scroll_enabled = False
    v['tofield'].clear_button_mode = 'while_editing'
    v['subjectfield'].clear_button_mode = 'while_editing'
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(email_user, email_pwd)
    v.present('sheet')

providers = dialogs.list_dialog(title='Select Your Email Provider', items=["Gmail", "AOL", "Yahoo!", "Comcast"], multiple=False)
if providers == 'Gmail':
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
elif providers == 'AOL':
    smtpserver = smtplib.SMTP("smtp.aol.com",587)
elif providers == 'Yahoo!':
    smtpserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
elif providers == 'Comcast':
    smtpserver = smtplib.SMTP("smtp.comcast.net",587)
login()
