import os
import shutil
from flask import Blueprint, jsonify, request, current_app
from models import get_note_db_session
from sqlalchemy import Select, Update, Delete
from sqlalchemy.orm.session import Session
from models.category import CategoryModel
from models.tag import TagModel
from models.note import NoteModel
from models.tag_note import TagNoteModel
from models.file_note import FileNoteModel
from models.comment import CommentModel
from schemas.category import CategorySchema
from schemas.tag import TagSchema
from schemas.note import NoteSchema, GetNoteSchema
from schemas.update_note import AddNoteSchema, AddNoteSchema1, ModifyNoteSchema
from schemas.tag_note import TagNoteSchema
from schemas.file_note import FileNoteSchema
from utils import get_hash_token
from datetime import datetime
from api import get_full_note


note_api = Blueprint("note_api",  "note")

def get_note_path(note_id, title, create_time):
    create_datetime = datetime.fromtimestamp(create_time)
    note_path = os.path.join(current_app.config["DATA"]["DATA_FOLDER"], f"{create_datetime.year}", f"{create_datetime.month}", f"{create_datetime.day}", note_id, f"{title}.md")
    os.makedirs(os.path.dirname(note_path), exist_ok=True)
    return note_path

def del_note_core(note_db_session:Session, note_id):
    note_model_select_expression = Select(NoteModel).filter(NoteModel.note_id == note_id)
    note_info = note_db_session.execute(note_model_select_expression).scalars().first()
    if note_info is None:
        return
    note_schema = NoteSchema(many=False)
    note_result = note_schema.dump(note_info)
    note_path = os.path.join(current_app.config["WORK_FOLDER"], note_result["path"])
    if os.path.exists(note_path):
        # 删除文件
        delete_note_dir = os.path.join(current_app.config["DELETE"]["DELETE_FOLDER"], os.path.relpath(os.path.dirname(note_path), current_app.config["WORK_FOLDER"]))
        os.makedirs(os.path.dirname(delete_note_dir), exist_ok=True)
        shutil.move(os.path.dirname(note_path), delete_note_dir)

        # 删除表记录
        tag_note_delete_expression = Delete(TagNoteModel).filter(TagNoteModel.note_id == note_id)
        note_db_session.execute(tag_note_delete_expression)
        note_db_session.commit()

        file_note_delete_expression = Delete(FileNoteModel).filter(FileNoteModel.note_id == note_id)
        note_db_session.execute(file_note_delete_expression)
        note_db_session.commit()

        comment_delete_expression = Delete(CommentModel).filter(CommentModel.note_id == note_id)
        note_db_session.execute(comment_delete_expression)
        note_db_session.commit()

        note_model_delete_expression = Delete(NoteModel).filter(NoteModel.note_id == note_id)
        note_db_session.execute(note_model_delete_expression)
        note_db_session.commit()

def update_files_by_note_id(note_db_session:Session, files, note_id, create_time):
    update_file_ids = [file_item["file_id"] for file_item in files]
    file_note_model_select_expression = Select(FileNoteModel).filter(FileNoteModel.note_id == note_id)
    source_file_note_info = note_db_session.execute(file_note_model_select_expression).scalars().all()
    file_note_schema = FileNoteSchema(many=True)
    source_file_note_result = file_note_schema.dump(source_file_note_info)
    for source_file_note_item in source_file_note_result:
        if source_file_note_item["file_id"] not in update_file_ids:
            # 删除表记录
            file_note_model_delete_expression = Delete(FileNoteModel).filter(FileNoteModel.file_id == source_file_note_item["file_id"], FileNoteModel.note_id == note_id)
            note_db_session.execute(file_note_model_delete_expression)
            note_db_session.commit()

    for file_item in files:
        file_note_model_select_expression = Select(FileNoteModel).filter(FileNoteModel.file_id == file_item["file_id"], FileNoteModel.note_id == note_id)
        is_exist_file_note_info = note_db_session.execute(file_note_model_select_expression).scalars().all()
        if len(is_exist_file_note_info) == 0:
            new_file_note = FileNoteModel(file_id=file_item["file_id"], note_id=note_id, create_time=create_time)
            note_db_session.add(new_file_note)
            note_db_session.commit()

