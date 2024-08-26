import pytest
import requests

def test_pet_operations(base_url, pet_id):
    update_data = {
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
        "status": "sold"
    }

    update_pet = requests.put(f"{base_url}/pet", json=update_data)
    print("Update pet" + update_pet.text)
    assert update_pet.status_code == 200
    print(update_pet.headers)
    assert update_pet.headers['Content-Type'] == 'application/json'

    get_pet = requests.get(f"{base_url}/pet/{pet_id}")
    print("Info pet" + get_pet.text)
    assert get_pet.status_code == 200
    print(get_pet.headers)
    assert get_pet.headers['Content-Type'] == 'application/json'
    pet_info = get_pet.json()
    assert pet_info['status'] == update_data['status']

