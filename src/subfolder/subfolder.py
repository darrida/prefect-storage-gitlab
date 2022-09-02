from prefect import task, get_run_logger


@task()
def subfolder_task():
    logger = get_run_logger()
    logger.info("SUCCESS: Subfolder Task")
