import os
import copy
from flask import current_app
from sqlalchemy import Select
from models.category import CategoryModel
from models.note import NoteModel
from models.tag import TagModel
from models.tag_note import TagNoteModel
from models.file import FileModel
from models.file_note import FileNoteModel
from models.comment import CommentModel
from schemas.category import CategorySchema
from schemas.note import NoteSchema
from schemas.tag import TagSchema
from schemas.tag_note import TagNoteSchema
from schemas.file import FileSchema
from schemas.file_note import FileNoteSchema
from schemas.comment import CommentSchema


def get_full_note(note_db_session, note_result, is_get_category=True, is_get_tags=True, is_get_files=False, is_get_content=False, is_get_comment=False):
    if len(note_result) > 0:
        note_id = note_result["note_id"]
        category_id = note_result["category_id"]

        if is_get_category:
            category_model_select_expression = Select(CategoryModel).filter(CategoryModel.category_id == category_id)
            category_info = note_db_session.execute(category_model_select_expression).scalars().first()
            category_schema = CategorySchema(many=False)
            category_result = category_schema.dump(category_info)
            if len(category_result) > 0:
                note_result["category"] = category_result

        if is_get_tags:
            tags = list()
            tag_note_model_select_expression = Select(TagNoteModel).filter(TagNoteModel.note_id == note_id)
            tag_note_info = note_db_session.execute(tag_note_model_select_expression).scalars().all()
            tag_note_schema = TagNoteSchema(many=True)
            tag_note_result = tag_note_schema.dump(tag_note_info)
            for tag_note_result_item in tag_note_result:
                tag_id = tag_note_result_item["tag_id"]
                tag_model_select_expression = Select(TagModel).filter(TagModel.tag_id == tag_id)
                tag_info = note_db_session.execute(tag_model_select_expression).scalars().first()
                tag_schema = TagSchema(many=False)
                tag_result = tag_schema.dump(tag_info)
                tags.append(tag_result)
            if len(tags) > 0:
                note_result["tags"] = tags
        
        if is_get_files:
            files = list()
            file_note_model_select_expression = Select(FileNoteModel).filter(FileNoteModel.note_id == note_id)
            file_note_info = note_db_session.execute(file_note_model_select_expression).scalars().all()
            file_note_schema = FileNoteSchema(many=True)
            file_note_result = file_note_schema.dump(file_note_info)
            for file_note_result_item in file_note_result:
                file_id = file_note_result_item["file_id"]
                file_model_select_expression = Select(FileModel).filter(FileModel.file_id == file_id)
                file_info = note_db_session.execute(file_model_select_expression).scalars().first()
                file_schema = FileSchema(many=False)
                file_result = file_schema.dump(file_info)
                files.append(file_result)
            if len(files) > 0:
                note_result["files"] = files

        if is_get_content:
            note_path = note_result["path"]
            note_path = os.path.join(current_app.config["WORK_FOLDER"], note_path)
            if os.path.exists(note_path):
                with open(note_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    note_result["content"] = content

        if is_get_comment:
            comment_model_select_expression = Select(CommentModel).filter(CommentModel.note_id == note_id)
            comment_info = note_db_session.execute(comment_model_select_expression).scalars().all()
            comment_schema = CommentSchema(many=True)
            comment_result = comment_schema.dump(comment_info)
            if len(comment_result) > 0:
                _, comment_tree = get_comment_tree(comment_result)
                note_result["comments"] = comment_tree

    return note_result

def get_comment_tree(comment_result, comment_ids = list(), parent_id = None):
    comment_tree = list()
    for comment_result_item in comment_result:
        # if "parent_id" not in comment_result_item:
        #     comment_result_item["parent_id"] = None
        if ("parent_id" not in comment_result_item and parent_id is None) or ("parent_id" in comment_result_item and parent_id is not None and comment_result_item["parent_id"] == parent_id):
            comment_ids.append(comment_result_item["comment_id"])
            comment_node = copy.deepcopy(comment_result_item)
            comment_ids, comment_node["children"] = get_comment_tree(comment_result, comment_ids, comment_result_item["comment_id"])
            comment_tree.append(comment_node)
    return comment_ids, comment_tree

def get_full_category(note_db_session, category_result):
    if len(category_result) > 0:
        notes = list()
        category_id = category_result["category_id"]
        note_model_select_expression = Select(NoteModel).filter(NoteModel.category_id == category_id)
        note_info = note_db_session.execute(note_model_select_expression).scalars().all()
        note_schema = NoteSchema(many=True)
        note_result = note_schema.dump(note_info)
        for note_result_item in note_result:
            notes.append(get_full_note(note_db_session, note_result_item))
        if len(notes) > 0:
            category_result["notes"] = notes
    return category_result

def get_full_tag(note_db_session, tag_result):
    if len(tag_result) > 0:
        notes = list()
        tag_id = tag_result["tag_id"]
        tag_note_model_select_expression = Select(TagNoteModel).filter(TagNoteModel.tag_id == tag_id)
        tag_note_info = note_db_session.execute(tag_note_model_select_expression).scalars().all()
        tag_note_schema = TagNoteSchema(many=True)
        tag_note_result = tag_note_schema.dump(tag_note_info)
        for tag_note_result_item in tag_note_result:
            note_id = tag_note_result_item["note_id"]
            note_model_select_expression = Select(NoteModel).filter(NoteModel.note_id == note_id)
            note_info = note_db_session.execute(note_model_select_expression).scalars().first()
            note_schema = NoteSchema(many=False)
            note_result = note_schema.dump(note_info)
            notes.append(get_full_note(note_db_session, note_result))
        if len(notes) > 0:
            tag_result["notes"] = notes
    return tag_result

def get_full_file(note_db_session, file_result):
    if len(file_result) > 0:
        notes = list()
        file_id = file_result["file_id"]
        file_note_model_select_expression = Select(FileNoteModel).filter(FileNoteModel.file_id == file_id)
        file_note_info = note_db_session.execute(file_note_model_select_expression).scalars().all()
        file_note_schema = FileNoteSchema(many=True)
        file_note_result = file_note_schema.dump(file_note_info)
        for file_note_result_item in file_note_result:
            note_id = file_note_result_item["note_id"]
            note_model_select_expression = Select(NoteModel).filter(NoteModel.note_id == note_id)
            note_info = note_db_session.execute(note_model_select_expression).scalars().first()
            note_schema = NoteSchema(many=False)
            note_result = note_schema.dump(note_info)
            notes.append(get_full_note(note_db_session, note_result))
        if len(notes) > 0:
            file_result["notes"] = notes
    return file_result
