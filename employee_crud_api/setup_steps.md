# Django DRF Employee CRUD Setup

This repository contains the project in `employee_crud_api`.

## 1. Open a terminal in the repository root

```powershell
cd "D:\Zeddd IDE\Python"
```

## 2. Move into the project directory

```powershell
cd employee_crud_api
```

## 3. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in the current terminal and retry:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Or

# If using Gitbash

```gitbash
source .venv/Scripts/activate
```

## 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 5. Apply database migrations

```powershell
python manage.py migrate
```

## 6. Run automated API tests (optional)

```powershell
python manage.py test employees
```

## 7. Start the development server

```powershell
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/employees/`.

## CRUD endpoints

| Operation | Method | Endpoint |
| --- | --- | --- |
| List employees | `GET` | `/api/employees/` |
| Create employee | `POST` | `/api/employees/` |
| Retrieve employee | `GET` | `/api/employees/<id>/` |
| Fully update employee | `PUT` | `/api/employees/<id>/` |
| Partially update employee | `PATCH` | `/api/employees/<id>/` |
| Delete employee | `DELETE` | `/api/employees/<id>/` |

## Example create request

```powershell
$body = @{
  full_name = "Ada Lovelace"
  email = "ada@example.com"
  department = "Engineering"
  position = "Software Engineer"
  salary = "85000.00"
  hired_date = "2024-01-15"
  is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/employees/" -ContentType "application/json" -Body $body
```

## Optional: enable Django admin

```powershell
python manage.py createsuperuser
```

Then open `http://127.0.0.1:8000/admin/` and sign in.
