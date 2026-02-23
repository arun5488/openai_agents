from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from pypdf import PdfReader
from src.aropenai_agents import constants as const
from src.aropenai_agents.utils.common import read_yaml, save_json
from src.aropenai_agents import logger
import re

load_dotenv(override=True)

class Reports:
    def __init__(self):
        logger.info("Initializing Reports class")
        self.params_file = read_yaml(const.PARAMS).report_reader
        self.schema_file = read_yaml(const.SCHEMA)
        self.openai = OpenAI()
        self.report_field_list = self.schema_file["report_lines_starting_with_to_be_deleted"]
        logger.info(f"lines with following starting words will be excluded:{self.report_field_list}")
        self.reader = PdfReader(self.params_file.input_file_location)
        self.report = ""
        for page in self.reader.pages:
            text = page.extract_text()
            if text:
                self.report += text
    
    def removing_lines_that_start_with_colon_or_stars_or_words_from_file(self):
        logger.info("Removing lines that start with colon or stars or words in the list")
        
        word = [re.escape(w) for w in self.report_field_list]
        pattern = f"(?:{'|'.join(word)})"
        logger.info(f"words read from the yaml file:{pattern}")
        cleaned_lines = []
        for line in self.report.split("\n"):
            if line.startswith("Test Name"):
                line = re.sub(r"^Test Name\b","Test_Name", line)
            elif line.startswith(":") or line.startswith("*"):
                continue
            elif re.match(r"^\s*:", line):
                continue
            elif re.match(r"^\d+", line):
                continue
            elif re.match(rf"^\s*{pattern}.*$", line):
                continue         
            cleaned_lines.append(line)
        self.report = "\n".join(cleaned_lines)
        #logger.info(self.report)
        return self.report

    def extracting_test_name_and_values(self, processed_report):
        logger.info("Extracting test name and values")
        sections = []
        current_section = None
        for line in processed_report.split("\n"):
            if line.startswith("Test_Name"):
                if current_section:
                    sections.append(current_section)
                else:
                    current_section = {"header": line, "content": []}
            else:
                if current_section:
                    current_section["content"].append(line)
        return sections
    
    def extracting_test_name_and_values_from_sections(self, sections):
        logger.info("Extracting test name and values from sections")
        test_name_and_values = []
        for section in sections:
            section_content = section["content"]
            #logger.info(f"section_content:{section_content}")
            content_in_line = "\n".join(section_content)
            #logger.info(f"content_in_line:{content_in_line}")
            test_name_and_values.append(content_in_line)
            
        return test_name_and_values
    
    def convert_report_to_json_openai(self, test_names_and_values):
        try:
            logger.info("inside convert_report_to_json_openai method")
            ref_json = self.params_file.ref_json
            system_prompt = f"""You will be provided with a list of medical tests and its test values. 
                                you have to read the list and create a json structured file as per the file {ref_json}"""
            response = self.openai.chat.completions.create(
                model = const.OPENAI_MODEL,
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role":"user", "content": json.dumps(test_names_and_values)}
                ]
            )
            response_text= response.choices[0].message.content

            response_as_json = json.loads(response_text)
            save_json(self.params_file.output_file_location, content = response_as_json)


        
        except Exception as e:
            logger.error(f"error occured inside convert_report_to_json_openai:{e}")

    def process_initial_report(self):
        try:
            logger.info("Inside process_initial_report method")
            formatted_report = self.removing_lines_that_start_with_colon_or_stars_or_words_from_file()
            sections_from_report = self.extracting_test_name_and_values(formatted_report)
            test_names_and_values = self.extracting_test_name_and_values_from_sections(sections_from_report)
            logger.info(f"test_names_and_values extracted as {type(test_names_and_values)}")
            self.convert_report_to_json_openai(test_names_and_values)
            logger.info(f"Initial report processed successfully")

        except Exception as e:
            logger.error(f"Error occured inside process_initial_report:{e}")





        


