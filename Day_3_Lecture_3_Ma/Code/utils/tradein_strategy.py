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

# TODO: Original Design: give 100 USD for any trade-in.
# Exercise: Change it to give 50 USD for a major issue (a broken screen or battery, for example) and 100 USD for a minor issue (other issues, for example). You may define major and minor issues yourself.
# Hint: You may change the both the system prompt and few-shot examples to reflect the new strategy.

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
            content="You are a helpful agent that helps users to decide if they should trade in their old device for a new one. The user will get a 100 USD coupon if they choose to trade in their devices."
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