import os
import sys
import hashlib
from configparser import ConfigParser


work_dir = os.getcwd()

note_settings_filepath = os.path.join(work_dir, "note_settings.ini")
default_note_settings_filepath = os.path.join(work_dir, "default_note_settings.ini")

def get_hash_token(content):
    return hashlib.sha3_512(content.encode("utf-8")).hexdigest()

class NoteConfigParser(ConfigParser):
    """ 笔记后端配置文件解析器 """
    def optionxform(self, optionstr):
        return optionstr
    
    def read_sections_from_file(self, filepath):
        if os.path.exists(filepath):
            self.read(filepath, encoding="utf-8")
            return self.sections()
        return list()
    
    def read_options_from_file(self, filepath, section):
        if os.path.exists(filepath):
            self.read(filepath, encoding="utf-8")
            return self.options(section)
        return list()

    def read_value_from_file(self, filepath, section, option, option_type, default_value=None):
        if os.path.exists(filepath):
            self.read(filepath, encoding="utf-8")
            if self.has_section(section) and self.has_option(section, option):
                if option_type == "boolean":
                    return self.getboolean(section, option)
                if option_type == "int":
                    return self.getint(section, option)
                if option_type == "float":
                    return self.getfloat(section, option)
                if option_type == "str":
                    return self.get(section, option)
        return default_value
    
    def write_config_file(self, filepath):
        self.clear()
        from settings import NoteConfig
        note_config_obj = NoteConfig()
        for key in vars(note_config_obj):
            if key.isupper():
                value = getattr(note_config_obj, key)
                if isinstance(value, dict):
                    if key not in self.sections():
                        self.add_section(key)
                    for k, v in value.items():
                        self.set(key, k, str(v))
                else:
                    if "BASE" not in self.sections():
                        self.add_section("BASE")
                    self.set("BASE", key, str(value))
        self.write(open(filepath, "w", encoding="utf-8"))

note_config_parser_obj = NoteConfigParser()

def get_sqlite_prefix():
    if sys.platform.startswith("win"):
        return "sqlite:///"
    else:
        return "sqlite:////"
