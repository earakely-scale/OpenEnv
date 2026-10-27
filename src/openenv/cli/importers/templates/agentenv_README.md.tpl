# ${env_name}: AgentEnv bundle

This package serves the vendored `${bundle}` bundle through
`agent_env.openenv.build_app`. The bundle keeps its original folder name at
`vendor/${bundle}`; the generated package name is `${env_name}`.

## Prerequisites

- Python >=3.11.4 and `agentenv-framework[openenv]>=0.9.1364` (declared in
  `pyproject.toml` and `server/requirements.txt`).
- Local Docker: a Docker CLI and a running daemon accessible to the server.
  The delegated server builds the bundle's environment images at startup and
  deploys episode containers using local Docker by default.
- A self-contained bundle: tasks, environment definitions, verifiers, data and
  dependencies must be included in the bundle or provided by agentenv-framework.
  Only the selected bundle is vendored; external plugin registrations and files
  elsewhere in the source repository are not included.

## Run locally

From this generated package directory, after setting up Docker:

```bash
uv sync
uv run server --host 127.0.0.1 --port 8000
```

The `server` entry point runs `server/app.py`, which passes
`vendor/${bundle}` to `build_app`. Task selection, splits, tools and rewards
are defined by the bundle and agentenv-framework. Follow
[AgentEnv's OpenEnv documentation](https://www.agentenvframework.com/docs/openenv)
for its API and client usage.

`client.py`, `models.py` and the exports in `__init__.py` are echo template
scaffolding. They do not match the delegated AgentEnv API and must not be used
as a working client for this server.

## Deployment limitations

**Warning:** `server/Dockerfile` does not provide the Docker runtime required
by the delegated server. `openenv build` / `openenv push` alone do not produce
a working deployment, including on Hugging Face Spaces. Deployment requires
separately provisioning the server's image-build and episode-container runtime;
this importer does not configure it. Review AgentEnv's runtime requirements
before choosing a deployment host.

## Generated files

- `server/app.py`: delegated application and local server entry point.
- `vendor/${bundle}`: the selected bundle and its data.
- `pyproject.toml`: package dependencies and the `server` entry point.
- `server/requirements.txt`: server dependencies.
- `openenv.yaml`: generated OpenEnv manifest.
- `server/Dockerfile`: shared image template with the limitation described above.
- `client.py`, `models.py`, `__init__.py`: echo template scaffolding.
