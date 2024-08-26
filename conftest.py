import pytest
import requests

@pytest.fixture(scope='module')
def base_url():
    base_url = "https://petstore.swagger.io/v2"
    return base_url

@pytest.fixture(scope='module')
def pet_id():
    pet_id = 1304
    return pet_id

#Setup
@pytest.fixture(scope='module', autouse=True)
def setup_function(base_url, pet_id):
    #создание юзера
    data = {
        "id": pet_id,
        "category": {
            "id": 4,
            "name": "testname"
        },
        "name": "lusia",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
            "id": 6,
            "name": "testtag"
            }
        ],
        "status": "available"
    }

    create_pet = requests.post(f"{base_url}/pet", json=data)
    print("Create pet" + create_pet.text)
    assert create_pet.status_code == 200
    print(create_pet.headers)
    assert create_pet.headers['Content-Type'] == 'application/json'

    yield

    # Удаление юзера
    del_pet = requests.delete(f"{base_url}/pet/{pet_id}")
    print("delete pet" + del_pet.text)
    assert del_pet.status_code == 200
    print(del_pet.headers)
    assert del_pet.headers['Content-Type'] == 'application/json'
