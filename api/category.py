from flask import Blueprint, jsonify, request
from models import get_note_db_session
from sqlalchemy import Select, Update, Delete
from models.category import CategoryModel
from models.note import NoteModel
from models.tag import TagModel
from models.tag_note import TagNoteModel
from models.file import FileModel
from models.file_note import FileNoteModel
from schemas.category import CategorySchema, AddCategorySchema, ModifyCategorySchema, GetCategorySchema
from schemas.note import NoteSchema
from schemas.tag import TagSchema
from schemas.tag_note import TagNoteSchema
from schemas.file import FileSchema
from schemas.file_note import FileNoteSchema
from utils import get_hash_token
from datetime import datetime
from api import get_full_category


category_api = Blueprint("category_api",  "note")

# 新增分类
@category_api.route("/add", methods=["POST"])
def add_category():
    params = request.json
    add_category_schema = AddCategorySchema(many=False)
    try:
        params_validate = add_category_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    name = params_validate["name"]
    description = params_validate["description"]
    now_datetime = datetime.now()
    create_time = now_datetime.timestamp()
    category_id = get_hash_token(f"{name}_{create_time}")
    category_model_select_expression = Select(CategoryModel).filter(CategoryModel.name == name)
    is_exist_category_info = note_db_session.execute(category_model_select_expression).scalars().all()
    if len(is_exist_category_info) == 0:
        new_category = CategoryModel(category_id=category_id, name=name, description=description, create_time=create_time)
        note_db_session.add(new_category)
        note_db_session.commit()

        category_model_select_expression = Select(CategoryModel).filter(CategoryModel.category_id == category_id)
        category_info = note_db_session.execute(category_model_select_expression).scalars().first()
        category_schema = CategorySchema(many=False)
        category_result = category_schema.dump(category_info)
        category_result = get_full_category(note_db_session, category_result)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": category_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"分类名 {name} 已存在!"
        })

# 修改分类
@category_api.route("/modify", methods=["POST"])
def modify_category():
    params = request.json
    modify_category_schema = ModifyCategorySchema(many=False)
    try:
        params_validate = modify_category_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    category_id = params_validate["category_id"]
    name = params_validate["name"]
    description = params_validate["description"]
    now_datetime = datetime.now()
    update_time = now_datetime.timestamp()

    category_model_select_expression = Select(CategoryModel).filter(CategoryModel.category_id == category_id)
    category_info = note_db_session.execute(category_model_select_expression).scalars().first()
    category_schema = CategorySchema(many=False)
    is_exist_category_result = category_schema.dump(category_info)
    if len(is_exist_category_result) > 0:
        category_model_update_expression = Update(CategoryModel).filter(
            CategoryModel.category_id == category_id
        ).values(
            name=name, 
            description=description, 
            update_time=update_time
        )
        note_db_session.execute(category_model_update_expression)
        note_db_session.commit()

        category_model_select_expression = Select(CategoryModel).filter(CategoryModel.category_id == category_id)
        category_info = note_db_session.execute(category_model_select_expression).scalars().first()
        category_schema = CategorySchema(many=False)
        category_result = category_schema.dump(category_info)
        category_result = get_full_category(note_db_session, category_result)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": category_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"分类信息 {category_id} 不存在!",
        })

# 删除分类
@category_api.route("/del", methods=["POST"])
def del_category():
    params = request.json
    get_category_schema = GetCategorySchema(many=False)
    try:
        params_validate = get_category_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    category_id = params_validate["category_id"]

    note_db_session = get_note_db_session()

    category_model_delete_expression = Delete(CategoryModel).filter(CategoryModel.category_id == category_id)
    note_db_session.execute(category_model_delete_expression)
    note_db_session.commit()

    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 查询分类
@category_api.route("", methods=["POST"])
def get_category():
    params = request.json
    get_category_schema = GetCategorySchema(many=False)

    note_db_session = get_note_db_session()

    try:
        params_validate = get_category_schema.load(params)
        category_id = params_validate["category_id"]
        category_model_select_expression = Select(CategoryModel).filter(CategoryModel.category_id == category_id)
        category_info = note_db_session.execute(category_model_select_expression).scalars().first()
        category_schema = CategorySchema(many=False)
    except Exception as e:
        category_model_select_expression = Select(CategoryModel)
        category_info = note_db_session.execute(category_model_select_expression).scalars().all()
        category_schema = CategorySchema(many=True)
    
    category_result = category_schema.dump(category_info)

    if isinstance(category_result, list):
        full_category_result = list()
        for category_result_item in category_result:
            full_category_result.append(get_full_category(note_db_session, category_result_item))
        category_result = full_category_result
    else:
        category_result = get_full_category(note_db_session, category_result)

    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": category_result
    })
