# 🔍 XploitRecon

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)

**Advanced Automated Reconnaissance Framework**

*Simple, Fast, and Effective Subdomain Discovery & Vulnerability Scanner*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Output](#-output) • [Screenshots](#-screenshots)

</div>

---

## 📖 About

XploitRecon is a powerful automated reconnaissance framework that chains three industry-standard tools to perform comprehensive security assessments:

1. **Subfinder** - Discovers all subdomains of a target domain
2. **HTTPx** - Filters and probes live hosts (HTTP 200 responses)
3. **Nuclei** - Scans for known vulnerabilities with customizable severity levels

### 🎯 Key Advantages

- ✅ **Simple Workflow** - Clean 3-step process
- ✅ **Organized Output** - Timestamped results in structured directories
- ✅ **Real-time Feedback** - Watch vulnerabilities as they're discovered
- ✅ **JSON Export** - Ready for automation and parsing
- ✅ **Flexible Severity** - Choose which vulnerability levels to scan
- ✅ **Reusable Data** - Save and reuse intermediate results

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Subdomain Enumeration** | Comprehensive subdomain discovery using multiple sources |
| **Live Host Detection** | Filter only responsive hosts with HTTP 200 status |
| **Vulnerability Scanning** | Automated scanning with 5000+ vulnerability templates |
| **Severity Filtering** | Focus on Critical, High, Medium, Low, or Info findings |
| **Real-time Display** | Watch scan progress and findings in real-time |
| **JSON Output** | Machine-readable JSON format for automation |
| **Organized Storage** | Timestamped results for easy tracking |
| **Summary Reports** | Automatic generation of scan summaries |

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Go 1.19 or higher
- Linux/Unix system

### Step 1: Install Go (if not installed)

```bash
# Download and install Go
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz

# Add to PATH
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### Step 2: Install Required Tools

```bash
# Install Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install HTTPx
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Install Nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Update Nuclei templates
nuclei -update-templates
```

### Step 3: Clone XploitRecon

```bash
git clone https://github.com/CtoXpLt_/XploitRecon.git
cd XploitRecon
chmod +x xploitrecon.py
```

### Verify Installation

```bash
./xploitrecon.py --help
```

---

## 🚀 Usage

### Basic Scan

```bash
python3 xploitrecon.py -d example.com
```

### Scan with Custom Severity

```bash
# Only Critical and High vulnerabilities
python3 xploitrecon.py -d example.com -s critical,high

# Only Critical vulnerabilities
python3 xploitrecon.py -d example.com -s critical

# All severity levels
python3 xploitrecon.py -d example.com -s critical,high,medium,low,info
```

### Custom Output Directory

```bash
python3 xploitrecon.py -d example.com -o /path/to/output
```

### Complete Example

```bash
python3 xploitrecon.py -d target.com -s critical,high -o ~/bug-bounty/scans
```

---

## 📊 Workflow

```
┌─────────────┐
│  Subfinder  │  Step 1: Discover subdomains
└──────┬──────┘
       │ subdomains.txt
       ▼
┌─────────────┐
│    HTTPx    │  Step 2: Filter live hosts (status 200)
└──────┬──────┘
       │ live_hosts.txt
       ▼
┌─────────────┐
│   Nuclei    │  Step 3: Scan for vulnerabilities
└──────┬──────┘
       │ vulnerabilities.json
       ▼
   📁 Results
```

---

## 📁 Output Structure

```
results/
└── example.com/
    └── 20251120_040000/
        ├── subdomains.txt          # All discovered subdomains
        ├── live_hosts.txt          # Live hosts with HTTP 200
        ├── vulnerabilities.json    # Found vulnerabilities (JSON)
        └── summary.txt             # Scan summary report
```

### Output Files

| File | Description |
|------|-------------|
| `subdomains.txt` | List of all discovered subdomains |
| `live_hosts.txt` | URLs of live hosts responding with HTTP 200 |
| `vulnerabilities.json` | Detailed vulnerability findings in JSON format |
| `summary.txt` | Quick overview of scan results |

---

## 🎨 Screenshots

### Scan in Progress
```
╔═══════════════════════════════════════════════════════╗
║              XploitRecon Framework v1.0               ║
║        Subfinder → HTTPx → Nuclei                     ║
║                  By CtoXpLt_                          ║
╚═══════════════════════════════════════════════════════╝

[*] Target Domain: example.com
[*] Output Directory: results/example.com/20251120_040000

[STEP 1] Subfinder - Subdomain Enumeration
============================================================
[+] Found: 45 subdomain(s)

[STEP 2] HTTPx - Filter Live Hosts (Status 200)
============================================================
[+] Found: 23 live host(s) with status 200
    ✓ https://www.example.com
    ✓ https://api.example.com
    ✓ https://admin.example.com

[STEP 3] Nuclei - Vulnerability Scanning
============================================================
[CRITICAL] SQL Injection Detected
    → https://admin.example.com/login.php

[HIGH] Cross-Site Scripting (XSS)
    → https://api.example.com/search

[MEDIUM] Information Disclosure
    → https://www.example.com/debug
```

---

## 📝 Command Line Options

```
usage: xploitrecon.py [-h] -d DOMAIN [-o OUTPUT] [-s SEVERITY]

XploitRecon - Simple Chain Scanner by CtoXpLt_

required arguments:
  -d, --domain DOMAIN    Target domain

optional arguments:
  -h, --help             Show this help message and exit
  -o, --output OUTPUT    Output directory (default: results)
  -s, --severity SEVERITY
                         Nuclei severity: critical,high,medium,low,info
                         (default: critical,high,medium)
```

---

## 🔧 Configuration

### Severity Levels

Choose which vulnerability severity levels to scan:

- `critical` - Critical vulnerabilities (RCE, SQLi, etc.)
- `high` - High-risk vulnerabilities
- `medium` - Medium-risk vulnerabilities
- `low` - Low-risk vulnerabilities
- `info` - Informational findings

### Examples

```bash
# Quick scan - Critical only
python3 xploitrecon.py -d target.com -s critical

# Balanced scan - Critical and High
python3 xploitrecon.py -d target.com -s critical,high

# Full scan - All levels
python3 xploitrecon.py -d target.com -s critical,high,medium,low,info
```

---

## ⚡ Performance Tips

### For Faster Scans

1. **Use specific severity levels**
   ```bash
   -s critical  # Fastest
   ```

2. **Scan during off-peak hours**
   - Less network congestion
   - Better response times

3. **Use screen/tmux for long scans**
   ```bash
   screen -S recon
   python3 xploitrecon.py -d target.com
   # Ctrl+A then D to detach
   ```

### Expected Scan Times

| Live Hosts | Estimated Time |
|-----------|---------------|
| 1-10 | 2-5 minutes |
| 10-20 | 5-10 minutes |
| 20-50 | 10-20 minutes |
| 50+ | 20-30+ minutes |

---

## 🛡️ Legal Disclaimer

**IMPORTANT:** This tool is provided for educational and ethical testing purposes only.

⚠️ **You must:**
- Have explicit permission to test target systems
- Comply with all applicable laws and regulations
- Respect bug bounty program rules and scope
- Not use this tool for malicious purposes

**The author is not responsible for any misuse or damage caused by this tool.**

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contribution

- [ ] Add progress bar for Nuclei scanning
- [ ] Implement parallel scanning for multiple domains
- [ ] Add Discord/Telegram notifications
- [ ] Create HTML/PDF report generation
- [ ] Add database support for scan history
- [ ] Implement resume functionality for interrupted scans

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**CtoXpLt_**

- GitHub: [@CtoXpLt_](https://github.com/CtoXplt)

---

## 🙏 Acknowledgments

Special thanks to the amazing tools that make XploitRecon possible:

- [Subfinder](https://github.com/projectdiscovery/subfinder) by ProjectDiscovery
- [HTTPx](https://github.com/projectdiscovery/httpx) by ProjectDiscovery  
- [Nuclei](https://github.com/projectdiscovery/nuclei) by ProjectDiscovery

---

## 📞 Support

If you found this tool helpful, please consider:

- ⭐ Starring this repository
- 🐛 Reporting bugs via [Issues](https://github.com/CtoXpLt_/XploitRecon/issues)
- 💡 Suggesting new features
- 📢 Sharing with the community

---

## 🔄 Changelog

### Version 1.0.0 (2025-11-20)
- Initial release
- Basic workflow: Subfinder → HTTPx → Nuclei
- JSON output support
- Real-time vulnerability display
- Severity filtering
- Organized output structure

---

<div align="center">

**Made with ❤️ by CtoXplt**

*Happy Hunting! 🎯*

</div>
