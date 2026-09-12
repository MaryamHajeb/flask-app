# Flask MySQL Student API

A small, production-friendly Flask REST API for a React frontend. It provides JSON Student CRUD endpoints backed by MySQL through SQLAlchemy and PyMySQL.

## Features

- Flask application factory, API blueprints, and a responsive Student Management dashboard at `/`
- MySQL database access via Flask-SQLAlchemy + PyMySQL
- Student CRUD (`id`, `name`, `email`, `department`)
- CORS configured for local React/Vite development
- Environment-based configuration
- Request validation and consistent JSON errors
- WSGI entry point for deployment

## Project layout

```text
flask_mysql_student_api/
├── app/
│   ├── routes/students.py
│   ├── __init__.py
│   ├── errors.py
│   ├── extensions.py
│   ├── models.py
│   └── validators.py
├── .env
├── .env.example
├── config.py
├── database.sql
├── requirements.txt
├── run.py
└── wsgi.py
```

## Windows + XAMPP setup

1. Start **Apache** and **MySQL** from the XAMPP Control Panel.
2. Create the database and table. Open `http://localhost/phpmyadmin`, choose **SQL**, paste the contents of `database.sql`, then click **Go**. Alternatively, run the SQL in the MySQL command line.
3. In PowerShell, open this project folder and create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. Edit `.env` if your MySQL root account has a password or uses a different port. XAMPP commonly uses a blank root password.
5. Start the API:

   ```powershell
   python run.py
   ```

The API and dashboard will be available at `http://127.0.0.1:5000`. Open this address to manage students visually; the dashboard uses the API at `http://127.0.0.1:5000/api/students`.

## React CORS

The included `.env` allows `http://localhost:3000` (Create React App) and `http://localhost:5173` (Vite). Add your frontend origin as a comma-separated value if needed:

```dotenv
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Restart Flask after changing `.env`.

## API reference

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/health` | Service health check |
| GET | `/api/students` | List students |
| POST | `/api/students` | Create a student |
| GET | `/api/students/{id}` | Get one student |
| PUT | `/api/students/{id}` | Replace all student fields |
| PATCH | `/api/students/{id}` | Update supplied fields |
| DELETE | `/api/students/{id}` | Delete a student |

### Create a student

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/students `
  -ContentType 'application/json' `
  -Body '{"name":"Ada Lovelace","email":"ada@example.com","department":"Computer Science"}'
```

### Fetch all students

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/students
```

### Update a student

```powershell
Invoke-RestMethod -Method Patch -Uri http://127.0.0.1:5000/api/students/1 `
  -ContentType 'application/json' -Body '{"department":"Mathematics"}'
```

### Delete a student

```powershell
Invoke-WebRequest -Method Delete http://127.0.0.1:5000/api/students/1
```

## Request and error format

Create and update requests use JSON, for example:

```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "department": "Computer Science"
}
```

Successful responses wrap the resource in `data`. Validation and API errors are JSON, for example:

```json
{
  "error": {
    "message": "Validation failed.",
    "status": 400,
    "details": {"email": "Must be a valid email address."}
  }
}
```

## Production notes

- Set a strong, unique `SECRET_KEY` and real MySQL credentials in the deployment environment.
- Set `DATABASE_URL` to override the individual MySQL variables when your platform supplies one.
- Run behind a production WSGI server. On Linux, for example: `gunicorn wsgi:app`.
- Restrict `CORS_ORIGINS` to only your deployed frontend domain.
