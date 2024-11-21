import rasa
from rasa import Action
from rasa.cli import console
from rasa.engine import Interpreter
from rasa.utils import today_str

# Define custom actions
class ActionGreetUser(Action):
    def name(self, dialogue):
        return "action_greet_user"

    async def run(self, dispatcher, tracker, domain, manifest, **kwars):
        greeting = "Hello! How can I assist you today?"
        dispatcher.utter_message(text=greeting)
        return []

class ActionExecuteCommand(Action):
    def name(self, dialogue):
        return "action_execute_command"

    async def run(self, dispatcher, tracker, domain, manifest, **kwars):
        command = tracker.latest_message[0]['text'].strip()
        if command.lower() == "shut down":
            dispatcher.utter_message(text="Goodbye! Have a great day!")
            raise keyboard.Interrupt
        else:
            try:
                output = subprocess.check_output(command.split(), universal_newline=True, stderr=subprocess.STDOUT)
                dispatcher.utter_message(text=str(output, 'utf-8'))
            except:
                dispatcher.utter_message(text="Unable to execute command. Please try again.")
            return []

# Configure Rasa NLU components and pipelines
interpreter = Interpreter()
manifest = {
    "version": "2.0",
    "language": "en",
    "project": {
        "id": "chat",
        "name": "Chat Demo",
        "version": "0.1"
    },
    "author": "vendetta25",
    "license": "Apache License Version 2.0",
    "description": "A simple demonstration of a chatbot using Rasa"
}

# Start the Rasa bot
if __name__ == "__main__":
    print(f"Welcome to the {manifest['project']['name']} bot! (c) {today_str()}")
    rasa.cli.run([sys.argv[0], '--config', 'domain.yml'], ['--no-capture-logging', '--enable-logging'], live_reload=False)
