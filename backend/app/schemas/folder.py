from pydantic import BaseModel


class FolderCreate(BaseModel):
    folder_name: str
    folder_path: str