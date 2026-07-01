from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from transcript import fetch_transcript
from rag import create_chain

app = FastAPI(title="TubeMind")

# -----------------------------
# Static Files
# -----------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# -----------------------------
# Global Chain
# -----------------------------

chain = None


# -----------------------------
# Request Models
# -----------------------------

class VideoRequest(BaseModel):
    url: str


class ChatRequest(BaseModel):
    question: str


# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# -----------------------------
# Load Video
# -----------------------------

@app.post("/load-video")
async def load_video(data: VideoRequest):

    global chain

    transcript = fetch_transcript(data.url)

   

    chain = create_chain(transcript)

    video_id = data.url.split("v=")[1].split("&")[0]

    

    return {
    "status": "success",
    "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
}


# -----------------------------
# Chat
# -----------------------------

@app.post("/chat")
async def chat(data: ChatRequest):

    global chain

    if chain is None:
      return {
        "answer": "Please load a video first."
    }

    answer = chain.invoke(data.question)

    return {
     "answer": answer
}