from dataclasses import dataclass


@dataclass
class WebhookConfig:
    domain: str
    host: str
    port: int
    path: str
    secret: str | None

    @property
    def url(self) -> str:
        return f"https://{self.domain}" + self.path
