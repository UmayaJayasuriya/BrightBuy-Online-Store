"""
Contact Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.contact import ContactCreate, ContactOut

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("/", response_model=ContactOut, status_code=201)
def create_contact_message(contact: ContactCreate, db=Depends(get_db)):
    """
    Create a new contact message
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        cursor.execute(
            "INSERT INTO contact (customer_name, email, subject_name, message) VALUES (%s, %s, %s, %s)",
            (contact.customer_name, contact.email, contact.subject_name, contact.message)
        )
        db.commit()
        contact_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM contact WHERE contact_id = %s", (contact_id,))
        new_contact = cursor.fetchone()
        cursor.close()
        
        return new_contact
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Failed to save contact message: {str(e)}")


@router.get("/", response_model=list[ContactOut])
def get_all_contact_messages(db=Depends(get_db)):
    """
    Get all contact messages (for admin purposes)
    """
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contact")
    contacts = cursor.fetchall()
    cursor.close()
    return contacts
