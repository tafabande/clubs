from sqlmodel import SQLModel, create_engine
from models import Club


DB_URL = 'sqlite:///clubs.db'


def init_db() -> None:
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
    print('Initialized database at clubs.db')
