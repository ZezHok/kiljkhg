import pytest
import requests
import jsonschema
from jsonschema import validate

base_url = 'https://petstore.swagger.io/v2'

@pytest.mark.parametrize("pet_id", [897, 465, 790])

def test_pet_operations(pet_id):

   # Add a new pet in the store

    data = {
        "name": "Test123",
        "photoUrls": [
            "strissdfvdsng",
            "sdgvdg"
        ],
        "id": 465,
        "category": {
            "id": 7967,
            "name": "egergeg"
        },
        "tags": [
            {
                "id": 678568,
                "name": "fjgk"
            },
            {
                "id": 235235,
                "name": "vo8io"
            }
        ],
        "status": "pending"
    }

    add_pet = requests.post(f'{base_url}/pet', json=data)
    print('Add a new pet ' + add_pet.text)
    print(add_pet.status_code)
    print(add_pet.headers)

    assert add_pet.status_code == 200
    assert add_pet.headers['Content-Type'] == 'application/json'

    #Update pet
    update_data = {
    "name": "Test123",
    "photoUrls": [
    "strissdfvdsng",
    "sdgvdg"
     ],
    "id": 465,
    "category": {
    "id": 7967,
    "name": "egergeg"
    },
    "tags": [
    {
      "id": 678568,
      "name": "fjgk"
    },
    {
      "id": 235235,
      "name": "vo8io"
    }
    ],
    "status": "available"
    }

    update_pet=requests.put(f'{base_url}/pet', json=update_data)
    print('Update pet info '+ update_pet.text)
    print(update_pet.status_code)
    print(update_pet.headers)

    assert update_pet.status_code == 200
    assert update_pet.headers['Content-Type'] == 'application/json'


    # Find pet by id
    get_pet = requests.get(f'{base_url}/pet/{pet_id}')
    print('Find pet by id '+ get_pet.text)
    print(get_pet.status_code)
    print(get_pet.headers)

    assert get_pet.status_code==200
    assert get_pet.headers['Content-Type']=='application/json'
    pet_info = get_pet.json()
    assert pet_info['id'] == update_data['id']
    assert pet_info['status'] == update_data['status']

    schema= {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer"
    },
    "category": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer"
        },
        "name": {
          "type": "string"
        }
      },
      "required": [
        "id",
        "name"
      ]
    },
    "name": {
      "type": "string"
    },
    "photoUrls": {
      "type": "array",
      "items": [
        {
          "type": "string"
        },
        {
          "type": "string"
        }
      ]
    },
    "tags": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            }
          },
          "required": [
            "id",
            "name"
          ]
        },
        {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            }
          },
          "required": [
            "id",
            "name"
          ]
        }
      ]
    },
    "status": {
      "type": "string"
    }
  },
  "required": [
    "id",
    "category",
    "name",
    "photoUrls",
    "tags",
    "status"
  ]
}
    try:
        validate(instance=pet_info,schema=schema)
        print("Json schema validation is success.")
    except jsonschema.exceptions.ValidationError as e:
        print("Error validation json schema: ")
        print(e)
        raise e

    # Delete a pet
    delete_pet = requests.delete(f'{base_url}/pet/{pet_id}')
    print('Delete a pet '+ delete_pet.text)
    print(delete_pet.status_code)
    print(delete_pet.headers)
    print(pet_id)

    assert delete_pet.status_code==200
    assert delete_pet.headers['Content-Type']=='application/json'
