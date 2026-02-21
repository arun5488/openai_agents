from src.aropenai_agents.components.report_reader import Reports
from src.aropenai_agents.components.report_generator import LabAdmin
from src.aropenai_agents import logger
from dotenv import load_dotenv

class ReportPipeline:

    async def run():
        report = Reports()
        report.removing_lines_that_start_with_colon_or_stars()
        sections = report.extracting_test_name_and_values()
        test_details = report.extracting_test_name_and_values_from_sections(sections)

        LabAdmin().