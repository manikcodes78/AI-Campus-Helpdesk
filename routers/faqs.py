
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import FAQ
from schemas import FAQCreate, FAQResponse

router = APIRouter(
    prefix="/faqs",
    tags=["FAQs"]
)


# 1. Create a new FAQ
@router.post("/", response_model=FAQResponse)
def create_faq(
    faq_data: FAQCreate,
    db: Session = Depends(get_db)
):
    new_faq = FAQ(
        question=faq_data.question,
        answer=faq_data.answer,
        category=faq_data.category
    )

    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)

    return new_faq


# 2. Get all FAQs or filter by category

# Get FAQs with category filter and pagination
@router.get("/", response_model=list[FAQResponse])
def get_faqs(
    category: str | None = Query(
        default=None,
        min_length=2,
        max_length=100
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(FAQ)

    if category:
        query = query.filter(
            FAQ.category.ilike(category.strip())
        )

    return query.offset(skip).limit(limit).all()



# 3. Search FAQs by question, answer, or category
# IMPORTANT: Keep this before /{faq_id}
@router.get("/search", response_model=list[FAQResponse])
def search_faqs(
    keyword: str = Query(
        min_length=2,
        max_length=100
    ),
    db: Session = Depends(get_db)
):
    search_term = f"%{keyword.strip()}%"

    results = db.query(FAQ).filter(
        (FAQ.question.ilike(search_term))
        | (FAQ.answer.ilike(search_term))
        | (FAQ.category.ilike(search_term))
    ).all()

    return results


# 4. Get one FAQ by ID
@router.get("/{faq_id}", response_model=FAQResponse)
def get_faq(
    faq_id: int,
    db: Session = Depends(get_db)
):
    faq = db.query(FAQ).filter(
        FAQ.id == faq_id
    ).first()

    if faq is None:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found"
        )

    return faq


# 5. Update an FAQ
@router.put("/{faq_id}", response_model=FAQResponse)
def update_faq(
    faq_id: int,
    faq_data: FAQCreate,
    db: Session = Depends(get_db)
):
    faq = db.query(FAQ).filter(
        FAQ.id == faq_id
    ).first()

    if faq is None:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found"
        )

    faq.question = faq_data.question
    faq.answer = faq_data.answer
    faq.category = faq_data.category

    db.commit()
    db.refresh(faq)

    return faq


# 6. Delete an FAQ
@router.delete("/{faq_id}")
def delete_faq(
    faq_id: int,
    db: Session = Depends(get_db)
):
    faq = db.query(FAQ).filter(
        FAQ.id == faq_id
    ).first()

    if faq is None:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found"
        )

    db.delete(faq)
    db.commit()

    return {"message": "FAQ deleted successfully"}
