from . import ReadOnlyModel
from sqlalchemy import Column, String


class FileModel(ReadOnlyModel):
    __bind_key__ = ""
    __tablename__ = "file"

    # 文件id
    file_id = Column("file_id", String(128), primary_key=True, comment="# 文件id")
    # 文件类型
    file_type = Column("file_type", String(256), nullable=True, default=None, comment="# 文件类型")
    # 文件名称
    name = Column("name", String(256), nullable=False, default=None, comment="# 文件名称")
    # 文件路径
    path = Column("path", String(256), nullable=True, default=None, comment="# 文件路径")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.file_id}"
