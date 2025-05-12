from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

class RDSOps:
    @classmethod
    def create_rds_engine(cls, username: str, password: str, host, port, database, namespace):
        try:
            db_uri = f"postgresql://{username}:{quote_plus(password)}@{host}:{port}/{database}"
            engine = create_engine(db_uri, connect_args= {
                'options': '-csearch_path={}'.format(namespace)},
                 pool_size=30)
            return engine
        except Exception as err:
            raise err
        
    @classmethod
    def get_rds_session(rds_engine):
        session = sessionmaker(bind=rds_engine)
        return session()
    
    @classmethod
    def close(cls, session):
        session().close

    @staticmethod
    def insert_record(cls, session, table, record: dict):
        with session() as Session:
            Session.execute(table.insert().values(**record))
            Session.commit()

    