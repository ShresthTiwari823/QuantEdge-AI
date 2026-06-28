import json
import os
from datetime import datetime


class ChatMemory:

    def __init__(self):

        self.file = "chat_history.json"

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:

                json.dump([], f)

    def load_history(self):

        with open(self.file, "r") as f:

            return json.load(f)

    def save_message(

        self,

        user,

        assistant

    ):

        history = self.load_history()

        history.append(

            {

                "timestamp": datetime.now().strftime(

                    "%d-%m-%Y %H:%M:%S"

                ),

                "user": user,

                "assistant": assistant

            }

        )

        with open(

            self.file,

            "w"

        ) as f:

            json.dump(

                history,

                f,

                indent=4

            )

    def clear_history(self):

        with open(

            self.file,

            "w"

        ) as f:

            json.dump(

                [],

                f

            )

    def get_last_question(self):

        history = self.load_history()

        if len(history) == 0:

            return None

        return history[-1]["user"]

    def get_last_answer(self):

        history = self.load_history()

        if len(history) == 0:

            return None

        return history[-1]["assistant"]

    def total_messages(self):

        return len(

            self.load_history()

        )

    def export_history(self):

        return self.load_history()