from prefect import task, get_run_logger


@task()
def submodule_task():
    logger = get_run_logger()
    logger.info("SUCCESS: Submodule Task")
