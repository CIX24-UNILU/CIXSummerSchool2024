from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Preference(BaseModel):  # Parser
    user_preference: str = Field(
        description="user's preference towards repair and trade-in or replace the device (if possible)", example="Yes"
    )


preference_identifier_template = """
Please help me summarize from user's input if the user have any preference towards repair and trade-in or replace the device (if possible). Summarize the user's preference in a sentence.

{format_instructions}

The user's input is: {user_input}
"""


preference_identifier_parser = JsonOutputParser(pydantic_object=Preference)

preference_identifier_prompt = PromptTemplate(
    template=preference_identifier_template,
    input_variables=["user_input"],
    partial_variables={
        "format_instructions": preference_identifier_parser.get_format_instructions()
    },
)