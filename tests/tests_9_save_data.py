import pytest
import os
import yaml
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

os.makedirs(os.path.join(os.getcwd(), "tests_data", "note"), exist_ok=True)

def test_read_data(client):
    notes = yaml.load(open(os.path.join(os.getcwd(), "note", 'notes.yaml'), 'r'), Loader=yaml.FullLoader)
    for note in notes:
        filename = note["filename"]
        with open(os.path.join(os.getcwd(), "note", filename), "r", encoding="utf-8") as f:
            content = f.read()
            param = {
                "title": note["title"],
                "content": content,
                "category": note["category"],
                "tags": [{"name": _} for _ in note["tags"]],
                "create_time": note["create_time"]
            }

            response = client.post("/api/note/add1", json=param)
            assert response.status_code == 200
            data = response.get_json()
            assert data["code"] == 200 or 400
            if data["code"] == 200:
                assert data["msg"] == "ok"
                assert isinstance(data["result"], dict)
            assert response.headers["Content-Type"] == "application/json"

def test_api_about_me_add(client):
    params = [
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
        assert response.headers["Content-Type"] == "application/json"

def test_api_friend_link_add(client):
    params = [
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
        assert response.headers["Content-Type"] == "application/json"

# ========== /api/category ==========
def test_api_category1(client):
    response = client.post("/api/category", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == 200
    json.dump(data["result"], open(os.path.join(os.getcwd(), "tests_data", "category.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    assert response.headers["Content-Type"] == "application/json"

# ========== /api/tag ==========
def test_api_tag1(client):
    response = client.post("/api/tag", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == 200
    json.dump(data["result"], open(os.path.join(os.getcwd(), "tests_data", "tag.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    assert response.headers["Content-Type"] == "application/json"

# ========== /api/about_me ==========
def test_api_about_me1(client):
    response = client.post("/api/about_me", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == 200
    json.dump(data["result"], open(os.path.join(os.getcwd(), "tests_data", "about_me.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    assert response.headers["Content-Type"] == "application/json"

# ========== /api/friend_link ==========
def test_api_friend_link1(client):
    response = client.post("/api/friend_link", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == 200
    json.dump(data["result"], open(os.path.join(os.getcwd(), "tests_data", "friend_link.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    assert response.headers["Content-Type"] == "application/json"

# ========== /api/visit_location/sum ==========
def test_api_visit_location_sum(client):
    response = client.post("/api/visit_location/sum", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], dict)
    assert isinstance(data["result"]["total_visit"], int)
    assert isinstance(data["result"]["total_country"], int)
    assert isinstance(data["result"]["total_city"], int)
    json.dump(data["result"], open(os.path.join(os.getcwd(), "tests_data", "visit_location_sum.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    assert response.headers["Content-Type"] == "application/json"

# ========== /api/visit_location/day ==========
def test_api_visit_location_day(client):
    response = client.post("/api/visit_location/day", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == 200 or 400
    if data["code"] == 200:
        assert data["msg"] == "ok"
        assert isinstance(data["result"], dict)
        json.dump(data["result"], open(os.path.join(os.getcwd(), "tests_data", "visit_location_day.json"), "w",  encoding="utf-8"), ensure_ascii=False)
        assert response.headers["Content-Type"] == "application/json"

def test_api_user1(client):
    response = client.post("/api/user", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == 200
    json.dump(data["result"], open(os.path.join(os.getcwd(), "tests_data", "user.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    assert response.headers["Content-Type"] == "application/json"

# ========== /api/note ==========
def test_api_note1(client):
    response = client.post("/api/note", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == 200
    json.dump(data["result"], open(os.path.join(os.getcwd(), "tests_data", "note.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    assert response.headers["Content-Type"] == "application/json"

def test_api_note2(client):
    response1 = client.post("/api/note", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    json.dump(data1["result"], open(os.path.join(os.getcwd(), "tests_data", "note.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    assert response1.headers["Content-Type"] == "application/json"

    # for result_item in data1["result"]:
    #     note_id = result_item["note_id"]
    #     param = {
    #         "note_id": note_id
    #     }
    #     response2 = client.post("/api/note", json=param)
    #     assert response2.status_code == 200
    #     data2 = response2.get_json()
    #     assert data2["code"] == 200
    #     assert data2["msg"] == "ok"
    #     assert isinstance(data2["result"], dict)
    #     json.dump(data2["result"], open(os.path.join(os.getcwd(), "tests_data", "note",  f"{note_id}.json"), "w",  encoding="utf-8"), ensure_ascii=False)
    #     assert response2.headers["Content-Type"] == "application/json"