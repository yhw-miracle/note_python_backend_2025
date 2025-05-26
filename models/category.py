from models import ReadWriteModel
from sqlalchemy import Column, String


class CategoryModel(ReadWriteModel):
    __bind_key__ = ""
    __tablename__ = "category"

    # 分类id
    category_id = Column("category_id", String(128), primary_key=True, comment="# 分类id")
    # 分类名称
    name = Column("name", String(256), nullable=False, default=None, comment="# 分类名称")
    # 分类描述
    description = Column("description", String(256), nullable=False, default=None, comment="# 分类描述")

    def __repr__(self):
        return f"{self.__tablename__}:{self.category_id}"
