import requests
import bs4  # BeautifulSoup from beautifulsoup4
import random
import string
import time
import os
import re
from datetime import date, timedelta
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from colorama import init, Fore, Style

init(autoreset=True)

class Colors:
    HEADER = Fore.MAGENTA
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    DIM = Style.DIM
# ANSI colors for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display a boxed message
def display_box(title, lines):
    max_len = max(len(line) for line in lines)
    if title:
        max_len = max(max_len, len(title) + 4)  # Adjust for title
    print(f"{Colors.OKBLUE}┌{'─' * (max_len + 2)}┐{Colors.ENDC}")
    if title:
        print(f"{Colors.OKBLUE}│ {Colors.BOLD}{title}{Colors.ENDC}{Colors.OKBLUE} {' ' * (max_len - len(title))} │{Colors.ENDC}")
        print(f"{Colors.OKBLUE}├{'─' * (max_len + 2)}┤{Colors.ENDC}")
    for line in lines:
        print(f"{Colors.OKBLUE}│ {line}{' ' * (max_len - len(line))} │{Colors.ENDC}")
    print(f"{Colors.OKBLUE}└{'─' * (max_len + 2)}┘{Colors.ENDC}")

# Banner info
def display_banner():
    info_lines = [
        "Tool Name: Mini_Dark_Clone",
        "Developer: The Realm of Classic Hackers (T.R.C.H)",
        "GitHub: T.R.C.H"
    ]
    display_box("—InFo", info_lines)




banner = f"""
{Colors.OKGREEN}
 _      _  _      _              
/ \__/|/ \/ \  /|/ \             
| |\/||| || |\ ||| |             
| |  ||| || | \||| |             
\_/  \|\_/\_/  \|\_/             
                                 
   ____  ____  ____  _  __       
  /  _ \/  _ \/  __\/ |/ /       
  | | \|| / \||  \/||   /        
  | |_/|| |-|||    /|   \        
  \____/\_/ \|\_/\_\\_|\_\       
                                 
 ____  _     ____  _      _____  
/   _\/ \   /  _ \/ \  /|/  __/  
|  /  | |   | / \|| |\ |||  \    
|  \__| |_/\| \_/|| | \|||  /_   
\____/\____/\____/\_/  \|\____\  
                                        
{Colors.ENDC}

"""
 
# Note box
def display_note():
    note_lines = [
        "this tool may take up so e time to create accounts",
        "This tool is for testin",
        "Dnt forget 2 be anonymous"
    ]
    display_box("—Note–", note_lines)

# List to store created accounts
accounts = []

# Function to generate random username
def random_username(length=8):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

# Function to generate random password
def random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to generate random birthdate (over 18 years old)
def random_birthdate():
    today = date.today()
    start_date = today - timedelta(days=365*50)  # Up to 50 years ago
    end_date = today - timedelta(days=365*18)    # At least 18 years ago
    random_days = random.randint(0, (end_date - start_date).days)
    birth_date = start_date + timedelta(days=random_days)
    return birth_date.strftime('%Y-%m-%d')  # Assume YYYY-MM-DD format

# Function to generate random gender
def random_gender():
    return random.choice(['male', 'female', 'other'])

# Function to get temp email using 1secmail API (used instead of tmailor.com for reliability and API support; tmailor scraping may require JS handling which is avoided)
def get_temp_email():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1')
    if response.status_code == 200:
        return response.json()[0]
    else:
        raise Exception("Failed to generate temp email")

# Function to get messages for temp email
def get_messages(email):
    login, domain = email.split('@')
    response = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}')
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Function to read a message
def read_message(email, msg_id):
    login, domain = email.split('@')
    response = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}')
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to read message")

