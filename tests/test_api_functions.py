import pytest
from fastapi import status

from app.components.http_errors import HttpErrorEnum


@pytest.mark.parametrize(
    'url',
    [
        'http://test.ru',
        'https://test.ru',
        'http://test.ru/',
        'http://test.ru/' + '1'*2068
    ]
)
def test_post_url_api_201(client, url):
    result = client.post('/', params={'original_url': url})

    assert result.status_code == status.HTTP_201_CREATED
    assert result.json()
    assert isinstance(result.json(), str)


@pytest.mark.parametrize(
    'url',
    [
        'test.ru',
        'https://',
        'http://test',
        'http://t.g',
        'ftp://test.ru',
        'http://test.ru/' + '1'*2069
    ]
)
def test_post_url_api_422(url, client):
    result = client.post('/', params={'original_url': url})
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_post_url_api_409(client, create_url_record_db):
    original_url, _, __, ___ = create_url_record_db

    result = client.post('/', params={'original_url': original_url})

    assert result.status_code == status.HTTP_409_CONFLICT
    assert result.json().get('detail') == HttpErrorEnum.URL_CREATED_409


def test_get_url_api_200(client, create_url_record_db):
    original_url, _, __, created = create_url_record_db

    result = client.get('/', params={'short_url': created})

    assert result.status_code == status.HTTP_200_OK, result.text
    assert result.json() == original_url


def test_get_url_api_404(client, create_url_record_data):
    _, __, short_url = create_url_record_data

    result = client.get('/', params={'short_url': short_url})

    assert result.status_code == status.HTTP_404_NOT_FOUND, result.text


def test_delete_url_api_200(client, create_url_record_db):
    original_url, _, __, created = create_url_record_db

    result = client.delete('/', params={'short_url': created})

    assert result.status_code == status.HTTP_200_OK, result.text
    assert result.json() == "OK"

    result = client.get('/', params={'short_url': created})

    assert result.status_code == status.HTTP_404_NOT_FOUND, result.text


def test_delete_url_api_404(client, create_url_record_data):
    _, __, short_url = create_url_record_data

    result = client.delete('/', params={'short_url': short_url})

    assert result.status_code == status.HTTP_404_NOT_FOUND, result.text

    result = client.get('/', params={'short_url': short_url})

    assert result.status_code == status.HTTP_404_NOT_FOUND, result.text