def update_tags_by_note_id(note_db_session:Session, tags, note_id, create_time):
    update_tag_ids = [tag_item["tag_id"] for tag_item in tags]
    tag_note_model_select_expression = Select(TagNoteModel).filter(TagNoteModel.note_id == note_id)
    source_tag_note_info = note_db_session.execute(tag_note_model_select_expression).scalars().all()
    tag_note_schema = TagNoteSchema(many=True)
    source_tag_note_result = tag_note_schema.dump(source_tag_note_info)
    for source_tag_note_item in source_tag_note_result:
        if source_tag_note_item["tag_id"] not in update_tag_ids:
            # 删除表记录
            tag_note_model_delete_expression = Delete(TagNoteModel).filter(TagNoteModel.tag_id == source_tag_note_item["tag_id"], TagNoteModel.note_id == note_id)
            note_db_session.execute(tag_note_model_delete_expression)
            note_db_session.commit()

    for tag_item in tags:
        tag_note_model_select_expression = Select(TagNoteModel).filter(TagNoteModel.tag_id == tag_item["tag_id"], TagNoteModel.note_id == note_id)
        is_exist_tag_note_info = note_db_session.execute(tag_note_model_select_expression).scalars().all()
        if len(is_exist_tag_note_info) == 0:
            new_tag_note = TagNoteModel(tag_id=tag_item["tag_id"], note_id=note_id, create_time=create_time)
            note_db_session.add(new_tag_note)
            note_db_session.commit()

# 新增笔记
@note_api.route("/add", methods=["POST"])
def add_note():
    params = request.json
    add_note_schema = AddNoteSchema(many=False)
    try:
        params_validate = add_note_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    content = params_validate["content"]
    content_hash = get_hash_token(content)
    title = params_validate["title"]
    category_id = params_validate["category_id"]
    now_datetime = datetime.now()
    create_time = now_datetime.timestamp()

    note_id = get_hash_token(f"{content}_{create_time}")
    note_path = get_note_path(note_id, title, create_time)
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(content)

    note_db_session = get_note_db_session()
    note_model_select_expression = Select(NoteModel).filter(NoteModel.content_hash == content_hash)
    is_exist_note_info = note_db_session.execute(note_model_select_expression).scalars().all()
    if len(is_exist_note_info) == 0:
        new_note = NoteModel(
            note_id=note_id, 
            title=title, 
            content_hash=content_hash,
            path=os.path.relpath(note_path, current_app.config["WORK_FOLDER"]), 
            category_id=category_id, 
            create_time=create_time
        )
        note_db_session.add(new_note)
        note_db_session.commit()

        files = params_validate["files"]
        update_files_by_note_id(note_db_session, files, note_id, create_time)

        tags = params_validate["tags"]
        update_tags_by_note_id(note_db_session, tags, note_id, create_time)

        note_model_select_expression = Select(NoteModel).filter(NoteModel.note_id == note_id)
        note_info = note_db_session.execute(note_model_select_expression).scalars().first()
        note_schema = NoteSchema(many=False)
        note_result = note_schema.dump(note_info)
        note_result = get_full_note(note_db_session, note_result, is_get_category=True, is_get_tags=True, is_get_files=True, is_get_content=True, is_get_comment=True)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": note_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"笔记 {title} 已存在!"
        })
    
