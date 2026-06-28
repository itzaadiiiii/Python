# Flask Hello World

A simple Flask application that displays a Hello World page.

---

## Prerequisites

- Python 3.10 or later
- pip

Verify installation:

```bash
python --version
pip --version
```

---

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd flask-hello-world
```

Or simply navigate to the project directory if already downloaded.

---

## Step 2: Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

### Linux/macOS

```bash
python3 -m venv venv
```

---

## Step 3: Activate the Virtual Environment

### Windows (Command Prompt)

```cmd
venv\Scripts\activate
```

### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source venv/bin/activate
```

You should now see:

```
(venv)
```

before your terminal prompt.

---

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5: Run the Application

```bash
python app.py
```

Output:

```
* Running on http://127.0.0.1:5000
```

---

## Step 6: Open the Browser

Visit:

```
http://127.0.0.1:5000
```

You should see:

```
Hello World!
Welcome to your first Flask application.
```

---

## Project Structure

```
flask-hello-world/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

---

## Stop the Application

Press:

```
CTRL + C
```

---

## Deactivate the Virtual Environment

```bash
deactivate
```

---

## Install New Packages

Example:

```bash
pip install requests
```

Update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## Author

Flask Hello World Sample Application
