from app.api.models import NoteSchema
from app.db import notes, database

async def post(payload:NoteSchema):
    '''
        Creates a SQLAlchemy insert object expression query
        Executes the query and returns the generated ID
    '''
    query = notes.insert().values(title=payload.title,description=payload.description)
    return await database.execute(query=query)