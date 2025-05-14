Python Port Scanner

This is a simple multithreaded port scanner written in Python.

Disclaimer
Only scan hosts you own or are authorized to test. Unauthorized scanning is illegal and unethical.

 Usage
`bash
python scanner.py

Scan Options

| Option           | Description                                    |
|------------------|------------------------------------------------|
| `--mode`         | Scan mode: `common`, `full`, or `custom`      |
| `--ports`        | Custom ports list, e.g. `22,80,1000-2000`      |
| `--timeout`      | Socket timeout in seconds (default: 1.0)       |
| `--threads`      | Number of worker threads (default: 100)        |

Examples

`bash
python scanner.py 192.168.1.1
python scanner.py 192.168.1.1 --mode full
python scanner.py 192.168.1.1 --mode custom --ports 22,80,443,1000-1010

