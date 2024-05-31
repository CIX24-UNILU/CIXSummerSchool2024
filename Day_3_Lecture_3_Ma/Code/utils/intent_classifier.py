from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Intent(BaseModel): # Parser 
    want_to_repair: str = Field(
        description="whether the user want to repair the device", example="Yes"
    )
    utterance: str = Field(
        description="AI's response to the user to host the conversation", example="Great! I will help you with that."
    )


intent_classifier_template = """
You are a customer service chatbot help to decide if the user want to repair its device. Base on the user's description, reply "Yes" if the user want to repair the device, "No" if the user do not want to repair the device, and "End" if the user want to end the conversation. Also reply a message to host the conversation.

{format_instructions}

The user's input is: {user_input}
"""





intent_classifier_parser = JsonOutputParser(pydantic_object=Intent)

intent_classifier_prompt = PromptTemplate(
    template=intent_classifier_template,
    input_variables=["user_input"],
    partial_variables={
        "format_instructions": intent_classifier_parser.get_format_instructions()
    },
)