# Integration testing for the entire project
# Needs a Postgres database running on localhost:5432
# Needs a Redis server running on localhost:6379
import requests
import pytest
from models.bitarray import BitArray


@pytest.mark.dependency()
def test_create_bit_array():
    path = '/bit-array'
    # Create a bit array
    response = requests.put(pytest.api_url + path)
    assert response.status_code == 200
    assert 'id' in response.json()
    pytest.created_bit_array_id = response.json()['id']


@pytest.mark.dependency(depends=['test_create_bit_array'])
def test_free_space():
    path = f'/bit-array/{pytest.created_bit_array_id}/free'
    response = requests.get(pytest.api_url + path)
    assert response.status_code == 200
    assert response.json()['free'] == 2**17


@pytest.mark.dependency(depends=['test_create_bit_array'])
def test_get_compressed():
    path = f'/bit-array/{pytest.created_bit_array_id}'
    response = requests.get(pytest.api_url + path)
    assert response.status_code == 200
    assert 'bit-array' in response.json()
    assert len(response.json()['bit-array']) == len('H4sIAGrhp2UC/+3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAIC3AYbSVKsAQAAA')


@pytest.mark.dependency(depends=['test_free_space', 'test_get_compressed'])
def test_acquire_index():
    path = f'/bit-array/{pytest.created_bit_array_id}/index'
    response = requests.put(pytest.api_url + path)
    assert response.status_code == 200
    assert 'index' in response.json()
    assert response.json()['index'] >= 0
    assert response.json()['index'] < 2**17
    pytest.acquired_index = response.json()['index']


@pytest.mark.dependency(depends=['test_acquire_index'])
def test_flip_bit():
    path = f'/bit-array/{pytest.created_bit_array_id}/{pytest.acquired_index}'
    response = requests.post(pytest.api_url + path)
    assert response.status_code == 200

    bit_array_path = f'/bit-array/{pytest.created_bit_array_id}'
    response = requests.get(pytest.api_url + bit_array_path)
    assert response.status_code == 200
    assert 'bit-array' in response.json()
    bit_array = BitArray.decompress(response.json()['bit-array'], id=pytest.created_bit_array_id)
    assert bit_array[pytest.acquired_index] == 1
