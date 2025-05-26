from flask import Blueprint, jsonify, request
from models import get_note_db_session
from sqlalchemy import Select, Update, Delete
from models.tag import TagModel
from schemas.tag import TagSchema, AddTagSchema, ModifyTagSchema, GetTagSchema
from utils import get_hash_token
from datetime import datetime
from api import get_full_tag


tag_api = Blueprint("tag_api",  "note")

# 新增标签
@tag_api.route("/add", methods=["POST"])
def add_tag():
    params = request.json
    add_tag_schema = AddTagSchema(many=False)
    try:
        params_validate = add_tag_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    name = params_validate["name"]
    now_datetime = datetime.now()
    create_time = now_datetime.timestamp()
    tag_id = get_hash_token(f"{name}_{create_time}")
    tag_model_select_expression = Select(TagModel).filter(TagModel.name == name)
    is_exist_tag_info = note_db_session.execute(tag_model_select_expression).scalars().all()
    if len(is_exist_tag_info) == 0:
        new_tag = TagModel(tag_id=tag_id, name=name, create_time=create_time)
        note_db_session.add(new_tag)
        note_db_session.commit()

        tag_model_select_expression = Select(TagModel).filter(TagModel.tag_id == tag_id)
        tag_info = note_db_session.execute(tag_model_select_expression).scalars().first()
        tag_schema = TagSchema(many=False)
        tag_result = tag_schema.dump(tag_info)
        tag_result = get_full_tag(note_db_session, tag_result)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": tag_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"标签名 {name} 已存在!"
        })

# 修改标签
@tag_api.route("/modify", methods=["POST"])
def modify_tag():
    params = request.json
    modify_tag_schema = ModifyTagSchema(many=False)
    try:
        params_validate = modify_tag_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    tag_id = params_validate["tag_id"]
    name = params_validate["name"]
    now_datetime = datetime.now()
    update_time = now_datetime.timestamp()

    tag_model_update_expression = Update(TagModel).filter(
        TagModel.tag_id == tag_id
    ).values(
        name=name, 
        update_time=update_time
    )
    note_db_session.execute(tag_model_update_expression)
    note_db_session.commit()

    tag_model_select_expression = Select(TagModel).filter(TagModel.tag_id == tag_id)
    tag_info = note_db_session.execute(tag_model_select_expression).scalars().first()
    tag_schema = TagSchema(many=False)
    tag_result = tag_schema.dump(tag_info)
    tag_result = get_full_tag(note_db_session, tag_result)

    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": tag_result
    })

# 删除标签
@tag_api.route("/del", methods=["POST"])
def del_tag():
    params = request.json
    get_tag_schema = GetTagSchema(many=False)
    try:
        params_validate = get_tag_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    tag_id = params_validate["tag_id"]

    note_db_session = get_note_db_session()

    tag_model_delete_expression = Delete(TagModel).filter(TagModel.tag_id == tag_id)
    note_db_session.execute(tag_model_delete_expression)
    note_db_session.commit()

    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 查询标签
@tag_api.route("", methods=["POST"])
def get_tag():
    params = request.json
    get_tag_schema = GetTagSchema(many=False)

    note_db_session = get_note_db_session()

    try:
        params_validate = get_tag_schema.load(params)
        tag_id = params_validate["tag_id"]
        tag_model_select_expression = Select(TagModel).filter(TagModel.tag_id == tag_id)
        tag_info = note_db_session.execute(tag_model_select_expression).scalars().first()
        tag_schema = TagSchema(many=False)
    except Exception as e:
        tag_model_select_expression = Select(TagModel)
        tag_info = note_db_session.execute(tag_model_select_expression).scalars().all()
        tag_schema = TagSchema(many=True)
    tag_result = tag_schema.dump(tag_info)
    if isinstance(tag_result, list):
        full_tag_result = list()
        for tag_result_item in tag_result:
            full_tag_result.append(get_full_tag(note_db_session, tag_result_item))
        tag_result = full_tag_result
    else:
        tag_result = get_full_tag(note_db_session, tag_result)
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": tag_result
    })
