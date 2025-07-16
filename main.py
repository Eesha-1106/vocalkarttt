from fastapi import FastAPI, UploadFile, Form
from firebase_service import add_product, get_inventory_alerts
from agents import (
    transcribe_voice, generate_description, categorize_product, detect_missing_fields,
    translate_text, get_market_insights, ai_chat_assistant
)
import uvicorn

app = FastAPI()

@app.post("/upload/")
async def upload_product(
    voice_input: UploadFile = None,
    text_input: str = Form(None),
    user_id: str = Form(...),
):
    if voice_input:
        text_input = await transcribe_voice(voice_input)

    missing_fields = detect_missing_fields(text_input)
    if missing_fields:
        return {"missing": missing_fields}

    desc = generate_description(text_input)
    category = categorize_product(text_input)
    translated = translate_text(text_input, target="en")

    product_data = {
        "user_id": user_id,
        "description": desc,
        "category": category,
        "input": text_input,
        "translated": translated
    }

    add_product(user_id, product_data)
    return {"status": "Product uploaded", "data": product_data}

@app.get("/inventory-alerts/{user_id}")
async def inventory_alerts(user_id: str):
    return get_inventory_alerts(user_id)

@app.get("/market-insights/")
async def market_insights():
    return get_market_insights()

@app.post("/ai-assistant/")
async def ai_assistant(prompt: str):
    return ai_chat_assistant(prompt)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
