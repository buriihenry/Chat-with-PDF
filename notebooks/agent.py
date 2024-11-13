from swarm import Swarm, Agent
from dotenv import load_dotenv

load_dotenv()
MODEL = "gpt-3.5-turbo"

client = Swarm()

def transfer_to_agent_b():
    return agent_b

agent_a = Agent(
    name="Agent A",
    instructions = "You are a helpful agent.",
    functions=[transfer_to_agent_b],
    model=MODEL,
)    

agent_b = Agent(
    name = "Agent B",
    instructions = "Only speak in English",
    model = MODEL,
)

repsonse = client.run(
    agent = agent_a,
    messages = [{"role": "user", "content": "I want to talk to agent B."}],
)
print(repsonse.messages[-1]["content"])