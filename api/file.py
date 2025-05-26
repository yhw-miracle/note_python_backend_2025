import os
import shutil
from flask import Blueprint, jsonify, request, current_app
from models import get_note_db_session
from sqlalchemy import Select, Update
from models.file import FileModel
from schemas.file import GetFileSchema, FileSchema
from schemas.upload import UploadFileSchema, UploadFileChunkSchema
from utils import get_hash_token
from datetime import datetime
from api import get_full_file


file_api = Blueprint("file_api",  "note")

def allow_file(filename):
    return filename.endswith(tuple(current_app.config["UPLOAD"]["ALLOWED_EXTENSIONS"].split(";")))

@file_api.route("/upload/start", methods=["POST"])
def upload_start():
    params = request.json
    upload_file_schema = UploadFileSchema(many=False)
    try:
        params_validate = upload_file_schema.load(params)
    except Exception as e:
        return jsonify({
            "code": "400",
            "msg": f"参数异常：{e}"
        })

    name = params_validate["name"]
    if allow_file(name):
        note_db_session = get_note_db_session()
        now_datetime = datetime.now()
        create_time = now_datetime.timestamp()
        file_id = get_hash_token(f"{name}_{create_time}")
        try:
            new_file = FileModel(file_id=file_id, name=name, create_time=create_time)
            note_db_session.add(new_file)
            note_db_session.commit()
        except Exception as e:
            return jsonify({
                "code": 400,
                "msg": f"文件上传失败：{e}"
            })

        file_model_select_expression = Select(FileModel).filter(FileModel.file_id == file_id)
        file_info = note_db_session.execute(file_model_select_expression).scalars().first()
        get_file_schema = GetFileSchema(many=False)
        file_result = get_file_schema.dump(file_info)
        return jsonify({
            "code": 200,
            "msg": "ok",
            "result": file_result
        })
    else:
        return jsonify({
            "code": 400,
            "msg": f'不支持该文件类型上传，支持的文件类型：{current_app.config["UPLOAD"]["ALLOWED_EXTENSIONS"]}'
        })

def get_chunk_path(file_id, chunk_number, now_datetime, file_type="image"):
    file_extension = "mp4" if file_type == "video" else "png"
    chunk_path = os.path.join(current_app.config["UPLOAD"]["UPLOAD_FOLDER"], f"{now_datetime.year}", f"{now_datetime.month}", f"{now_datetime.day}", file_id, f"{chunk_number}.{file_extension}")
    os.makedirs(os.path.dirname(chunk_path), exist_ok=True)
    return chunk_path

def get_result_path(file_id, now_datetime, file_type="image"):
    file_extension = "mp4" if file_type == "video" else "png"
    result_path = os.path.join(current_app.config["UPLOAD"]["UPLOAD_FOLDER"], f"{now_datetime.year}", f"{now_datetime.month}", f"{now_datetime.day}", f"{file_id}.{file_extension}")
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    return result_path

@file_api.route("/upload/chunk", methods=["POST"])
def upload_chunk():
    chunk_content = request.files.get("chunk")
    file_id = request.form.get("file_id", type=str)
    file_type = request.form.get("file_type", type=str)
    chunk_number = request.form.get("chunk_number", type=int)
    total_chunks = request.form.get("total_chunks", type=int)
    param = {
        "file_id": file_id,
        "file_type": file_type,
        "chunk_number": chunk_number,
        "total_chunks": total_chunks
    }
    upload_file_chunk_schema = UploadFileChunkSchema(many=False)
    try:
        params_validate = upload_file_chunk_schema.load(param)
    except Exception as e:
        return jsonify({
            "code": 400,
            "msg": f"参数异常：{e}"
        })

    file_id = params_validate["file_id"]
    file_type = params_validate["file_type"]
    chunk_number = params_validate["chunk_number"]
    total_chunks = params_validate["total_chunks"]
    now_datetime = datetime.now()
    chunk_path = get_chunk_path(file_id, chunk_number, now_datetime, file_type)
    try:
        chunk_content.save(chunk_path)
        if chunk_number == total_chunks:
            result_path = get_result_path(file_id, now_datetime, file_type)
            temp_dir = os.path.join(current_app.config["UPLOAD"]["UPLOAD_FOLDER"], f"{now_datetime.year}", f"{now_datetime.month}", f"{now_datetime.day}", file_id)
            with open(result_path, "ab") as f:
                for chunk_name in sorted(os.listdir(temp_dir), key=lambda x:int(os.path.splitext(x)[0])):
                    chunk_path = os.path.join(temp_dir, chunk_name)
                    with open(chunk_path, "rb") as chunk_file:
                        f.write(chunk_file.read())
            shutil.rmtree(temp_dir)

            note_db_session = get_note_db_session()
            file_model_update_expression = Update(FileModel).filter(
                FileModel.file_id == file_id
            ).values(
                file_type=file_type,
                path=os.path.relpath(result_path, current_app.config["WORK_FOLDER"])
            )
            note_db_session.execute(file_model_update_expression)
            note_db_session.commit()

            file_model_select_expression = Select(FileModel).filter(FileModel.file_id == file_id)
            file_info = note_db_session.execute(file_model_select_expression).scalars().first()
            get_file_schema = GetFileSchema(many=False)
            file_result = get_file_schema.dump(file_info)
            return jsonify({
                "code": 200,
                "msg": "ok",
                "result": file_result
            })
        
        return jsonify({
            "code": 200,
            "msg": "ok"
        })
    except Exception as e:
        return jsonify({
            "code": 400,
            "msg": f"文件上传异常：{e}"
        })

# 查询文件
@file_api.route("", methods=["POST"])
def get_tag():
    params = request.json
    get_file_schema = GetFileSchema(many=False)

    note_db_session = get_note_db_session()
    file_model_select_expression = Select(FileModel)

    try:
        params_validate = get_file_schema.load(params)
        file_id = params_validate["file_id"]
        file_model_select_expression = file_model_select_expression.filter(FileModel.file_id == file_id)
        file_info = note_db_session.execute(file_model_select_expression).scalars().first()
        file_schema = FileSchema(many=False)
    except Exception as e:
        file_info = note_db_session.execute(file_model_select_expression).scalars().all()
        file_schema = FileSchema(many=True)
    
    file_result = file_schema.dump(file_info)
    if isinstance(file_result, list):
        full_file_result = list()
        for file_result_item in file_result:
            full_file_result.append(get_full_file(note_db_session, file_result_item))
        file_result = full_file_result
    else:
        file_result = get_full_file(note_db_session, file_result)
    return jsonify({
        "code": 200,
        "msg": "ok",
        "result": file_result
    })
