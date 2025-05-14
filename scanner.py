# scanner.py
import socket
import threading
import argparse
from queue import Queue

print_lock = threading.Lock()
q = Queue()

def scan_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            with print_lock:
                print(f"[+] Port {port} is OPEN")
    except:
        pass

def threader(host, timeout):
    while True:
        worker = q.get()
        scan_port(host, worker, timeout)
        q.task_done()

def parse_ports(option, port_list):
    if option == 'common':
        return [
            20, 21, 22, 23, 25, 53, 80, 110, 139,
            143, 443, 445, 3389, 8080
        ]
    elif option == 'full':
        return list(range(1, 65536))
    elif option == 'custom':
        ports = []
        try:
            for part in port_list.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    ports.extend(range(start, end + 1))
                else:
                    ports.append(int(part))
        except:
            print("[-] Invalid port format.")
            exit(1)
        return ports
    else:
        print("[-] Unknown port scan option.")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("host", help="Target IP or hostname")
    parser.add_argument("-m", "--mode", choices=["common", "full", "custom"], default="common",
                        help="Scan mode: common (default), full (1-65535), or custom")
    parser.add_argument("-p", "--ports", help="Custom ports, e.g. 22,80,1000-2000")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Socket timeout (seconds)")
    parser.add_argument("-th", "--threads", type=int, default=100, help="Number of threads")

    args = parser.parse_args()
    target = args.host

    print(f"\n Scanning {target} with mode: {args.mode}")
    if args.mode == "custom":
        if not args.ports:
            print("[-] You must specify ports with --ports when using custom mode.")
            exit(1)
        port_list = parse_ports("custom", args.ports)
    else:
        port_list = parse_ports(args.mode, args.ports)

    # Start threads
    for _ in range(args.threads):
        t = threading.Thread(target=threader, args=(target, args.timeout), daemon=True)
        t.start()

    # Queue ports
    for port in port_list:
        q.put(port)

    q.join()
    print("\n Scan complete.")

if __name__ == "__main__":
    main()
