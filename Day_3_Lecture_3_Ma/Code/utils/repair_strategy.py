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
class Repair(BaseModel):
    Analysis: str = Field(description="AI's analysis of the current situation.")
    Cost: str = Field(description="The cost to fix a product.")
    Utterance: str = Field(description="AI's response to the user")


repair_parser = JsonOutputParser(pydantic_object=Repair)


repair_strategy_examples = [
    {
        "ai_question": "Which part of the product is broken?",
        "human_response": "The screen and the battery.",
        "ai_response": "Analysis: Let's think step by step. The cost for fixing the screen is 120 USD, and the cost for fixing the battery is 30 USD. The total cost is 150 USD. Cost: 150 USD. Utterance: The total cost to fix the product is 150 USD.",
    },
    {
        "ai_question": "Which part of the product is broken?",
        "human_response": "I want to repair my device.",
        "ai_response": "Analysis: Let's think step by step. The user didn't specify which part of the product is broken. To help, we need to know which part of the product is broken. Cost: unknown. Utterance: Which part of the product is broken?",
    },
]

repair_strategy_example_template = ChatPromptTemplate.from_messages(
    [
        ("ai", "{ai_question}"),
        ("human", "{human_response}"),
        ("ai", "{ai_response}"),
    ]
)

repair_strategy_fewshot_examples = FewShotChatMessagePromptTemplate(
    example_prompt=repair_strategy_example_template,
    examples=repair_strategy_examples,
)


repair_strategy_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are a helpful agent that help to workout the cost for repairing a product. The price for fixing are: screen 120 USD, battery 30 USD, charging port 50 USD, keyboard 20 USD, other 60 USD. You will be given the users description of the problem and you will need to calculate the total cost."
        ),
        repair_strategy_fewshot_examples,
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{user_input}\n{format_instructions}",
                input_variables=["user_input"],
                partial_variables={
                    "format_instructions": repair_parser.get_format_instructions()
                },
            )
        ),
    ]
)
