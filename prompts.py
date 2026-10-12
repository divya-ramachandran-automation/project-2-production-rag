def build_answer_prompt(context, question, conversation_history=None):

    history_text = ""

    if conversation_history:
        history_lines = []

        for message in conversation_history:
            role = message["role"].capitalize()
            content = message["content"]
            history_lines.append(f"{role}: {content}")

        history_text = "\n".join(history_lines)

    prompt = f"""
You are a helpful company policy assistant.

Answer the user's latest question using the provided policy context.
Use the conversation history to understand follow-up questions and references.
Conversation history provides context, but policy facts must come only from
the retrieved policy context below.

Rules:
- Do not invent facts or policies.
- If the answer is not available in the policy context, clearly say that you do not have enough information.
- Keep the answer clear and relevant.

Conversation history:
{history_text if history_text else "No previous conversation."}

Retrieved policy context:
{context}

Latest question:
{question}

Answer:
"""

    return prompt

def build_standalone_question_prompt(question, conversation_history):

    history_text = ""

    if conversation_history:
        history_lines = []

        for message in conversation_history:
            role = message["role"].capitalize()
            content = message["content"]
            history_lines.append(f"{role}: {content}")

        history_text = "\n".join(history_lines)

    prompt = f"""
Rewrite the latest user question as a standalone question that can
be understood without conversation history.

Rules:
- Use conversation history only to resolve references such as "it",
  "that policy", or "those rules".
- Preserve the user's original intent.
- Do not answer the question.
- Do not add facts that are not present in the conversation.
- If the question is already standalone, keep its meaning unchanged.
- Return only the rewritten question.

Conversation history:
{history_text if history_text else "No previous conversation."}

Latest user question:
{question}

Standalone question:
"""

    return prompt