import datetime
import json

import pytest
from django.urls import reverse

url = reverse("course:ClassDetail", kwargs={"slug": "test-course-999"})
pytestmark = pytest.mark.django_db


def test_no_class_detail(client, create_test_student):
    """
    Check the response if no course is present in our database / wrong slug
    """
    token = create_test_student

    response = client.get(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )  # act

    # assert response.status_code == 404
    assert json.loads(response.content) == {"errors": {"detail": "Not found."}}


@pytest.mark.xfail()
def test_lvl_1_class_detail(
    client,
    create_test_course_with_kwargs,
    create_test_class_with_kwargs,
    create_test_admin,
):
    """Check the response if there is one level 1 coure present in our DB"""

    token = create_test_admin
    create_test_course_with_kwargs(
        client=client,
        name="Test Course 1",
        course_code="TC 1",
        ch="4",
        pre_req_courses=[],
    )
    create_test_class_with_kwargs(
        client=client,
        course_code="TC 1",
        enrollment_start_date=datetime.date.today(),
        enrollment_end_date=datetime.date.today(),
        section="A",
    )

    response = client.get(
        reverse(
            "course:ClassDetail",
            kwargs={"slug": "test-course-1_a"},
        ),
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )  # act

    predicted_response = [
        {
            "course": {
                "course_detail": "http://testserver/api/classes/courses/test-course-1/",
                "name": "Test Course 1",
            },
            "teacher_name": "Teacher",
            "enrollment_start_date": "2022-10-07",
            "enrollment_end_date": "2022-10-07",
            "section": "A",
            "mid_exammination_date": None,
            "final_exammination_date": None,
            "student": [],
        },
    ]
    assert json.loads(response.content) == predicted_response
