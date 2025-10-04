[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-energy-drinks.svg)](https://forthebadge.com)

# 🐍 Mini Python Projects – Cyber Security Edition
  
This repository contains a collection of **small Python projects focused on cybersecurity and digital forensics**.  
Each project is simple, educational, and designed to improve your skills in **offensive and defensive security**. 

---

## 📋 Projects List

| #  | Project Name                        | Description                                 |
|----|-------------------------------------|---------------------------------------------|
| 1  | [secretscout](projects/secretscout) | Simple scanner for exposed secrets          |
| 2  | [siteanalyser](projects/siteanalyzer) |Website analyzer with crawling and reports |

> **Disclaimer**: These projects are for **educational purposes only**.  
Do not use them for unauthorized access or illegal activities.

---

## 🚀 How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/YourUsername/Mini_Python_Projects.git
   ```

2. Change into the repository:

   ```bash
   cd Mini_Python_Projects
   ```

3. (Optional but recommended) Create and activate a virtual environment:

   * macOS / Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   * Windows (PowerShell):

     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

4. Install dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

5. Enter a project folder and run the script:

   Example — Port Scanner:

   ```bash
   cd Project1_PortScanner
   python port_scanner.py target.example.com 1 1024
   ```

   Example — Password generator:

   ```bash
   cd ../Project2_PasswordGenerator
   python password_gen.py --length 16 --count 5
   ```

   > Tip: use `python3` instead of `python` on some systems if `python` points to Python 2.

6. If a script requires network/sniffing or low-level access (e.g., `scapy`), you may need elevated permissions:

   * Linux/macOS: `sudo python port_scanner.py ...`
   * Windows: run terminal as Administrator

