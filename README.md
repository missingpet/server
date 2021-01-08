# MissingPet Server

Backend for MissingPet project

# Requirements 
 
- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- [PostgreSQL](https://www.postgresql.org/download/)

# Installation

Clone repository
```bash
git clone git@github.com:MissingPet/server.git
```
Change directory
```bash
cd server/
```
Create virtual environment
```bash
python3 -m venv venv
```
Activate virtual environment
```bash
# Windows:
venv\Scripts\activate.bat

# On Unix or MacOS:
source venv/bin/activate
```
Install all dependencies
```bash
pip install -r requirements.txt
```

# Setup

Migrate

```python
python manage.py migrate
```
Create superuser

```python
python manage.py createsuperuser

E-email address: # enter your email address
Username: # enter your username
Password: # enter your password
Password (again): # enter your password again
```
Run server

```python
python manage.py runserver
```
