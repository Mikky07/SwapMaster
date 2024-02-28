from dataclasses import dataclass


@dataclass
class MessageBrokerConfig:
    transport: str
    user: str
    password: str
    host: str
    port: int

    @property
    def url(self) -> str:
        return "{transport}://{user}:{password}@{host}:{port}//".format(
            transport=self.transport,
            user=self.user,
            password=self.password,
            host=self.host,
            port=str(self.port)
        )
