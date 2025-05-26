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

write_test_data(["### visit_location", ""], os.path.join(os.getcwd(), "tests", "result", "visit_location.md"))

# ========== /api/visit_location/sum ==========
def test_api_visit_location_sum(client):
    write_test_data(["###### POST /api/visit_location/sum", "", ""], os.path.join(os.getcwd(), "tests", "result", "visit_location.md"))
    response = client.post("/api/visit_location/sum", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(data)
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], dict)
    assert isinstance(data["result"]["total_visit"], int)
    assert isinstance(data["result"]["total_country"], int)
    assert isinstance(data["result"]["total_city"], int)
    write_test_data([
        f"* 查询访客总统计测试数据", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "visit_location.md"))
    assert response.headers["Content-Type"] == "application/json"

# ========== /api/visit_location/day ==========
def test_api_visit_location_day(client):
    write_test_data(["###### POST /api/visit_location/day", "", ""], os.path.join(os.getcwd(), "tests", "result", "visit_location.md"))
    response = client.post("/api/visit_location/day", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(data)
    assert data["code"] == 200 or 400
    if data["code"] == 200:
        assert data["msg"] == "ok"
        assert isinstance(data["result"], dict)
        write_test_data([
            f"* 查询访客日统计测试数据", "", 
            "响应", "", 
            "```json", str(data), "```", "", ""
        ], os.path.join(os.getcwd(), "tests", "result", "visit_location.md"))
        assert response.headers["Content-Type"] == "application/json"
