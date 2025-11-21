#!/usr/bin/env python3
"""
XploitRecon - Simple Chain Scanner
By CtoXpLt_

Workflow:
1. Subfinder → subdomains.txt
2. HTTPx (filter 200) → live_hosts.txt  
3. Nuclei → vulnerabilities.json
"""

import subprocess
import os
import sys
import argparse
from datetime import datetime
import json

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class XploitRecon:
    def __init__(self, domain, output_dir="results"):
        self.domain = self.clean_domain(domain)
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_directories()
        
    def clean_domain(self, domain):
        """Membersihkan domain dari protocol dan trailing slash"""
        domain = domain.replace('https://', '').replace('http://', '')
        domain = domain.rstrip('/')
        return domain
        
    def setup_directories(self):
        """Membuat direktori output"""
        self.domain_dir = os.path.join(self.output_dir, self.domain, self.timestamp)
        os.makedirs(self.domain_dir, exist_ok=True)
        
        # Define file paths
        self.subdomains_file = os.path.join(self.domain_dir, "subdomains.txt")
        self.live_hosts_file = os.path.join(self.domain_dir, "live_hosts.txt")
        self.vulnerabilities_file = os.path.join(self.domain_dir, "vulnerabilities.json")
        self.summary_file = os.path.join(self.domain_dir, "summary.txt")
    
    def print_banner(self):
        banner = f"""
{Colors.OKCYAN}
╔═══════════════════════════════════════════════════════╗
║              XploitRecon Framework v1.0               ║
║        Subfinder → HTTPx → Nuclei                     ║
║                  By CtoXpLt_                          ║
╚═══════════════════════════════════════════════════════╝
{Colors.ENDC}
{Colors.OKBLUE}[*] Target Domain: {self.domain}{Colors.ENDC}
{Colors.OKBLUE}[*] Output Directory: {self.domain_dir}{Colors.ENDC}
{Colors.OKBLUE}[*] Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{Colors.ENDC}
"""
        print(banner)
    
    def check_tools(self):
        """Memeriksa apakah tools yang diperlukan sudah terinstall"""
        tools = ['subfinder', 'httpx', 'nuclei']
        missing = []
        
        print(f"\n{Colors.HEADER}[*] Checking required tools...{Colors.ENDC}")
        for tool in tools:
            result = subprocess.run(['which', tool], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(f"{Colors.OKGREEN}[✓] {tool}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}[✗] {tool} not found{Colors.ENDC}")
                missing.append(tool)
        
        if missing:
            print(f"\n{Colors.FAIL}[!] Missing tools: {', '.join(missing)}{Colors.ENDC}")
            print(f"{Colors.WARNING}[!] Install: go install -v github.com/projectdiscovery/<tool>/v2/cmd/<tool>@latest{Colors.ENDC}")
            return False
        return True
    
    def step1_subfinder(self):
        """Step 1: Subfinder - Mencari subdomain"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}[STEP 1] Subfinder - Subdomain Enumeration{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        
        cmd = [
            'subfinder',
            '-d', self.domain,
            '-all',
            '-o', self.subdomains_file,
            '-silent'
        ]
        
        print(f"{Colors.OKBLUE}[*] Running: subfinder -d {self.domain} -all -o subdomains.txt{Colors.ENDC}")
        
        try:
            subprocess.run(cmd, check=True)
            
            # Hitung hasil
            if os.path.exists(self.subdomains_file):
                with open(self.subdomains_file, 'r') as f:
                    subdomains = [line.strip() for line in f if line.strip()]
                
                if len(subdomains) == 0:
                    print(f"{Colors.WARNING}[!] No subdomains found, using main domain{Colors.ENDC}")
                    with open(self.subdomains_file, 'w') as f:
                        f.write(f"{self.domain}\n")
                    subdomains = [self.domain]
                
                print(f"{Colors.OKGREEN}[+] Found: {len(subdomains)} subdomain(s){Colors.ENDC}")
                print(f"{Colors.OKGREEN}[+] Saved to: {self.subdomains_file}{Colors.ENDC}")
                
                # Tampilkan sample
                print(f"\n{Colors.OKBLUE}[*] Sample subdomains:{Colors.ENDC}")
                for sub in subdomains[:5]:
                    print(f"{Colors.OKBLUE}    • {sub}{Colors.ENDC}")
                if len(subdomains) > 5:
                    print(f"{Colors.OKBLUE}    ... and {len(subdomains)-5} more{Colors.ENDC}")
                
                return len(subdomains)
            else:
                print(f"{Colors.FAIL}[!] Failed to create subdomains file{Colors.ENDC}")
                return 0
                
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
            return 0
    
    def step2_httpx(self):
        """Step 2: HTTPx - Filter live hosts dengan status code 200"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}[STEP 2] HTTPx - Filter Live Hosts (Status 200){Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        
        cmd = [
            'httpx',
            '-l', self.subdomains_file,
            '-mc', '200',
            '-o', self.live_hosts_file,
            '-silent'
        ]
        
        print(f"{Colors.OKBLUE}[*] Running: httpx -l subdomains.txt -mc 200 -o live_hosts.txt{Colors.ENDC}")
        print(f"{Colors.WARNING}[*] Filtering only status code 200...{Colors.ENDC}")
        
        try:
            subprocess.run(cmd, check=True, timeout=300)
            
            # Hitung hasil
            if os.path.exists(self.live_hosts_file):
                with open(self.live_hosts_file, 'r') as f:
                    live_hosts = [line.strip() for line in f if line.strip()]
                
                if len(live_hosts) == 0:
                    print(f"{Colors.WARNING}[!] No live hosts with status 200 found{Colors.ENDC}")
                    return 0
                
                print(f"{Colors.OKGREEN}[+] Found: {len(live_hosts)} live host(s) with status 200{Colors.ENDC}")
                print(f"{Colors.OKGREEN}[+] Saved to: {self.live_hosts_file}{Colors.ENDC}")
                
                # Tampilkan sample
                print(f"\n{Colors.OKBLUE}[*] Live hosts:{Colors.ENDC}")
                for host in live_hosts[:10]:
                    print(f"{Colors.OKGREEN}    ✓ {host}{Colors.ENDC}")
                if len(live_hosts) > 10:
                    print(f"{Colors.OKBLUE}    ... and {len(live_hosts)-10} more{Colors.ENDC}")
                
                return len(live_hosts)
            else:
                print(f"{Colors.WARNING}[!] No live hosts file created{Colors.ENDC}")
                return 0
                
        except subprocess.TimeoutExpired:
            print(f"{Colors.WARNING}[!] HTTPx timeout after 5 minutes{Colors.ENDC}")
            return 0
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
            return 0
    
    def step3_nuclei(self, severity='critical,high,medium'):
        """Step 3: Nuclei - Vulnerability scanning"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}[STEP 3] Nuclei - Vulnerability Scanning{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        
        # Cek apakah ada live hosts
        if not os.path.exists(self.live_hosts_file):
            print(f"{Colors.WARNING}[!] No live hosts file found. Skipping Nuclei...{Colors.ENDC}")
            return 0
        
        with open(self.live_hosts_file, 'r') as f:
            hosts = [line.strip() for line in f if line.strip()]
        
        if len(hosts) == 0:
            print(f"{Colors.WARNING}[!] No hosts to scan. Skipping Nuclei...{Colors.ENDC}")
            return 0
        
        cmd = [
            'nuclei',
            '-l', self.live_hosts_file,
            '-severity', severity,
            '-json',
            '-o', self.vulnerabilities_file,
            '-stats'
        ]
        
        print(f"{Colors.OKBLUE}[*] Running: nuclei -l live_hosts.txt -severity {severity} -json -o vulnerabilities.json{Colors.ENDC}")
        print(f"{Colors.WARNING}[*] Severity filter: {severity}{Colors.ENDC}")
        print(f"{Colors.WARNING}[*] This may take several minutes...{Colors.ENDC}\n")
        
        try:
            # Run nuclei dengan real-time output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            vuln_count = 0
            critical_count = 0
            high_count = 0
            medium_count = 0
            low_count = 0
            
            # Process output real-time
            for line in process.stdout:
                line = line.strip()
                if line:
                    # Parse JSON vulnerability
                    try:
                        vuln = json.loads(line)
                        vuln_count += 1
                        
                        info = vuln.get('info', {})
                        severity_level = info.get('severity', 'unknown').upper()
                        name = info.get('name', 'Unknown')
                        host = vuln.get('host', vuln.get('matched-at', 'Unknown'))
                        
                        # Count by severity
                        if severity_level == 'CRITICAL':
                            critical_count += 1
                            color = Colors.FAIL
                        elif severity_level == 'HIGH':
                            high_count += 1
                            color = Colors.FAIL
                        elif severity_level == 'MEDIUM':
                            medium_count += 1
                            color = Colors.WARNING
                        elif severity_level == 'LOW':
                            low_count += 1
                            color = Colors.OKBLUE
                        else:
                            color = Colors.OKBLUE
                        
                        # Display finding
                        print(f"{color}[{severity_level}] {name}{Colors.ENDC}")
                        print(f"{Colors.OKBLUE}    → {host}{Colors.ENDC}\n")
                        
                    except json.JSONDecodeError:
                        # Not JSON, probably stats
                        if '[INF]' in line or 'Templates' in line:
                            print(f"{Colors.OKBLUE}[*] {line}{Colors.ENDC}")
            
            process.wait()
            
            # Summary
            if vuln_count > 0:
                print(f"\n{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
                print(f"{Colors.OKGREEN}[+] Vulnerability Summary:{Colors.ENDC}")
                if critical_count > 0:
                    print(f"{Colors.FAIL}    CRITICAL: {critical_count}{Colors.ENDC}")
                if high_count > 0:
                    print(f"{Colors.FAIL}    HIGH: {high_count}{Colors.ENDC}")
                if medium_count > 0:
                    print(f"{Colors.WARNING}    MEDIUM: {medium_count}{Colors.ENDC}")
                if low_count > 0:
                    print(f"{Colors.OKBLUE}    LOW: {low_count}{Colors.ENDC}")
                print(f"{Colors.OKGREEN}    TOTAL: {vuln_count}{Colors.ENDC}")
                print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
                print(f"\n{Colors.OKGREEN}[+] Saved to: {self.vulnerabilities_file}{Colors.ENDC}")
            else:
                print(f"\n{Colors.OKBLUE}[*] No vulnerabilities found{Colors.ENDC}")
            
            return vuln_count
            
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}[!] Scan interrupted by user{Colors.ENDC}")
            return 0
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")
            return 0
    
    def generate_summary(self, subdomain_count, live_host_count, vuln_count):
        """Generate scan summary"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}[*] Scan Summary{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        
        summary = f"""XploitRecon Scan Summary
{'='*60}

Target Domain: {self.domain}
Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Results:
--------
Subdomains Found: {subdomain_count}
Live Hosts (200): {live_host_count}
Vulnerabilities: {vuln_count}

Output Files:
-------------
Subdomains: {self.subdomains_file}
Live Hosts: {self.live_hosts_file}
Vulnerabilities: {self.vulnerabilities_file}

Scan Directory: {self.domain_dir}
"""
        
        with open(self.summary_file, 'w') as f:
            f.write(summary)
        
        print(f"{Colors.OKBLUE}[*] Domain: {self.domain}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Subdomains: {subdomain_count}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Live Hosts: {live_host_count}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Vulnerabilities: {vuln_count}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}[+] Summary saved to: {self.summary_file}{Colors.ENDC}")
    
    def run(self, severity='critical,high,medium'):
        """Run full scan"""
        self.print_banner()
        
        if not self.check_tools():
            sys.exit(1)
        
        # Step 1: Subfinder
        subdomain_count = self.step1_subfinder()
        if subdomain_count == 0:
            print(f"{Colors.FAIL}[!] No subdomains found. Exiting...{Colors.ENDC}")
            sys.exit(1)
        
        # Step 2: HTTPx
        live_host_count = self.step2_httpx()
        if live_host_count == 0:
            print(f"{Colors.WARNING}[!] No live hosts found. Skipping vulnerability scan...{Colors.ENDC}")
            self.generate_summary(subdomain_count, 0, 0)
            sys.exit(0)
        
        # Step 3: Nuclei
        vuln_count = self.step3_nuclei(severity)
        
        # Summary
        self.generate_summary(subdomain_count, live_host_count, vuln_count)
        
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}[✓] Scan completed successfully!{Colors.ENDC}\n")

