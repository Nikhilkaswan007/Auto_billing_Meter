# Auto Billing Meter ⚡
**An Open-Source IoT-based Automatic Electricity Billing System**

This project combines a **Raspberry Pi + PZEM-004T v3.0** energy meter with a **Django web dashboard** to monitor real-time electricity usage, manage multiple meters, generate professional PDF invoices automatically, and send them via email — all in one system.

Perfect for landlords, small housing societies, sub-metering, or learning full-stack IoT!

<p align="center">
  <a href="https://www.youtube.com/watch?v=1Th8oZYvSRI">
    <img src="https://img.youtube.com/vi/1Th8oZYvSRI/maxresdefault.jpg" 
         alt="Click to Watch Full Demo Video" 
         style="width:100%; max-width:850px; border-radius:16px; box-shadow: 0 15px 40px rgba(0,0,0,0.3); cursor:pointer; transition:transform 0.3s;"
         onmouseover="this.style.transform='scale(1.03)'"
         onmouseout="this.style.transform='scale(1)'">
  </a>
  <br>
  <sup><strong>▶ Click above to watch the full demo video (plays in lightbox)</strong></sup>
</p>

## ✨ Features
- Secure user authentication (login/logout)
- Real-time dashboard with voltage, current, power & energy graphs
- Automatic PDF invoice generation with custom rates
- One-click email invoice delivery
- Admin panel to add/manage meters
- REST API for IoT hardware data push
- Responsive design (works on mobile & desktop)
- Remote power monitoring (foundation for future relay control)

## 🛠 Technology Stack
| Layer         | Technology                                      |
|---------------|--------------------------------------------------|
| Backend       | Django (Python)                                  |
| Frontend      | HTML, Tailwind CSS, JavaScript                   |
| Database      | SQLite (production-ready with PostgreSQL swap)   |
| Hardware      | Raspberry Pi + PZEM-004T v3.0 Energy Monitor     |
| Communication | HTTP POST API (from Pi → Django)                 |
| Styling       | django-tailwind                                  |

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Node.js & npm
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/Auto_billing_Meter.git
cd Auto_billing_Meter/Res_meter/Res_Meter
```

### 3. Backend Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# or
.\.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file (see below)
cp .env.example .env

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Frontend (Tailwind CSS)
```bash
npm install
```

### 5. Run the Project
Open **two terminals**:

**Terminal 1** – Django server:
```bash
python manage.py runserver
```

**Terminal 2** – Tailwind watcher:
```bash
python manage.py tailwind start
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## ⚙ Hardware & IoT Integration
The `Demo Res_pi code/` folder contains the Python script that runs on the **Raspberry Pi**:
- Reads real-time data from PZEM-004T via serial
- Sends voltage, current, power, and energy to Django API every few seconds

> Future plan: Add relay control for remote disconnect (prepaid meter mode)

## 📧 Email Configuration (.env)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

---

<p align="center">
  <br><br>
  Made with ❤️ for the open-source and IoT community<br>
  <strong>Star this repo if you found it useful! ⭐</strong>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=1Th8oZYvSRI">📺 Watch Demo</a> • 
  <a href="">📖 Documentation</a> • 
  <a href="">🐞 Report Bug</a>
</p>
