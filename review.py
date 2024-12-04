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
    actions=[
        Action.CANVAS_GET_ASSIGNMENT,
        Action.CANVAS_LIST_ASSIGNMENT_SUBMISSIONS,
        Action.CANVAS_GRADE_COMMENT_SUBMISSION,
    ],
    caller=chatbot,
    executor=user_proxy,
)

task = """
You need to review the submissions for an assignment:
1. First get the assignent details using: CANVAS_GET_ASSIGNMENT
2. Then get the submissions for the assignment using: CANVAS_LIST_ASSIGNMENT_SUBMISSIONS
3. Based on the assignment details, review the submissions, check if they are correct
    a. If all answers are correct, give full points (10)
    b. If one or more answers are incorrect, give partial points (5)
    c. If all answers are incorrect, give 0 points
    and grade the submissions using: CANVAS_GRADE_COMMENT_SUBMISSION
Below are the details of the assignment:
- Course ID: 10798836
- Assignment ID: 51398858
"""
response = user_proxy.initiate_chat(chatbot, message=task)
print(response.chat_history)
