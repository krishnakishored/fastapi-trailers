from pydantic import BaseModel

class NoteSchema(BaseModel):
    # NoteSchema will be used for validating the payloads for creating and updating notes.
    title: str
    description: str


class NoteDB(NoteSchema):
    #pydantic model for use as response_model
    id:int