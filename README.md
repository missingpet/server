# MissingPet Server
Backend for MissingPet project

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
Run server

```python
python manage.py runserver
```
