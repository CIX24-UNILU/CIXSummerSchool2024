from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class TechIssue(BaseModel):  # Parser
    tech_issue: list = Field(
        description="The tech issues that the user's tablet has", example="Yes"
    )


tech_issue_analyser_template = """
You are a customer service chatbot that helps to decide which part of the tablet is broken. Base on the user's description and chat history, reply all the parts that are broken. If the user do not mention any part, reply "No part is broken". Broken parts should be separated by commas. Broken parts should be "Screen", "Charging port", "Battery", "Keyboard", or "Others". If the user mention a part that is not in the list, reply "Others". If the user did not mention any part, reply an emtpy list. 

{format_instructions}

The previous chat history is: {chat_history}

The user's input is: {user_input}
"""


tech_issue_analyser_parser = JsonOutputParser(pydantic_object=TechIssue)

tech_issue_analyser_prompt = PromptTemplate(
    template=tech_issue_analyser_template,
    input_variables=["user_input", "chat_history"],
    partial_variables={
        "format_instructions": tech_issue_analyser_parser.get_format_instructions()
    },
)