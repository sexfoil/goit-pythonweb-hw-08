from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.repository.database import engine, Base, get_db
from app.repository.models import Contact
from app.services.crud import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_birthdays_next_week,
)
from app.repository.schemas import ContactCreate, ContactUpdate, ContactOut


router = APIRouter()
Base.metadata.create_all(bind=engine)


def get_existing_contact(contact_id: int, db: Session = Depends(get_db)) -> Contact:
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.post("/contacts/", response_model=ContactOut)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)


@router.get("/contacts/", response_model=list[ContactOut])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_contacts(db, skip, limit)


@router.get("/contacts/{contact_id}", response_model=ContactOut)
def read_contact(db_contact: Contact = Depends(get_existing_contact)):
    return db_contact


@router.put("/contacts/{contact_id}", response_model=ContactOut)
def update_existing_contact(
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    db_contact: Contact = Depends(get_existing_contact),
):
    return update_contact(db, db_contact.id, contact)


@router.delete("/contacts/{contact_id}", status_code=204)
def delete_contact_entry(
    db: Session = Depends(get_db), db_contact: Contact = Depends(get_existing_contact)
):
    delete_contact(db, db_contact.id)
    return


@router.get("/contacts/search/")
def search_contact(query: str, db: Session = Depends(get_db)):
    return search_contacts(db, query)


@router.get("/contacts/birthdays/")
def birthdays_next_week(db: Session = Depends(get_db)):
    return get_birthdays_next_week(db)
