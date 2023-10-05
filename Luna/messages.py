import pickle


class Messages:
    def __init__(self):
        with open("guide.txt", "r") as guide:
            self.data = [{"role": "system", "content": guide.read()}]

        self.length = 0

    def insert(self, role, content):
        self.data.append({"role": role,
                          "content": content})

        self.length += 1

    def latest(self):
        tar = len(self.data) - 1
        return self.data[tar]

    def all(self):
        return self.data

    def save(self, save_name):
        with open(f"{save_name}.luna", "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        try:
            with open("messages.list", "rb") as file:
                self.data = pickle.load(file)
        except:
            pass

    def clear(self):
        with open("guide.txt", "r") as guide:
            self.data = [{"role": "system", "content": guide.read()}]

        self.length = 0

    def remove(self, content):
        removed = None
        if type(content) == dict:
            self.data.remove(content)
            removed = content
            self.length -= 1
        else:
            for message in self.data:
                if content.replace("user: ", "") in message["content"]:
                    index = self.data.index(message)
                    removed = self.data.pop(index)

            self.length -= 1

        return removed

    def filter(self, size):
        for message in self.data:
            if len(message["content"]) > size and len(message["content"]) != 7349:
                l = len(message["content"])
                message["content"] = f"Message removed due to length: {l}. Original sender: {message['role']}"
                message["role"] = "system"

                self.length -= 1

    def sys_purge(self):
        for message in self.data:
            if message["role"] == "system":
                self.remove(message)

    def __len__(self):
        return self.length
