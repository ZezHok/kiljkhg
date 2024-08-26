import pytest
import requests

def test_update_pet_data(base_url, update_pet_data):
    update_pet = requests.put(f'{base_url}/pet', json=update_pet_data)

    print('\nUpdate pet data')
    print('Text: ' + update_pet.text)
    print('Status: ' + str(update_pet.status_code))
    assert update_pet.status_code == 200
    print('Headers: ' + str(update_pet.headers))
    assert update_pet.headers['Content-Type'] == 'application/json'



