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

write_test_data(["### comment", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))

# ============================================================================================================================
# 匿名用户评论
# ============================================================================================================================
# ========== /api/comment/add ==========
def test_no_user_api_comment_add1(client):
    write_test_data(["###### POST /api/comment/add", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_comment_add1:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    params = [
        {"content": "写得真好!", "note_id": data1["result"][0]["note_id"]},
        {"content": "写得真好!", "note_id": data1["result"][1]["note_id"]},
        {"content": "写得真好!", "note_id": data1["result"][2]["note_id"]},
        {"content": "写得真好!", "note_id": data1["result"][3]["note_id"]},
        {"content": "写得真好!", "note_id": data1["result"][4]["note_id"]},
    ]
    for param_index, param in enumerate(params):
        response2 = client.post("/api/comment/add", json=param)
        assert response2.status_code == 200
        data2 = response2.get_json()
        assert data2["code"] == 200 or 400
        if data2["code"] == 200:
            assert data2["msg"] == "ok"
            assert isinstance(data2["result"], list)
            write_test_data([
                f"* 新增评论测试数据{param_index + 1}", "", 
                "参数", "", 
                "```json", str(param), "```", "", 
                "响应", "", 
                "```json", str(data2), "```", "", ""
            ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
        assert response2.headers["Content-Type"] == "application/json"

def test_no_user_api_comment_add2(client):
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_comment_add2:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    note_id = data1["result"][0]["note_id"]
    param2 = {"note_id": note_id}
    response2 = client.post("/api/comment", json=param2)
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], list)
    assert response2.headers["Content-Type"] == "application/json"
    comment_id = data2["result"][0]["comment_id"]
    
    param3 = {"content": "谢谢!", "note_id": note_id, "parent_id": comment_id}
    response3 = client.post("/api/comment/add", json=param3)
    assert response3.status_code == 200
    data3 = response3.get_json()
    assert data3["code"] == 200 or 400
    if data3["code"] == 200:
        assert data3["msg"] == "ok"
        assert isinstance(data3["result"], list)
        write_test_data([
            f"* 回复评论测试数据", "", 
            "参数", "", 
            "```json", str(param3), "```", "", 
            "响应", "", 
            "```json", str(data3), "```", "", ""
        ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response3.headers["Content-Type"] == "application/json"

# ========== /api/comment/del ==========
def test_no_user_api_comment_del(client):
    write_test_data(["###### POST /api/comment/del", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_comment_add2:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"
    note_id = data1["result"][1]["note_id"]
    
    param2 = {"note_id": note_id}
    response2 = client.post("/api/comment", json=param2)
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], list)
    assert response2.headers["Content-Type"] == "application/json"
    comment_id = data2["result"][0]["comment_id"]

    param = {
        "comment_id": comment_id
    }
    response3 = client.post("/api/comment/del", json=param)
    assert response3.status_code == 200
    data3 = response3.get_json()
    app.logger.info(f"test_api_comment_del:/api/comment/del => {data3}")
    assert data3["code"] == 200
    assert data3["msg"] == "ok"
    write_test_data([
        f"* 删除评论测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data3), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response3.headers["Content-Type"] == "application/json"

# ========== /api/comment ==========
def test_no_user_api_comment(client):
    write_test_data(["###### POST /api/comment", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_comment_add2:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"
    note_id = data1["result"][2]["note_id"]

    param2 = {"note_id": note_id}
    response2 = client.post("/api/comment", json=param2)
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], list)
    write_test_data([
        f"* 查询评论测试数据", "", 
        "参数", "", 
        "```json", str(param2), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response2.headers["Content-Type"] == "application/json"
# ============================================================================================================================

# ============================================================================================================================
# 用户管理
# ============================================================================================================================
# ========== /api/user/add ==========
def test_api_user_add(client):
    write_test_data(["###### POST /api/user/add", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    params = [
        {"username": "demo01", "email": "demo01@note.com"},
        {"username": "demo02", "email": "demo02@note.com"},
        {"username": "demo03", "email": "demo03@note.com"},
        {"username": "demo04", "email": "demo04@note.com"},
        {"username": "demo05", "email": "demo05@note.com"},
    ]
    for param_index, param in enumerate(params):
        response = client.post("/api/user/add", json=param)
        assert response.status_code == 200
        data = response.get_json()
        app.logger.info(f"test_api_user_add:/api/user/add => {data}")
        assert data["code"] == 200 or 400
        if data["code"] == 200:
            assert data["msg"] == "ok"
            assert isinstance(data["result"], dict)
            write_test_data([
                f"* 新增用户测试数据{param_index + 1}", "", 
                "参数", "", 
                "```json", str(param), "```", "", 
                "响应", "", 
                "```json", str(data), "```", "", ""
            ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
        assert response.headers["Content-Type"] == "application/json"

# ========== /api/user/del ==========
def test_api_user_del(client):
    write_test_data(["###### POST /api/user/del", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    response1 = client.post("/api/user", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_user_del:/api/user => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "user_id": data1["result"][4]["user_id"]
    }
    response2 = client.post("/api/user/del", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_user_del:/api/user/del => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    write_test_data([
        f"* 删除用户测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/user ==========
def test_api_user1(client):
    write_test_data(["###### POST /api/user", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    response = client.post("/api/user", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(f"test_api_user1:/api/user => {data}")
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    write_test_data([
        f"* 查询用户测试数据", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response.headers["Content-Type"] == "application/json"

def test_api_user2(client):
    response1 = client.post("/api/user", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_user2:/api/user => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "user_id": data1["result"][0]["user_id"]
    }
    response2 = client.post("/api/user", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_user2:/api/user user_id => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        f"* 查询用户测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response2.headers["Content-Type"] == "application/json"
# ============================================================================================================================

# ============================================================================================================================
# 实名用户评论
# ============================================================================================================================
# ========== /api/comment/add ==========
def test_user_api_comment_add1(client):
    write_test_data(["###### POST /api/comment/add", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_comment_add1:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    response2 = client.post("/api/user", json={})
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_comment_add1:/api/user => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], list)
    assert response2.headers["Content-Type"] == "application/json"

    params = [
        {"content": "写得真好!", "note_id": data1["result"][0]["note_id"], "user_id": data2["result"][0]["user_id"]},
        {"content": "写得真好!", "note_id": data1["result"][1]["note_id"], "user_id": data2["result"][0]["user_id"]},
        {"content": "写得真好!", "note_id": data1["result"][2]["note_id"], "user_id": data2["result"][0]["user_id"]},
        {"content": "写得真好!", "note_id": data1["result"][3]["note_id"], "user_id": data2["result"][0]["user_id"]},
        {"content": "写得真好!", "note_id": data1["result"][4]["note_id"], "user_id": data2["result"][0]["user_id"]},
    ]
    for param_index, param in enumerate(params):
        response3 = client.post("/api/comment/add", json=param)
        assert response3.status_code == 200
        data3 = response3.get_json()
        app.logger.info(f"test_api_comment_add1:/api/comment/add => {data3}")
        assert data3["code"] == 200 or 400
        if data3["code"] == 200:
            assert data3["msg"] == "ok"
            assert isinstance(data3["result"], list)
            write_test_data([
                f"* 新增评论测试数据{param_index + 1}", "", 
                "参数", "", 
                "```json", str(param), "```", "", 
                "响应", "", 
                "```json", str(data3), "```", "", ""
            ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
        assert response3.headers["Content-Type"] == "application/json"

def test_user_api_comment_add2(client):
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_comment_add2:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"
    note_id = data1["result"][0]["note_id"]

    response2 = client.post("/api/user", json={})
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_comment_add2:/api/user => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], list)
    assert response2.headers["Content-Type"] == "application/json"
    user_id = data2["result"][0]["user_id"]

    response3 = client.post("/api/comment", json={
        "note_id": note_id
    })
    assert response3.status_code == 200
    data3 = response3.get_json()
    app.logger.info(f"test_api_comment_add2:/api/user => {data3}")
    assert data3["code"] == 200
    assert data3["msg"] == "ok"
    assert isinstance(data3["result"], list)
    assert response3.headers["Content-Type"] == "application/json"
    comment_id = data3["result"][0]["comment_id"]

    param = {"content": "谢谢!", "note_id": note_id, "user_id": user_id, "parent_id": comment_id}
    response4 = client.post("/api/comment/add", json=param)
    assert response4.status_code == 200
    data4 = response4.get_json()
    app.logger.info(f"test_api_comment_add2:/api/comment/add => {data4}")
    assert data4["code"] == 200 or 400
    if data4["code"] == 200:
        assert data4["msg"] == "ok"
        assert isinstance(data4["result"], list)
        write_test_data([
            f"* 回复评论测试数据", "", 
            "参数", "", 
            "```json", str(param), "```", "", 
            "响应", "", 
            "```json", str(data4), "```", "", ""
        ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response4.headers["Content-Type"] == "application/json"

# ========== /api/comment/del ==========
def test_user_api_comment_del(client):
    write_test_data(["###### POST /api/comment/del", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_comment_del:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"
    note_id = data1["result"][1]["note_id"]

    response2 = client.post("/api/comment", json={
        "note_id": note_id
    })
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_comment_del:/api/comment => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], list)
    assert response2.headers["Content-Type"] == "application/json"
    comment_id = data2["result"][0]["comment_id"]

    param = {
        "comment_id": comment_id
    }
    response3 = client.post("/api/comment/del", json=param)
    assert response3.status_code == 200
    data3 = response3.get_json()
    app.logger.info(f"test_api_comment_del:/api/comment/del => {data3}")
    assert data3["code"] == 200
    assert data3["msg"] == "ok"
    write_test_data([
        f"* 删除评论测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data3), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response3.headers["Content-Type"] == "application/json"

# ========== /api/comment ==========
def test_user_api_comment1(client):
    write_test_data(["###### POST /api/comment", "", ""], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_comment_del:/api/note => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"
    note_id = data1["result"][1]["note_id"]

    param = {
        "note_id": note_id
    }
    response = client.post("/api/comment", json=param)
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(f"test_api_comment1:/api/comment => {data}")
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    write_test_data([
        f"* 查询评论测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "comment.md"))
    assert response.headers["Content-Type"] == "application/json"
# ============================================================================================================================
