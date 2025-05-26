from flask import Blueprint, jsonify, request
from models import get_note_db_session
from sqlalchemy import Select, Delete
from models.user import UserModel
from schemas.user import UserSchema, AddUserSchema, GetUserSchema
from utils import get_hash_token
from datetime import datetime


user_api = Blueprint("user_api",  "note")

# 新增用户
@user_api.route("/add", methods=["POST"])
def add_user():
    params = request.json
    add_user_schema = AddUserSchema(many=False)
    try:
        params_validate = add_user_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    username = params_validate["username"]
    email = params_validate["email"]
    now_datetime = datetime.now()
    create_time = now_datetime.timestamp()
    user_id = get_hash_token(f"{username}_{create_time}")
    user_model_select_expression = Select(UserModel).filter(UserModel.username == username)
    is_exist_user_info = note_db_session.execute(user_model_select_expression).scalars().all()
    if len(is_exist_user_info) == 0:
        new_user = UserModel(user_id=user_id, username=username, email=email, create_time=create_time)
        note_db_session.add(new_user)
        note_db_session.commit()

        user_model_select_expression = Select(UserModel).filter(UserModel.user_id == user_id)
        user_info = note_db_session.execute(user_model_select_expression).scalars().first()
        user_schema = UserSchema(many=False)
        user_result = user_schema.dump(user_info)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": user_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"用户名 {username} 已存在!"
        })

# 删除用户
@user_api.route("/del", methods=["POST"])
def del_user():
    params = request.json
    get_user_schema = GetUserSchema(many=False)
    try:
        params_validate = get_user_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    user_id = params_validate["user_id"]

    note_db_session = get_note_db_session()

    user_model_delete_expression = Delete(UserModel).filter(UserModel.user_id == user_id)
    note_db_session.execute(user_model_delete_expression)
    note_db_session.commit()

    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 查询用户
@user_api.route("", methods=["POST"])
def get_user():
    params = request.json
    get_user_schema = GetUserSchema(many=False)

    note_db_session = get_note_db_session()
    user_model_select_expression = Select(UserModel)
    try:
        params_validate = get_user_schema.load(params)
        user_id = params_validate["user_id"]
        user_model_select_expression = user_model_select_expression.filter(UserModel.user_id == user_id)
        user_info = note_db_session.execute(user_model_select_expression).scalars().first()
        user_schema = UserSchema(many=False)
    except Exception as e:
        user_info = note_db_session.execute(user_model_select_expression).scalars().all()
        user_schema = UserSchema(many=True)
    
    user_result = user_schema.dump(user_info)
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": user_result
    })
