import pytest
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm.session import Session

from app.db import engine, init_db, get_db


class TestModels:
    def test_init_db_creates_tables(self):
        init_db()
        inspector = sqlalchemy.inspect(engine)
        table_names = inspector.get_table_names()
        assert len(table_names) > 0, "No tables were created in the database."

    def test_get_db_returns_session(self):
        db_gen = get_db()
        session = next(db_gen)

        assert isinstance(session, Session)

        result = session.execute(text("SELECT 1")).scalar()
        assert result == 1

        with pytest.raises(StopIteration):
            next(db_gen)
