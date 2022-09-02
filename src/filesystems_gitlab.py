from typing import Optional
import io
from pathlib import Path
import tempfile
from pydantic import Field, SecretStr
from prefect.filesystems import ReadableDeploymentStorage
from prefect.utilities.processutils import run_process


class GitLab(ReadableDeploymentStorage):
    """
    Interact with files stored on public or private GitLab repositories.
    """

    _block_type_name = "GitLab"

    repository: str = Field(
        ...,
        description="The URL of a GitLab repository to read from, in either HTTPS or SSH format.",
    )
    reference: Optional[str] = Field(
        None,
        description="An optional reference to pin to; can be a branch name or tag.",
    )
    token_name: Optional[str] = Field(
        None,
        description="An optional token name (Example: username, user defined token name, 'gitlab-ci-token', 'oauth2', etc).",
    )
    token: Optional[SecretStr] = Field(
        None,
        description="An optional token used to access a private repository.",
    )

    async def get_directory(
        self, from_path: str = None, local_path: str = None
    ) -> None:
        """
        Clones a GitLab project specified in `from_path` to the provided `local_path`; defaults to cloning
        the repository reference configured on the Block to the present working directory.

        Args:
            - from_path: if provided, interpreted as a subdirectory of the underlying repository that will
                be copied to the provided local path
            - local_path: a local path to clone to; defaults to present working directory
        """
        cmd = "git clone"

        if not (self.token_name and self.token):
            raise ValueError(
                "If token is used, strings must be passed for both 'token_name' and 'token' parameters."
            )
        elif self.token_name and self.token:
            if "http" not in self.repository:
                raise ValueError(
                    "GitLab token can only be used with a 'http(s)' git clone path."
                )
            prefix, url = self.repository.split("://")
            repository_path = (
                f"{prefix}://{self.token_name}:{self.token.get_secret_value()}@{url}"
            )
        else:
            repository_path = self.repository

        cmd += f" {repository_path}"
        if self.reference:
            cmd += f" -b {self.reference} --depth 1"

        if local_path is None:
            local_path = Path(".").absolute()

        # in this case, we clone to a temporary directory and move the subdirectory over
        tmp_dir = None
        if from_path:
            tmp_dir = tempfile.TemporaryDirectory(suffix="prefect")
            path_to_move = str(Path(tmp_dir.name).joinpath(from_path))
            print(path_to_move)
            cmd += f" {tmp_dir.name} && cp -R {path_to_move}/."

        cmd += f" {local_path}"

        try:
            err_stream = io.StringIO()
            out_stream = io.StringIO()
            process = await run_process(cmd, stream_output=(out_stream, err_stream))
        finally:
            if tmp_dir:
                tmp_dir.cleanup()

        if process.returncode != 0:
            err_stream.seek(0)
            raise OSError(f"Failed to pull from remote:\n {err_stream.read()}")
