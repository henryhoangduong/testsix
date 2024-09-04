import os
import sys
import re
import pathlib
import tempfile
import importlib
import subprocess
from dotenv import load_dotenv
from datetime import datetime

from helpers.logger.logger import logger
from helpers.gitlab_client.gitlab_client import GitlabClient
from helpers.parameter_loader.parameter_loader import load_parameters
load_dotenv()

print('start: ', datetime.now())
arg = sys.argv

param = arg[1]
# param = os.environ.get('param', '20240822_0001_000001')


token = os.getenv("GITLAB_ACCESS_TOKEN")
gitlab_host = os.getenv("GITLAB_HOST")
gitlab_task_repo = os.getenv("GITLAB_TASKS_REPO")
gitlab_scripts_repo = os.getenv("GITLAB_SCRIPTS_REPO")

def parse_param(param):
    regex = r"^([0-9]{8})_([0-9]{4})_([0-9]{6})"
    match = re.match(pattern=regex, string=param)
    if match:
        yyyymmdd, backend_instance_id, task_id = match.groups()
    else:
        yyyymmdd, backend_instance_id, task_id = None, None, None
    return yyyymmdd, backend_instance_id, task_id


def get_file_from_repo(file_name, path, destination, gitlab_host, gitlab_repo, token, branch="main"):

    file_name_destination = pathlib.Path(destination, file_name)
    python_gitlab_client = GitlabClient(url=gitlab_host, authkey=token, project=gitlab_repo)
    python_gitlab_client.get_raw_file(file_path=f"{path}{file_name}", destination=file_name_destination, branch=branch)

def get_module_from_string(module_name : str):
    return importlib.import_module(module_name)

yyyymmdd, backend_instance_id, task_id = parse_param(param)

current_working_dir = os.getcwd()
logger.info(f"cwd={current_working_dir} for task_id={task_id}")
# create a temporary directory using the context manager
with tempfile.TemporaryDirectory(dir="scripts") as tmpdirname:
    logger.info(f"created temporary directory={tmpdirname} for task_id={task_id}" )

    # get param_task_id.json
    param_file_name = f"param_{yyyymmdd}_{backend_instance_id}_{task_id}.json"

    logger.info(f"param_file_name={param_file_name} for task_id={task_id}")

    # get param json
    get_file_from_repo(file_name = param_file_name, path="",
                       destination=tmpdirname, gitlab_host=gitlab_host,
                       gitlab_repo=gitlab_task_repo, token=token, branch="main")

    param_payload = load_parameters(file_name = pathlib.Path(tmpdirname, param_file_name))

    # get script_id
    script_id = param_payload.get("script_id")
    logger.info(f"script_id={script_id} for task_id={task_id}")

    # use mapping to get the script name
    # TODO migrate as config file
    script_mapping = {
        0: "t_0_gemini_linkedin_keywords.py",
        1: "t_1_linkedin_profiles.py",
        2: "t_2_linkedin_profile.py",
        3: "t_3_profile_evaluation.py",
        9: "t_9_dummy_run.py"
    }
    script_name = f"{script_mapping.get(script_id)}"

    logger.info(f"script_name={script_name} for task_id={task_id}")

    # get script.py
    get_file_from_repo(file_name=script_name, path="scripts/",
                       destination=tmpdirname, gitlab_host=gitlab_host,
                       gitlab_repo=gitlab_scripts_repo, token=token, branch="main")

    task_dir = ".".join(pathlib.Path(tmpdirname).parts[-2:])

    logger.info(f"script_name={script_name} for task_id={task_id}")
    script_basename = pathlib.Path(script_name).stem

    logger.info(f"script_basename={script_basename} for task_id={task_id}")
    # importing the task module from path as string
    logger.info(f"Importing={task_dir}.{script_basename} task_dir={task_dir} script_basename={script_basename}")
    task = importlib.import_module(f"{task_dir}.{script_basename}")

    logger.info(f"Executing task={script_basename} for task_id={task_id}")
    # call the task module run function
    task.run(**param_payload)
    print('end: ', datetime.now())
