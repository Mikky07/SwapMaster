from swapmaster.presentation.api.config.models.auth import AuthConfig


def load_auth_config(config_dct: dict):
    return AuthConfig(
        secret_key=config_dct.get("secret-key"),
        expire_minutes=int(config_dct.get("expire-minutes", 30))
    )
