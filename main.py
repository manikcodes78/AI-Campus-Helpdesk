
from fastapi import FastAPI
from database import Base, engine
import models
from routers.faqs import router as faqs_router
from routers.tickets import router as tickets_router
from routers.chatbot import router as chatbot_router
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import FAQ, SupportTicket
app = FastAPI(
    title="AI Campus Helpdesk API",
    description="A helpdesk API for college students",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)
app.include_router(faqs_router)
app.include_router(tickets_router)
app.include_router(chatbot_router)

@app.get("/")
def home():
    return {
        "message": "AI Campus Helpdesk API is running!",
        "status": "success"
    }


@app.get("/dashboard/stats", tags=["Dashboard"])
def dashboard_stats(db: Session = Depends(get_db)):
    total_faqs = db.query(FAQ).count()

    total_tickets = db.query(SupportTicket).count()

    open_tickets = db.query(SupportTicket).filter(
        SupportTicket.status == "Open"
    ).count()

    in_progress_tickets = db.query(SupportTicket).filter(
        SupportTicket.status == "In Progress"
    ).count()

    resolved_tickets = db.query(SupportTicket).filter(
        SupportTicket.status == "Resolved"
    ).count()

    return {
        "total_faqs": total_faqs,
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "resolved_tickets": resolved_tickets
    }
