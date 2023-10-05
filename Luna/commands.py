import os
import subprocess
import googlesearch
import networking
import utilities


def find_command(text):
    lines = text.split("\n")
    for line in lines:
        line = line.replace("[Reply]: ", "")
        if line.startswith("|"):
            # print("command found")
            chunks = line.split("$")
            if chunks[0] == "|sys":
                return "sys", chunks[1]
            elif chunks[0] == "|exec":
                return "exec", chunks[1]
            elif chunks[0] == "|write":
                return "write", chunks[1]
            elif chunks[0] == "|retrieve":
                return "retrieve", chunks[1]
            elif chunks[0] == "|search":
                return "search", chunks[1]
            elif chunks[0] == "|scrape":
                return "scrape", chunks[1]
            elif chunks[0] == "|multiscrape":
                return "multiscrape", chunks[1]
    return None, None


class CommandHandler:
    def __init__(self):
        self.commands = []

    def run(self, cmd_type, cmd):
        if cmd_type == "sys":
            if "start " not in cmd:
                # print("no start")
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # print("returning stdout")
                # print(f"expected stdout: {p.stdout.read().decode('utf-8', errors='ignore')}")
                stdout = p.stdout.read().decode('utf-8', errors="ignore")
                stderr = p.stderr.read().decode('utf-8', errors="ignore")
                if len(stdout) > 0:
                    return stdout
                else:
                    return stderr
            else:
                try:
                    os.system(cmd)
                except Exception as e:
                    return e
                return 0
        elif cmd_type == "exec":
            try:
                exec(cmd)
            except Exception as e:
                return e
        elif cmd_type == "write":
            try:
                print("write detected")
                parts = cmd.split("(fn)")
                print(parts)
                with open(parts[1], "w") as file:
                    file.write(parts[0])
                return "Write successful"
            except:
                return "Write unsuccessful"
        elif cmd_type == "search":
            results = googlesearch.search(cmd, num_results=10)
            to_return = ""
            for i in results:
                if i not in to_return:
                    to_return += i + "\n"
            return to_return

        elif cmd_type == "scrape":
            results = networking.scrape_text(cmd)
            summary = utilities.summarize(results)
            return summary
        elif cmd_type == "multiscrape":
            urls = cmd.split("(s)")
            summaries = ""
            for url in urls:
                results = networking.scrape_text(url)
                summary = utilities.summarize(results)
                summaries += summary
            return summaries
        elif cmd_type == "retrieve":
            to_return = ""
            with open("luna.py", "r") as file:
                main_script = file.read()
            return main_script
