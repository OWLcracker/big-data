from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
# Hive
engine = create_engine('hive://localhost:10000/default')

# SQLAlchemy >= 2.0
metadata_obj = MetaData()
books = Table("books", metadata_obj, Column("id", Integer), Column("title", String), Column("primary_author", String))
metadata_obj.create_all(engine)
inspector = inspect(engine)
inspector.get_columns('books')

with engine.connect() as con:
    data = [{ "id": 1, "title": "The Hobbit", "primary_author": "Tolkien" },
            { "id": 2, "title": "The Silmarillion", "primary_author": "Tolkien" }]
    con.execute(books.insert(), data[0])
    result = con.execute(text("select * from books"))
    print(result.fetchall())
