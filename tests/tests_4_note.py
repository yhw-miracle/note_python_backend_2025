import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import app
from tests import write_test_data

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

write_test_data(["### note", ""], os.path.join(os.getcwd(), "tests", "result", "note.md"))

# ========== /api/note/add ==========
def test_api_note_add(client):
    write_test_data(["###### POST /api/note/add", "", ""], os.path.join(os.getcwd(), "tests", "result", "note.md"))
    response1 = client.post("/api/category", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_note_add:/api/category => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    response2 = client.post("/api/tag", json={})
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_note_add:/api/tag => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], list)
    assert response2.headers["Content-Type"] == "application/json"

    response3 = client.post("/api/file", json={})
    assert response3.status_code == 200
    data3 = response3.get_json()
    app.logger.info(f"test_api_note_add:/api/file => {data3}")
    assert data3["code"] == 200
    assert data3["msg"] == "ok"
    assert isinstance(data3["result"], list)
    assert response3.headers["Content-Type"] == "application/json"

    params = [
        {"title": "测试笔记1", "content": "测试笔记1内容", "category_id": data1["result"][0]["category_id"], "tags": data2["result"][0:1], "files": data3["result"]},
        {"title": "测试笔记2", "content": "测试笔记2内容", "category_id": data1["result"][0]["category_id"], "tags": data2["result"][0:2]},
        {"title": "测试笔记3", "content": "测试笔记3内容", "category_id": data1["result"][0]["category_id"], "tags": data2["result"][0:3]},
        {"title": "测试笔记4", "content": "测试笔记4内容", "category_id": data1["result"][0]["category_id"], "tags": data2["result"][0:4]},
        {"title": "测试笔记5", "content": "测试笔记5内容", "category_id": data1["result"][0]["category_id"], "tags": data2["result"][1:2]},
        {"title": "测试笔记6", "content": "测试笔记6内容", "category_id": data1["result"][0]["category_id"], "tags": data2["result"][1:3]},
    ]
    for param_index, param in enumerate(params):
        response4 = client.post("/api/note/add", json=param)
        assert response4.status_code == 200
        data4 = response4.get_json()
        app.logger.info(f"test_api_note_add:/api/note/add => {data4}")
        assert data4["code"] == 200 or 400
        if data4["code"] == 200:
            assert data4["msg"] == "ok"
            assert isinstance(data4["result"], dict)
            write_test_data([
                f"* 新增笔记测试数据{param_index + 1}", "", 
                "参数", "", 
                "```json", str(param), "```", "", 
                "响应", "", 
                "```json", str(data4), "```", "", ""
            ], os.path.join(os.getcwd(), "tests", "result", "note.md"))
        assert response4.headers["Content-Type"] == "application/json"

# ========== /api/note/modify ==========
def test_api_note_modify(client):
    write_test_data(["###### POST /api/note/modify", "", ""], os.path.join(os.getcwd(), "tests", "result", "note.md"))
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_note_modify:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    if len(data1["result"]) > 0:
        note_path = os.path.join(app.config["WORK_FOLDER"], data1["result"][0]["path"])
        with open(note_path, "r", encoding="utf-8") as f:
            content = f.read()
            param = {
                "note_id": data1["result"][0]["note_id"],
                "title": f'{data1["result"][0]["title"]}_修改', 
                "content": f'{content}_修改', 
                "category_id": data1["result"][0]["category_id"],
                "tags": data1["result"][0]["tags"],
                "files": data1["result"][0]["files"]
            }
            response2 = client.post("/api/note/modify", json=param)
            assert response2.status_code == 200
            data2 = response2.get_json()
            app.logger.info(f"test_api_note_modify:/api/note/modify => {data2}")
            assert data2["code"] == 200 or 400
            if data2["code"] == 200:
                assert data2["msg"] == "ok"
                assert isinstance(data2["result"], dict)
                write_test_data([
                    f"* 修改笔记测试数据", "", 
                    "参数", "", 
                    "```json", str(param), "```", "", 
                    "响应", "", 
                    "```json", str(data2), "```", "", ""
                ], os.path.join(os.getcwd(), "tests", "result", "note.md"))
            assert response2.headers["Content-Type"] == "application/json"

# ========== /api/note/del ==========
def test_api_note_del(client):
    write_test_data(["###### POST /api/note/del", "", ""], os.path.join(os.getcwd(), "tests", "result", "note.md"))
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_note_del:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    if len(data1["result"]) > 0:
        param = {
            "note_id": data1["result"][5]["note_id"]
        }
        response2 = client.post("/api/note/del", json=param)
        assert response2.status_code == 200
        data2 = response2.get_json()
        app.logger.info(f"test_api_note_del:/api/note/del => {data2}")
        assert data2["code"] == 200
        assert data2["msg"] == "ok"
        write_test_data([
            f"* 删除笔记测试数据", "", 
            "参数", "", 
            "```json", str(param), "```", "", 
            "响应", "", 
            "```json", str(data2), "```", "", ""
        ], os.path.join(os.getcwd(), "tests", "result", "note.md"))
        assert response2.headers["Content-Type"] == "application/json"

# ========== /api/note ==========
def test_api_note1(client):
    write_test_data(["###### POST /api/note", "", ""], os.path.join(os.getcwd(), "tests", "result", "note.md"))
    response = client.post("/api/note", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(f"test_api_note1:/api/note => {data}")
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    write_test_data([
        f"* 查询笔记测试数据", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "note.md"))
    assert response.headers["Content-Type"] == "application/json"

def test_api_note2(client):
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_note2:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    if len(data1["result"]) > 0:
        param = {
            "note_id": data1["result"][2]["note_id"]
        }
        response2 = client.post("/api/note", json=param)
        assert response2.status_code == 200
        data2 = response2.get_json()
        app.logger.info(f"test_api_note2:/api/note note_id => {data2}")
        assert data2["code"] == 200
        assert data2["msg"] == "ok"
        assert isinstance(data2["result"], dict)
        write_test_data([
            f"* 查询笔记测试数据", "", 
            "参数", "", 
            "```json", str(param), "```", "", 
            "响应", "", 
            "```json", str(data2), "```", "", ""
        ], os.path.join(os.getcwd(), "tests", "result", "note.md"))
        assert response2.headers["Content-Type"] == "application/json"
