import json
from openai import OpenAI
import streamlit as st


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def analyze_public_document(text: str) -> dict:
    prompt = f"""
You are a policy and public communication analyst.

Your job is to simplify complex public documents, council updates, policy statements, funding decisions, and public communications into clear, structured insight for everyday residents.

Return STRICT JSON only. Do not include markdown. Do not include explanation outside JSON.

Use this exact JSON structure:

{{
  "simple_summary": "Explain the document in plain English for a normal resident.",
  "key_decisions": [
    "Decision 1",
    "Decision 2",
    "Decision 3"
  ],
  "risks": [
    "Risk 1",
    "Risk 2",
    "Risk 3"
  ],
  "public_impact": "Explain what this means for the local economy, jobs, services, public trust, or residents.",
  "what_it_means_for_residents": [
    "Point 1",
    "Point 2",
    "Point 3"
  ],
  "recommended_actions": [
    "Action 1",
    "Action 2",
    "Action 3"
  ]
}}

Be clear, concise, neutral, and practical.

Document:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a structured public document analyst. Always return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "simple_summary": "The AI response could not be parsed properly.",
            "key_decisions": [],
            "risks": [],
            "public_impact": content,
            "what_it_means_for_residents": [],
            "recommended_actions": []
        }