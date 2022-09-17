import json
from copy import deepcopy

import pytest
from classes.messages import *
from django.urls import reverse

from .extra import non_field_error

url = reverse('ClassRegister')
pytestmark = pytest.mark.django_db

_DATA = {
    "course_code": "TC123",
    "enrollment_start_date": "2022-04-14",
    "enrollment_end_date": "2022-04-18",
    "section": "A"
}


def test_admin_create_class(client, create_test_admin, create_test_class):
    """Check the expected response if the for some how admin try to register course
    """

    DATA = deepcopy(_DATA)
    token = create_test_admin

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    error_message = {'errors': {
        'detail': 'You do not have permission to perform this action.'}}
    assert response_content == error_message


def test_create_class_with_wrong_coursecode(client, create_test_teacher):
    DATA = deepcopy(_DATA)
    token = create_test_teacher

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    error_message = non_field_error(NO_COURSE_ERROR_MESSAGE)
    assert response_content == error_message


def test_create_class_success(client, create_test_teacher, create_test_course):
    DATA = deepcopy(_DATA)
    token = create_test_teacher

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response_content == {'msg': CLASS_CREATE_SUCCESS_MESSAGE}
