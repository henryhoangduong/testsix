import os

import google.generativeai as genai
from dotenv import load_dotenv

from helpers.logger.logger import logger
from helpers.linkedin.linkedin_keywords import all_industries_list

load_dotenv()
list_api_key = os.getenv("GEMINI_API_KEY").split(", ")
genai.configure(api_key=list_api_key[0])
GEMINI_API_VERSION = os.getenv("GEMINI_API_VERSION")

GENERATION_CONTIG = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
    }

def detect_domain_from_description(company_description):
    logger.debug(f"Detecting domain from company description: {company_description}")
    model = genai.GenerativeModel(model_name=GEMINI_API_VERSION,
                                    generation_config=GENERATION_CONTIG)

    conversation = model.start_chat()
    conversation.send_message('''instructions = I will give you the list of all available industries/domains, and the description of a company.
                              Your responsibility is to give me the list of all possible related industries/domains of that company compared to the given full list.
                              The number of element in the list is NOT restricted to 4 but 8 at most. If the number of element in the list is equal or greater than 8, please select the 8 most related one.
    Answer must be structured like this and contain only this structured: [{"$domain_key1": "$domain1"}, {"$domain_key": "$domain2"}, {"$domain_id3": "$domain3"}, {"$domain_id4": "$domain4"}]
    Here is the list of all available industries/domains: ''' + str(all_industries_list()) + 'Here is the description of a company:' + str(company_description))
    related_industries = conversation.last.text
    return related_industries

def detect_position_from_description(job_description):
    logger.debug(f"Detecting position from job description: {job_description}")
    model = genai.GenerativeModel(model_name=GEMINI_API_VERSION,
                                    generation_config=GENERATION_CONTIG)

    conversation = model.start_chat()
    conversation.send_message('''instructions = I will give you the job description.
                              Your responsibility is to give me the list of 4 most closest role/position based on the given job description.
                              The number of element in the list is must restricted to 4 at most. If the number of element in the list is less than 4, please keep it as it is.
                              The answer must be in English.
    Answer must be structured like this and contain only this structured: ["position1", "position2", position3", "position4"]
    Here is the job description: ''' + str(job_description))
    related_positions = conversation.last.text
    return related_positions