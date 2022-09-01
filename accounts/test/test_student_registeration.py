import json
from unittest.mock import patch

import pytest
from accounts.models import Student
from django.urls import reverse

url = reverse('Student_Register')
pytestmark = pytest.mark.django_db

FIELD_REQUIRED_MESSAGE = {
    'errors': {
        "email": [
            "This field is required."
        ],
        "name": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ],
        "password2": [
            "This field is required."
        ]}
}


def test_get_zero_content(client, create_test_admin):
    token = create_test_admin

    response = client.post(
        url,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
    )

    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == FIELD_REQUIRED_MESSAGE


def test_wrong_confirm_password(client, create_test_admin):
    data = {
        'name': 'Student', 'email': 'student@test.com', 'password': '1234',
        'password2': '12345'}
    token = create_test_admin
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {'errors': {
        "non_field_errors": [
            "Password and Confirm Password doesn't match"
        ]}
    }


def test_with_same_email(client, create_test_admin):
    Student.objects.create(name='Admin', email='student@test.com')
    data = {'name': 'Student', 'email': 'student@test.com',
            'password': '1234', 'password2': '1234'}
    token = create_test_admin
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {'errors': {
        "email": [
            "user with this Email already exists."
        ]}
    }


def test_with_wrong_data(client, create_test_admin):
    data = {'name': 'Admin', 'email': 'studenttest.com',
            'password': '1234', 'password2': '1234'}
    token = create_test_admin
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {'errors': {
        "email": [
            "Enter a valid email address."
        ]}
    }


@patch('accounts.views.get_tokens_for_user')
def test_registeration_success(patch_token, client, create_test_admin):
    patch_token.return_value = {
        "refresh": "DummyRefreshToken",
        "access": "DummyAccessToken"
    }
    data = {
        'name': 'Student',
        'email': 'student@example.com',
        'password': '1234',
        'password2': '1234'
    }
    token = create_test_admin
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content == {
        "msg": "Registeration Success",
        "token": {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken"
        }
    }
