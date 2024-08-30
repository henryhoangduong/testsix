import os
import sys
import json
import argparse
from dotenv import load_dotenv

from helpers.linkedin.linkedin_selenium_crawler import LinkedInWebCrawlerBase as SeleniumCrawling
from helpers.linkedin.linkedin_profile_crawling import LinkedInProfile
from helpers.linkedin.crawling_talent_list import crawl_people_linkedin

from helpers.logger.logger import logger
from helpers.parameter_loader.parameter_loader import load_parameters
from helpers.connectors.pusher.pusher_connection import Pusher


load_dotenv()

pusher_client = Pusher().pusher_client

def get_crawler():
    logger.info("starting crawl_profile_task")
    crawler = SeleniumCrawling(cookies=None)
    crawler.override_cookies(account=os.getenv("LINKEDIN_USERNAME").split("@")[0])
    return crawler


def run(*args, **kwargs):
    logger.info(f"Starting linkedin profiles")

    criteria = {
        "network": ['F', 'S'],
        "geoUrn": kwargs.get('content', {}).get('location') or [],
        "keywords": " OR ".join(kwargs.get('content', {}).get('keywords') or []),
        "industry": kwargs.get('content', {}).get('industry') or []
        }
    crawler = get_crawler()
    talent_pool = crawl_people_linkedin(crawler=crawler, criteria=criteria)
   
    logger.info(f"Getting talent result:{talent_pool}")
    private_channel = kwargs.get("pusher-channel-name")
    server_event_profiling = kwargs.get('pusher-event-name')
    pusher_client.trigger(private_channel, server_event_profiling, talent_pool)
        
if __name__ == "__main__":

    params = json.loads("""
{
    "task_id": "00004",
    "script_id": 1,
    "pusher-channel-name": "private-heppai-container-1",
    "pusher-event-name": "private-heppai-event-00004",
    "content": {
        "network": ["F", "S"],
        "geoUrn": ["104195383"],
        "keywords": ["Senior Software Engineer", "Backend Engineer", "Lead Software Engineer", "Technical Lead"],
        "industry": ["6", "4", "96", "118", "3", "5", "3101", "3102"]
    }
}
""")
    run(**params)