#!/bin/bash

# --- Vampire-Hub-X Installer Script ---
# This script automates the setup process for Vampire-Hub-X on Linux/macOS.

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[+] Starting Vampire-Hub-X Installation...${NC}"

# --- 1. Check for Git ---
echo -e "${YELLOW}[*] Checking for git...${NC}"
if ! command -v git &> /dev/null
then
    echo -e "${RED}[-] git is not installed. Attempting to install git...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install git -y
    elif command -v yum &> /dev/null; then
        sudo yum install git -y
    elif command -v dnf &> /dev/null; then
        sudo dnf install git -y
    elif command -v brew &> /dev/null; then # macOS Homebrew
        brew install git
    else
        echo -e "${RED}[-] Could not install git. Please install git manually and re-run the script.${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}[+] Git is installed.${NC}"

# --- 2. Check for Nmap (essential for port scanning) ---
echo -e "${YELLOW}[*] Checking for Nmap...${NC}"
if ! command -v nmap &> /dev/null
then
    echo -e "${RED}[-] Nmap is not installed. Attempting to install Nmap...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install nmap -y
    elif command -v yum &> /dev/null; then
        sudo yum install nmap -y
    elif command -v dnf &> /dev/null; then
        sudo dnf install nmap -y
    elif command -v brew &> /dev/null; then # macOS Homebrew
        brew install nmap
    else
        echo -e "${RED}[-] Could not install Nmap. Please install Nmap manually and re-run the script.${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}[+] Nmap is installed.${NC}"


# --- 3. Clone the repository (if not already cloned) ---
REPO_NAME="Vampire-Hub-XX"
if [ -d "$REPO_NAME" ]; then
    echo -e "${YELLOW}[*] Directory $REPO_NAME already exists. Skipping cloning.${NC}"
    cd "$REPO_NAME"
else
    echo -e "${YELLOW}[*] Cloning Vampire-Hub-X repository...${NC}"
    git clone https://github.com/vampiresquad/Vampire-Hub-XX.git
    if [ $? -ne 0 ]; then
        echo -e "${RED}[-] Failed to clone repository. Exiting.${NC}"
        exit 1
    fi
    cd "$REPO_NAME"
fi
echo -e "${GREEN}[+] Repository ready.${NC}"

# --- 4. Create and Activate Virtual Environment ---
echo -e "${YELLOW}[*] Setting up virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}[*] Virtual environment 'venv' already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[-] Failed to create virtual environment. Ensure python3-venv is installed or python3 is in PATH.${NC}"
        exit 1
    fi
fi

source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}[-] Failed to activate virtual environment. Exiting.${NC}"
    exit 1
fi
echo -e "${GREEN}[+] Virtual environment activated.${NC}"

# --- 5. Install Python dependencies ---
echo -e "${YELLOW}[*] Installing Python dependencies from requirements.txt...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}[-] Failed to install Python dependencies. Please check your internet connection or pip.${NC}"
        deactivate # Deactivate venv before exiting
        exit 1
    fi
    echo -e "${GREEN}[+] All Python dependencies installed.${NC}"
else
    echo -e "${RED}[-] requirements.txt not found! Cannot install Python dependencies.${NC}"
    deactivate # Deactivate venv before exiting
    exit 1
fi

# --- 6. Set execute permissions for the main script ---
echo -e "${YELLOW}[*] Setting execute permissions for main script...${NC}"
chmod +x Vampire_Hub_X.py
echo -e "${GREEN}[+] Permissions set.${NC}"

echo -e "${GREEN}\n[+] Vampire-Hub-X Installation Complete!${NC}"
echo -e "${YELLOW}----------------------------------------------------${NC}"
echo -e "${YELLOW}To run Vampire-Hub-X, navigate to its directory:${NC}"
echo -e "${GREEN}cd ${REPO_NAME}${NC}"
echo -e "${YELLOW}Then activate the virtual environment:${NC}"
echo -e "${GREEN}source venv/bin/activate${NC}"
echo -e "${YELLOW}And run the tool:${NC}"
echo -e "${GREEN}python Vampire_Hub_X.py${NC}"
echo -e "${YELLOW}----------------------------------------------------${NC}"

# Keep the virtual environment active for immediate use, or deactivate.
# For a user-friendly script, it's often better to leave it active and let them deactivate manually.
# For this guide, we'll suggest manual deactivation.
# deactivate # Uncomment this if you want to deactivate the venv automatically after install
