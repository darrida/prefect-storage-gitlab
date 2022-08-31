# prefect-storage-gitlab

## Ideas to Explore

- base action to build off of `git clone https://<token-name>:<token>@github.com/username/repo/folder`
  - may be able to construct something like this based off of a storage block
- structure this after https://github.com/PrefectHQ/prefect/blob/d8178e882a55cb106e9c6ea5056899cb8330321f/src/prefect/filesystems.py#L731
  - this is the similarly functioning `GitHub` block that was just merged
- [x] look into authentication
- [ ] look into how to QA agaist private GitLab instance and gitlab.com
- [x] explore what merged GitHub block does to bypass (?) the standard `deployment build` that pushes deployed flow to storage
  - Uses an inherited class called `ReadableDeploymentStorage`, which causes it to skip the upload step
- [x] explore if the GitHub block is able to also pull and use submodules (unlike the GitLab functionality in Prefect 1.0)
  - submodules and directories successfully pull, import into main flow, and run
- [ ] functioning proof of concepts:
  - [ ] public gitlab.com repo works without authorization
  - [x] private gitlab.com repo works (with authorization)
  - [ ] public on-premise gitlab repo works without authorization
  - [ ] private on-premise repo works (with authorization)
- [ ] token types
  - [x] works with "Deploy Token"
  - [ ] works with PAT (personal access token)