def main():
    parser = argparse.ArgumentParser(
        description='XploitRecon - Simple Chain Scanner by CtoXpLt_',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic scan
  python3 xploitrecon.py -d example.com
  
  # Custom severity
  python3 xploitrecon.py -d example.com -s critical,high
  
  # Only critical
  python3 xploitrecon.py -d example.com -s critical
  
  # All severity levels
  python3 xploitrecon.py -d example.com -s critical,high,medium,low,info
  
  # Custom output directory
  python3 xploitrecon.py -d example.com -o /path/to/output

Workflow:
  Step 1: Subfinder → subdomains.txt
  Step 2: HTTPx (filter 200) → live_hosts.txt
  Step 3: Nuclei → vulnerabilities.json

Created by: CtoXpLt_
        """
    )
    
    parser.add_argument('-d', '--domain', 
                       required=True, 
                       help='Target domain')
    parser.add_argument('-o', '--output', 
                       default='results', 
                       help='Output directory (default: results)')
    parser.add_argument('-s', '--severity', 
                       default='critical,high,medium',
                       help='Nuclei severity: critical,high,medium,low,info (default: critical,high,medium)')
    
    args = parser.parse_args()
    
    scanner = XploitRecon(args.domain, args.output)
    scanner.run(args.severity)

if __name__ == '__main__':
    main()