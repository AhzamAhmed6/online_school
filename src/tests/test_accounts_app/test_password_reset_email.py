import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from django.core import mail
from django.urls import reverse

from accounts.messages import (
    PASSWORD_RESET_EMAIL_MESSAGE,
    USER_WITH_EMAIL_DOESNT_EXIST,
    password_reset_link,
)

from .extra import non_field_error

pytestmark = pytest.mark.django_db

_DATA = {
    "email": "ahzamahmed6@gmail.com",
    "name": "Student",
    "roll_no": "roll_no_1",
    "password": "1234",
    "password2": "1234",
}

EMAIL = {"email": "ahzamahmed6@gmail.com"}


def test_ending_emails(mailoutbox):

    assert len(mailoutbox) == 0

    mail.send_mail(  # act
        subject="TestSubject",
        message="TestMessage",
        from_email="test@gmail.com",
        recipient_list=["test1@gmail.com"],
        fail_silently=False,
    )

    m = mailoutbox[0]

    # assert
    assert m.subject == "TestSubject"
    assert m.body == "TestMessage"
    assert m.from_email == "test@gmail.com"
    assert list(m.to) == ["test1@gmail.com"]
    assert len(mailoutbox) == 1


def test_reset_password_with_wrong_email(client):
    response = client.post(  # act
        reverse("student:Admin_Reset_Password"),
        data=EMAIL,
    )

    # assert
    assert json.loads(response.content) == non_field_error(
        USER_WITH_EMAIL_DOESNT_EXIST,
    )


@pytest.fixture()
def create_test_student_with_legit_email(client, create_test_admin):
    data = deepcopy(_DATA)
    token = create_test_admin

    response = client.post(
        reverse("student:Student_Register"),
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )
    response_content = json.loads(response.content)

    return response_content["token"]["access"]


def test_reset_password_response(client, create_test_student_with_legit_email):

    response = client.post(  # act
        reverse("student:Admin_Reset_Password"),
        data=EMAIL,
    )

    # assert
    assert json.loads(response.content) == {
        "msg": PASSWORD_RESET_EMAIL_MESSAGE,
    }


@patch(
    ("accounts.serializers.common_serializers.PasswordResetTokenGenerator.make_token"),
)
@patch("accounts.serializers.common_serializers.urlsafe_base64_encode")
def test_reset_password_mail(
    patch_encode,
    make_token,
    client,
    create_test_student_with_legit_email,
    mailoutbox,
):

    # arrange
    patch_encode.return_value = "thisispatchencode"
    make_token.return_value = "thisispatchtoken"

    client.post(  # act
        reverse("student:Admin_Reset_Password"),
        data={"email": "ahzamahmed6@gmail.com"},
    )

    reset_link = password_reset_link("thisispatchencode", "thisispatchtoken")
    mail_message = mailoutbox[0]

    # assert
    assert mail_message.body.split(" ")[-1] == reset_link


@patch("accounts.views.student_views.get_tokens_for_user")
def test_reset_password(
    patch_token,
    client,
    create_test_student_with_legit_email,
    student_login,
    mailoutbox,
):

    # arrange
    response = student_login(
        patch_token=patch_token,
        client=client,
        email="ahzamahmed6@gmail.com",
        password="changed_password",
    )
    response = client.post(
        reverse("student:Admin_Reset_Password"),
        EMAIL,
    )
    mail_message = mailoutbox[0]
    reset_link = mail_message.body.split(" ")[-1] + "/"
    data = {
        "password": "changed_password",
        "password2": "changed_password",
    }

    response = client.post(reset_link, data=data)  # act

    # assert
    response.status_code == 200
    assert json.loads(response.content) == {
        "msg": "Password Reset Successfully",
    }
