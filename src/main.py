from fastapi import FastAPI, Body

from src.gemini_client import get_answer_from_gemini

app = FastAPI()


@app.get("/requests")
async def get_my_requests():
    return "Hello world"

@app.post("/requests")
async def send_prompt(
        prompt: str = Body(embed=True),
):
    answer = await get_answer_from_gemini(prompt)
    return {"data": answer}