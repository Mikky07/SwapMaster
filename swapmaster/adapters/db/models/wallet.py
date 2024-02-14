from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import Base


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
