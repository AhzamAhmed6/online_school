from accounts.custom_permissions import IsAdmin, IsAdminTeacher
from accounts.generate_tokens import get_tokens_for_user
from accounts.messages import (
    ADMIN_REGISTERATION_SUCCESS_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_STATUS,
    LOGIN_SUCCESS_MESSAGE,
    LOGIN_SUCCESS_STATUS,
    PASSWORD_CHANGE_SUCCESS_MESSAGE,
    PASSWORD_CHANGE_SUCCESS_STATUS,
    REGISTERATION_SUCCESS_STATUS,
)
from accounts.models import Student, StudentMore, Teacher, TeacherMore
from accounts.serializers import (
    AdminChangePasswordSerializer,
    AdminChangeTeacherStudentPasswordSerializer,
    AdminLoginSerializer,
    AdminProfileSerializer,
    AdminRegisterationSerializer,
)
from classes.models import Classes, Course
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from swagger_responses.accounts_responses.admin_responses import (
    admin_change_password_response,
    admin_change_ts_password_response,
    admin_login_response,
    admin_profile_response,
    admin_register_response,
)


class AdminRegisterationView(GenericAPIView):
    """## For Admin **`Registeration`**"""

    serializer_class = AdminRegisterationSerializer

    @swagger_auto_schema(responses=admin_register_response)
    def post(self, request):
        serializer = AdminRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        return Response(
            {"msg": ADMIN_REGISTERATION_SUCCESS_MESSAGE, "token": token},
            status=REGISTERATION_SUCCESS_STATUS,
        )


class AdminLoginView(GenericAPIView):
    """## For Admin **`Login`**"""

    serializer_class = AdminLoginSerializer

    @swagger_auto_schema(responses=admin_login_response)
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {
                    "errors": {
                        "non_field_errors": [
                            EMAIL_PASSWORD_NOT_VALID_MESSAGE,
                        ],
                    },
                },
                status=EMAIL_PASSWORD_NOT_VALID_STATUS,
            )

        return Response(
            {"msg": LOGIN_SUCCESS_MESSAGE, "token": get_tokens_for_user(user)},
            status=LOGIN_SUCCESS_STATUS,
        )


class AdminProfileView(GenericAPIView):
    """## For Admin to view his/her **`Profile`**"""

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminProfileSerializer

    @swagger_auto_schema(responses=admin_profile_response)
    def get(self, request):
        serializer = AdminProfileSerializer(request.user)

        return Response(serializer.data, status=200)


class AdminChangeTeacherStudentPasswordView(GenericAPIView):
    """## For Admin to change Teacher's/Student's account's **`password`**"""

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminChangeTeacherStudentPasswordSerializer

    @swagger_auto_schema(responses=admin_change_ts_password_response)
    def post(self, request):
        serializer = AdminChangeTeacherStudentPasswordSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": PASSWORD_CHANGE_SUCCESS_MESSAGE},
            status=PASSWORD_CHANGE_SUCCESS_STATUS,
        )


class AdminChangePasswordView(GenericAPIView):
    """## For Admin to change his/her account's **`password`**"""

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminChangePasswordSerializer

    @swagger_auto_schema(responses=admin_change_password_response)
    def post(self, request):
        seriaizer = AdminChangePasswordSerializer(
            data=request.data,
            context={
                "user": request.user,
            },
        )
        seriaizer.is_valid(raise_exception=True)

        return Response(
            {"msg": PASSWORD_CHANGE_SUCCESS_MESSAGE},
            status=PASSWORD_CHANGE_SUCCESS_STATUS,
        )


class AdminDeleteStudent(GenericAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, slug):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        if student_more := StudentMore.objects.filter(slug=slug):
            student: Student = student_more[0].user
            student.delete()
            student_more.delete()
            return Response({"msg": "Student deleted successfully"}, status=200)
        return Response({"msg": "Student not Found"}, status=404)


class AdminDeleteTeacher(GenericAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, slug):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        if teacher_more := TeacherMore.objects.filter(slug=slug):
            teacher: Teacher = teacher_more[0].user
            teacher.delete()
            teacher_more.delete()
            return Response({"msg": "Teacher deleted successfully"}, status=200)
        return Response({"msg": "Teacher not Found"}, status=404)


class AdminDeleteCourse(GenericAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, slug):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        if course := Course.objects.filter(slug=slug):
            course.delete()
            return Response({"msg": "Course deleted successfully"}, status=200)
        return Response({"msg": "Course not Found"}, status=404)


class AdminDeleteClass(GenericAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = [IsAuthenticated, IsAdminTeacher]

    def delete(self, request, slug):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        if course := Classes.objects.filter(slug=slug):
            course.delete()
            return Response({"msg": "Class deleted successfully"}, status=200)
        return Response({"msg": "Class not Found"}, status=404)
