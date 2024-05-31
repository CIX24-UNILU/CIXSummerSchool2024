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
class Replacement(BaseModel):
    Analysis: str = Field(description="AI's analysis of the current situation.")
    Valid: str = Field(description="Whether the user can replace the product.")
    Utterance: str = Field(description="AI's response to the user")


replacement_parser = JsonOutputParser(pydantic_object=Replacement)


replacement_strategy_examples = [
    {
        "ai_question": "Which part of the product is broken?",
        "human_response": "The screen and the battery. Additional info: warranty: no.",
        "ai_response": "Analysis: Let's think step by step. The user does not have warranty, so he cannot get a replacement. Replacement: No. Utterance: I'm sorry, but you cannot get a replacement. Only products with warranty can be replaced.",
    },
    {
        "ai_question": "Which part of the product is broken?",
        "human_response": "The screen and the battery. Additional info: warranty: Yes.",
        "ai_response": "Analysis: Let's think step by step. The user have a warranty. The product can be replaced free of charge. Replacement: Yes. Utterance: You can get a replacement for the product as it is under warranty. The cost is 0 USD.",
    },
]

replacement_strategy_example_template = ChatPromptTemplate.from_messages(
    [
        ("ai", "{ai_question}"),
        ("human", "{human_response}"),
        ("ai", "{ai_response}"),
    ]
)

replacement_strategy_fewshot_examples = FewShotChatMessagePromptTemplate(
    example_prompt=replacement_strategy_example_template,
    examples=replacement_strategy_examples,
)


replacement_strategy_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are a helpful agent that help to workout if a user can get a replacement for a product. Note that only products with warranty can be replaced. Today is May 20th, 2024."
        ),
        replacement_strategy_fewshot_examples,
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{user_input}\n{additional_info}\n{format_instructions}",
                input_variables=["user_input, additional_info"],
                partial_variables={
                    "format_instructions": replacement_parser.get_format_instructions()
                },
            )
        ),
    ]
)
