import logging

logger = logging.getLogger("execute_task")
logger.setLevel(logging.DEBUG)

# remove all default handlers
for handler in logger.handlers:
    logger.removeHandler(handler)

# create console handler and set level to debug
console_handle = logging.StreamHandler()
console_handle.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s")
console_handle.setFormatter(formatter)

# now add new handler to logger
logger.addHandler(console_handle)