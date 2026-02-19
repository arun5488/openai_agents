from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from pypdf import PdfReader
import gradio as gr
from src.aropenai_agents import logger
import re

load_dotenv(override=True)

class Reports:
    def __init__(self):
        logger.info("Initializing Reports class")
        self.openai = OpenAI()
        reader = PdfReader("resources/Lab_report.pdf")
        self.report = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.report += text
    
    def removing_lines_that_start_with_colon_or_stars(self):
        logger.info("Removing lines that start with colon or stars")
        cleaned_lines = []
        for line in self.report.split("\n"):
            if line.startswith("Test Name"):
                line = re.sub(r"^Test Name\b","Test_Name", line)
            elif line.startswith(":") or line.startswith("*"):
                continue
            elif re.match(r"^\s*:", line):
                continue
            elif re.match(r"^Mobile\b.*$", line):
                continue
            elif re.match(r"^RegNo\b.*$", line):
                continue
            elif re.match(r"^CMH.*$", line):
                continue
            elif re.match(r"^correlation\b.*$", line):
                continue   
            elif re.match(r"^\d+.*$", line):
                continue   
            elif re.match(r"^.*Method\b.*$", line):
                continue                       
            elif re.match(r"^(?:Dr|only|M\.D|Report|Page|End|Sample|EDTASample|SerumSample)\b.*$", line):
                continue          
            cleaned_lines.append(line)
        self.report = "\n".join(cleaned_lines)
        #logger.info(self.report)
        return self.report

    def extracting_test_name_and_values(self):
        logger.info("Extracting test name and values")
        sections = []
        current_section = None
        section_content_value = []
        for line in self.report.split("\n"):
            if line.startswith("Test_Name"):
                if current_section:
                    sections.append(current_section)
                else:
                    current_section = {"header": line, "content": []}
            else:
                if current_section:
                    current_section["content"].append(line)
                    #section_content_value.append(line)
        #logger.info(sections)
        #logger.info(section_content_value)
        return sections
    
    def extracting_test_name_and_values_from_sections(self, sections):
        logger.info("Extracting test name and values from sections")
        test_name_and_values = []
        for section in sections:
            section_content = section["content"]
            logger.info(f"section_content:{section_content}")
            content_in_line = "\n".join(section_content)
            logger.info(f"content_in_line:{content_in_line}")
            test_name_and_values.append(content_in_line)
            break
        return test_name_and_values


        


