import os
import sys
import json
import argparse
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.logger.logger import logger
from helpers.gemini_processing.gemini_processing import detect_domain_from_description, detect_position_from_description
from helpers.parameter_loader.parameter_loader import load_parameters
from helpers.connectors.pusher.pusher_connection import Pusher


# # THIS IS PRIVATE PUSHER CHANNEL IS USED FOR COMMUNICATE BETWEEN FASTAPI AND DJANGO
# PRIVATE_CHANNEL = 'heppai-private-channel'
#
# # THIS IS EVENT IS USED TO PUSH DATA TO PUSHER AFTER CRAWLING PROFILE SUCCESSFULLY
# SERVER_EVENT_PROFILING =  'server-profiling.crawl'
#
# # THIS IS EVENT IS USED TO PUSH DATA TO PUSHER AFTER EVALUTE SUCCESSFULLY
# SERVER_EVENT_EVALUATE = 'server-profiling.evaluate'


load_dotenv()

pusher_client = Pusher().pusher_client

def load_parameters(file_name):
    with open(file=file_name, mode="r") as file:
        data = json.load(file)
    return data


def run(*args, **kwargs):
    logger.info(f"Starting Gemini processing linkedin profile")

    company_description = kwargs.get('content', {}).get("company_description")
    job_description = kwargs.get('content', {}).get("job_description")
    related_industries = detect_domain_from_description(company_description)
    related_positions = detect_position_from_description(job_description)
    job_description_info = {
        "related_industries": related_industries,
        "related_positions": related_positions
        }
    logger.info(f"Getting related_industries:{related_industries}. related_positions={related_positions}")
    private_channel = kwargs.get("pusher-channel-name")
    server_event_profiling = kwargs.get('pusher-event-name')
    pusher_client.trigger(private_channel, server_event_profiling, job_description_info)


if __name__ == "__main__":

    params = json.loads("""
{
    "task_id": "00002",
    "script_id": 0,
    "pusher-channel-name": "private-heppai-container-0",
    "pusher-event-name": "private-heppai-event-00002",
    "content": {
        "company_description": "Design and develop robust, scalable, and high-performance software applications using GoLang. Identify, prioritize, and execute tasks in the software development life cycle. Automate tasks through appropriate tools and scripting. Collaborate with a cross-functional team to define, design, and ship new features and functionalities. Lead the architecture and coding standards efforts, ensuring clean & efficient code. Implement modern best practices and patterns in software development. Mentor junior software engineers, providing guidance and support to foster their growth and development. Conduct code reviews, ensuring coding standards, best practices, and security guidelines are adhered to. Troubleshoot, debug, and upgrade existing software. Stay up-to-date with emerging trends and technologies in software development to continuously improve our products and processes.",
        "job_description": "Bachelor's degree in Computer Science, Engineering, or a related field. Strong background in backend development with clear architecture mindset. Solid understanding of programming principles, financial transaction consistency, and Git version control. Strong understanding of software development life cycle and agile methodologies. Proven experience in designing scalable and maintainable architectures. Excellent problem-solving skills and ability to think analytically. Strong communication and teamwork skills, with the ability to collaborate effectively with cross-functional teams. A passion for mentoring and guiding junior team members. A continuous learner, open to embracing new technologies and development practices. Aspirations to be/become a Team Lead is a pre."
    }
}""")
    run(**params)