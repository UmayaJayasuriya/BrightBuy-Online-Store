"""
Contact Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactOut

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("/", response_model=ContactOut, status_code=201)
def create_contact_message(contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Create a new contact message
    """
    try:
        db_contact = Contact(
            customer_name=contact.customer_name,
            email=contact.email,
            subject_name=contact.subject_name,
            message=contact.message
        )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save contact message: {str(e)}")


@router.get("/", response_model=list[ContactOut])
def get_all_contact_messages(db: Session = Depends(get_db)):
    """
    Get all contact messages (for admin purposes)
    """
    contacts = db.query(Contact).all()
    return contacts
