from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..repository.models import Contact
from ..repository.schemas import ContactCreate, ContactUpdate


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact(db: Session, contact_data: ContactCreate):
    new_contact = Contact(**contact_data.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def update_contact(db: Session, contact_id: int, contact_data: ContactUpdate):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    for key, value in contact_data.dict(exclude_unset=True).items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(contact)
    db.commit()


def search_contacts(db: Session, query: str):
    return (
        db.query(Contact)
        .filter(
            (Contact.first_name.ilike(f"%{query}%"))
            | (Contact.last_name.ilike(f"%{query}%"))
            | (Contact.email.ilike(f"%{query}%"))
        )
        .all()
    )


def get_birthdays_next_week(db: Session):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(Contact.birthday.between(today, next_week)).all()
