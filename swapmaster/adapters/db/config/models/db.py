from dataclasses import dataclass


@dataclass
class RedisConfig:
    host: str
    port: int


@dataclass
class DBConfig:
    driver: str
    database: str
    port: int
    host: str
    user: str
    password: str
    dialect: str

    @property
    def url(self) -> str:
        db_url = "{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}".format(
            dialect=self.dialect,
            driver=self.driver,
            user=self.user,
            password=self.password,
            host=self.host,
            port=str(self.port),
            database=self.database
        )
        return db_url
