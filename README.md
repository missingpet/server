# MissingPet Server

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) 

<a name=""></a>
# Table of contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)

<a name="requirements"></a>
# Requirements 
 
- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)
- [PostgreSQL](https://www.postgresql.org/download/)

<a name="installation"></a>
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

<a name="setup"></a>
# Setup

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