@note_api.route("/add1", methods=["POST"])
def add1_note():
    params = request.json
    add_note_schema = AddNoteSchema1(many=False)
    try:
        params_validate = add_note_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    content = params_validate["content"]
    content_hash = get_hash_token(content)
    title = params_validate["title"]
    category = params_validate["category"]
    now_datetime = datetime.now()
    create_time = now_datetime.timestamp() if "create_time" not in params_validate else params_validate["create_time"]
    note_db_session = get_note_db_session()

    category_model_select_expression = Select(CategoryModel).filter(CategoryModel.name == category)
    is_exist_category_info = note_db_session.execute(category_model_select_expression).scalars().all()
    if len(is_exist_category_info) == 0:
        category_id = get_hash_token(f"{category}_{create_time}")
        new_category = CategoryModel(category_id=category_id, name=category, description=category, create_time=create_time)
        note_db_session.add(new_category)
        note_db_session.commit()
    else:
        category_model_select_expression = Select(CategoryModel).filter(CategoryModel.name == category)
        category_info = note_db_session.execute(category_model_select_expression).scalars().first()
        category_schema = CategorySchema(many=False)
        category_result = category_schema.dump(category_info)
        category_id = category_result["category_id"]
    
    tags = params_validate["tags"]
    full_tag_infos = list()
    for tag in tags:
        tag_name = tag["name"]
        tag_model_select_expression = Select(TagModel).filter(TagModel.name == tag_name)
        is_exist_tag_info = note_db_session.execute(tag_model_select_expression).scalars().all()
        if len(is_exist_tag_info) == 0:
            tag_id = get_hash_token(f"{tag_name}_{create_time}")
            new_tag = TagModel(tag_id=tag_id, name=tag_name, create_time=create_time)
            note_db_session.add(new_tag)
            note_db_session.commit()
        else:
            tag_model_select_expression = Select(TagModel).filter(TagModel.name == tag_name)
            tag_info = note_db_session.execute(tag_model_select_expression).scalars().first()
            tag_schema = TagSchema(many=False)
            tag_result = tag_schema.dump(tag_info)
            tag_id = tag_result["tag_id"]
        full_tag_infos.append({
            "tag_id": tag_id,
            "name": tag_name
        })

    note_id = get_hash_token(f"{content}_{create_time}")
    note_path = get_note_path(note_id, title, create_time)
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(content)

    note_model_select_expression = Select(NoteModel).filter(NoteModel.content_hash == content_hash)
    is_exist_note_info = note_db_session.execute(note_model_select_expression).scalars().all()
    if len(is_exist_note_info) == 0:
        new_note = NoteModel(
            note_id=note_id, 
            title=title, 
            content_hash=content_hash,
            path=os.path.relpath(note_path, current_app.config["WORK_FOLDER"]), 
            category_id=category_id, 
            create_time=create_time
        )
        note_db_session.add(new_note)
        note_db_session.commit()

        files = params_validate["files"]
        update_files_by_note_id(note_db_session, files, note_id, create_time)

        update_tags_by_note_id(note_db_session, full_tag_infos, note_id, create_time)

        note_model_select_expression = Select(NoteModel).filter(NoteModel.note_id == note_id)
        note_info = note_db_session.execute(note_model_select_expression).scalars().first()
        note_schema = NoteSchema(many=False)
        note_result = note_schema.dump(note_info)
        note_result = get_full_note(note_db_session, note_result, is_get_category=True, is_get_tags=True, is_get_files=True, is_get_content=True, is_get_comment=True)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": note_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"笔记 {title} 已存在!"
        })

