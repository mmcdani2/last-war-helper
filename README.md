
# 🚂 Last War Helper

**Last War Helper** is a mobile-friendly Flask app designed to help alliance leaders and players in *Last War* manage VIP train picks fairly and efficiently.

Built for functionality first, this app uses a Supabase backend and offers customizable picker tools, VIP logic, and optional language support.

---

## 🌟 Features

- ✅ User registration and login
- 🚂 Contestant picker (no repeats within 7 days)
- 🛡️ Defender picker for VIP users
- 📜 Supabase integration (users, picks, defenders)
- 📱 Mobile-first Tailwind UI
- 💡 Optional animated spin wheel
- 🔒 Session-based authentication

---

## 📁 Project Structure

```
last-war-helper/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # All routes (login, register, picker)
│   ├── templates/           # HTML templates (Jinja2)
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── picker.html
│   └── static/              # Custom CSS/JS (optional)
├── .env                     # Supabase keys and Flask secret
├── run.py                   # App entry point
├── requirements.txt         # Python dependencies
└── README.md                # You are here
```

---

## 🔧 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/last-war-helper.git
cd last-war-helper
```

### 2. Set Up Environment
Create a `.env` file:
```
SUPABASE_URL=your-url
SUPABASE_KEY=your-anon-key
SECRET_KEY=changeme
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python run.py
```

Open the browser at `http://localhost:5000` or your Codespaces port preview.

---

## 🧪 Supabase Tables (Minimum Required)

### `users`
- `username` (text, unique)
- `password` (text)
- `server` (text)
- `alliance` (text)
- `vip` (boolean)

### `picks`
- `name` (text)
- `role` (text) — `"contestant"` or `"defender"`
- `picked_on` (timestamp)

### `defenders`
- `name` (text)
- `power` (int, optional)

---

## 📌 To-Do (Upcoming Features)

- Pick confirmation before saving
- Pick history view
- Admin-only tools (clear/reset picks)
- Language selector (Spanish, Portuguese, Korean, Indonesian)
- Password hashing + security upgrades

---

## 📃 License

MIT — Use it, fork it, build on it.
