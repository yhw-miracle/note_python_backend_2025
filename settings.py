import os
from utils import work_dir, get_hash_token, get_sqlite_prefix, note_config_parser_obj, note_settings_filepath

class NoteConfig(object):
    def __init__(self):
        self.WORK_FOLDER = note_config_parser_obj.read_value_from_file(note_settings_filepath, "BASE", "WORK_FOLDER", "str", work_dir)

        self.PROJECT_NAME = note_config_parser_obj.read_value_from_file(note_settings_filepath, "BASE", "PROJECT_NAME", "str", "yhw-miracle-note")

        self.SECRET_KEY = note_config_parser_obj.read_value_from_file(note_settings_filepath, "BASE", "SECRET_KEY", "str", get_hash_token(self.PROJECT_NAME))

        self.PORT = note_config_parser_obj.read_value_from_file(note_settings_filepath, "BASE", "PORT", "int", 20250)

        self.WORKERS = note_config_parser_obj.read_value_from_file(note_settings_filepath, "BASE", "WORKERS", "int", 100)

        # 数据
        self.DATA = {
            "DATA_FOLDER" : note_config_parser_obj.read_value_from_file(note_settings_filepath, "DATA", "DATA_FOLDER", "str", os.path.join(self.WORK_FOLDER, "data")),
            "VISIT_INFO_DB_FOLDER" : note_config_parser_obj.read_value_from_file(note_settings_filepath, "DATA", "VISIT_INFO_DB_FOLDER", "str", os.path.join(self.WORK_FOLDER, "data", "visit_info_db")),
        }
        os.makedirs(self.DATA["DATA_FOLDER"], exist_ok=True)
        os.makedirs(self.DATA["VISIT_INFO_DB_FOLDER"], exist_ok=True)
        self.SQLALCHEMY_RECORD_QUERIES = note_config_parser_obj.read_value_from_file(note_settings_filepath, "BASE", "SQLALCHEMY_RECORD_QUERIES", "bool", True)
        # self.SQLALCHEMY_DATABASE_URI = ""
        self.SQLALCHEMY_BINDS = {
            "note": f'{get_sqlite_prefix()}{self.DATA["DATA_FOLDER"]}/note.db'
        }

        # 日志
        self.LOG = {
            "LOG_FOLDER": note_config_parser_obj.read_value_from_file(note_settings_filepath, "LOG", "LOG_FOLDER", "str", os.path.join(self.WORK_FOLDER, "logs")),
        }
        self.LOG["DEBUG_LOG_FILEPATH"] = note_config_parser_obj.read_value_from_file(note_settings_filepath, "LOG", "DEBUG_LOG_FILEPATH", "str", os.path.join(self.LOG["LOG_FOLDER"], "DEBUG", "debug.log"))

        self.LOG["INFO_LOG_FILEPATH"] = note_config_parser_obj.read_value_from_file(note_settings_filepath, "LOG", "INFO_LOG_FILEPATH", "str", os.path.join(self.LOG["LOG_FOLDER"], "INFO", "info.log"))

        self.LOG["WARNING_LOG_FILEPATH"] = note_config_parser_obj.read_value_from_file(note_settings_filepath, "LOG", "WARNING_LOG_FILEPATH", "str", os.path.join(self.LOG["LOG_FOLDER"], "WARNING", "warning.log"))

        self.LOG["ERROR_LOG_FILEPATH"] = note_config_parser_obj.read_value_from_file(note_settings_filepath, "LOG", "ERROR_LOG_FILEPATH", "str", os.path.join(self.LOG["LOG_FOLDER"], "ERROR", "error.log"))

        self.LOG["CRITICAL_LOG_FILEPATH"] = note_config_parser_obj.read_value_from_file(note_settings_filepath, "LOG", "CRITICAL_LOG_FILEPATH", "str", os.path.join(self.LOG["LOG_FOLDER"], "CRITICAL", "critical.log"))

        os.makedirs(os.path.dirname(self.LOG["DEBUG_LOG_FILEPATH"]), exist_ok=True)
        os.makedirs(os.path.dirname(self.LOG["INFO_LOG_FILEPATH"]), exist_ok=True)
        os.makedirs(os.path.dirname(self.LOG["WARNING_LOG_FILEPATH"]), exist_ok=True)
        os.makedirs(os.path.dirname(self.LOG["ERROR_LOG_FILEPATH"]), exist_ok=True)
        os.makedirs(os.path.dirname(self.LOG["CRITICAL_LOG_FILEPATH"]), exist_ok=True)

        # 上传文件
        self.UPLOAD = {
            "UPLOAD_FOLDER": note_config_parser_obj.read_value_from_file(note_settings_filepath, "UPLOAD", "UPLOAD_FOLDER", "str", os.path.join(self.WORK_FOLDER, "upload")),
            "ALLOWED_EXTENSIONS": note_config_parser_obj.read_value_from_file(note_settings_filepath, "UPLOAD", "ALLOWED_EXTENSIONS", "str", "jpg;jpeg;png;gif;mp4;avi"),
            "MAX_CONTENT_LENGTH": note_config_parser_obj.read_value_from_file(note_settings_filepath, "UPLOAD", "MAX_CONTENT_LENGTH", "int", 10 * 1024 * 1024 * 1024),
            "CHUNK_SIZE": note_config_parser_obj.read_value_from_file(note_settings_filepath, "UPLOAD", "CHUNK_SIZE", "int", 1024 * 1024)
        }
        os.makedirs(self.UPLOAD["UPLOAD_FOLDER"], exist_ok=True)

        # 删除目录
        self.DELETE = {
            "DELETE_FOLDER": note_config_parser_obj.read_value_from_file(note_settings_filepath, "DELETE", "DELETE_FOLDER", "str", os.path.join(self.WORK_FOLDER, "delete")),
        }

        # IP location
        self.IP_LOCATION = {
            "HOST": "https://c2ba.api.huachen.cn",
            "PATH": "/ip",
            "APPCODE": "4e03e1811fc8436183ca42f77af65dd4",
            "QUERYS": "ip="
        }


if __name__ == "__main__":
    note_config_obj = NoteConfig()
    print(dir(NoteConfig), dir(note_config_obj))
    print(vars(NoteConfig).keys(), vars(note_config_obj).keys())
    # for key in dir(NoteConfig):
    #     if key.isupper():
    #         print(f"{key} => {getattr(note_config_obj, key)}")
