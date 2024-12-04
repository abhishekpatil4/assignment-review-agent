from autogen import AssistantAgent, UserProxyAgent
from composio_autogen import ComposioToolSet, Action
from composio import AppType
import os
from dotenv import load_dotenv

load_dotenv()

toolset = ComposioToolSet(
    api_key=os.getenv("COMPOSIO_API_KEY"),
    entity_id="karthik",
)
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ]
}

chatbot = AssistantAgent(
    "chatbot",
    system_message="You're a helpful assistant that creates assignments for a course. You will be given the details of the assigment, after creating you need to reply with the assignment details and TERMINATE.",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="User",
    is_termination_msg=lambda x: x.get("content", "")
    and "TERMINATE" in x.get("content", ""),
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
)

toolset.register_tools(
    actions=[Action.CANVAS_CREATE_ASSIGNMENT], caller=chatbot, executor=user_proxy
)

task = """
Create a new assignment for the course with id 10798836.
Assignment details:
- Name: Giooooooo
- Description: 
    a. What is the capital of France?
    b. What is the capital of Germany?
    c. What is the capital of Italy?
- Published: True
- Assignment Group: everyone
- Submission Types: Online (Text Entry)
- Display grade as: Points (10 is total points)
"""
response = user_proxy.initiate_chat(chatbot, message=task)
print(response.chat_history)
