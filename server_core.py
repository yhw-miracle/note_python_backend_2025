from flask import Flask
from utils import note_config_parser_obj, default_note_settings_filepath
from settings import NoteConfig
from log import register_logging
from models import sqlalchemy_obj
from schemas import marshmallow_obj
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import create_session
from sqlalchemy.schema import CreateTable
from models.category import CategoryModel
from models.note import NoteModel
from models.file import FileModel
from models.tag import TagModel
from models.tag_note import TagNoteModel
from models.file_note import FileNoteModel
from models.comment import CommentModel
from models.user import UserModel
from models.about_me import AboutMeModel
from models.friend_link import FriendLinkModel
from models.visitor import VisitInfoModel, VisitLocationModel
from api.category import category_api
from api.tag import tag_api
from api.file import file_api
from api.note import note_api
from api.user import user_api
from api.comment import comment_api
from api.about_me import about_me_api
from api.friend_link import friend_link_api
from api.visit_info import visit_info_api
from api.visit_location import visit_location_api

def create_tables(app):
    note_db_engine = create_engine(app.config["SQLALCHEMY_BINDS"]["note"])
    note_db_session = create_session(bind=note_db_engine)

    data_models = [
        CategoryModel, NoteModel, FileModel, TagModel, TagNoteModel, FileNoteModel, CommentModel, UserModel, AboutMeModel, FriendLinkModel, VisitInfoModel, VisitLocationModel
    ]
    for index, data_model in enumerate(data_models):
        table_name = data_model.__tablename__
        if table_name not in inspect(note_db_engine).get_table_names():
            create_table_sql = text(str(CreateTable(data_model.__table__)))
            note_db_session.execute(create_table_sql)

def create_app():
    app = Flask("yhw-miracle-notes")

    # 配置信息
    note_config_obj = NoteConfig()
    app.config.from_object(note_config_obj)
    note_config_parser_obj.write_config_file(default_note_settings_filepath)
    # 日志
    register_logging(app)

    sqlalchemy_obj.init_app(app)
    
    marshmallow_obj.init_app(app)

    create_tables(app)

    app.register_blueprint(category_api, url_prefix="/api/category")
    app.register_blueprint(tag_api, url_prefix="/api/tag")
    app.register_blueprint(file_api, url_prefix="/api/file")
    app.register_blueprint(note_api, url_prefix="/api/note")
    app.register_blueprint(user_api, url_prefix="/api/user")
    app.register_blueprint(comment_api, url_prefix="/api/comment")
    app.register_blueprint(about_me_api, url_prefix="/api/about_me")
    app.register_blueprint(friend_link_api, url_prefix="/api/friend_link")
    app.register_blueprint(visit_info_api, url_prefix="/api/visit_info")
    app.register_blueprint(visit_location_api, url_prefix="/api/visit_location")
    
    return app
