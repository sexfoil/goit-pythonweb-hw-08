# goit-pythonweb-hw-08
Home work in scope of "Fullstack Web Development with Python" module

## Project structure
```
contacts_api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── crud.py
│   ├── main.py
├── migrations/
```

## Install
```
pip install fastapi sqlalchemy psycopg2 pydantic uvicorn
```

## Run
```
uvicorn app.main:app --reload
```

## Usage
```
http://127.0.0.1:8000/docs 
```

