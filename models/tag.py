from . import ReadWriteModel
from sqlalchemy import Column, String


class TagModel(ReadWriteModel):
    __bind_key__ = ""
    __tablename__ = "tag"

    # 标签id
    tag_id = Column("tag_id", String(128), primary_key=True, comment="# 标签id")
    # 标签名
    name = Column("name", String(256), nullable=False, default=None, comment="# 标签名")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.tag_id}"
