conversation_history = []
MAX_MESSAGES = 10
def add_message(role, content):
    conversation_history.append({
        "role": role,
        "content": content
    })
    while len(conversation_history) > MAX_MESSAGES:
        conversation_history.pop(0)

def get_conversation_history():
    return conversation_history