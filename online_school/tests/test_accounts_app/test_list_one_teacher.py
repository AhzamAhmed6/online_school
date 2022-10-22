import json

import pytest
from django.urls import reverse


url = reverse("student:TeacherDetail", kwargs={"slug": "teacher_no_10"})
pytestmark = pytest.mark.django_db


def test_list_no_teacher_detail(client, create_test_admin):
    """
    Check the response when no teacher is present in out database / wrong slug
    """
    token = create_test_admin

    response = client.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {token}"})  # act

    assert response.status_code == 404
    assert json.loads(response.content) == {"errors": {"detail": "Not found."}}


@pytest.mark.xfail()
def test_list_one_teacher(client, create_test_teacher_with_kwargs):
    create_test_teacher_with_kwargs(
        client=client,
        email="test1@example.com",
        name="Test",
        tea_id="teacher_no_10",
        password="password1234",
        password2="password1234",
    )

    response = client.get(url)  # act

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "email": "test1@example.com",
        "name": "Test",
        "tea_id": "teacher_no_10",
        "currently_teaching": [],
    }
