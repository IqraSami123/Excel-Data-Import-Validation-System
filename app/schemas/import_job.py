from datetime import datetime

from pydantic import BaseModel


class ImportJobResponse(BaseModel):
    id: int
    filename: str
    status: str
    total_records: int
    processed_records: int
    valid_records: int
    invalid_records: int
    imported_records: int
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

    model_config = {
        "from_attributes": True    # this will allow the model to be created from the attributes of the ImportJob model
    }