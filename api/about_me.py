from flask import Blueprint, jsonify, request
from models import get_note_db_session
from sqlalchemy import Select, Update, Delete
from models.about_me import AboutMeModel
from schemas.about_me import AboutMeSchema, AddAboutMeSchema, ModifyAboutMeSchema, GetAboutMeSchema
from utils import get_hash_token
from datetime import datetime


about_me_api = Blueprint("about_me_api",  "note")

# 新增关于我
@about_me_api.route("/add", methods=["POST"])
def add_about_me():
    params = request.json
    add_about_me_schema = AddAboutMeSchema(many=False)
    try:
        params_validate = add_about_me_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    content = params_validate["content"]
    now_datetime = datetime.now()
    create_time = now_datetime.timestamp()
    about_me_id = get_hash_token(f"{content}_{create_time}")
    about_me_model_select_expression = Select(AboutMeModel).filter(AboutMeModel.content == content)
    is_exist_about_me_info = note_db_session.execute(about_me_model_select_expression).scalars().all()
    if len(is_exist_about_me_info) == 0:
        new_about_me = AboutMeModel(about_me_id=about_me_id, content=content, create_time=create_time)
        note_db_session.add(new_about_me)
        note_db_session.commit()

        about_me_model_select_expression = Select(AboutMeModel)
        about_me_info = note_db_session.execute(about_me_model_select_expression).scalars().all()
        about_me_schema = AboutMeSchema(many=True)
        about_me_result = about_me_schema.dump(about_me_info)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": about_me_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"关于信息 {content} 已存在!"
        })

# 修改关于我
@about_me_api.route("/modify", methods=["POST"])
def modify_about_me():
    params = request.json
    modify_about_me_schema = ModifyAboutMeSchema(many=False)
    try:
        params_validate = modify_about_me_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    note_db_session = get_note_db_session()

    about_me_id = params_validate["about_me_id"]
    content = params_validate["content"]
    now_datetime = datetime.now()
    update_time = now_datetime.timestamp()

    about_me_model_update_expression = Update(AboutMeModel).filter(
        AboutMeModel.about_me_id == about_me_id
    ).values(
        content=content, 
        update_time=update_time
    )
    note_db_session.execute(about_me_model_update_expression)
    note_db_session.commit()

    about_me_model_select_expression = Select(AboutMeModel).filter(AboutMeModel.about_me_id == about_me_id)
    about_me_info = note_db_session.execute(about_me_model_select_expression).scalars().first()
    about_me_schema = AboutMeSchema(many=False)
    about_me_result = about_me_schema.dump(about_me_info)

    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": about_me_result
    })

# 删除关于我
@about_me_api.route("/del", methods=["POST"])
def del_about_me():
    params = request.json
    get_about_me_schema = GetAboutMeSchema(many=False)
    try:
        params_validate = get_about_me_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    about_me_id = params_validate["about_me_id"]

    note_db_session = get_note_db_session()

    about_me_model_delete_expression = Delete(AboutMeModel).filter(AboutMeModel.about_me_id == about_me_id)
    note_db_session.execute(about_me_model_delete_expression)
    note_db_session.commit()

    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 查询关于我
@about_me_api.route("", methods=["POST"])
def get_about_me():
    params = request.json
    get_about_me_schema = GetAboutMeSchema(many=False)

    note_db_session = get_note_db_session()

    try:
        params_validate = get_about_me_schema.load(params)
        about_me_id = params_validate["about_me_id"]
        about_me_model_select_expression = Select(AboutMeModel).filter(AboutMeModel.about_me_id == about_me_id)
        about_me_info = note_db_session.execute(about_me_model_select_expression).scalars().first()
        about_me_schema = AboutMeSchema(many=False)
    except Exception as e:
        about_me_model_select_expression = Select(AboutMeModel)
        about_me_info = note_db_session.execute(about_me_model_select_expression).scalars().all()
        about_me_schema = AboutMeSchema(many=True)
    
    about_me_result = about_me_schema.dump(about_me_info)
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": about_me_result
    })
