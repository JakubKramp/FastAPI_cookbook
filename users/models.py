from sqlmodel import Field, SQLModel, create_engine, Session
from config import settings

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str

class UserDetail(SQLModel):
    email: str
    password: str



database_url = settings.DATABASE_URL

engine = create_engine(database_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":  #
    create_db_and_tables()

    u = User(email='siema@siema.pl', password='siema')
    with Session(engine) as session:
        session.add(u)
        session.commit()