import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import app
from io import BytesIO
from tests import write_test_data

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

write_test_data(["### file", ""], os.path.join(os.getcwd(), "tests", "result", "file.md"))

# ========== /api/file/upload/start /api/file/upload/chunk ==========
def test_api_file_upload1(client):
    write_test_data(["###### POST 文件上传", "", ""], os.path.join(os.getcwd(), "tests", "result", "file.md"))
    param1 = {
        "name": "test_file.png", 
    }
    response2 = client.post("/api/file/upload/start", json=param1)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_file_upload:/api/file/upload/start => {data2}")
    assert data2["code"] == 200 or 400
    if data2["code"] == 200:
        assert data2["msg"] == "ok"
        assert isinstance(data2["result"], dict)
        write_test_data([
            f"* /api/file/upload/start", "", 
            "参数", "", 
            "```json", str(param1), "```", "", 
            "响应", "", 
            "```json", str(data2), "```", "", ""
        ])
        assert "file_id" in data2["result"]
        file_id = data2["result"]["file_id"]

        test_file_filepath = os.path.join(os.getcwd(), "tests", "test_image.png")
        with open(test_file_filepath, "rb") as f:
            file_data = f.read()
            chunk_size = app.config["UPLOAD"]["CHUNK_SIZE"]
            total_chunks = len(list(range(0, len(file_data), chunk_size)))
            for chunk_index, data_index in enumerate(range(0, len(file_data), chunk_size)):
                chunk = file_data[data_index : data_index + chunk_size]
                param2 = {
                    "chunk": (BytesIO(chunk), f"{chunk_index + 1}.chunk", "file/png"),
                    "file_id": file_id, 
                    "file_type": "image",
                    "chunk_number": chunk_index + 1,
                    "total_chunks": total_chunks
                }
                response3 = client.post(
                    "/api/file/upload/chunk", 
                    data=param2,
                    content_type="multipart/form-data"
                )
                assert response3.status_code == 200
                data3 = response3.get_json()
                app.logger.info(f"test_api_file_upload:/api/file/upload/chunk => {data3}")
                assert data3["code"] == 200 or 400
                if data3["code"] == 200:
                    assert data3["msg"] == "ok"
                    if "result" in data3:
                        assert isinstance(data3["result"], dict)

                        if chunk_index == 0 or chunk_index == total_chunks - 1:
                            write_test_data([
                                f"* /api/file/upload/chunk", "", 
                                "参数", "", 
                                "```json", str(param2), "```", "", 
                                "响应", "", 
                                "```json", str(data3), "```", "", ""
                            ], os.path.join(os.getcwd(), "tests", "result", "file.md"))
                assert response3.headers["Content-Type"] == "application/json"
    assert response2.headers["Content-Type"] == "application/json"

def test_api_file_upload2(client):
    param1 = {
        "name": "test_video.mp4"
    }
    response2 = client.post("/api/file/upload/start", json=param1)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_file_upload:/api/file/upload/start => {data2}")
    assert data2["code"] == 200 or 400
    if data2["code"] == 200:
        assert data2["msg"] == "ok"
        assert isinstance(data2["result"], dict)
        write_test_data([
            f"* /api/file/upload/start", "", 
            "参数", "", 
            "```json", str(param1), "```", "", 
            "响应", "", 
            "```json", str(data2), "```", "", ""
        ], os.path.join(os.getcwd(), "tests", "result", "file.md"))
        assert "file_id" in data2["result"]
        file_id = data2["result"]["file_id"]

        test_file_filepath = os.path.join(os.getcwd(), "tests", "test_video.mp4")
        with open(test_file_filepath, "rb") as f:
            file_data = f.read()
            chunk_size = app.config["UPLOAD"]["CHUNK_SIZE"]
            total_chunks = len(list(range(0, len(file_data), chunk_size)))
            for chunk_index, data_index in enumerate(range(0, len(file_data), chunk_size)):
                chunk = file_data[data_index : data_index + chunk_size]
                param2 = {
                    "chunk": (BytesIO(chunk), f"{chunk_index + 1}.chunk", "vidoe/mp4"),
                    "file_id": file_id, 
                    "file_type": "video",
                    "chunk_number": chunk_index + 1,
                    "total_chunks": total_chunks
                }
                response3 = client.post(
                    "/api/file/upload/chunk", 
                    data=param2,
                    content_type="multipart/form-data"
                )
                assert response3.status_code == 200
                data3 = response3.get_json()
                app.logger.info(f"test_api_file_upload:/api/file/upload/chunk => {data3}")
                assert data3["code"] == 200 or 400
                if data3["code"] == 200:
                    assert data3["msg"] == "ok"
                    if "result" in data3:
                        assert isinstance(data3["result"], dict)
                        if chunk_index == 0 or chunk_index == total_chunks - 1:
                            write_test_data([
                                f"* /api/file/upload/chunk", "", 
                                "参数", "", 
                                "```json", str(param2), "```", "", 
                                "响应", "", 
                                "```json", str(data3), "```", "", ""
                            ], os.path.join(os.getcwd(), "tests", "result", "file.md"))
                assert response3.headers["Content-Type"] == "application/json"
    assert response2.headers["Content-Type"] == "application/json"

# ========== /api/file ==========
def test_api_file1(client):
    write_test_data(["###### POST /api/file", "", ""], os.path.join(os.getcwd(), "tests", "result", "file.md"))
    response = client.post("/api/file", json={})
    assert response.status_code == 200
    data = response.get_json()
    app.logger.info(f"test_api_file1:/api/file => {data}")
    assert data["code"] == 200
    assert data["msg"] == "ok"
    assert isinstance(data["result"], list)
    write_test_data([
        "* 查询文件测试数据2", "", 
        "响应", "", 
        "```json", str(data), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "file.md"))
    assert response.headers["Content-Type"] == "application/json"

def test_api_file2(client):
    response1 = client.post("/api/file", json={})
    assert response1.status_code == 200
    data1 = response1.get_json()
    app.logger.info(f"test_api_file2:/api/file => {data1}")
    assert data1["code"] == 200
    assert data1["msg"] == "ok"
    assert isinstance(data1["result"], list)
    assert response1.headers["Content-Type"] == "application/json"

    param = {
        "file_id": data1["result"][0]["file_id"]
    }
    response2 = client.post("/api/file", json=param)
    assert response2.status_code == 200
    data2 = response2.get_json()
    app.logger.info(f"test_api_file2:/api/file file_id => {data2}")
    assert data2["code"] == 200
    assert data2["msg"] == "ok"
    assert isinstance(data2["result"], dict)
    write_test_data([
        "* 查询文件测试数据2", "", 
        "参数", "", 
        "```json", str(param), "```", "", 
        "响应", "", 
        "```json", str(data2), "```", "", ""
    ], os.path.join(os.getcwd(), "tests", "result", "file.md"))
    assert response2.headers["Content-Type"] == "application/json"
