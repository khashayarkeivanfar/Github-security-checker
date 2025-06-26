# 🔍 GitHub Live Secret Scanner

This is a Python script that watches **live GitHub commits** in real time and checks if anything sensitive like **private keys, API tokens, passwords, or secrets** is accidentally exposed.

It's helpful if you're into security research, ethical hacking, or just want to build something useful around GitHub data.

---

##  What It Does

- Connects to GitHub’s public events (live feed)
- Checks every new commit pushed to public repos
- Scans the commit content for common secret patterns
- Flags anything that looks like a private key, token, or sensitive info

---

##  How to Use

1. **Clone the repo**  
   ```bash
   [git clone https://github.com/khashayarkeivanfar/Github-security-checker.git]
   cd Github-security-checker
   
2. **Install the requirements**  
   ```bash
   pip install -r requirements.txt
   
3. **Create a .env file in the root folder and add your GitHub token like this:**  
   ```ini
   GITHUB_TOKENS="PUT YOUR OWN GITHUB TOKEN"
   
4. **run it**  
   ```bash
   python scanner.py



