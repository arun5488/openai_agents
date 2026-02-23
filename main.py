from src.aropenai_agents.components.report_reader import Reports
from src.aropenai_agents.components.report_generator import LabAdmin
from src.aropenai_agents.agents.json_converter_agent import JsonConverter
from src.aropenai_agents.utils.common import read_yaml, read_json
from src.aropenai_agents import constants as const
from src.aropenai_agents import logger
from dotenv import load_dotenv
import asyncio
from pathlib import Path


# async def main():
#     admin = LabAdmin()
#     async for update in admin.run(query=test_details):
#         print(update)  # or handle each yielded value (status updates, final report, etc.)

if __name__ == "__main__":
    logger.info("Loading the env file")
    load_dotenv(override=True)

    logger.info("Starting main")
    report = Reports()
    report.process_initial_report()



    # with open("resources/analysis.txt", "r", encoding="utf-8") as f:
    #     test_details = f.read()
    # logger.info(f"test_details:{test_details}")
    # asyncio.run(main())