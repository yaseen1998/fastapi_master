from email import message
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_blog():
    response=client.get("/blog/all")
    assert response.status_code == 200
    
def test_auth_error():
    response = client.post("/token",data={"username":"test","password":"test"})
    access_toke = response.json().get("access_token")
    message = response.json().get("detail")
    print(message)
    assert access_toke==None
    
    
def test_auth_success():
    response = client.post("/token",data={"username":"admin","password":"123456"})
    access_toke = response.json().get("access_token")
    assert access_toke!=None