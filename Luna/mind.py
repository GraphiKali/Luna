import re


class Mind:
    def __init__(self):
        self.thoughts = "none"
        self.emotions = []
        self.stress_level = 0

        self.goal = "none"
        self.current_step = "none"

        self.desires_to_continue = 0

        self.search_query = "none"

    def get_thoughts(self):
        return self.thoughts

    def get_emotions(self):
        return self.emotions

    def get_stress_level(self):
        return self.stress_level

    def get_goal(self):
        return self.goal

    def get_desire_to_continue(self):
        return self.desires_to_continue

    def set_thoughts(self, thoughts):
        self.thoughts = thoughts

    def set_emotions(self, emotions):
        self.emotions = emotions

    def set_stress_level(self, level):
        self.stress_level = level

    def populate_from_message(self, message):
        message_lines = message.split("\n")
        pattern = r"\[(.*?)\]\: (.*?)"
        for line in message_lines:
            match = re.match(pattern, line)
            if match:
                cat, _ = match.groups()
                if cat.lower() == "thoughts":
                    self.thoughts = line.replace(f"[{cat}]: ", "")
                elif cat.lower() == "emotions":
                    self.emotions = line.replace(f"[{cat}]: ", "")
                elif cat.lower() == "stress":
                    self.stress_level = int(line.replace(f"[{cat}]: ", ""))
                elif cat.lower() == "continue":
                    self.desires_to_continue = int(line.replace(f"[{cat}]: ", ""))
            else:
                pass
                # print(line)

    def __str__(self):
        to_return = f"[Thoughts]: {self.thoughts}\n" \
                    f"[Emotions]: {self.emotions}\n" \
                    f"[Stress]: {self.stress_level}\n" \
                    f"[Goal]: {self.goal}\n" \
                    f"[Step]: {self.current_step}\n" \
                    f"[Continue]: {self.desires_to_continue}"
        return to_return
