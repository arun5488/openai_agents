from src.aropenai_agents.components.report_reader import Reports
from src.aropenai_agents.components.report_generator import LabAdmin
from src.aropenai_agents import logger
from dotenv import load_dotenv
import asyncio


async def main():
    admin = LabAdmin()
    async for update in admin.run(query=test_details):
        print(update)  # or handle each yielded value (status updates, final report, etc.)

if __name__ == "__main__":
    logger.info("Loading the env file")
    load_dotenv(override=True)

    logger.info("Starting main")
    # report = Reports()
    # report.removing_lines_that_start_with_colon_or_stars()
    # sections = report.extracting_test_name_and_values()
    # test_details = report.extracting_test_name_and_values_from_sections(sections)
    # with open("resources/analysis.txt", "w", encoding="utf-8") as f:
    #     f.write(str(test_details))   

    with open("resources/analysis.txt", "r", encoding="utf-8") as f:
        test_details = f.read()
    logger.info(f"test_details:{test_details}")
    asyncio.run(main())