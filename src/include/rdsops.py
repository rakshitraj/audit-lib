from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

class RDSOps:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.metadata = MetaData(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @classmethod
    def connect(cls, db_url: str, username: str, password: str):
        auth_url = db_url.replace("://", f"://{username}:{password}@")
        engine = create_engine(db_url)
        metadata = MetaData(bind=self.engine)
        session = sessionmaker(bind=self.engine)
        return session()

    @classmethod
    def insert_record(cls, session, table, record: dict):
        with session() as Session:
            Session.execute(table.insert().values(**record))
            Session.commit()

    @classmethod
    def close(cls, session):
        session().close