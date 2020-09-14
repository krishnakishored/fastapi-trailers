import os
from sqlalchemy import (Column, Datetime, Integer, MetaData,String,Table,create_engine)
from sqlalchemy.sql import func
from databases import Database 

DATABASE_URL = os.getenv("DATABASE_URL")

#SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# notes model
notes = Table(
    "notes",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("title",String(50)),
    Column("description",String(50)),
    Column("created_date",Datetime,default=func.now(),nullable=False)
)






# databases query builder
database = Database(DATABASE_URL)

