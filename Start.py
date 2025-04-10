import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def log_result(filename, result_message):
    with open(filename, 'a') as log_file:
        log_file.write(result_message + '\n')

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def load_smtp_details(smtp_file):
    try:
        smtp_servers = []
        with open(smtp_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                smtp_details = line.strip().split('|')
                if len(smtp_details) == 4:
                    smtp_servers.append(smtp_details)
        if smtp_servers:
            print(f"{GREEN}{len(smtp_servers)} SMTP servers successfully loaded from {smtp_file}!{RESET}")
            return smtp_servers
        else:
            print(f"{RED}No valid SMTP servers found in {smtp_file}!{RESET}")
            return []
    except FileNotFoundError:
        print(f"\nError: {smtp_file} file not found!")
        return []

def check_smtp_connection(smtp_server, smtp_port):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.quit()
        print(f"{GREEN}SMTP connection successful to {smtp_server}:{smtp_port}!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}SMTP connection failed to {smtp_server}:{smtp_port}: {e}{RESET}")
        return False

def load_html_letter(letter_file):
    try:
        with open(letter_file, 'r') as f:
            body = f.read()
            print(f"{GREEN}HTML letter successfully loaded from {letter_file}!{RESET}")
            return body
    except FileNotFoundError:
        print(f"\nError: {letter_file} file not found!")
        return None

def load_emails(emails_file):
    try:
        with open(emails_file, 'r') as f:
            receiver_emails = f.readlines()
        receiver_emails = [email.strip() for email in receiver_emails]
        if not receiver_emails:
            print(f"\nNo emails found in {emails_file}.")
        else:
            print(f"{GREEN}{len(receiver_emails)} recipient email(s) successfully loaded from {emails_file}!{RESET}")
        return receiver_emails
    except FileNotFoundError:
        print(f"\nError: {emails_file} file not found!")
        return None

def check_combo(emails_file):
    receiver_emails = load_emails(emails_file)
    if not receiver_emails:
        print(f"{RED}No valid emails found in {emails_file}!{RESET}")
        return False
    invalid_emails = [email for email in receiver_emails if '@' not in email]
    if invalid_emails:
        print(f"{RED}Invalid emails found: {', '.join(invalid_emails)}{RESET}")
        return False
    else:
        print(f"{GREEN}All emails are valid in {emails_file}!{RESET}")
        return True

def send_email(smtp_file, letter_file, emails_file, subject_file):
    smtp_servers = load_smtp_details(smtp_file)
    if not smtp_servers:
        return
    body = load_html_letter(letter_file)
    if not body:
        return
    receiver_emails = load_emails(emails_file)
    if not receiver_emails:
        return
    try:
        with open(subject_file, 'r') as f:
            subject = f.readline().strip()
            print(f"{GREEN}Subject successfully loaded from {subject_file}!{RESET}")
    except FileNotFoundError:
        print("\nError: Subject file not found!")
        return
    for receiver_email in receiver_emails:
        email_sent = False
        for smtp_details in smtp_servers:
            smtp_server, smtp_port, smtp_user, smtp_password = smtp_details
            if not check_smtp_connection(smtp_server, smtp_port):
                continue
            sender_email = smtp_user
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "html"))
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                log_result('sent.txt', f"Email successfully sent to {receiver_email} using {smtp_server}")
                print(f"{GREEN}\nEmail sent successfully to {receiver_email} using {smtp_server}!{RESET}")
                email_sent = True
                break
            except Exception as e:
                log_result('failed.txt', f"Failed to send email to {receiver_email} using {smtp_server}. Error: {e}")
                print(f"{RED}\nFailed to send email to {receiver_email} using {smtp_server}: {e}{RESET}")
            finally:
                server.quit()
        if not email_sent:
            print(f"{RED}Failed to send email to {receiver_email} after trying all SMTP servers.{RESET}")

