import os
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy import create_engine, Column, Float, text
from sqlalchemy.orm import create_session
from sqlalchemy.schema import CreateTable
from datetime import datetime
from utils import get_sqlite_prefix

sqlalchemy_obj = SQLAlchemy()

def get_note_db_session():
    note_db_engine = create_engine(current_app.config["SQLALCHEMY_BINDS"]["note"])
    note_db_session = create_session(bind=note_db_engine)
    return note_db_session

def get_visit_info_db_session():
    now_datetime = datetime.now()
    visit_info_db_filepath = os.path.join(current_app.config["DATA"]["VISIT_INFO_DB_FOLDER"], f'{now_datetime.strftime("%Y%m%d")}.db')
    visit_info_db_engine = create_engine(f"{get_sqlite_prefix()}{visit_info_db_filepath}")
    visit_info_db_session = create_session(bind=visit_info_db_engine)
    if os.path.exists(visit_info_db_filepath) is False:
        from .visitor import VisitInfoModel, VisitLocationModel
        for data_model in [VisitInfoModel, VisitLocationModel]:
            create_table_sql = text(str(CreateTable(data_model.__table__)))
            visit_info_db_session.execute(create_table_sql)
    return visit_info_db_session

class ReadOnlyModel(sqlalchemy_obj.Model):
    __abstract__ = True

    # 创建时间
    create_time = Column("create_time", Float, nullable=False, default=None, comment="# 创建时间")

class ReadWriteModel(sqlalchemy_obj.Model):
    __abstract__ = True

    # 创建时间
    create_time = Column("create_time", Float, nullable=False, default=None, comment="# 创建时间")
    # 更新时间
    update_time = Column("update_time", Float, nullable=True, default=None, comment="# 更新时间")
