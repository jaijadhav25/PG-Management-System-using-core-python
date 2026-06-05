# 🏠 PG Management System

A Python-based console application to manage a Paying Guest (PG) accommodation. It supports two roles — **Admin** and **User** — with features for room management, payments, complaints, and more.

---

## 📁 Project Structure

```
PG Management system/
│
├── main.py               # Entry point — handles login for Admin & User
├── admin.py              # Admin dashboard and menu
├── person.py             # User/Person model and profile
├── userManage.py         # Add, update, delete users
├── roomManage.py         # Room allocation and management
├── paymentManage.py      # Payment tracking
├── complaintManage.py    # Complaint registration and resolution
│
└── Data/
    ├── login.json        # Admin credentials (hashed) — not tracked by git
    ├── user.json         # Tenant data — not tracked by git
    ├── room.json         # Room details
    ├── payment.json      # Payment records
    └── user_complaint.json  # Complaint records
```

---

## ⚙️ Requirements

- Python 3.x (no external libraries required — uses only standard library)

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/PG-Management-System.git
   cd PG-Management-System
   ```

2. Set up the data files (see below).

3. Run the application:
   ```bash
   python main.py
   ```

---

## 🔧 Setup Data Files

The `Data/login.json` and `Data/user.json` files are not included in the repo for privacy reasons.  
Create them manually before running:

**`Data/login.json`** — Admin credentials (passwords stored as MD5 hash):
```json
[
    {"admin": "your_md5_hashed_password_here"}
]
```

**`Data/user.json`** — Tenant data (initially empty):
```json
[]
```

> 💡 You can generate an MD5 hash using Python:
> ```python
> import hashlib
> print(hashlib.md5("your_password".encode()).hexdigest())
> ```

---

## 👤 Features

### Admin
- Manage rooms (add, update, delete, view)
- Manage users/tenants
- View and resolve complaints
- Track payments
- Add new admin accounts

### User
- View room and bed details
- Register complaints
- Check payment status

---

## 📝 Notes

- Passwords are stored as MD5 hashes.
- All data is stored locally in JSON files inside the `Data/` folder.

---

## 🙋 Author

**Your Name**  
[GitHub Profile](https://github.com/your-username)
