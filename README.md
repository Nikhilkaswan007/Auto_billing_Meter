# Auto Billing Meter

An IoT-based project for an automatic electricity billing system. This project uses a Raspberry Pi with a PZEM-004T energy meter to measure electricity consumption and a Django web application to manage users, visualize data, and automate billing.
<iframe width="560" height="315" src="https://youtu.be/1Th8oZYvSRI" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Features

- **User Authentication:** Secure login and logout functionality for users and administrators.
- **Real-time Data Dashboard:** A comprehensive dashboard to visualize real-time energy consumption data, including voltage, current, power, and total energy.
- **Automated Billing:** Automatic generation of bills based on energy consumption.
- **Meter Management:** Interface for administrators to add and manage meters.
- **API:** A dedicated API to receive data from the IoT hardware.

## Technology Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript, Tailwind CSS
- **Database:** SQLite 3
- **Hardware:** Raspberry Pi, PZEM-004T v3.0 Energy Meter
- **Libraries:** `django-tailwind`, `python-dotenv`, and more.

## Project Setup and Installation

Follow these steps to get the project up and running on your local machine.

### 1. Prerequisites

Make sure you have the following installed:
- Python 3.x
- `pip` (Python package installer)
- Node.js and `npm`

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd Auto_billing_Meter/Res_meter/Res_Meter
```

### 3. Backend Setup

**a. Create and Activate Virtual Environment:**

- For Windows:
  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
- For macOS/Linux:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

**b. Install Python Dependencies:**

_A `requirements.txt` file should be present in the root directory. If not, you may need to generate it based on the project's dependencies._

```bash
pip install -r requirements.txt
```

**c. Configure Environment Variables:**

Create a `.env` file in the `Res_meter/Res_Meter` directory. You can copy the example below and replace the placeholder values.

```
# Django Project Environment Variables
SECRET_KEY="your-django-secret-key"
DEBUG=True
ALLOWED_HOSTS=*

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD="your-email-app-password"
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**d. Run Database Migrations:**

```bash
python manage.py migrate
```

**e. Create a Superuser:**

To access the Django admin panel, create a superuser account.

```bash
python manage.py createsuperuser
```
Follow the prompts to set up your username, email, and password.

### 4. Frontend Setup

Install the necessary Node.js packages for Tailwind CSS.

```bash
npm install
```

## Running the Application

You need to run two commands in separate terminals.

**1. Start the Django Development Server:**

```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000`.

**2. Start the Tailwind CSS Watcher:**

This command will watch for changes in your template files and automatically rebuild the CSS.

```bash
python manage.py tailwind start
```

## Hardware and API

The `Demo Res_pi code/` directory contains the Python scripts designed to run on the Raspberry Pi. This code is responsible for reading data from the PZEM-004T sensor and sending it to the Django application's API.

## License

This project is licensed under the terms of the license specified in the `LICENSE` file.
