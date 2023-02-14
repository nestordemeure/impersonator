
class Chat:
    """
    represent a chat
    """
    def __init__(self):
        self.history = []
    
    def add_message(self, speaker, message, verbose=False):
        """adds a message to the history"""
        if verbose:
            print(f"{speaker}: {message}")
        self.history.append((speaker,message))
    
    def get_last_message(self):
        """returns the latest message and its author"""
        return self.history[-1]

    def to_string(self, max_messages=10):
        """
        turns the last max_messages messages in the chat into a string
        """
        # truncate the chat history
        if len(self.history) > max_messages:
            chat_history = self.history[-max_messages:]
            result = "..."
        else:
            chat_history = self.history
            result = ""
        # assembles the chat
        for (speaker,message) in chat_history:
            result += f"{speaker}: {message}\n"
        return result
