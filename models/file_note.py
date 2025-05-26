from . import ReadOnlyModel
from sqlalchemy import Column, String


class FileNoteModel(ReadOnlyModel):
    __bind_key__ = ""
    __tablename__ = "file_note"

    # 文件id
    file_id = Column("file_id", String(128), primary_key=True, comment="# 文件id")
    # 笔记id
    note_id = Column("note_id", String(128), primary_key=True, comment="# 笔记id")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.file_id}:{self.note_id}"
