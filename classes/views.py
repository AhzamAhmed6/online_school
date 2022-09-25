import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.custom_permissions import IsAdmin, IsTeacher
from classes.models import Course, Classes

from .helper import UUIDEncoder
from .messages import (
    CLASS_CREATE_SUCCESS_MESSAGE,
    CLASS_CREATE_SUCCESS_STATUS,
    COURSE_REGISTER_SUCCESS_MESSAGE,
    COURSE_REGISTER_SUCCESS_STATUS,
    TIMETABLE_REGISTER_SUCCESS_MESSAGE,
    TIMETABLE_REGISTER_SUCCESS_STATUS,
)
from .serializer import (
    ClassSerializer,
    CourseSerializer,
    ListAllClassesSerializer,
    ListAllCourseSerializer,
    ListOneClasseSerializer,
    ListOneCourseSerializer,
    TimeTableSerializer,
)


class AdminCreateCourseView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"msg": COURSE_REGISTER_SUCCESS_MESSAGE},
            status=COURSE_REGISTER_SUCCESS_STATUS,
        )


class TeacherCreateClassView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        teacher = request.user
        serializer = ClassSerializer(
            data=request.data,
            context={"teacher": teacher},
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": CLASS_CREATE_SUCCESS_MESSAGE},
            status=CLASS_CREATE_SUCCESS_STATUS,
        )


class AdminCreateTimeTableView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = TimeTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": TIMETABLE_REGISTER_SUCCESS_MESSAGE},
            status=TIMETABLE_REGISTER_SUCCESS_STATUS,
        )


# TODO
# courses should have other pre req courses
# Student can see all availabel classes
# student can enroll themself in a class of a course they are eligable of(they
# have already cleared pre req classes of that course)
# Teacher can create and insert Attendence


class ListAllCoursesView(APIView):
    def get(self, request):
        data = Course.objects.all()
        serializer = ListAllCourseSerializer(
            data,
            context={"request": request},
            many=True,
        )

        return Response(
            {"data": serializer.data},
            status=200,
        )


class ListOneCourseView(APIView):
    def get(self, request, slug):
        course = Course.objects.filter(slug=slug)
        serializer = ListOneCourseSerializer(
            course,
            context={"request": request},
            many=True,
        )
        json_data = json.dumps(serializer.data, cls=UUIDEncoder)
        json_without_slash = json.loads(json_data)

        return Response(json_without_slash, status=200)


# student can see all classes


class ListAllClassesView(APIView):
    def get(self, request):
        data = Classes.objects.all()
        serializer = ListAllClassesSerializer(
            data, many=True, context={"request": request}
        )
        json_data = json.dumps(serializer.data, cls=UUIDEncoder)
        json_without_slash = json.loads(json_data)
        return Response({"data": json_without_slash}, status=200)


class ListOneClassView(APIView):
    def get(self, request, slug):
        data = Classes.objects.filter(slug=slug)
        serializer = ListOneClasseSerializer(data, many=True)
        json_data = json.dumps(serializer.data, cls=UUIDEncoder)
        json_without_slash = json.loads(json_data)
        return Response({"data": json_without_slash}, status=200)
