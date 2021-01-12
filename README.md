## Installation

Clone repository

```bash
git clone git@github.com:missingpet/server.git
```

Change directory

```bash
cd server
```

Create virtual environment

```bash
python3 -m venv venv
```

Activate virtual environment

```bash
# Windows:
venv\Scripts\activate.bat

# Unix:
. venv/bin/activate
```

Install all dependencies

```bash
pip install -r requirements.txt
```

<a name="setup"></a>

## Setup

Migrate

```python
python manage.py migrate
```

Create superuser

```python
python manage.py createsuperuser
```

Run server

```python
python manage.py runserver
```
