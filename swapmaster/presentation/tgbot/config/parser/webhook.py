from ..models.webhook import WebhookConfig


def load_webhook_config(dct: dict) -> WebhookConfig:
    return WebhookConfig(
        domain=dct.get("domain"),
        port=dct.get("server-port", 8000),
        secret=dct.get("secret", "test"),
        path=dct.get("path", "/webhook"),
        host=dct.get("server-host", "127.0.0.1")
    )
