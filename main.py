from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env file se API key load karna
load_dotenv()

# Gemini AI configure karna
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

# FastAPI app initialize karna
app = FastAPI(title="AI Humanizer API")

# CORS Setup - Sirf specific domains ko allow karna for security
origins = [
    "http://127.0.0.1:5500",      
    "http://localhost:3000",      
    "https://nexussolver.in",     
    "https://www.nexussolver.in"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Data Structure define karna
class TextRequest(BaseModel):
    text: str
    tone: str = "Natural & Human-like" 

@app.get("/")
def home():
    return {"message": "AI Humanizer API is running perfectly!"}

@app.post("/humanize")
async def humanize_text(request: TextRequest):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # SMART PROMPT - Jo AI ke saare nakhre theek kar dega
        # SMART PROMPT 2.0 - Context-Aware Logic Ke Sath
        prompt = f"""
        You are an expert AI text humanizer. Your job is to rewrite the provided text to make it sound 100% human-written. 
        
        You MUST strictly obey these rules:
        1. EXACT LANGUAGE & SCRIPT: You MUST reply in the EXACT SAME LANGUAGE and SCRIPT as the input. 
           - If the input is in "Hinglish" or "Roman Urdu" (Hindi/Urdu written in English alphabets), your output MUST also be in Hinglish/Roman Urdu.
           - DO NOT translate the text into pure English. DO NOT use Devanagari or Arabic scripts.
        2. CONTEXT-AWARE LENGTH (SMART SIZING): Analyze the core message and intent of the text. Let the context dictate the exact length. 
           - Do NOT artificially inflate short paragraphs with unnecessary fluff just to increase word count. 
           - Do NOT ruthlessly cut down detailed explanations. 
           - Keep the length natural and proportional to the original (roughly within +/- 15% of the original word count). Prioritize a natural, human-like flow over strict mathematical word counting.
        3. TONE MATCHING: Apply the requested tone: **{request.tone}**.
        4. HUMAN TOUCH: Add burstiness (mix short and long sentences naturally) and perplexity. Make it sound conversational, slightly imperfect, and emotionally engaging. Remove robotic AI transition words (like "Furthermore", "In conclusion", "Moreover").

        Text to humanize:
        {request.text}
        """
        
        response = model.generate_content(prompt)
        
        return {
            "status": "success",
            "original_text": request.text,
            "selected_tone": request.tone,
            "humanized_text": response.text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Note: Render par ise run karne ke liye start command hogi: uvicorn main:app --host 0.0.0.0 --port 10000