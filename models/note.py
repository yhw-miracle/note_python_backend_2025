from . import ReadWriteModel
from sqlalchemy import Column, String, Text


class NoteModel(ReadWriteModel):
    __bind_key__ = ""
    __tablename__ = "note"

    # 笔记id
    note_id = Column("note_id", String(128), primary_key=True, comment="# 笔记id")
    # 笔记标题
    title = Column("title", String(256), nullable=False, default=None, comment="# 笔记标题")
    # 笔记内容 hash
    content_hash = Column("content_hash", Text, nullable=False, default=None, comment="# 笔记内容 hash")
    # 笔记路径
    path = Column("path", String(256), nullable=False, default=None, comment="# 笔记路径")
    # 分类id
    category_id = Column("category_id", String(256), nullable=False, default=None, comment="# 分类id")
    

    def __repr__(self):
        return f"{self.__tablename__}:{self.note_id}"
