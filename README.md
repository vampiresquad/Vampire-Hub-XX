# Vampire-Hub-X

[![GitHub license](https://img.shields.io/github/license/vampiresquad/Vampire-Hub-XX?style=flat-square)](https://github.com/vampiresquad/Vampire-Hub-XX/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/vampiresquad/Vampire-Hub-XX?style=flat-square)](https://github.com/vampiresquad/Vampire-Hub-XX/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/vampiresquad/Vampire-Hub-XX?style=flat-square)](https://github.com/vampiresquad/Vampire-Hub-XX/network/members)
[![GitHub issues](https://img.shields.io/github/issues/vampiresquad/Vampire-Hub-XX?style=flat-square)](https://github.com/vampiresquad/Vampire-Hub-XX/issues)
[![Python Version](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)](https://www.python.org/)

---

## 🧛‍♂️ Project Overview

**Vampire-Hub-X** is a powerful, multi-supported ethical hacking tool designed for penetration testers and cybersecurity professionals. Built with Python, it offers a robust suite of functionalities for information gathering and testing network resilience.

**Disclaimer:** This tool is intended *strictly for ethical and legal use only*. Any unauthorized access, malicious activities, or misuse of this tool is strictly prohibited and carries severe legal consequences. The developers are not responsible for any misuse. Use at your own risk and always ensure you have explicit, written authorization before conducting any tests.

---

## ✨ Features

Vampire-Hub-X comes packed with an intuitive, colorful, and menu-driven interface, ensuring a seamless experience.

* **Multi-Mode Access:**
    * **Normal User Mode:** Provides limited access to core features, perfect for general reconnaissance.
    * **Hidden Admin Mode:** Unlocks advanced, high-powerful functionalities. Accessible via a secure password.

* **Robust Information Gathering:**
    * **Whois Lookup:** Retrieve domain registration details.
    * **DNS Lookup:** Query A, MX, NS records for comprehensive domain information.
    * **IP Geolocation:** Pinpoint the geographical location of IP addresses or domains.
    * **Port Scanning (Nmap Integration):** Conduct thorough port scans using Nmap for identifying open ports and services.
    * **Subdomain Enumeration:** Discover hidden subdomains associated with a target.

* **DDoS Attack Simulation (Ethical Use Only):**
    * **SYN Flood:** Simulate SYN floods (for authorized stress testing environments).
    * **HTTP Flood:** Perform HTTP request floods to test web server resilience.
    * **UDP Flood (Under Development):** Future support for UDP-based attacks.

* **Enhanced User Experience:**
    * **Colorful & Advanced UI:** Utilizes `rich` and `colorama` for a beautiful, responsive terminal interface.
    * **Slow Writing Effect:** Engaging text display for banners and disclaimers.
    * **Hidden Password Input:** Ensures secure entry of sensitive credentials (Master & Admin passwords).

* **Reliability & Stability:**
    * **Automatic Dependency Installation:** Automatically checks and installs required Python libraries from `requirements.txt`.
    * **Advanced Error Handling:** Comprehensive `try-except` blocks to gracefully handle errors, log issues, and provide user-friendly feedback.
    * **Auto-Fixing Logic (for common issues):** Designed to automatically resolve common environment setup problems.

---

## 🚀 Installation & Setup

Follow these simple steps to get Vampire-Hub-X up and running on your system.

**Prerequisites:**

* **Python 3.x:** Ensure Python 3 and `pip` are installed and in your system's PATH.
* **Git:** Required to clone the repository.
* **Nmap:** Essential for the Port Scanning feature.
    * **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install nmap git -y`
    * **Linux (Fedora/CentOS):** `sudo dnf install nmap git -y`
    * **macOS (with Homebrew):** `brew install nmap git`
    * **Windows:** Download installer from [nmap.org/download.html](https://nmap.org/download.html). Ensure "Add to PATH" is selected during installation.

**Installation Steps (Linux/macOS recommended):**

1.  **Clone the Repository:**
    Navigate to the directory where you want to save the tool, then run:
    ```bash
    git clone [https://github.com/vampiresquad/Vampire-Hub-XX.git](https://github.com/vampiresquad/Vampire-Hub-XX.git)
    cd Vampire-Hub-XX
    ```

2.  **Make `install.sh` Executable & Run:**
    The `install.sh` script automates dependency installation and setup.
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
    * **Note:** The script may ask for your `sudo` password to install system packages like `git` and `nmap`.

    **For Windows Users:**
    Currently, there is no direct `install.bat` provided. You will need to:
    * Manually install Python 3.x, Git, and Nmap (ensure they are added to PATH).
    * Open PowerShell/CMD in the cloned `Vampire-Hub-XX` directory.
    * Create and activate a virtual environment: `python -m venv venv` then `.\venv\Scripts\activate`
    * Install Python dependencies: `pip install -r requirements.txt`

---

## 🏃‍♀️ How to Run

After successful installation:

1.  **Navigate to the Tool Directory:**
    ```bash
    cd Vampire-Hub-XX
    ```

2.  **Activate Virtual Environment (if not already active):**
    ```bash
    source venv/bin/activate  # On Linux/macOS
    # .\venv\Scripts\activate  # On Windows PowerShell
    ```

3.  **Run the Tool:**
    ```bash
    python Vampire_Hub_X.py
    ```

    You will be prompted to enter the **Master Password**: `VampireX`
    For **Admin Mode**, the password is: `SH404`

---

## 📦 Building an Executable (Advanced)

For easier distribution, you can create a standalone executable using `PyInstaller`.
(Note: You will need to temporarily comment out `check_and_install_dependencies()` in `Vampire_Hub_X.py` before building, as PyInstaller bundles all dependencies.)

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Navigate to the main tool directory:**
    ```bash
    cd Vampire-Hub-XX
    ```
3.  **Build the executable:**
    ```bash
    pyinstaller Vampire_Hub_X.py --onefile --name Vampire-Hub-X-Secure
    ```
    The executable will be generated in the `dist/` directory.

---

## ⚠️ Ethical Usage & Disclaimer

Vampire-Hub-X is developed *solely for educational purposes and authorized penetration testing*. The powerful features included (especially DDoS capabilities) must be used with extreme caution and only against systems for which you have explicit, written permission from the owner.

**Any unauthorized use of this tool against any system is illegal and unethical.** The developers hold no responsibility for any misuse or damage caused by this tool.

---

## 🤝 Contributing

We welcome contributions! If you have suggestions for new features, improvements, or bug fixes, feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeatureName`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/YourFeatureName`).
6.  Open a Pull Request.

---

## 🐞 Bug Reporting

If you encounter any bugs or issues, please report them on the [Issues page](https://github.com/vampiresquad/Vampire-Hub-XX/issues). Provide a detailed description of the problem, including steps to reproduce it and any error messages you receive.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💖 Support the Project

If you find Vampire-Hub-X useful, consider giving it a star on GitHub! ⭐

---
