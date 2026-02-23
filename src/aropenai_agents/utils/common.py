import os 
import yaml
from src.aropenai_agents import logger
from pathlib import Path
from box import ConfigBox
import json

def read_yaml(file_path: Path):
    try:
        logger.info("Inside read_yaml method")
        with open(file_path, 'r', encoding = 'utf-8') as f:
            content = yaml.safe_load(f)
            return ConfigBox(content)
    except Exception as e:
        logger.error(f"error occured inside read_yaml method:{e}")

def read_json(json_path: Path):
    try:
        logger.info("Inside read_json path")
        with open(json_path) as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error occured inside read_json method:{e}")

def save_json(json_path: Path, content):
    try:
        logger.info("inside save_json path")
        with open(json_path, "w+", encoding="utf-8") as f:
            json.dump(content, f, indent = 4)
        logger.info(f"json saved in: {json_path}")
    except Exception as e:
        logger.error(f"Error occured inside save_json method: {e}")


