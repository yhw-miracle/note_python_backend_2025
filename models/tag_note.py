from . import ReadOnlyModel
from sqlalchemy import Column, String


class TagNoteModel(ReadOnlyModel):
    __bind_key__ = ""
    __tablename__ = "tag_note"

    # 标签id
    tag_id = Column("tag_id", String(128), primary_key=True, comment="# 标签id")
    # 笔记id
    note_id = Column("note_id", String(128), primary_key=True, comment="# 笔记id")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.tag_id}:{self.note_id}"