def translate(language):
    translations = {
        "EN": {
            "menu_1": "Add your SMTPS",
            "menu_2": "Add HTML Letter",
            "menu_3": "Enter Emails for Send",
            "menu_4": "Check SMTP (smtps.txt)",
            "menu_5": "Sending",
            "menu_6": "Exit",
            "choose_option": "Choose an option:",
            "smtp_file_not_found": "Error: SMTP file not found!",
            "letter_file_not_found": "Error: Letter file not found!",
            "subject_file_not_found": "Error: Subject file not found!",
            "invalid_choice": "Invalid choice! Please select a valid option.",
            "exiting": "Exiting the program."
        },
        "ID": {
            "menu_1": "Tambahkan SMTPS Anda",
            "menu_2": "Tambahkan Surat HTML",
            "menu_3": "Masukkan Email untuk Kirim",
            "menu_4": "Cek SMTP (smtps.txt)",
            "menu_5": "Mengirim",
            "menu_6": "Keluar",
            "choose_option": "Pilih opsi:",
            "smtp_file_not_found": "Error: File SMTP tidak ditemukan!",
            "letter_file_not_found": "Error: File surat tidak ditemukan!",
            "subject_file_not_found": "Error: File subjek tidak ditemukan!",
            "invalid_choice": "Pilihan tidak valid! Silakan pilih opsi yang valid.",
            "exiting": "Keluar dari program."
        },
        "RU": {
            "menu_1": "Добавить ваши SMTPS",
            "menu_2": "Добавить HTML письмо",
            "menu_3": "Ввод email для отправки",
            "menu_4": "Проверить SMTP (smtps.txt)",
            "menu_5": "Отправка",
            "menu_6": "Выход",
            "choose_option": "Выберите опцию:",
            "smtp_file_not_found": "Ошибка: файл SMTP не найден!",
            "letter_file_not_found": "Ошибка: файл письма не найден!",
            "subject_file_not_found": "Ошибка: файл темы не найден!",
            "invalid_choice": "Неверный выбор! Пожалуйста, выберите правильную опцию.",
            "exiting": "Выход из программы."
        },
        "DE": {
            "menu_1": "Fügen Sie Ihre SMTPS hinzu",
            "menu_2": "HTML-Brief hinzufügen",
            "menu_3": "E-Mails zum Senden eingeben",
            "menu_4": "Überprüfen Sie SMTP (smtps.txt)",
            "menu_5": "Versenden",
            "menu_6": "Beenden",
            "choose_option": "Wählen Sie eine Option:",
            "smtp_file_not_found": "Fehler: SMTP-Datei nicht gefunden!",
            "letter_file_not_found": "Fehler: Briefdatei nicht gefunden!",
            "subject_file_not_found": "Fehler: Dateityp nicht gefunden!",
            "invalid_choice": "Ungültige Wahl! Bitte wählen Sie eine gültige Option.",
            "exiting": "Verlassen des Programms."
        },
        "ES": {
            "menu_1": "Agregar tus SMTPS",
            "menu_2": "Agregar carta HTML",
            "menu_3": "Ingresar correos electrónicos para enviar",
            "menu_4": "Verificar SMTP (smtps.txt)",
            "menu_5": "Enviando",
            "menu_6": "Salir",
            "choose_option": "Elige una opción:",
            "smtp_file_not_found": "Error: ¡Archivo SMTP no encontrado!",
            "letter_file_not_found": "Error: ¡Archivo de carta no encontrado!",
            "subject_file_not_found": "Error: ¡Archivo de asunto no encontrado!",
            "invalid_choice": "¡Elección inválida! Por favor seleccione una opción válida.",
            "exiting": "Saliendo del programa."
        }
    }
    return translations.get(language, translations["EN"])

def main_menu():
    print("Select language: [EN/ID/RU/DE/ES]")
    language = input("Enter choice (EN/ID/RU/DE/ES): ").strip().upper()
    texts = translate(language)
    smtp_file = ''
    letter_file = ''
    emails_file = ''
    subject_file = ''
    while True:#Credit: Collee1
        print(f"\n{BLUE}{texts['choose_option']}{RESET}")
        print(f"{BLUE}1. {texts['menu_1']}{RESET}")
        print(f"{BLUE}2. {texts['menu_2']}{RESET}")
        print(f"{BLUE}3. {texts['menu_3']}{RESET}")
        print(f"{BLUE}4. {texts['menu_4']}{RESET}")
        print(f"{BLUE}5. {texts['menu_5']}{RESET}")
        print(f"{BLUE}6. {texts['menu_6']}{RESET}")
        choice = input(f"{BLUE}{texts['choose_option']} {RESET}")
        if choice == '1':
            smtp_file = input("Enter SMTP file path: ")
            if not os.path.isfile(smtp_file):
                print(f"{RED}{texts['smtp_file_not_found']}{RESET}")
        elif choice == '2':
            letter_file = input("Enter HTML letter file path: ")
            if not os.path.isfile(letter_file):
                print(f"{RED}{texts['letter_file_not_found']}{RESET}")
        elif choice == '3':
            emails_file = input("Enter emails file path: ")
            if not os.path.isfile(emails_file):
                print(f"{RED}{texts['smtp_file_not_found']}{RESET}")
        elif choice == '4':
            if not os.path.isfile(smtp_file):
                print(f"{RED}{texts['smtp_file_not_found']}{RESET}")
            else:
                send_email(smtp_file, letter_file, emails_file, subject_file)
        elif choice == '5':
            if smtp_file and letter_file and emails_file:
                send_email(smtp_file, letter_file, emails_file, subject_file)
            else:
                print(f"{RED}{texts['smtp_file_not_found']} {texts['letter_file_not_found']}{RESET}")
        elif choice == '6':
            print(f"{GREEN}{texts['exiting']}{RESET}")
            break
        else:
            print(f"{RED}{texts['invalid_choice']}{RESET}")

if __name__ == "__main__":
    main_menu()


