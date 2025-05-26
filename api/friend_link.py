from flask import Blueprint, jsonify, request
from models import get_note_db_session
from sqlalchemy import Select, Update, Delete
from models.friend_link import FriendLinkModel
from schemas.friend_link import FriendLinkSchema, AddFriendLinkSchema, ModifyFriendLinkSchema, GetFriendLinkSchema
from utils import get_hash_token
from datetime import datetime


friend_link_api = Blueprint("friend_link_api",  "note")

# 新增友链
@friend_link_api.route("/add", methods=["POST"])
def add_friend_link():
    params = request.json
    add_friend_link_schema = AddFriendLinkSchema(many=False)
    try:
        params_validate = add_friend_link_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    name = params_validate["name"]
    link = params_validate["link"]
    description = params_validate["description"]
    now_datetime = datetime.now()
    create_time = now_datetime.timestamp()
    friend_link_id = get_hash_token(f"{name}_{link}_{create_time}")
    
    friend_link_model_select_expression = Select(FriendLinkModel).filter(FriendLinkModel.name == name, FriendLinkModel.link == link)
    is_exist_friend_link_info = note_db_session.execute(friend_link_model_select_expression).scalars().all()
    if len(is_exist_friend_link_info) == 0:
        new_friend_link = FriendLinkModel(friend_link_id=friend_link_id, name=name, link=link, description=description, create_time=create_time)
        note_db_session.add(new_friend_link)
        note_db_session.commit()

        friend_link_model_select_expression = Select(FriendLinkModel)
        friend_link_info = note_db_session.execute(friend_link_model_select_expression).scalars().all()
        friend_link_schema = FriendLinkSchema(many=True)
        friend_link_result = friend_link_schema.dump(friend_link_info)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": friend_link_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"链接 {name}:{link} 已存在!"
        })

# 修改友链
@friend_link_api.route("/modify", methods=["POST"])
def modify_friend_link():
    params = request.json
    modify_friend_link_schema = ModifyFriendLinkSchema(many=False)
    try:
        params_validate = modify_friend_link_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    friend_link_id = params_validate["friend_link_id"]
    name = params_validate["name"]
    link = params_validate["link"]
    description = params_validate["description"]
    now_datetime = datetime.now()
    update_time = now_datetime.timestamp()

    friend_link_model_update_expression = Update(FriendLinkModel).filter(
        FriendLinkModel.friend_link_id == friend_link_id
    ).values(
        name=name, 
        link=link, 
        description=description, 
        update_time=update_time
    )
    note_db_session.execute(friend_link_model_update_expression)
    note_db_session.commit()

    friend_link_model_select_expression = Select(FriendLinkModel).filter(FriendLinkModel.friend_link_id == friend_link_id)
    friend_link_info = note_db_session.execute(friend_link_model_select_expression).scalars().first()
    friend_link_schema = FriendLinkSchema(many=False)
    friend_link_result = friend_link_schema.dump(friend_link_info)

    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": friend_link_result
    })

# 删除友链
@friend_link_api.route("/del", methods=["POST"])
def del_friend_link():
    params = request.json
    get_friend_link_schema = GetFriendLinkSchema(many=False)
    try:
        params_validate = get_friend_link_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    friend_link_id = params_validate["friend_link_id"]

    note_db_session = get_note_db_session()

    friend_link_model_delete_expression = Delete(FriendLinkModel).filter(FriendLinkModel.friend_link_id == friend_link_id)
    note_db_session.execute(friend_link_model_delete_expression)
    note_db_session.commit()

    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 查询友链
@friend_link_api.route("", methods=["POST"])
def get_friend_link():
    params = request.json
    get_friend_link_schema = GetFriendLinkSchema(many=False)

    note_db_session = get_note_db_session()

    try:
        params_validate = get_friend_link_schema.load(params)
        friend_link_id = params_validate["friend_link_id"]
        friend_link_model_select_expression = Select(FriendLinkModel).filter(FriendLinkModel.friend_link_id == friend_link_id)
        friend_link_info = note_db_session.execute(friend_link_model_select_expression).scalars().first()
        friend_link_schema = FriendLinkSchema(many=False)
    except Exception as e:
        friend_link_model_select_expression = Select(FriendLinkModel)
        friend_link_info = note_db_session.execute(friend_link_model_select_expression).scalars().all()
        friend_link_schema = FriendLinkSchema(many=True)
    
    friend_link_result = friend_link_schema.dump(friend_link_info)
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": friend_link_result
    })
