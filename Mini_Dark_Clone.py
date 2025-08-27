import requests
from bs4 import BeautifulSoup
import random
import time
import os
import re
import sys
from colorama import init, Fore, Style

init(autoreset=True)

# ANSI color codes for formatting
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
    
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_size():
    """Returns the current terminal width."""
    try:
    	return os.get_terminal_size().columns
    except OSError:
        return 80

def create_responsive_box(content, color=Colors.CYAN, border_color=Colors.CYAN):
    """Creates a text box with a border that adapts to terminal width."""
    terminal_width = get_terminal_size()
    
    lines = content.strip().split('\n')
    max_length = max(len(re.sub(r'\x1b\[[0-9;]*m', '', line)) for line in lines)
    
    box_width = min(max_length + 2, terminal_width - 4)
    
    top_line = '┌' + '─' * box_width + '┐'
    bottom_line = '└' + '─' * box_width + '┘'
    
    print(border_color + top_line + Colors.RESET)
    
    for line in lines:
        clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
        padded_line = clean_line.ljust(box_width)
        truncated_line = padded_line[:box_width]
        print(f"{border_color}│ {color}{truncated_line}{Colors.RESET} {border_color}│{Colors.RESET}")
    
    print(border_color + bottom_line + Colors.RESET)

def print_banner(color=Colors.GREEN):
    clear_screen()
    banner = f"""
{color}{Style.BRIGHT}
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
                                        
{Colors.RESET}
"""
    print(banner)

def tool_info():
    clear_screen()
    tool_info_content = f"""
{Colors.BOLD}{Colors.CYAN}✨ Tool Name:{Colors.RESET}Mini Dark Clone
{Colors.BOLD}{Colors.CYAN}✨ Created by:{Colors.RESET} T.R & C.H
{Colors.BOLD}{Colors.CYAN}✨ Version:{Colors.RESET} 2.1
"""
    create_responsive_box(tool_info_content, color=Colors.CYAN, border_color=Colors.CYAN)
    
    print()
    note_info = f"{Colors.BOLD}{Colors.YELLOW}Note:{Colors.RESET} If the tool doesn't work, toggle airplane mode.\n{Colors.BOLD}{Colors.YELLOW}VPN:{Colors.RESET} Ensure your VPN is active for anonymity."
    create_responsive_box(note_info, color=Colors.YELLOW, border_color=Colors.YELLOW)
    print()
    input(f"{Colors.BOLD}Press Enter to return to the menu...{Colors.RESET}")

