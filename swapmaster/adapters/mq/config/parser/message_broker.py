from ..models.message_broker import MessageBrokerConfig


def load_message_broker_config(dct: dict) -> MessageBrokerConfig:
    return MessageBrokerConfig(
        transport=dct.get("transport", "amqp"),
        user=dct.get("user", "guest"),
        password=dct.get("password", "guest"),
        host=dct.get("host", "localhost"),
        port=dct.get("port", 15672)
    )
