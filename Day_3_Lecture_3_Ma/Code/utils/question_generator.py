from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Question(BaseModel):  # Parser
    utterance: str = Field(
        description="AI's question to user to acquire information", example="Yes"
    )


question_generator_template = """
You are a customer service chatbot that helps collect information from the User. You need to frame a question to ask the user, based on the required information and chat history. Use the suggested question if you only need to ask about warranty. Reply with only one question you want to ask the user.

{format_instructions}

Chat History: {chat_history}

Required Information: {required_information}
Suggested Question: {suggested_question}
"""


question_generator_parser = JsonOutputParser(pydantic_object=Question)

question_generator_prompt = PromptTemplate(
    template=question_generator_template,
    input_variables=["chat_history", "required_information", "suggested_question"],
    partial_variables={
        "format_instructions": question_generator_parser.get_format_instructions()
    },
)