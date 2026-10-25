
import os

import openai
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

router = APIRouter(
    prefix="/chat",
    tags=["AI Chatbot"]
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=500)


class ChatResponse(BaseModel):
    question: str
    answer: str


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key is not configured"
        )

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are a helpful college campus helpdesk assistant. "
                "Answer politely and clearly. "
                "Do not invent college-specific dates, fees, or policies. "
                "If the information is unknown, tell the student to "
                "contact the college administration."
            ),
            input=request.question
        )

        return {
            "question": request.question,
            "answer": response.output_text
        }

    except openai.APIStatusError as exc:
        print("OpenAI status:", exc.status_code)
        print("OpenAI error:", str(exc))

        raise HTTPException(
            status_code=502,
            detail=f"OpenAI API returned status {exc.status_code}"
        )

    except openai.APIConnectionError as exc:
        print("OpenAI connection error:", repr(exc))

        raise HTTPException(
            status_code=502,
            detail="Could not connect to OpenAI API"
        )

    except Exception as exc:
        print("Unexpected error:", repr(exc))

        raise HTTPException(
            status_code=500,
            detail="Unexpected server error; check terminal"
        )
