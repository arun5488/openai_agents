from src.aropenai_agents.components.report_reader import Reports
from src.aropenai_agents.components.report_generator import LabAdmin
#from src.aropenai_agents.agents.json_converter_agent import JsonConverter
from src.aropenai_agents.utils.common import read_yaml, read_json
from src.aropenai_agents import constants as const
from src.aropenai_agents import logger
from dotenv import load_dotenv
import asyncio
from pathlib import Path
import json


async def lab_admin_run(test_details: json):
    admin = LabAdmin()
    async for update in admin.run(query=test_details):
        print(update)  # or handle each yielded value (status updates, final report, etc.)

if __name__ == "__main__":
    logger.info("Loading the env file")
    load_dotenv(override=True)

    logger.info("Starting main")
    report = Reports()
    report.process_initial_report()

    test_details = read_json(Path(const.TEST_REPORT_JSON)) #read the test details from the json file
    asyncio.run(lab_admin_run(test_details)) #run the lab admin run function
    





    # with open("resources/analysis.txt", "r", encoding="utf-8") as f:
    #     test_details = f.read()
    # logger.info(f"test_details:{test_details}")
    # asyncio.run(main())