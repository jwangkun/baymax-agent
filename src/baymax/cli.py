from dotenv import load_dotenv

# Load environment variables BEFORE importing any baymax modules
load_dotenv()

from baymax.agent import Agent
from baymax.utils.intro import print_intro
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

def main():
    print_intro()
    agent = Agent()

    # Create a prompt session with history support
    session = PromptSession(history=InMemoryHistory())

    while True:
        try:
            query = session.prompt(">> ")
            if query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if query:
                agent.run(query)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()