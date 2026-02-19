from src.aropenai_agents.components.report_reader import Reports
from src.aropenai_agents import logger


if __name__ == "__main__":
    logger.info("Starting main")
    report = Reports()
    report.removing_lines_that_start_with_colon_or_stars()
    sections = report.extracting_test_name_and_values()
    test_details = report.extracting_test_name_and_values_from_sections(sections)
