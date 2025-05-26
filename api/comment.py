from flask import Blueprint, jsonify, request
from models import get_note_db_session
from sqlalchemy import Select, Delete
from models.note import NoteModel
from models.comment import CommentModel
from schemas.comment import CommentSchema, AddCommentSchema, GetCommentSchema
from schemas.note import GetNoteSchema
from utils import get_hash_token
from datetime import datetime
from api import get_comment_tree


comment_api = Blueprint("comment_api",  "note")

# 新增评论
@comment_api.route("/add", methods=["POST"])
def add_comment():
    params = request.json
    add_comment_schema = AddCommentSchema(many=False)
    try:
        params_validate = add_comment_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    # 评论内容
    content = params_validate["content"]
    # 笔记id
    note_id = params_validate["note_id"]
    # 用户id
    user_id = params_validate["user_id"] if "user_id" in params_validate else None
    # 父级评论
    parent_id = params_validate["parent_id"] if "parent_id" in params_validate else None
    now_datetime = datetime.now()
    create_time = now_datetime.timestamp()
    comment_id = get_hash_token(f"{content}_{note_id}_{user_id}_{parent_id}_{create_time}")
    comment_model_select_expression = Select(CommentModel).filter(CommentModel.comment_id == comment_id)
    note_db_session = get_note_db_session()
    is_exist_comment_info = note_db_session.execute(comment_model_select_expression).scalars().all()
    if len(is_exist_comment_info) == 0:
        new_comment = CommentModel(
            comment_id=comment_id, 
            content=content, 
            note_id=note_id,
            user_id=user_id,
            parent_id=parent_id, 
            create_time=create_time
        )
        note_db_session.add(new_comment)
        note_db_session.commit()

        comment_model_select_expression = Select(CommentModel).filter(CommentModel.note_id == note_id)
        comment_info = note_db_session.execute(comment_model_select_expression).scalars().all()
        comment_schema = CommentSchema(many=True)
        comment_result = comment_schema.dump(comment_info)
        _, commment_tree = get_comment_tree(comment_result)

        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": commment_tree
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f"评论 {content} 已存在!"
        })

# 删除评论
@comment_api.route("/del", methods=["POST"])
def del_comment():
    params = request.json
    get_comment_schema = GetCommentSchema(many=False)
    try:
        params_validate = get_comment_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    comment_id = params_validate["comment_id"]

    note_db_session = get_note_db_session()

    comment_model_select_expression = Select(CommentModel)
    comment_info = note_db_session.execute(comment_model_select_expression).scalars().all()
    comment_schema = CommentSchema(many=True)
    comment_result = comment_schema.dump(comment_info)
    comment_ids=[]
    comment_ids, comment_tree = get_comment_tree(comment_result, comment_ids, parent_id=comment_id)
    for comment_id in comment_ids:
        comment_model_delete_expression = Delete(CommentModel).filter(CommentModel.comment_id == comment_id)
        note_db_session.execute(comment_model_delete_expression)
        note_db_session.commit()
    comment_model_delete_expression = Delete(CommentModel).filter(CommentModel.comment_id == comment_id)
    note_db_session.execute(comment_model_delete_expression)
    note_db_session.commit()

    return jsonify({
        "code": 200,
        "msg": "ok"
    })

# 查询评论
@comment_api.route("", methods=["POST"])
def get_comment():
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
    
    comment_model_select_expression = Select(CommentModel).filter(CommentModel.note_id == note_id)
    comment_info = note_db_session.execute(comment_model_select_expression).scalars().all()
    comment_schema = CommentSchema(many=True)
    comment_result = comment_schema.dump(comment_info)
    comment_ids=[]
    comment_ids, comment_tree = get_comment_tree(comment_result, comment_ids)
    
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": comment_tree
    })