# Function to create an account on the website
def create_account(base_url, num):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        print(f"{Colors.OKGREEN}Starting account creation {num}...{Colors.ENDC}")

        # Generate account details
        temp_email = get_temp_email()
        username = random_username()
        password = random_password()
        birthdate = random_birthdate()
        gender = random_gender()

        # Get home page to find sign up link
        resp = session.get(base_url, timeout=10)
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')

        # Find create account button/link (adjust regex if needed)
        signup_tag = soup.find(lambda tag: (tag.name == 'a' or tag.name == 'button') and re.search(r'create\s+account|sign\s+up|register', tag.text, re.IGNORECASE))
        if not signup_tag:
            raise Exception("Could not find sign up button/link. Please adjust the selector.")

        if signup_tag.name == 'button':
            # Assume it's a submit button in a form, but for simplicity, assume it's a link
            raise Exception("Button found but handling forms for signup link not implemented; assume <a> tag.")

        signup_href = signup_tag['href']
        signup_url = urljoin(base_url, signup_href)

        # Get signup page
        resp = session.get(signup_url, timeout=10)
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')

        # Find the registration form
        form = soup.find('form')
        if not form:
            raise Exception("No form found on signup page.")

        action = urljoin(resp.url, form.get('action', ''))
        method = form.get('method', 'get').lower()

        # Prepare data by filling fields
        data = {}
        for input_tag in form.find_all('input'):
            name = input_tag.get('name')
            if not name:
                continue
            itype = input_tag.get('type', 'text').lower()
            if itype == 'email':
                data[name] = temp_email
            elif itype == 'password':
                data[name] = password
            elif itype == 'text':
                if 'user' in name.lower():
                    data[name] = username
                elif 'birth' in name.lower() or 'date' in name.lower():
                    data[name] = birthdate
                else:
                    data[name] = 'Test ' + name  # Fallback for other texts
            elif itype in ['radio', 'checkbox']:
                if 'gender' in name.lower():
                    data[name] = gender
            # Ignore submit, hidden might be included if value present
            if itype == 'hidden':
                data[name] = input_tag.get('value', '')

        # Handle selects (e.g., gender)
        for select in form.find_all('select'):
            name = select.get('name')
            if name and 'gender' in name.lower():
                data[name] = gender
            # Add more if needed

        # Submit the form
        if method == 'post':
            resp = session.post(action, data=data, timeout=10, allow_redirects=True)
        else:
            resp = session.get(action, params=data, timeout=10, allow_redirects=True)
        resp.raise_for_status()

        # Now handle verification or skip
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')

        # Look for skip button
        skip_tag = soup.find(lambda tag: (tag.name == 'a' or tag.name == 'button') and 'skip' in tag.text.lower())
        if skip_tag:
            print(f"{Colors.WARNING}Found skip button, skipping verification...{Colors.ENDC}")
            if skip_tag.name == 'a':
                skip_url = urljoin(resp.url, skip_tag['href'])
                resp = session.get(skip_url, timeout=10)
            else:
                # Assume submit form
                skip_form = skip_tag.find_parent('form')
                if skip_form:
                    skip_action = urljoin(resp.url, skip_form.get('action', ''))
                    skip_method = skip_form.get('method', 'get').lower()
                    skip_data = {}  # Assume no data needed
                    if skip_method == 'post':
                        resp = session.post(skip_action, data=skip_data, timeout=10)
                    else:
                        resp = session.get(skip_action, params=skip_data, timeout=10)

        else:
            # Assume verification needed, poll for code
            print(f"{Colors.OKBLUE}Waiting for verification code...{Colors.ENDC}")
            code = None
            start_time = time.time()
            while time.time() - start_time < 60:
                messages = get_messages(temp_email)
                if messages:
                    latest_msg = messages[0]  # Latest message
                    msg_data = read_message(temp_email, latest_msg['id'])
                    body = msg_data.get('textBody') or msg_data.get('body') or ''
                    codes = re.findall(r'\b\d{4,6}\b', body)  # Find 4-6 digit codes
                    if codes:
                        code = codes[0]
                        break
                time.sleep(5)

            if not code:
                raise Exception("No verification code received in time.")

            print(f"{Colors.OKGREEN}Verification code found: {code}{Colors.ENDC}")

            # Submit code (assume form on current page)
            verify_form = soup.find('form')  # Assume the verification form
            if not verify_form:
                raise Exception("No verification form found.")

            verify_action = urljoin(resp.url, verify_form.get('action', ''))
            verify_method = verify_form.get('method', 'get').lower()
            verify_data = {}
            for input_tag in verify_form.find_all('input'):
                name = input_tag.get('name')
                if name and ('code' in name.lower() or 'verify' in name.lower()):
                    verify_data[name] = code
                elif input_tag.get('type') == 'hidden':
                    verify_data[name] = input_tag.get('value', '')

            if verify_method == 'post':
                resp = session.post(verify_action, data=verify_data, timeout=10, allow_redirects=True)
            else:
                resp = session.get(verify_action, params=verify_data, timeout=10, allow_redirects=True)
            resp.raise_for_status()

        # Assume account created successfully if no errors
        account_info = {
            'email': temp_email,
            'username': username,
            'password': password,
            'gender': gender,
            'birthdate': birthdate
        }
        accounts.append(account_info)

        print(f"{Colors.OKGREEN}Account created successfully!{Colors.ENDC}")
        display_account_info(account_info)

        return True

    except Exception as e:
        print(f"{Colors.FAIL}Error creating account: {str(e)}{Colors.ENDC}")
        return False

# Function to display account info in a box
def display_account_info(info):
    lines = [
        f"Email: {info['email']}",
        f"Username: {info['username']}",
        f"Password: {info['password']}",
        f"Gender: {info['gender']}",
        f"Birthdate: {info['birthdate']}"
    ]
    display_box(None, lines)

# Function to view all accounts
def view_accounts():
    if not accounts:
        print(f"{Colors.WARNING}No accounts created yet.{Colors.ENDC}")
        return
    for idx, acc in enumerate(accounts, 1):
        print(f"{Colors.HEADER}Account {idx}:{Colors.ENDC}")
        display_account_info(acc)

# Main menu
def main():
    base_url = input(f"{Colors.OKBLUE}Enter your  website URL (e.g., https://example.com): {Colors.ENDC}").strip()
    while True:
        clear_screen()
        print(banner)
        display_banner()
        display_note()
        print(f"\n{Colors.HEADER}Menu:{Colors.ENDC}")
        print("1. Create accounts")
        print("2. View accounts")
        print("3. Exit")
        choice = input(f"{Colors.OKBLUE}Enter choice: {Colors.ENDC}").strip()

        if choice == '1':
            try:
                num_accounts = int(input(f"{Colors.OKBLUE}How many accounts to create (1-25)? {Colors.ENDC}"))
                if num_accounts < 1 or num_accounts > 25:
                    print(f"{Colors.FAIL}Number must be between 1 and 25.{Colors.ENDC}")
                    continue
            except ValueError:
                print(f"{Colors.FAIL}Invalid number.{Colors.ENDC}")
                continue

            successes = 0
            for i in range(1, num_accounts + 1):
                if create_account(base_url, i):
                    successes += 1
                time.sleep(2)  # Delay between creations to avoid overload

            print(f"{Colors.OKGREEN}Created {successes}/{num_accounts} accounts successfully.{Colors.ENDC}")

        elif choice == '2':
            view_accounts()

        elif choice == '3':
            print(f"{Colors.OKGREEN}Exiting...{Colors.ENDC}")
            break

        else:
            print(f"{Colors.FAIL}Invalid choice.{Colors.ENDC}")

        input(f"{Colors.OKBLUE}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    main()