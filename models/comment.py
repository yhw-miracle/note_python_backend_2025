from . import ReadOnlyModel
from sqlalchemy import Column, String, Text

class CommentModel(ReadOnlyModel):
    __bind_key__ = ""
    __tablename__ = "comment"

    # 评论id
    comment_id = Column("comment_id", String(128), primary_key=True, comment="# 评论id")
    # 评论内容
    content = Column("content", Text, nullable=False, default=None, comment="# 评论内容")
    # 笔记id
    note_id = Column("note_id", String(128), nullable=False, default=None, comment="# 笔记id")
    # 用户id
    user_id = Column("user_id", String(128), nullable=True, default=None, comment="# 用户id")
    # 父级评论
    parent_id = Column("parent_id", String(128), nullable=True, default=None, comment="# 父级评论")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.comment_id}"
