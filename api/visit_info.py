from flask import Blueprint, jsonify, request, current_app
from models import get_note_db_session, get_visit_info_db_session
from sqlalchemy import Select
from models.visitor import VisitInfoModel
from schemas.visit_info import VisitInfoSchema, GetVisitInfoSchema
from utils import get_hash_token
from datetime import datetime


visit_info_api = Blueprint("visit_info_api",  "note")

# 新增访问信息
def add_visit_info():
    now_datetime = datetime.now()

    current_app.logger.info(f"\nscheme=>{request.scheme}\n"
                            f"host=>{request.host}\n"
                            f"full_path=>{request.full_path}\n"
                            f"path=>{request.path}\n"
                            f"base_url=>{request.base_url}\n"
                            f"content_type=>{request.content_type}\n"
                            f"files=>{request.files}\n"
                            f"form=>{request.form}\n"
                            f"data=>{request.data}"
                            )

    # 按天统计
    day = now_datetime.strftime("%Y%m%d")
    # 请求url协议
    scheme = request.scheme
    # 请求url主机
    host = request.host
    # 请求url路径
    path = request.path
    # 请求方式
    method = request.method
    # 请求参数
    path_params = str(request.args)
    body_params = str(request.json) if method in ["POST", "PUT"] and request.content_type == "application/json" else None
    # 客户端地址
    remote_addr = request.remote_addr
    # 客户端标识
    user_agent = str(request.user_agent)
    # 客户端cookies
    cookies = str(request.cookies)
    # 客户端请求头
    headers = str(request.headers)

    create_time = now_datetime.timestamp()
    visit_info_id = get_hash_token(f"{day}_{remote_addr}_{create_time}")
    visit_info_model_select_expression = Select(VisitInfoModel).filter(VisitInfoModel.visit_info_id == visit_info_id)
    note_db_session = get_note_db_session()
    visit_info_db_session = get_visit_info_db_session()
    is_exist_visit_info_info = note_db_session.execute(visit_info_model_select_expression).scalars().all()
    if len(is_exist_visit_info_info) == 0:
        new_visit_info_for_visit_info_db = VisitInfoModel(
            visit_info_id=visit_info_id, 
            day=day, 
            scheme=scheme, 
            host=host, 
            path=path, 
            method=method, 
            path_params=path_params, 
            body_params=body_params, 
            remote_addr=remote_addr, 
            user_agent=user_agent, 
            cookies=cookies, 
            headers=headers,
            create_time=create_time
        )
        visit_info_db_session.add(new_visit_info_for_visit_info_db)
        visit_info_db_session.commit()

        new_visit_info = VisitInfoModel(
            visit_info_id=visit_info_id, 
            day=day, 
            scheme=scheme, 
            host=host, 
            path=path, 
            method=method, 
            path_params=path_params, 
            body_params=body_params, 
            remote_addr=remote_addr, 
            user_agent=user_agent, 
            cookies=cookies, 
            headers=headers,
            create_time=create_time
        )
        note_db_session.add(new_visit_info)
        note_db_session.commit()
    else:
        current_app.logger.error(f"访问信息 {visit_info_id} 已存在!")

# 查询访问信息
@visit_info_api.route("", methods=["POST"])
def get_visit_info():
    params = request.json
    get_visit_info_schema = GetVisitInfoSchema(many=False)

    note_db_session = get_note_db_session()
    visit_info_model_select_expression = Select(VisitInfoModel)
    try:
        params_validate = get_visit_info_schema.load(params)
        visit_info_id = params_validate["visit_info_id"]
        visit_info_model_select_expression = visit_info_model_select_expression.filter(VisitInfoModel.visit_info_id == visit_info_id)
        visit_info_info = note_db_session.execute(visit_info_model_select_expression).scalars().first()
        visit_info_schema = VisitInfoSchema(many=False)
    except Exception as e:
        visit_info_info = note_db_session.execute(visit_info_model_select_expression).scalars().all()
        visit_info_schema = VisitInfoSchema(many=True)
    
    visit_info_result = visit_info_schema.dump(visit_info_info)
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": visit_info_result
    })
