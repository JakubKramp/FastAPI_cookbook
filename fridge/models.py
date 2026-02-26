from sqlalchemy.orm import Mapped, mapped_column
from app.utils.db import Base

class Fridge(Base):
    """
    Model that reflects the produce an user currently have in their fridge.
    Relations:
    - User (auth) one to one
    - Produce (reicpes) one to many
    """
    __tablename__ = "fridge"