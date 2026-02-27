# NetGuard

NetGuard is a Django-based firewall management and security monitoring project I built on an Ubuntu Server lab environment.

The goal of this project was to integrate Linux `iptables` with a web-based control panel and simulate basic SOC-style monitoring workflows.

---

## What NetGuard Does

- Allows IP banning and unbanning from a Django admin interface
- Automatically updates `iptables` rules
- Syncs banned IPs with a local JSON store (`bans.json`)
- Models security alerts and assets inside Django
- Implements basic role-based access control

This project was developed and tested inside a VirtualBox Ubuntu Server environment.

---

## Architecture Overview

Detection scripts → `bans.json` → Django backend → iptables rules

The system separates:

- Core detection logic (Python scripts)
- Firewall enforcement (iptables)
- Administrative control (Django)
- Persistent state (JSON + database models)

---

## Tech Stack

- Python 3.12
- Django
- Linux iptables
- Ubuntu Server
- VirtualBox
- Git

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/netguard.git
cd netguard
```

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Django backend:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Important

This project executes `iptables` commands.  
To allow firewall modification from Django, configure sudo permissions properly:

```
netguard ALL=(ALL) NOPASSWD: /usr/sbin/iptables
```

Use carefully in production environments.

---

## Why I Built This

I built NetGuard to better understand:

- How backend systems interact with Linux firewall rules
- Secure privilege handling
- Role-based access control
- State synchronization between file-based and database storage
- Designing a security-focused backend architecture

---

## Author

Vishnu Palakkottu  
Cybersecurity | SOC | Python
