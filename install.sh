#!/bin/bash

# XploitRecon Installation Script
# By CtoXpLt_

set -e

COLORS_RED='\033[0;31m'
COLORS_GREEN='\033[0;32m'
COLORS_YELLOW='\033[1;33m'
COLORS_BLUE='\033[0;34m'
COLORS_CYAN='\033[0;36m'
COLORS_NC='\033[0m'

echo -e "${COLORS_CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║           XploitRecon Installation Script             ║
║                    By CtoXpLt_                        ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${COLORS_NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${COLORS_YELLOW}[!] This script should NOT be run as root${COLORS_NC}"
   echo -e "${COLORS_YELLOW}[!] Please run as a normal user${COLORS_NC}"
   exit 1
fi

echo -e "${COLORS_BLUE}[*] Starting installation...${COLORS_NC}\n"

# Check Python
echo -e "${COLORS_BLUE}[*] Checking Python installation...${COLORS_NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${COLORS_GREEN}[+] Python $PYTHON_VERSION found${COLORS_NC}"
else
    echo -e "${COLORS_RED}[!] Python 3 is not installed${COLORS_NC}"
    echo -e "${COLORS_YELLOW}[!] Please install Python 3.8 or higher${COLORS_NC}"
    exit 1
fi

# Check Go
echo -e "\n${COLORS_BLUE}[*] Checking Go installation...${COLORS_NC}"
if command -v go &> /dev/null; then
    GO_VERSION=$(go version | cut -d' ' -f3)
    echo -e "${COLORS_GREEN}[+] Go $GO_VERSION found${COLORS_NC}"
else
    echo -e "${COLORS_RED}[!] Go is not installed${COLORS_NC}"
    echo -e "${COLORS_YELLOW}[!] Installing Go...${COLORS_NC}"
    
    # Download and install Go
    GO_VERSION="1.21.0"
    wget -q "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz" -O /tmp/go.tar.gz
    sudo tar -C /usr/local -xzf /tmp/go.tar.gz
    rm /tmp/go.tar.gz
    
    # Add to PATH
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
    export PATH=$PATH:/usr/local/go/bin
    export PATH=$PATH:$HOME/go/bin
    
    echo -e "${COLORS_GREEN}[+] Go installed successfully${COLORS_NC}"
fi

# Ensure Go bin is in PATH
export PATH=$PATH:/usr/local/go/bin
export PATH=$PATH:$HOME/go/bin

# Install Subfinder
echo -e "\n${COLORS_BLUE}[*] Installing Subfinder...${COLORS_NC}"
if command -v subfinder &> /dev/null; then
    echo -e "${COLORS_GREEN}[+] Subfinder already installed${COLORS_NC}"
else
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    echo -e "${COLORS_GREEN}[+] Subfinder installed${COLORS_NC}"
fi

# Install HTTPx
echo -e "\n${COLORS_BLUE}[*] Installing HTTPx...${COLORS_NC}"
if command -v httpx &> /dev/null; then
    echo -e "${COLORS_GREEN}[+] HTTPx already installed${COLORS_NC}"
else
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
    echo -e "${COLORS_GREEN}[+] HTTPx installed${COLORS_NC}"
fi

# Install Nuclei
echo -e "\n${COLORS_BLUE}[*] Installing Nuclei...${COLORS_NC}"
if command -v nuclei &> /dev/null; then
    echo -e "${COLORS_GREEN}[+] Nuclei already installed${COLORS_NC}"
else
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
    echo -e "${COLORS_GREEN}[+] Nuclei installed${COLORS_NC}"
fi

# Update Nuclei templates
echo -e "\n${COLORS_BLUE}[*] Updating Nuclei templates...${COLORS_NC}"
nuclei -update-templates -silent
echo -e "${COLORS_GREEN}[+] Templates updated${COLORS_NC}"

# Make xploitrecon.py executable
echo -e "\n${COLORS_BLUE}[*] Setting up XploitRecon...${COLORS_NC}"
chmod +x xploitrecon.py
echo -e "${COLORS_GREEN}[+] XploitRecon is now executable${COLORS_NC}"

# Create results directory
mkdir -p results
echo -e "${COLORS_GREEN}[+] Results directory created${COLORS_NC}"

# Verify installations
echo -e "\n${COLORS_BLUE}[*] Verifying installations...${COLORS_NC}"
MISSING=0

if ! command -v subfinder &> /dev/null; then
    echo -e "${COLORS_RED}[✗] Subfinder not found${COLORS_NC}"
    MISSING=1
else
    echo -e "${COLORS_GREEN}[✓] Subfinder${COLORS_NC}"
fi

if ! command -v httpx &> /dev/null; then
    echo -e "${COLORS_RED}[✗] HTTPx not found${COLORS_NC}"
    MISSING=1
else
    echo -e "${COLORS_GREEN}[✓] HTTPx${COLORS_NC}"
fi

if ! command -v nuclei &> /dev/null; then
    echo -e "${COLORS_RED}[✗] Nuclei not found${COLORS_NC}"
    MISSING=1
else
    echo -e "${COLORS_GREEN}[✓] Nuclei${COLORS_NC}"
fi

echo ""

if [ $MISSING -eq 1 ]; then
    echo -e "${COLORS_YELLOW}[!] Some tools are missing. Please add Go bin to PATH:${COLORS_NC}"
    echo -e "${COLORS_YELLOW}    export PATH=\$PATH:\$HOME/go/bin${COLORS_NC}"
    echo -e "${COLORS_YELLOW}    Or run: source ~/.bashrc${COLORS_NC}"
else
    echo -e "${COLORS_GREEN}╔═══════════════════════════════════════════════════════╗${COLORS_NC}"
    echo -e "${COLORS_GREEN}║         Installation completed successfully!          ║${COLORS_NC}"
    echo -e "${COLORS_GREEN}╚═══════════════════════════════════════════════════════╝${COLORS_NC}"
    echo ""
    echo -e "${COLORS_CYAN}[*] Usage: ./xploitrecon.py -d example.com${COLORS_NC}"
    echo -e "${COLORS_CYAN}[*] Help:  ./xploitrecon.py --help${COLORS_NC}"
fi

echo ""
