from backend.chat_memory import ChatMemory


class ConversationManager:

    def __init__(self):
        self.memory = ChatMemory()

    def add_message(self, user, assistant):
        self.memory.save_message(user, assistant)

    def get_history(self):
        return self.memory.load_history()

    def clear(self):
        self.memory.clear_history()

    def last_question(self):
        return self.memory.get_last_question()

    def last_answer(self):
        return self.memory.get_last_answer()

    def total_messages(self):
        return self.memory.total_messages()
