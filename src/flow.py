from prefect import flow, task, get_run_logger
from submodule import submodule_task
from subfolder.subfolder import subfolder_task
# from filesystems_gitlab import GitLab


@task()
def same_module():
    logger = get_run_logger()
    logger.info('SUCCESS: Same Module Task.')


@flow(name='GitLab Storage Test')
def main():
    same_module()
    submodule_task()
    subfolder_task()


if __name__ == '__main__':
    main()


# prefect block register --file filesystems_gitlab.py
# python create_block.py
# prefect deployment build flow.py:main -sb gitlab/test-storage --path test -n gitlab-test --apply