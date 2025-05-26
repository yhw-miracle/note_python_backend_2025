from . import ReadWriteModel
from sqlalchemy import Column, String


class FriendLinkModel(ReadWriteModel):
    __bind_key__ = ""
    __tablename__ = "friend_link"

    # 友链id
    friend_link_id = Column("friend_link_id", String(128), primary_key=True, comment="# 友链id")
    # 友链名称
    name = Column("name", String(256), nullable=False, default=None, comment="# 友链名称")
    # 链接
    link = Column("link", String(256), nullable=False, default=None, comment="# 链接")
    # slogan
    description = Column("description", String(256), nullable=True, default=None, comment="# slogan")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.friend_link_id}"
