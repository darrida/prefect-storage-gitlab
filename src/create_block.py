from prefect.filesystems import GitLab


gitlab = GitLab(
    repository="https://gitlab.com/projects-bh/prefect-gitlab-storage",
    token_name="prefect-deploy",
    token="<password>",
)
gitlab.save("test-storage", overwrite=True)
