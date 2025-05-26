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

write_test_data(["### tag", ""], os.path.join(os.getcwd(), "tests", "result", "tag.md"))

# ========== /api/tag/add ==========
def test_api_tag_add(client):
    write_test_data(["###### POST /api/tag/add", "", ""], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
    params = [
        {"name": "c"},
        {"name": "c++"},
        {"name": "python"},
        {"name": "java"},
        {"name": "test"},
    ]
    for param_index, param in enumerate(params):
        response = client.post("/api/tag/add", json=param)
        assert response.status_code == 200
        data = response.get_json()
        app.logger.info(data)
        assert data["code"] == 200 or 400
        if data["code"] == 200:
            assert data["msg"] == "ok"
            assert isinstance(data["result"], dict)
            write_test_data([
                f"* 添加标签测试数据{param_index + 1}", "", 
                "参数", "", 
                "```json", str(param), "```", "", 
                "响应", "", 
                "```json", str(data), "```", "", ""
            ], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
        assert response.headers["Content-Type"] == "application/json"

# ========== /api/tag/modify ==========
def test_api_tag_modify(client):
    write_test_data(["###### POST /api/tag/modify", "", ""], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
    response1 = client.post("/api/tag", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_tag_modify:/api/tag => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"
    
    param = {
        "tag_id": data1["result"][2]["tag_id"],
        "name": "python3"
    }
    response2 = client.post("/api/tag/modify", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(data2)
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        "* 修改标签测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/tag/del ==========
def test_api_tag_del(client):
    write_test_data(["###### POST /api/tag/del", "", ""], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
    response1 = client.post("/api/tag", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_tag_del:/api/tag => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "tag_id": data1["result"][4]["tag_id"]
    }
    response2 = client.post("/api/tag/del", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(data2)
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    write_test_data([
        "* 删除标签测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/tag ==========
def test_api_tag1(client):
    write_test_data(["###### POST /api/tag", "", ""], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
    response = client.post("/api/tag", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(f"test_api_tag1:/api/tag => {data}")
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    write_test_data([
        "* 查询标签测试数据1", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
    assert response.headers["Content-Type"] == "application/json"

def test_api_tag2(client):
    response1 = client.post("/api/tag", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_tag2:/api/tag => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "tag_id": data1["result"][0]["tag_id"]
    }
    response2 = client.post("/api/tag", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_tag2:/api/tag tag_id => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        "* 查询标签测试数据2", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "tag.md"))
    assert response2.headers["Content-Type"] == "application/json"
