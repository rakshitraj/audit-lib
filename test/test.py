import unittest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import Table, Column, Integer, String, MetaData
from src.include.rdsops import RDSOps

class TestRDSOps(unittest.TestCase):
    def setUp(self):
        # Start a PostgreSQL container
        self.postgres_container = PostgresContainer("postgres:15")
        self.postgres_container.start()

        # Get connection details
        self.db_url = self.postgres_container.get_connection_url()
        self.username = "test"
        self.password = "test"

        # Initialize RDSOps
        self.rds_ops = RDSOps(self.db_url)

        # Create a test schema and table
        self.metadata = MetaData(bind=self.rds_ops.engine)
        self.test_table = Table(
            "test_table",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String, nullable=False),
            schema="test_schema"
        )
        self.metadata.create_all()

    def tearDown(self):
        # Drop the schema and stop the container
        self.metadata.drop_all()
        self.rds_ops.close()
        self.postgres_container.stop()

    def test_insert_record(self):
        # Insert a record into the test table
        record = {"id": 1, "name": "Alice"}
        self.rds_ops.insert_record("test_schema.test_table", record)

        # Query the table to verify the record
        with self.rds_ops.Session() as session:
            result = session.execute("SELECT * FROM test_schema.test_table").fetchall()
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "Alice")

    def test_close(self):
        # Ensure the engine is disposed of when close is called
        self.rds_ops.close()
        with self.assertRaises(Exception):
            self.rds_ops.engine.connect()

    def test_connect_classmethod(self):
        # Test the connect class method
        session = RDSOps.connect(self.db_url, self.username, self.password)
        self.assertIsNotNone(session)

if __name__ == "__main__":
    unittest.main()