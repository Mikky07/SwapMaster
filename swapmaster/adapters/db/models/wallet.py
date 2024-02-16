from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import Base
from swapmaster.core import models as dto


class Wallet(Base):
    __tablename__ = "wallets"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    blockchain: Mapped[str]
    address: Mapped[str]

    reserve: Mapped['Reserve'] = relationship(back_populates="wallet", foreign_keys="Reserve.wallet_id")

    def __repr__(self):
        return (
            f"<Wallet"
            f" id={self.id}"
            f" name={self.name}"
            f" blockchain={self.blockchain}"
            f" address={self.address}>"
        )

    def to_dto(self) -> dto.Wallet:
        return dto.Wallet(
            wallet_id=self.id,
            name=self.name,
            blockchain=self.blockchain,
            address=self.address,
        )
