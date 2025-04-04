import socket
import sys

def hprint(text: str):
    with open(".\settings.txt", "r") as f:
        settings = f.read().strip()
    
    hackerMode = settings[1] == "1"

    if hackerMode:
        print(f"\033[32m{text}\033[0m")
    else:
        print(text)

def hinput(prompt: str):
    f = open(".\settings.txt", "r")
    settings = f.read().strip()
    f.close()
    hackerMode = settings[1] == "1"
    if hackerMode:
        return input(f"\033[32m{prompt}\033[0m")
    else:
        return input(prompt)

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.01)
        if s.connect_ex((ip, port)) == 0:
            print(f"\033[32m[+] Port {port} is open\033[0m")
        s.close()
    except:
        pass

def pscan(ip, maximum_scan):
    for port in range(1, maximum_scan + 1):
        scan_port(ip, port)

def main():
    if len(sys.argv) < 2:
        hprint("Usage: python script.py <IP>")
        hprint("Example: python script.py 192.168.1.1")
        sys.exit(1)
    
    ip = sys.argv[1]
    
    try:
        maximum_scan = int(hinput("\nEnter the port number to scan up to: "))
        
        if maximum_scan > 65535:
            hprint("Maximum amount of ports too high! Setting to 8080")
            maximum_scan = 8080
            
        hprint(f"\nScanning {ip} from port 1 to {maximum_scan}...\n")
        pscan(ip, maximum_scan)
        
    except ValueError:
        hprint("Error: Please enter a valid number")
        sys.exit(1)

if __name__ == "__main__":
    main()