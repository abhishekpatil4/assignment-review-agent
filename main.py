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
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ]
}

chatbot = AssistantAgent(
    "chatbot",
    system_message="Reply TERMINATE when the task is done or when user's content is empty",
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
    actions=[Action.CANVAS_GET_ALL_ASSIGNMENTS], caller=chatbot, executor=user_proxy
)

task = "Get all the assignments for the course 10798836"
response = user_proxy.initiate_chat(chatbot, message=task)
print(response.chat_history)
