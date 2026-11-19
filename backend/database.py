from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///movies.db"

# check_same_thread=False is needed for SQLite because FastAPI can
# handle a request on a different thread than the one that opened the connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_tables():
    SQLModel.metadata.create_all(engine)


# each request gets its own session, and it closes when the request is done
def get_session():
    with Session(engine) as session:
        yield session
