import os
import json

from dotenv import load_dotenv

from helpers.linkedin.linkedin_selenium_crawler import LinkedInWebCrawlerBase as SeleniumCrawling
from helpers.linkedin.linkedin_profile_crawling import LinkedInProfile

from helpers.logger.logger import logger
from helpers.connectors.pusher.pusher_connection import Pusher

load_dotenv()

pusher_client = Pusher().pusher_client

def crawl_profile_task(talent_url, api_index):
    logger.info("starting crawl_profile_task")
    crawler = SeleniumCrawling(cookies=None)
    crawler.override_cookies(account=os.getenv("LINKEDIN_USERNAME").split("@")[0])
    detail_updater = LinkedInProfile()
    result = detail_updater.crawl_profile(talent_url, crawler, api_index)
    logger.info(f"finished crawl_profile_task. result={result}")
    return result

def run(*args, **kwargs):
    logger.info(f"Starting linkedin profile")

    talent_url = kwargs.get("content", {}).get("talent_url")
    api_index = kwargs.get("content", {}).get("api_index")
    crawl_profile = crawl_profile_task(talent_url=talent_url, api_index=api_index)

    logger.info(f"Getting talent result:{crawl_profile}")
    private_channel = kwargs.get("pusher-channel-name")
    server_event_profiling = kwargs.get('pusher-event-name')
    pusher_client.trigger(private_channel, server_event_profiling, crawl_profile)
	
        
if __name__ == "__main__":
    params = json.loads("""
{
    "task_id": "00005",
    "script_id": 2,
    "pusher-channel-name": "private-heppai-container-1",
    "pusher-event-name": "private-heppai-event-00005",
    "content": {
        "talent_url": "https://www.linkedin.com/in/vlad-gev",
        "api_index": 0
        }
    }""")
    run(**params)	
