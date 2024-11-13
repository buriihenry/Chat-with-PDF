from swarm import Swarm, Agent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the model for the agents
MODEL = "gpt-3.5-turbo"

# Initialize Swarm client
client = Swarm()

# Define Agent B (this needs to be defined before Agent A because Agent A refers to Agent B)
agent_b = Agent(
    name="Agent B",
    instructions="Only speak in English.",
    model=MODEL,
)

# Function in Agent A that refers to Agent B
def transfer_to_agent_b():
    return agent_b

# Define Agent A
agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],  # Function to transfer to Agent B
    model=MODEL,
)

# Run the interaction by sending a message to Agent A
response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I want to talk to agent B."}],
)

# Print the final response from the interaction
print(response.messages[-1]["content"])
