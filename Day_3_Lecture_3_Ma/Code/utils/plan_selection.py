from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    FewShotChatMessagePromptTemplate,
    FewShotPromptTemplate
)
from langchain_core.messages import SystemMessage


# Make a parser for the response
class Plan(BaseModel):
    Analysis: str = Field(description="AI's analysis of the current situation.")
    Cost: str = Field(description="The cost of the plan. Could be a price in usd or unknown.")
    Plan: str = Field(description="The plan type to solve the problem. It should be either replace, repair or trade-in.")
    Utterance: str = Field(description="AI's response to the user")


plan_parser = JsonOutputParser(pydantic_object=Plan)

plan_selection_prompt = PromptTemplate.from_template(
    "Plans to select from: \n Replace: {replace_plan} \n Repair: {repair_plan} \n Trade-in: {tradein_plan} \n Please select one of the plans by considering the total cost and user's preference. Generate a proper response to the user. Note that the price for a new device is 249 USD. Replacement, if valid, cost 0 usd. User's previous attitude: {user_preference}  \n Analysis: {ai_analysis} \n Selected plan: {selected_plan}\n AI response: {ai_response}",
)

plan_selection_fewshot_examples = [
    {
        "replace_plan": "I'm sorry, but you cannot get a replacement. Only products with warranty can be replaced.",
        "repair_plan": "The total cost to fix the product is 150 USD.",
        "tradein_plan": "You can get a 100 USD coupon if you want to trade in your old device for a new one.",
        "user_preference": "None",
        "ai_analysis": "Let's thing step by step. The product cannot be replaced without a warranty. For repair, the cost for fixing the old device is 150 USD. For Trade-in, the cost for a new device is 249 USD, and the user can get a coupon. So he will spend 149 USD for the new device. Therefore, it is better to buy a new device as the cost is almost the same.",
        "selected_plan": "Trade-in",
        "ai_response": "Maybe you should consider buying a new device instead of fixing the old one. The cost for fixing the old device is 150 USD, and the cost for a new device is 249 USD. You can get a 100 USD coupon if you want to trade in your old device for a new one. The total cost to fix the product is 150 USD.",
    }
]

# TODO: Original Design: purely let LLM decide which plan to choose. Generally, LLM prefers to choose the plan with the lowest cost.
# Exercise: Design your own strategy to choose the plan.
# Hint: You may change the both the system prompt and few-shot examples to reflect the new strategy. 

plan_selection_prompt = FewShotPromptTemplate(
    examples=plan_selection_fewshot_examples,
    example_prompt=plan_selection_prompt,
    suffix="Plans to select from: \n Replace: {replace_plan} \n Repair: {repair_plan} \n Trade-in: {tradein_plan} \n Please select one of the plans and generate a proper response to the user. Note that the price for a new device is 249 USD. User's previous attitude: {user_preference} \n {format_instructions}",
    input_variables=["replace_plan", "repair_plan", "tradein_plan", "user_preference"],
    partial_variables={
        "format_instructions": plan_parser.get_format_instructions()
    }
)