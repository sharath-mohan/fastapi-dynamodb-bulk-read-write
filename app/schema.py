from pydantic import BaseModel
from uuid import UUID, uuid4

class Item(BaseModel):
    search_id: UUID

    model_config = {
        "json_schema_extra":{
            "examples":[
                {
                    "search_id": uuid4()
                }
            ]
        }
    }
