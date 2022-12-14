import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from django.urls import reverse

from accounts.messages import PASSWORD_CONFIRM_PASSWORD_NOT_MATCH
from accounts.models import Teacher

from .extra import non_field_error

url = reverse("student:Teacher_Register")
pytestmark = pytest.mark.django_db


_DATA = {
    "name": "Admin",
    "email": "teacher@test.com",
    "tea_id": "Teacher_No_10",
    "password": "1234",
    "password2": "1234",
}


def test_get_zero_content(client, create_test_admin):

    # arrange
    token = create_test_admin

    response = client.post(  # act
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": {
            "email": [
                "This field is required.",
            ],
            "name": [
                "This field is required.",
            ],
            "password": [
                "This field is required.",
            ],
            "password2": [
                "This field is required.",
            ],
            "tea_id": ["This field is required."],
        },
    }


def test_wrong_confirm_password(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    data["password2"] = "12345"
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == non_field_error(
        PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    )


def test_with_same_email(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    Teacher.objects.create(
        name="Admin",
        email="teacher@test.com",
    )
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": {
            "email": [
                "user with this Email already exists.",
            ],
        },
    }


def test_with_wrong_data(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    data["email"] = "teachertest.com"
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": {
            "email": [
                "Enter a valid email address.",
            ],
        },
    }


@patch("accounts.views.teacher_views.get_tokens_for_user")
def test_registeration_success(patch_token, client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    patch_token.return_value = {
        "refresh": "DummyRefreshToken",
        "access": "DummyAccessToken",
    }
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 201
    assert json.loads(response.content) == {
        "msg": "Registeration Success",
        "token": {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken",
        },
    }
