
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Literal

from database import get_db
from models import SupportTicket
from schemas import TicketCreate, TicketResponse


router = APIRouter(
    prefix="/tickets",
    tags=["Support Tickets"]
)


# 1. Create a new support ticket
@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db)
):
    new_ticket = SupportTicket(
        student_name=ticket_data.student_name,
        title=ticket_data.title,
        description=ticket_data.description,
        category=ticket_data.category
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# 2. Get tickets with status/category filters and pagination
@router.get("/", response_model=list[TicketResponse])
def get_tickets(
    status: str | None = Query(default=None),
    category: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(SupportTicket)

    allowed_statuses = ["Open", "In Progress", "Resolved"]

    if status:
        if status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail="Invalid status. Use Open, In Progress, or Resolved."
            )

        query = query.filter(
            SupportTicket.status == status
        )

    if category:
        query = query.filter(
            SupportTicket.category.ilike(category.strip())
        )

    return query.offset(skip).limit(limit).all()


# 3. Search tickets by student name, title, or description
@router.get("/search", response_model=list[TicketResponse])
def search_tickets(
    keyword: str = Query(min_length=2, max_length=100),
    db: Session = Depends(get_db)
):
    search_term = f"%{keyword.strip()}%"

    return db.query(SupportTicket).filter(
        (SupportTicket.student_name.ilike(search_term))
        | (SupportTicket.title.ilike(search_term))
        | (SupportTicket.description.ilike(search_term))
    ).all()


# 4. Allowed ticket status values
class TicketStatusUpdate(BaseModel):
    status: Literal["Open", "In Progress", "Resolved"]


# 5. Update support ticket status
@router.patch("/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    status_data: TicketStatusUpdate,
    db: Session = Depends(get_db)
):
    ticket = (
        db.query(SupportTicket)
        .filter(SupportTicket.id == ticket_id)
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.status = status_data.status

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket status updated successfully",
        "ticket_id": ticket.id,
        "status": ticket.status
    }
