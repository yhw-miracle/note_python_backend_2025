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

write_test_data(["### category", ""], os.path.join(os.getcwd(), "tests", "result", "category.md"))

# ========== /api/category/add ==========
def test_api_category_add(client):
    write_test_data(["###### POST /api/category/add", "", ""], os.path.join(os.getcwd(), "tests", "result", "category.md"))
    params = [
        {"name": "前端", "description": "前端路上走过的坑"},
        {"name": "后端", "description": "后端旅途上经历的风景"},
        {"name": "运维", "description": "在前端和后端夹缝中学习到的运维技巧"},
        {"name": "算法", "description": "在后端开发中寻觅到的光"},
        {"name": "test", "description": "test"},
    ]
    for param_index, param in enumerate(params):
        response = client.post("/api/category/add", json=param)
        assert response.status_code == 200
        data = response.get_json()
        app.logger.info(f"test_api_category_add:/api/category/add => {data}")
        assert data["code"] == 200 or 400
        if data["code"] == 200:
            assert data["msg"] == "ok"
            assert isinstance(data["result"], dict)
            write_test_data([
                f"* 添加分类测试数据{param_index + 1}", "", 
                "参数", "", 
                "```json", str(param), "```", "", 
                "响应", "", 
                "```json", str(data), "```", "", ""
            ], os.path.join(os.getcwd(), "tests", "result", "category.md"))
        assert response.headers["Content-Type"] == "application/json"

# ========== /api/category/modify ==========
def test_api_category_modify(client):
    write_test_data(["###### POST /api/category/modify", "", ""], os.path.join(os.getcwd(), "tests", "result", "category.md"))
    response1 = client.post("/api/category", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_category_modify:/api/category => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "category_id": data1["result"][3]["category_id"],
        "name": data1["result"][3]["name"],
        "description": "算法也是一种后端技术"
    }
    response2 = client.post("/api/category/modify", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_category_modify:/api/category/modify => {data2}")
    assert data2["code"] == 200 or 400
    if data2["code"] == 200:
        assert data2["msg"] == "ok"
        assert isinstance(data2["result"], dict)
        write_test_data([
            "* 修改分类测试数据", "", 
            "参数", "", 
            "```json", str(param), "```", "", 
            "响应", "", 
            "```json", str(data2), "```", "", ""
        ], os.path.join(os.getcwd(), "tests", "result", "category.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/category/del ==========
def test_api_category_del(client):
    write_test_data(["###### POST /api/category/del", "", ""], os.path.join(os.getcwd(), "tests", "result", "category.md"))
    response1 = client.post("/api/category", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_category_del:/api/category => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "category_id": data1["result"][4]["category_id"]
    }
    response2 = client.post("/api/category/del", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_category_del:/api/category/del => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    write_test_data([
        "* 删除分类测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "category.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/category ==========
def test_api_category1(client):
    write_test_data(["###### POST /api/category", "", ""], os.path.join(os.getcwd(), "tests", "result", "category.md"))
    response = client.post("/api/category", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(f"test_api_category1:/api/category => {data}")
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    write_test_data([
        "* 查询分类测试数据1", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "category.md"))
    assert response.headers["Content-Type"] == "application/json"

def test_api_category2(client):
    response1 = client.post("/api/category", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_category2:/api/category => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "category_id": data1["result"][0]["category_id"]
    }
    response2 = client.post("/api/category", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_category2:/api/category category_id => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        "* 查询分类测试数据2", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "category.md"))
    assert response2.headers["Content-Type"] == "application/json"
