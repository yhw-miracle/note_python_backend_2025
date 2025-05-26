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

write_test_data(["### about_me", ""], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))

# ========== /api/about_me/add ==========
def test_api_about_me_add(client):
    write_test_data(["###### POST /api/about_me/add", "", ""], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
    params = [
        {"content": "test"},
        {"content": "全栈开发"},
        {"content": "熟悉c/c++编程 QT/C++11/Boost ......"},
        {"content": "熟悉python开发 Django/Flask/Scrapy ......"},
        {"content": "熟悉java开发 SpringBoot ......"},
        {"content": "熟悉kubernetes运维系统搭建"},
        {"content": "后端开发技能 数据库/异步任务/Celery/Docker/Kubernetes ......"},
        {"content": "前端开发技能 Html/CSS/JavaScript/Vue ......"},
        {"content": "爱读书, 截止到目前累计阅读字数超过 3000 万字"},
        {"content": "爱编程, 多语言开发者，使用过 C、C++、Python、JAVA, 写过网页、Android APP、PC 桌面应用程序"},
        {"content": "爱写作, 截止到目前发表文字数超过 5 万字"},
        {"content": "Github: https://github.com/yhw-miracle"}
    ]
    for param_index, param in enumerate(params):
        response = client.post("/api/about_me/add", json=param)
        assert response.status_code == 200
        data = response.get_json()
        app.logger.info(data)
        assert data["code"] == 200 or 400
        if data["code"] == 200:
            assert data["msg"] == "ok"
            assert isinstance(data["result"], list)
            write_test_data([
                f"* 新增关于我测试数据{param_index + 1}", "", 
                "参数", "", 
                "```json", str(param), "```", "", 
                "响应", "", 
                "```json", str(data), "```", "", ""
            ], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
        assert response.headers["Content-Type"] == "application/json"

# ========== /api/about_me/modify ==========
def test_api_about_me_modify(client):
    write_test_data(["###### POST /api/about_me/modify", "", ""], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
    response1 = client.post("/api/about_me", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(data1)
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "about_me_id": data1["result"][0]["about_me_id"],
        "content": "具备全栈开发能力"
    }
    response2 = client.post("/api/about_me/modify", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(data2)
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        f"* 修改关于我测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/about_me/del ==========
def test_api_about_me_del(client):
    write_test_data(["###### POST /api/about_me/del", "", ""], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
    response1 = client.post("/api/about_me", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(data1)
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "about_me_id": data1["result"][0]["about_me_id"]
    }
    response2 = client.post("/api/about_me/del", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(data2)
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    write_test_data([
        f"* 删除关于我测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/about_me ==========
def test_api_about_me1(client):
    write_test_data(["###### POST /api/about_me", "", ""], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
    response = client.post("/api/about_me", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(data)
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    write_test_data([
        f"* 查询关于我测试数据", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
    assert response.headers["Content-Type"] == "application/json"

def test_api_about_me2(client):
    response1 = client.post("/api/about_me", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(data1)
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "about_me_id": data1["result"][3]["about_me_id"]
    }
    response2 = client.post("/api/about_me", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(data2)
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        f"* 查询关于我测试数据", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "about_me.md"))
    assert response2.headers["Content-Type"] == "application/json"
