from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import Base


class Wallet(Base):
    __tablename__ = "wallets"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    link: Mapped[str]

    reserve: Mapped['Reserve'] = relationship(back_populates="wallet", foreign_keys="reserves.wallet_id")

    def __repr__(self):
        return (
            f"<Wallet"
            f" id={self.id}"
            f" name={self.name}"
            f" link={self.link}>"
        )
