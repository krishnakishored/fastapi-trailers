from pydantic import BaseModel, Field

class NoteSchema(BaseModel):
    # NoteSchema will be used for validating the payloads for creating and updating notes.
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    #pydantic model for use as response_model
    id:int