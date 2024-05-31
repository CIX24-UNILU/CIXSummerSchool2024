# A non-LLM logic that specify the time of each plan.
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import (
    FewShotPromptTemplate,
    PromptTemplate,
)
from langchain_core.pydantic_v1 import BaseModel, Field


def get_time_contrain_of_plans(plan: dict):
    if "Plan" not in plan:
        plan["Time"] = "unknown"
        return plan
    if plan["Plan"].lower() == "repair":
        plan["Time"] = "7 days to repair"
        return plan
    if plan["Plan"].lower() == "trade-in":
        plan["Time"] = (
            "Get a space grey tablet now as it is in stock. Get a black tablet in 7 days as it is out of stock. You need to choose from these two options."
        )
        return plan
    if plan["Plan"].lower() == "replace":
        plan["Time"] = (
            "Get a space grey tablet now as it is in stock. Get a black tablet in 7 days as it is out of stock. You need to choose from these two options."
        )
        return plan
    return plan






# Make a parser for the response
class Plan_w_Time(BaseModel):
    Analysis: str = Field(description="AI's analysis of the current situation.")
    Cost: str = Field(
        description="The cost of the plan. Could be a price in usd or unknown."
    )
    Time: str = Field(description="The time it takes to complete the plan.")
    Plan: str = Field(
        description="The plan type to solve the problem. It should be either replace, repair or trade-in."
    )
    Utterance: str = Field(description="AI's response to the user")


time_aware_plan_parser = JsonOutputParser(pydantic_object=Plan_w_Time)

time_aware_plan_selection_template = """
You are given options to choose from. If it is a repair plan, just return it. If it is a plan with options, choose the one that requires the least time. Modify the response to human accordingly and fill the slots for response.\n Here is the plan in dict format: {plans} \n {format_instructions}
"""


time_aware_plan_selection_prompt = PromptTemplate(
    template=time_aware_plan_selection_template,
    input_variables=["plans"],
    partial_variables={
        "format_instructions": time_aware_plan_parser.get_format_instructions()
    },
)