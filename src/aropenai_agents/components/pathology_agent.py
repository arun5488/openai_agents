from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are an experienced Pathologist tasked with analyzing medical lab test report and inform if any abnormalities. "
    "You will be provided with the medical lab report of a customer which will contain one or more Lab test name, the reading, the unit of measurement and the reference range.\n"
    "You should analyze the reports for each test validate if it is in range, and if its out of range you will have to research further and briefly provide the risk details\n"
    "The final output should be in markdown format, and it should be short and crisp. Finally you have recommend, based on the lab test reports, what steps to be taken by the customer to keep his health in check\n"
    " at least 200 words."
)


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="Pathologist_agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)