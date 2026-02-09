import json
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


api_key_=os.getenv("GROQ_API_KEY")
model_=os.getenv("groq_model")


def safe_json(text: str):
    if not text or not text.strip():
        return {
            "explanation": "LLM returned empty response.",
            "recommendation": "Retry or check LLM availability.",
            "recommended_offers": []
        }

    try:
        return json.loads(text)
    except Exception:
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            return json.loads(text[start:end])
        except Exception:
            return {
                "explanation": "Invalid LLM output.",
                "recommendation": text[:400],
                "recommended_offers": []
            }

def generate_explanation(result):
    llm = ChatGroq(
        api_key=api_key_,
        model=model_,
        temperature=0
    )

    system = SystemMessage(content="""
Return ONLY valid JSON.

Format:
{
 "explanation": "...",
 "recommendation": "...",
 "recommended_offers": ["...", "...", "..."]
}
""")

    human = HumanMessage(content=str(result))

    response = llm.invoke([system, human])
    return safe_json(response.content)
