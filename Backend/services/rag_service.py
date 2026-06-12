from core.llm import gemini_model

def build_prompt(context: str, question: str) -> str:
    return f"""
You are a strict document AI assistant.

Rules:
- Answer ONLY using context
- If not found, say "Not found in document"
- Be concise and structured

Context:
{context}

Question:
{question}
"""

def get_answer(context: str, question: str):
    prompt = build_prompt(context, question)
    response = gemini_model.generate_content(prompt)
    return response.text