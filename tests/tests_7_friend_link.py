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

write_test_data(["### friend_link", ""], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))

# ========== /api/friend_link/add ==========
def test_api_friend_link_add(client):
    write_test_data(["###### POST /api/friend_link/add", "", ""], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
    params = [
        {"name": "test", "link": "https://test.cn", "description": ""},
        {"name": "yhw-miracle", "link": "https://yhw-miracle.github.io", "description": "人不可能通过逃避获得平静。极致的逃避不仅没可耻，而且也没什么用。"},
        {"name": "whark", "link": "https://whark.cn", "description": "除了一个小秘密，我只是一个极其平凡的人。"},
        {"name": "qiracle", "link": "https://qiracle.cn", "description": "no pains,no gains."},
        {"name": "mour", "link": "https://yhw-miracle.github.io", "description": "人生其实宽广的很"},
        {"name": "slycmiaoxi", "link": "https://slycmiaoxi.github.io", "description": "I believe my dream will come true."},
    ]
    for param_index, param in enumerate(params):
        response = client.post("/api/friend_link/add", json=param)
        assert response.status_code == 200
        data = response.get_json()
        app.logger.info(data)
        assert data["code"] == 200 or 400
        if data["code"] == 200:
            assert data["msg"] == "ok"
            assert isinstance(data["result"], list)
            write_test_data([
                f"* 新增友链测试数据{param_index + 1}", "", 
                "参数", "", 
                "```json", str(param), "```", "", 
                "响应", "", 
                "```json", str(data), "```", "", ""
            ], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
        assert response.headers["Content-Type"] == "application/json"

# ========== /api/friend_link/modify ==========
def test_api_friend_link_modify(client):
    write_test_data(["###### POST /api/friend_link/modify", "", ""], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
    response1 = client.post("/api/friend_link", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(data1)
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "friend_link_id": data1["result"][0]["friend_link_id"],
        "name": "yhw-miracle111",
        "link": "https://yhw-miracle.github.io",
        "description": ""
    }
    response2 = client.post("/api/friend_link/modify", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(data2)
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        f"* 修改友链测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/friend_link/del ==========
def test_api_friend_link_del(client):
    write_test_data(["###### POST /api/friend_link/del", "", ""], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
    response1 = client.post("/api/friend_link", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(data1)
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "friend_link_id": data1["result"][0]["friend_link_id"]
    }
    response2 = client.post("/api/friend_link/del", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(data2)
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    write_test_data([
        f"* 删除友链测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/friend_link ==========
def test_api_friend_link1(client):
    write_test_data(["###### POST /api/friend_link", "", ""], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
    response = client.post("/api/friend_link", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(data)
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    write_test_data([
        f"* 查询友链测试数据", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
    assert response.headers["Content-Type"] == "application/json"

def test_api_friend_link2(client):
    response1 = client.post("/api/friend_link", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(data1)
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "friend_link_id": data1["result"][1]["friend_link_id"]
    }
    response2 = client.post("/api/friend_link", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(data2)
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        f"* 查询友链测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "friend_link.md"))
    assert response2.headers["Content-Type"] == "application/json"
