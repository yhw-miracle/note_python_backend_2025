from . import ReadWriteModel
from sqlalchemy import Column, String, Text

class AboutMeModel(ReadWriteModel):
    __bind_key__ = ""
    __tablename__ = "about_me"

    # 关于我id
    about_me_id = Column("about_me_id", String(128), primary_key=True, comment="# 关于我id")
    # 内容
    content = Column("content", Text, nullable=False, default=None, comment="# 内容")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.about_me_id}"
