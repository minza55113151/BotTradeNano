import requests

base_url = "http://119.59.114.241"

def test_app():
    url = base_url + "/"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == "Hello World"
    
    url = base_url + "/test/"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == "test"
    
    url = base_url + "/keep-alive/"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text == "OK"
    
    
if __name__ == "__main__":
    test_app()
    print("All tests passed")
    pass