# 修改笔记
@note_api.route("/modify", methods=["POST"])
def modify_note():
    params = request.json
    modify_note_schema = ModifyNoteSchema(many=False)
    try:
        params_validate = modify_note_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    note_id = params_validate["note_id"]
    title = params_validate["title"]
    content = params_validate["content"]
    category_id = params_validate["category_id"]

    note_db_session = get_note_db_session()
    note_model_select_expression = Select(NoteModel).filter(NoteModel.note_id == note_id)
    current_note_info = note_db_session.execute(note_model_select_expression).scalars().first()
    note_schema = NoteSchema(many=False)
    current_note_result = note_schema.dump(current_note_info)
    if len(current_note_result) > 0:
        old_note_path = os.path.join(current_app.config["WORK_FOLDER"], current_note_result["path"])
        note_path = os.path.join(os.path.dirname(old_note_path), f"{title}.md")
        old_title = current_note_result["title"]
        create_time = current_note_result["create_time"]
        update_time = current_note_result["update_time"] if "update_time" in current_note_result else None
        if os.path.exists(old_note_path):
            backup_note_dir = os.path.dirname(old_note_path)
            backup_note_path = os.path.join(backup_note_dir, f"{old_title}.{update_time}.md") if update_time is not None else os.path.join(backup_note_dir, f"{old_title}.{create_time}.md")
            shutil.copyfile(old_note_path, backup_note_path)
            with open(old_note_path, "w", encoding="utf-8") as f:
                f.write(content)
            shutil.move(old_note_path, note_path)
        else:
            return jsonify({
                "code": 400,
                "msg": f"笔记 {title} 文件不存在!"
            })
        
        now_datetime = datetime.now()
        update_time = now_datetime.timestamp()

        note_model_update_expression = Update(NoteModel).filter(
            NoteModel.note_id == note_id
        ).values(
            title=title, 
            path=os.path.relpath(note_path, current_app.config["WORK_FOLDER"]),
            category_id=category_id, 
            update_time=update_time
        )
        note_db_session.execute(note_model_update_expression)
        note_db_session.commit()

        files = params_validate["files"]
        update_files_by_note_id(note_db_session, files, note_id, update_time)

        tags = params_validate["tags"]
        update_tags_by_note_id(note_db_session, tags, note_id, update_time)

        note_model_select_expression = Select(NoteModel).filter(NoteModel.note_id == note_id)
        current_note_info = note_db_session.execute(note_model_select_expression).scalars().first()
        note_schema = NoteSchema(many=False)
        current_note_result = note_schema.dump(current_note_info)
        current_note_result = get_full_note(note_db_session, current_note_result, is_get_category=True, is_get_tags=True, is_get_files=True, is_get_content=True, is_get_comment=True)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": current_note_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"笔记 {title} 不存在!"
        })

# 删除笔记
@note_api.route("/del", methods=["POST"])
def del_note():
    params = request.json
    get_note_schema = GetNoteSchema(many=False)
    try:
        params_validate = get_note_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_id = params_validate["note_id"]

    note_db_session = get_note_db_session()
    update_files_by_note_id(note_db_session, [], note_id, None)
    update_tags_by_note_id(note_db_session, [], note_id, None)
    del_note_core(note_db_session, note_id)

    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 查询笔记
@note_api.route("", methods=["POST"])
def get_note():
    params = request.json
    get_note_schema = GetNoteSchema(many=False)

    note_db_session = get_note_db_session()

    note_model_select_expression = Select(NoteModel)

    try:
        params_validate = get_note_schema.load(params)
        note_id = params_validate["note_id"]
        note_model_select_expression = note_model_select_expression.filter(NoteModel.note_id == note_id)
        note_info = note_db_session.execute(note_model_select_expression).scalars().first()
        note_schema = NoteSchema(many=False)
    except Exception as e:
        note_info = note_db_session.execute(note_model_select_expression).scalars().all()
        note_schema = NoteSchema(many=True)
    
    note_result = note_schema.dump(note_info)
    if isinstance(note_result, list):
        full_note_result = list()
        for note_result_item in note_result:
            full_note_result.append(get_full_note(note_db_session, note_result_item, is_get_category=True, is_get_tags=True, is_get_files=True, is_get_content=False, is_get_comment=False))
        note_result = full_note_result
    else:
        note_result = get_full_note(note_db_session, note_result, is_get_category=True, is_get_tags=True, is_get_files=True, is_get_content=True, is_get_comment=True)
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": note_result
    })
