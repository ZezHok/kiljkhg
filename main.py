import pytest
import requests
from randimage import get_random_image
from PIL import Image
import tempfile
import numpy as np
import jsonschema
from jsonschema import validate


@pytest.mark.parametrize("img_format", ['PNG', 'JPEG'])
def test_upload_pet_image_format(base_url, pet_id, img_format):
    img_size = (128, 128)
    img = get_random_image(img_size)
    img = (img * 255).astype(np.uint8)

    additional_metadata = 'Random image upload'

    with tempfile.NamedTemporaryFile(suffix=f'.{img_format}', delete=False) as temp_image_file:
        image_path = temp_image_file.name
        image = Image.fromarray(img)
        image.save(image_path, format=img_format.upper())

    with open(image_path, 'rb') as file:
        upload_image_pet = requests.post(
            f'{base_url}/pet/{pet_id}/uploadImage',
            data={'additionalMetadata': additional_metadata},
            files={'file': file}
        )

    print('\n1.1. Upload pet image: checking format of images')
    print('Text: ' + upload_image_pet.text)
    print('Status: ' + str(upload_image_pet.status_code))
    assert upload_image_pet.status_code == 200


@pytest.mark.parametrize("additional_metadata", ['Random image upload', '112324', ''])
def test_upload_image_metadata(base_url, pet_id, additional_metadata):
    img_size = (128, 128)
    img = get_random_image(img_size)
    img = (img * 255).astype(np.uint8)

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image_file:
        image_path = temp_image_file.name
        image = Image.fromarray(img)
        image.save(image_path)

    with open(image_path, 'rb') as file:
        upload_image_pet = requests.post(
            f'{base_url}/pet/{pet_id}/uploadImage',
            data={'additionalMetadata': additional_metadata},
            files={'file': file}
        )

    print('\nUpload pet image: checking additional data')
    print('Text: ' + upload_image_pet.text)
    print('Status: ' + str(upload_image_pet.status_code))
    assert upload_image_pet.status_code == 200


@pytest.mark.parametrize("img_size, expected_status", [
    ((256, 512), 200),
    ((512, 1024), 200),
    ((1, 1), 200),
    ((0, 0), 400)
])
def test_upload_pet_image_sizes_statuses(base_url, pet_id, img_size, expected_status):
    def upload_image(file, metadata):
        return requests.post(
            f'{base_url}/pet/{pet_id}/uploadImage',
            data={'additionalMetadata': metadata},
            files={'file': file}
        )

    if img_size == (0, 0):
        response = upload_image(('empty.png', b'', 'image/png'), 'Testing with (0, 0) image')
        print('\nAttempted upload with image size (0, 0)')

    elif img_size == (1, 1):
        response = upload_image(('small.png', b'', 'image/png'), 'Testing with (1, 1) image')
        print('\nAttempted upload with image size (1, 1)')

    else:
        img = get_random_image(img_size)
        img = (img * 255).astype(np.uint8)
        additional_metadata = 'Random image upload'

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image_file:
            image_path = temp_image_file.name
            Image.fromarray(img).save(image_path)

        with open(image_path, 'rb') as file:
            response = upload_image(file, additional_metadata)

        print(f'\nUpload pet image with size {img_size}')

    print('\nUpload pet image: image size & status code')
    print('Text: ' + response.text)
    print('Status: ' + str(response.status_code))
    assert response.status_code == expected_status


def test_update_pet_data(base_url, update_pet_data):
    update_pet = requests.put(f'{base_url}/pet', json=update_pet_data)

    print('\nUpdate pet data')
    print('Text: ' + update_pet.text)
    print('Status: ' + str(update_pet.status_code))
    assert update_pet.status_code == 200
    print('Headers: ' + str(update_pet.headers))
    assert update_pet.headers['Content-Type'] == 'application/json'


def test_find_by_pet_id(base_url, pet_id, update_pet_data):
    find_pet = requests.get(f'{base_url}/pet/{pet_id}')

    print('\nFind pet by pet ID')
    print('Text: ' + find_pet.text)
    print('Status: ' + str(find_pet.status_code))
    assert find_pet.status_code == 200
    print('Headers: ' + str(find_pet.headers))
    assert find_pet.headers['Content-Type'] == 'application/json'

    pet_info = find_pet.json()
    assert pet_info['status'] == update_pet_data['status']
    assert pet_info['id'] == update_pet_data['id']

    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "category": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                },
                "required": ["id", "name"]
            },
            "name": {"type": "string"},
            "photoUrls": {
                "type": "array",
                "items": {"type": "string"}
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"}
                    },
                    "required": ["id", "name"]
                }
            },
            "status": {"type": "string"}
        },
        "required": ["id", "category", "name", "photoUrls", "tags", "status"]
    }

    try:
        validate(instance=pet_info, schema=schema)
        print('JSON schema validation success')

    except jsonschema.exceptions.ValidationError as e:
        print('Error validation JSON schema')
        print(e)
        raise e