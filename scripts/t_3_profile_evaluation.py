import os
import json
import argparse
from dotenv import load_dotenv

from helpers.profile_evaluation.profile_evaluation import ProfileEvaluation
from helpers.logger.logger import logger
from helpers.gemini_processing.gemini_processing import detect_domain_from_description, detect_position_from_description
from helpers.parameter_loader.parameter_loader import load_parameters
from helpers.connectors.pusher.pusher_connection import Pusher

load_dotenv()

pusher_client = Pusher().pusher_client


def run(*args, **kwargs):
    logger.info(f"Starting Gemini profiling evaluation")

    fullname = kwargs.get("content", {}).get("fullname")
    position = kwargs.get("content", {}).get("position")
    talent_info = {
        "experience":  kwargs.get("content", {}).get("education"),
        "education": kwargs.get("content", {}).get("experience"),
        "languages": kwargs.get("content", {}).get("languages"),
        "skills": kwargs.get("content", {}).get("skills")
    }

    jd = "B"

    profile_evaluation = ProfileEvaluation(jd=jd)
    profile_evaluation_info = profile_evaluation.set_profile_id(fullname, position, talent_info, jd)

    logger.info(f"Getting profile_evaluation_info:{profile_evaluation_info}")
    private_channel = kwargs.get("pusher-channel-name")
    server_event_profiling = kwargs.get('pusher-event-name')
    pusher_client.trigger(private_channel, server_event_profiling, profile_evaluation_info)


if __name__ == "__main__":

    params = json.loads("""
{
    "task_id": "00003",
    "script_id": 3,
    "pusher-channel-name": "private-heppai-container-3",
    "pusher-event-name": "private-heppai-event-00003",
    "content": {
        "full_name": "Nguyen Vo",
        "position": "Senior at VNUHCM - University of Science",
        "education": [{
                "school": "VNUHCM - University of Science",
                "degree_type": "Bachelor's degree, Computer Software Engineering",
                "period": "2020 - 2024"
            }
        ],
        "experience": [{
                "company": "FIKA IELTS",
                "title": "Cloud Backend Engineer",
                "period": "08/2023 - 08/2024",
                "description": null
            }, {
                "company": "Schneider Electric",
                "title": "Software Engineer Intern",
                "period": "08/2023 - 10/2023",
                "description": null
            }
        ],
        "languages": [""],
        "skills": ["Docker", "FastAPI", "Amazon Web Services (AWS)", "DevOps", "Scripting", "Relational Databases", "NoSQL", "Terraform", "C#", "ASP.NET MVC", "Microsoft SQL Server", "Requirements Analysis", "Database Design", "Linux", "Bash", "Shell Scripting", "Computer Science", "Algorithms", "PostgreSQL", "Python Programming", "Data Engineering", "Problem Solving", "Jupyter notebooks", "Information Engineering", "Cloud Databases", "RDBMS", "IBM Db2", "Pandas", "NumPy", "Web Scraping", "Python (Programming Language)", "Data Manipulation", "Object-Oriented Programming (OOP)", "Data Stuctures and Algorithms", "Extract, Transform, Load (ETL)", "PySpark", "Apache Airflow", "DAG", "C++", "Computer Networking", "SQL", "Software Development", "Mathematics"]
    
    }
}""")
    run(**params)
