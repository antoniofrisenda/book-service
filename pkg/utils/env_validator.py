import os


def get_env(env_var: str) -> str:
    value = os.getenv(env_var)
    if not value:
        raise RuntimeError(f"Missing required env var: {env_var}")
    return value
