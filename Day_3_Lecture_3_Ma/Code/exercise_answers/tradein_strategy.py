from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage

# Make a parser for the response
class Tradein(BaseModel):
    Analysis: str = Field(description="AI's analysis of the current situation.")
    Coupon: str = Field(description="The amount of discount the user can get.")
    Utterance: str = Field(description="AI's response to the user")


tradein_parser = JsonOutputParser(pydantic_object=Tradein)

# TODO: original: give 100 USD for any trade-in. Let student modify this part. Let student change it to give 50 USD for a major issue and 100 USD for a minor issue. (let student define major and minor issues themselves)

tradein_strategy_examples = [
    {
        "ai_question": "Which part of the product is broken?",
        "human_response": "The screen and the battery.",
        "ai_response": "Analysis: Let's think step by step. The user has a major issue including a broken screen and battery. The user will get a 50 USD coupon. Coupon: 50 USD. Utterance: You can get a 50 USD coupon if you want to trade in your old device for a new one.",
    },
]

tradein_strategy_example_template = ChatPromptTemplate.from_messages(
    [
        ("ai", "{ai_question}"),
        ("human", "{human_response}"),
        ("ai", "{ai_response}"),
    ]
)

tradein_strategy_fewshot_examples = FewShotChatMessagePromptTemplate(
    example_prompt=tradein_strategy_example_template,
    examples=tradein_strategy_examples,
)


tradein_strategy_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are a helpful agent that helps users to decide if they should trade in their old device for a new one. You will be given the user's description of the phone and you will need to calculate the amount of discount the user can get. If there is a major issue including a broken screen or battery, the user will get a 50 USD coupon. If there is a minor issue including a broken charging port, keyboard, or other, the user will get a 100 USD coupon. "
        ),
        tradein_strategy_fewshot_examples,
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{user_input}\n{format_instructions}",
                input_variables=["user_input"],
                partial_variables={
                    "format_instructions": tradein_parser.get_format_instructions()
                },
            )
        ),
    ]
)