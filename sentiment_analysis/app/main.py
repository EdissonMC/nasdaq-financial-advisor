from fastapi import FastAPI
from pydantic import BaseModel
from app.analysis import analyze_text
import app.models as models
import app.database as database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.post("/analyze")
def analyze(input: InputText):
    result = analyze_text(input.text)
    return {"text": input.text, **result}
