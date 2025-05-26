from . import ReadOnlyModel
from sqlalchemy import Column, String

class UserModel(ReadOnlyModel):
    __bind_key__ = ""
    __tablename__ = "user"

    # 用户id
    user_id = Column("user_id", String(128), primary_key=True, comment="# 用户id")
    # 用户名
    username = Column("username", String(256), nullable=False, default=None, comment="# 用户名")
    # 邮箱
    email = Column("email", String(256), nullable=False, default=None, comment="# 邮箱")
    
    def __repr__(self):
        return f"{self.__tablename__}:{self.user_id}"
