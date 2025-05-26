import os
from sqlalchemy import String, Integer, Float, DateTime
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
from marshmallow import fields

def save_schemas_init_code():
    schemas_init_code = [
        'from flask import current_app',
        'from flask_marshmallow import Marshmallow',
        'from marshmallow import fields, ValidationError, post_dump',
        'from typing import AbstractSet, Any, Iterable, Mapping, Optional, Sequence, Union',
        '',
        'marshmallow_obj = Marshmallow()',
        '',
        '',
        'class NotEmptyString(fields.String):',
        '\tdef _deserialize(self, value, attr, data, **kwargs):',
        '\t\tvalue = super()._deserialize(value, attr, data, **kwargs)',
        '\t\tif not value or value.strip() == "":',
        '\t\t\traise ValidationError("参数不能为空!")',
        '\t\treturn value',
        '',
        '',
        'class BaseSchema(marshmallow_obj.Schema):',
        '\tdef dump(self, obj:Any, *, many:Optional[bool] = None):',
        '\t\tresult = super().dump(obj, many=many)',
        '\t\t# current_app.logger.info(f"dump => {self.__class__.__name__} {result}")',
        '\t\treturn result',
        '',
        '\tdef load(self, data:Union[Mapping[str, Any], Iterable[Mapping[str, Any]]], *, many:Optional[bool] = None, partial:Union[bool, Sequence[str], AbstractSet[str], None] = None, unknown:Union[str, None] = None):',
        '\t\tresult = super().load(data, many=many, partial=partial, unknown=unknown)',
        '\t\t# current_app.logger.info(f"load => {self.__class__.__name__} {result}")',
        '\t\treturn result',
        '',
        '\t@post_dump',
        '\tdef remove_none_fields(self, data, **kwargs):',
        '\t\t# Remove None fields',
        '\t\treturn {k: v for k, v in data.items() if v is not None}'
    ]
    save_schema_code("__init__", schemas_init_code)

def main_core(data_model_class):
    type_mapping = {
        String: fields.String,
        Integer: fields.Integer,
        Float: fields.Float,
        DateTime: fields.DateTime
    }
    
    table_name = data_model_class.__tablename__

    column_names = [column.name for column in data_model_class.__table__.columns]
    primary_key_column_names = [column.name for column in data_model_class.__table__.columns if column.primary_key is True]
    
    schema_code = ['from schemas import BaseSchema, NotEmptyString', 'from marshmallow import fields', '', '']
    schema_code1 = [f'class {table_name.title().replace("_", "")}Schema(BaseSchema):']
    if len(primary_key_column_names) == 1:
        if table_name not in ["note"]:
            add_schema_code = [f'class Add{table_name.title().replace("_", "")}Schema(BaseSchema):']
            modify_schema_code = [f'class Modify{table_name.title().replace("_", "")}Schema(BaseSchema):']
        get_schema_code = [f'class Get{table_name.title().replace("_", "")}Schema(BaseSchema):']
    
    for column in data_model_class.__table__.columns:
        # print(f"Column: {column.name}, Type: {column.type}, Nullable: {column.nullable}, Default: {column.default}, Primary Key: {column.primary_key}, doc: {column.comment}")
        name = column.name
        column_type = column.type
        field_type = type_mapping.get(type(column_type), fields.Raw)
        comment = column.comment
        field_kwargs1 = dict()
        field_kwargs2 = dict()
        if column.nullable:
            field_kwargs1["allow_none"] = True
        else:
            field_kwargs1["required"] = True
            field_kwargs2["required"] = True
        if column.default is not None:
            field_kwargs1["default"] = column.default
        field_kwargs_str1 = ", ".join([f"{key}={repr(value)}" for key, value in field_kwargs1.items()])
        field_kwargs_str2 = ", ".join([f"{key}={repr(value)}" for key, value in field_kwargs2.items()])
        if comment is not None:
            schema_code1.append(f"    {comment}")
            if len(primary_key_column_names) == 1:
                if table_name not in ["note"]:
                    if name not in ["create_time", "update_time"] and column.primary_key is False:
                        add_schema_code.append(f"    {comment}")
                    if "update_time" in column_names and name not in ["create_time", "update_time"]:
                        modify_schema_code.append(f"    {comment}")
                if column.primary_key is True:
                    get_schema_code.append(f"    {comment}")
        schema_code1.append(f"    {name} = fields.{field_type.__name__}({field_kwargs_str1})")
        if len(primary_key_column_names) == 1:
            if table_name not in ["note"]:
                if name not in ["create_time", "update_time"] and column.primary_key is False:
                    if column.nullable:
                        add_schema_code.append(f"    {name} = fields.{field_type.__name__}({field_kwargs_str2})")
                    else:
                        add_schema_code.append(f"    {name} = NotEmptyString({field_kwargs_str2})")
                if "update_time" in column_names and name not in ["create_time", "update_time"]:
                    if column.nullable:
                        modify_schema_code.append(f"    {name} = fields.{field_type.__name__}({field_kwargs_str2})")
                    else:
                        modify_schema_code.append(f"    {name} = NotEmptyString({field_kwargs_str2})")
            if column.primary_key is True:
                if column.nullable:
                    get_schema_code.append(f"    {name} = fields.{field_type.__name__}({field_kwargs_str1})")
                else:
                    get_schema_code.append(f"    {name} = NotEmptyString({field_kwargs_str1})")
    schema_code.extend(schema_code1)
    schema_code.append("")
    if len(primary_key_column_names) == 1:
        if table_name not in ["note"]:
            schema_code.extend(add_schema_code)
            schema_code.append("")
            if "update_time" in column_names:
                schema_code.extend(modify_schema_code)
                schema_code.append("")
        schema_code.extend(get_schema_code)
        schema_code.append("")
    save_schema_code(table_name, schema_code)

def save_schema_code(table_name, schema_code, schemas_dir = os.path.join(os.getcwd(), "schemas")):
    os.makedirs(schemas_dir, exist_ok=True)
    with open(os.path.join(schemas_dir, f"{table_name}.py"), "w", encoding="utf-8") as f:
        f.write("\n".join(schema_code))

def main():
    save_schemas_init_code()
    data_models = [
        CategoryModel, NoteModel, FileModel, TagModel, TagNoteModel, FileNoteModel, CommentModel, UserModel, AboutMeModel, FriendLinkModel, VisitInfoModel, VisitLocationModel
    ]
    for index, data_model in enumerate(data_models):
        main_core(data_model)


if __name__ == "__main__":
    main()
