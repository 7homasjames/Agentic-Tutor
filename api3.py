import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import autogen

app = FastAPI()

# LLM Configuration
llm_config = {
    "model": "gpt-3.5-turbo",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "temperature": 0.3
}

# Define Pydantic Request Model
class ConceptRequest(BaseModel):
    concept_name: str

# Function to fetch ML concept details
def get_ml_concept(concept_name: str) -> Dict:
    """Fetches explanations and visual representations of ML concepts."""
    return concept_name  # Modify to fetch actual concept details if needed.

# Define agents for explaining ML concepts through interactive decision trees
agents = [
    autogen.AssistantAgent(
        name="concept_identifier",
        system_message="Identify the most relevant ML or mathematical concept based on user input. Example: If input involves categorization, select Decision Trees.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),
    autogen.ConversableAgent(
        name="concept_explainer",
        system_message="Explain the identified concept in a simple way so that a 6th-grade student can understand it. Use relatable analogies.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),
    autogen.ConversableAgent(
        name="user_input_collector",
        system_message=(
            "Explain the identified ML concept using food-based analogies to make it fun and relatable for a 6th-grade student. "
            "For example, use pizzas to explain Decision Trees, fruit grouping for Clustering, sandwich layers for Neural Networks, "
            "cookie baking for Supervised Learning, and cooking experiments for Reinforcement Learning. "
            "Ensure the explanation is simple, engaging, and interactive."
        ),
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),

    autogen.AssistantAgent(
        name="example_generator",
        system_message="Generate an example based on the identified concept and the user's favorite dish. Ensure the example is easy to understand and fun.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),
    autogen.AssistantAgent(
        name="visualization_agent",
        system_message="Create a visually appealing diagram or chart to illustrate the concept. Use Matplotlib, Graphviz, or another tool for clarity.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),
    autogen.AssistantAgent(
        name="output_formatter",
        system_message="Combine the concept explanation, user input, generated example, and visual representation into a single section with a structured and engaging layout.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    )
]

# Updated FSM Graph for Transitions
agent_dict = {agent.name: agent for agent in agents}

fsm_graph = {
    agent_dict["concept_identifier"]: [agent_dict["concept_explainer"]],
    agent_dict["concept_explainer"]: [agent_dict["user_input_collector"]],
    agent_dict["user_input_collector"]: [agent_dict["example_generator"]],
    agent_dict["example_generator"]: [agent_dict["visualization_agent"]],
    agent_dict["visualization_agent"]: [agent_dict["output_formatter"]],
    agent_dict["output_formatter"]: [agent_dict["concept_identifier"]]  # Loop back for iteration
}


# Ensure FSM graph agents exist
for key in fsm_graph.keys():
    if key not in agents:
        raise ValueError(f"FSM Graph Error: '{key.name}' is not a valid agent object.")

# Initialize Group Chat for Agents
groupchat = autogen.GroupChat(
    agents=agents,
    messages=[],
    allowed_or_disallowed_speaker_transitions=fsm_graph,
    speaker_transitions_type="allowed",
    send_introductions=True,
    func_call_filter=True,
    max_round=6 # Prevent infinite looping
)

# GroupChatManager to manage interactions
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    name="ChatManager",
    system_message="Managing agentic workflow for ML explanations.",
    human_input_mode="TERMINATE",
    llm_config=llm_config
)

# API Endpoint for ML Concept Explanation
@app.post("/ml_explanation/")
async def ml_explanation(request: ConceptRequest):
    concept_name = request.concept_name.strip()
    
    # Fetch ML concept details
    concept_details = get_ml_concept(concept_name)
    if not concept_details:
        raise HTTPException(status_code=404, detail="ML concept not found.")

    # ✅ Corrected agent lookup
    explanation_agent = next(a for a in agents if a.name == "concept_explainer")

    # Start agentic conversation with the manager
    response = explanation_agent.initiate_chat(
        recipient=manager, 
        message=f"Explain ML concept: {concept_name} with details {concept_details}"
    )

    return {"output": response.get("content", "No response generated.") if isinstance(response, dict) else response}