def get_temp_email(retries=3):
    """Fetches a temporary email address from tmailor.com with retries"""
    create_responsive_box("Fetching a temporary an email address...", color=Colors.BLUE, border_color=Colors.BLUE)
    for attempt in range(retries):
        try:
            response = requests.get('https://tmailor.com', timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            email_input = soup.find('input', {'id': 'tmail'})
            if email_input:
                email = email_input.get('value')
                create_responsive_box(f"{Colors.GREEN}✅ Got an email: {email}", color=Colors.GREEN, border_color=Colors.GREEN)
                return email
            else:
                create_responsive_box(f"{Colors.YELLOW}⚠️ Could not find email input. Retrying...{Colors.DIM}", color=Colors.YELLOW, border_color=Colors.YELLOW)
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            create_responsive_box(f"{Colors.RED}❌ Failed to get email on attempt {attempt + 1}: {e}", color=Colors.RED, border_color=Colors.RED)
            time.sleep(1)
    return None

def get_verification_code(email, timeout=60):
    """Waits for and fetches the verification code from the inbox"""
    create_responsive_box(f"⏳ Waiting for verification email at: {email}...", color=Colors.BLUE, border_color=Colors.BLUE)
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            inbox_url = f'https://tmailor.com/api/get_inbox_by_email?email={email}'
            response = requests.get(inbox_url)
            emails_data = response.json()
            if 'emails' in emails_data:
                for mail in emails_data['emails']:
                    if "ChatSphere" in mail.get('subject', ''):
                        code = re.search(r'\d{6}', mail.get('body', ''))
                        if code:
                            create_responsive_box(f"{Colors.GREEN}✅ Found verification code: {code.group(0)}", color=Colors.GREEN, border_color=Colors.GREEN)
                            return code.group(0)
        except (requests.exceptions.RequestException, ValueError) as e:
            create_responsive_box(f"{Colors.YELLOW}⚠️ An error occurred while checking inbox: {e}{Colors.DIM}", color=Colors.YELLOW, border_color=Colors.YELLOW)
        
        time.sleep(5)
    
    create_responsive_box(f"{Colors.RED}❌ Timed out waiting for verification code.", color=Colors.RED, border_color=Colors.RED)
    return None

def create_account(session, website_url, email, password, username):
    """Automates the account creation process"""
    create_responsive_box(f"🌐 Starting account creation for {username}...", color=Colors.BLUE, border_color=Colors.BLUE)
    try:
        response = session.get(website_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        skip_button = soup.find(['button', 'a'], string=re.compile(r'skip', re.IGNORECASE))
        if skip_button:
            create_responsive_box("✅ Found and pressing 'Skip' button.", color=Colors.GREEN, border_color=Colors.GREEN)
        
        form = soup.find('form')
        if not form:
            create_responsive_box("❌ Could not find the registration form.", color=Colors.RED, border_color=Colors.RED)
            return False
            
        form_action = form.get('action') if form.get('action') else website_url
        
        birth_year = random.randint(1950, 2005)
        
        payload = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password,
            'gender': random.choice(['male', 'female', 'other']),
            'birth_year': birth_year,
            'agree_to_terms': 'on',
        }
        
        response = session.post(form_action, data=payload)
        
        if 'Verification Code' in response.text or 'awaiting verification' in response.text:
            create_responsive_box("✅ Account created successfully. Awaiting verification code...", color=Colors.GREEN, border_color=Colors.GREEN)
            return True
        else:
            create_responsive_box(f"❌ Account creation failed. Response status: {response.status_code}", color=Colors.RED, border_color=Colors.RED)
            return False
            
    except requests.exceptions.RequestException as e:
        create_responsive_box(f"❌ An error occurred during account creation: {e}", color=Colors.RED, border_color=Colors.RED)
        return False
        
def confirm_account(session, verify_url, verification_code):
    """Submits the verification code to the website"""
    create_responsive_box("Submitting verification code...", color=Colors.BLUE, border_color=Colors.BLUE)
    try:
        response = session.get(verify_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        
        if not form:
            create_responsive_box("❌ Could not find the verification form.", color=Colors.RED, border_color=Colors.RED)
            return False
            
        payload = {
            'verification_code': verification_code
        }
        
        response = session.post(form.get('action'), data=payload)
        
        if 'Account Verified' in response.text or 'Login Page' in response.text:
            return True
        else:
            create_responsive_box(f"❌ Verification failed. Response status: {response.status_code}", color=Colors.RED, border_color=Colors.RED)
            return False
            
    except requests.exceptions.RequestException as e:
        create_responsive_box(f"❌ An error occurred during verification: {e}", color=Colors.RED, border_color=Colors.RED)
        return False

def generate_user_data():
    """Generates random username, password, and other data"""
    username = 'testuser_' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    password = 'Pass' + ''.join(random.choices('0123456789!@#$%^&*', k=8))
    
    return {
        'username': username,
        'password': password,
        'gender': random.choice(['Male', 'Female']),
        'birth_date': f"{random.randint(1950, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    }

def display_account_info(info):
    """Displays created account information in a colorful box"""
    content = f"""
{Colors.BOLD}{Colors.GREEN}New Account Created! 🎉{Colors.RESET}
{Colors.BOLD}{Colors.CYAN}Username:{Colors.RESET} {info['username']}
{Colors.BOLD}{Colors.CYAN}Password:{Colors.RESET} {info['password']}
{Colors.BOLD}{Colors.CYAN}Email:{Colors.RESET} {info['email']}
{Colors.BOLD}{Colors.CYAN}Gender:{Colors.RESET} {info['gender']}
{Colors.BOLD}{Colors.CYAN}Birth Date:{Colors.RESET} {info['birth_date']}
"""
    create_responsive_box(content, color=Colors.GREEN, border_color=Colors.GREEN)

def print_progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    """Prints a simple progress bar in the terminal"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} {Colors.CYAN}|{bar}| {percent}% {suffix}{Colors.RESET}', end='\r', file=sys.stdout)
    if iteration == total: 
        print()

def main_menu():
    """Main menu for the user"""
    while True:
        print_banner()
        menu_content = f"""
{Colors.BOLD}{Colors.CYAN}Welcome to the Mini DarkClone!{Colors.RESET}

{Colors.GREEN}1. Create accounts
{Colors.GREEN}2. Tool Info
{Colors.RED}3. Exit
"""
        create_responsive_box(menu_content, color=Colors.GREEN, border_color=Colors.GREEN)

        choice = input(f"{Colors.BOLD}{Colors.YELLOW}Enter your choice (1-3): {Colors.RESET}")

        if choice == '1':
            try:
                website_url = input(f"{Colors.BOLD}{Colors.BLUE}Enter your website URL (https://example.com): {Colors.RESET}")
                num_accounts = int(input(f"{Colors.BOLD}{Colors.BLUE}How many accounts to create (max 25)? {Colors.RESET}"))
                if 1 <= num_accounts <= 25:
                    test_chat_sphere(website_url, num_accounts)
                else:
                    create_responsive_box("❌ Please enter a number between 1 and 25.", color=Colors.RED, border_color=Colors.RED)
            except ValueError:
                create_responsive_box("❌ Invalid input. Please enter a number.", color=Colors.RED, border_color=Colors.RED)
        elif choice == '2':
            tool_info()
        elif choice == '3':
            create_responsive_box("👋 Exiting...", color=Colors.YELLOW, border_color=Colors.YELLOW)
            break
        else:
            create_responsive_box("❌ Invalid choice. Please try again.", color=Colors.RED, border_color=Colors.RED)

def test_chat_sphere(website_url, num_accounts):
    """Main function to run the account creation process"""
    
    print_banner()
    create_responsive_box(f"--- Starting account creation for {num_accounts} accounts ---", color=Colors.CYAN, border_color=Colors.CYAN)
    
    for i in range(num_accounts):
        print(f"\n{Colors.BOLD}{Colors.HEADER}--- Account {i+1} of {num_accounts} ---{Colors.RESET}")
        print_progress_bar(i, num_accounts, prefix='Progress:', suffix='Complete')

        session = requests.Session()
        
        temp_email = get_temp_email()
        if not temp_email:
            continue
            
        user_data = generate_user_data()
        user_data['email'] = temp_email
        
        account_created = create_account(session, website_url, user_data['email'], user_data['password'], user_data['username'])
        
        if account_created:
            verify_url = website_url.rsplit('/', 1)[0] + '/verify' 
            verification_code = get_verification_code(temp_email)
            if verification_code:
                account_verified = confirm_account(session, verify_url, verification_code)
                if account_verified:
                    display_account_info(user_data)
                else:
                    create_responsive_box(f"❌ Account verification failed for {user_data['username']}.", color=Colors.RED, border_color=Colors.RED)
            else:
                create_responsive_box(f"❌ Could not get verification code for {user_data['username']}.", color=Colors.RED, border_color=Colors.RED)
        else:
            create_responsive_box(f"❌ Account creation failed for {user_data['username']}.", color=Colors.RED, border_color=Colors.RED)
            
        time.sleep(3)
    
    print_progress_bar(num_accounts, num_accounts, prefix='Progress:', suffix='Complete')
    create_responsive_box("✅ Task completed!", color=Colors.GREEN, border_color=Colors.GREEN)
    input(f"{Colors.BOLD}Press Enter to return to the menu...{Colors.RESET}")

if __name__ == '__main__':
    main_menu()