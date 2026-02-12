import json
import os
import re
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("groq_model")


def clean_markdown(text: str):
    """
    Remove ```json markdown wrappers if present
    """
    if text.startswith("```"):
        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)
    return text.strip()


def extract_json(text: str):
    """
    Extract JSON object from any surrounding text
    """
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return text[start:end]
    except ValueError:
        return None


def safe_json(text: str):
    if not text or not text.strip():
        return {
            "explanation": "LLM returned empty response.",
            "recommendation": "Retry or check LLM availability.",
            "recommended_offers": []
        }

    text = clean_markdown(text)

    try:
        return json.loads(text)
    except Exception:
        pass

    extracted = extract_json(text)
    if extracted:
        try:
            return json.loads(extracted)
        except Exception:
            pass

    return {
        "explanation": "Unable to parse LLM response.",
        "recommendation": text[:500],
        "recommended_offers": []
    }


def generate_explanation(result):

    if not api_key:
        return {
            "explanation": "LLM disabled.",
            "recommendation": "Set GROQ_API_KEY to enable.",
            "recommended_offers": []
        }

    llm = ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=0
    )

    system = SystemMessage(content="""
You are a churn analysis assistant.

Respond with STRICT JSON only.
Do NOT include markdown.
Do NOT include backticks.
Do NOT repeat input.

Format:
{
  "explanation": "Explain churn decision clearly.",
  "recommendation": "What action should business take?",
  "recommended_offers": ["offer1", "offer2", "offer3"]
}
""")

    human = HumanMessage(content=f"""
Customer prediction details:

Prediction: {result["prediction"]}
Probability: {result["probability"]}%
""")

    response = llm.invoke([system, human])

    return safe_json(response.content)


# This is TOP SHAP Factor its display the values on the all fields
# This was need in futher to keep in the "human" prompt after probability
# Top SHAP factors: {sorted(result["shap"].items(), key=lambda x: abs(x[1]), reverse=True)[:5]}