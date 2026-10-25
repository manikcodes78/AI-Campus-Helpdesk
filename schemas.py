
from pydantic import BaseModel, Field


class FAQCreate(BaseModel):
    question: str = Field(min_length=5, max_length=255)
    answer: str = Field(min_length=2)
    category: str = Field(min_length=2, max_length=100)


class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    category: str


from pydantic import Field


class TicketCreate(BaseModel):
    student_name: str = Field(min_length=2, max_length=100)
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    category: str = Field(min_length=2, max_length=100)


class TicketResponse(BaseModel):
    id: int
    student_name: str
    title: str
    description: str
    category: str
    status: str
