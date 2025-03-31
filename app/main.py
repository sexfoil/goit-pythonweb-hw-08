from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Contact
from .crud import (
    get_contacts, get_contact, create_contact, update_contact, delete_contact, 
    search_contacts, get_birthdays_next_week
)
from .schemas import ContactCreate, ContactUpdate, ContactOut

# Ініціалізація FastAPI
app = FastAPI(title="Contacts API")

# Створення таблиць у базі даних
Base.metadata.create_all(bind=engine)

@app.post("/contacts/", response_model=ContactOut)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)

@app.get("/contacts/", response_model=list[ContactOut])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_contacts(db, skip, limit)

@app.get("/contacts/{contact_id}", response_model=ContactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=ContactOut)
def update_existing_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return update_contact(db, contact_id, contact)

@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact_entry(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    delete_contact(db, contact_id)
    return

@app.get("/contacts/search/")
def search_contact(query: str, db: Session = Depends(get_db)):
    return search_contacts(db, query)

@app.get("/contacts/birthdays/")
def birthdays_next_week(db: Session = Depends(get_db)):
    return get_birthdays_next_week(db)
