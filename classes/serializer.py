from rest_framework import serializers
from .models import Classes, Course, TimeTable
from accounts.models import Teacher
from .messages import *


class CourseSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)

    class Meta:
        model = Course
        exclude = ['teacher']

    def validate(self, data):

        name = data.get('name')
        course_code: Course.course_code = data.get('course_code')
        ch = data.get('ch')
        email = data.get('email')
        teacher: Teacher = Teacher.objects.filter(email=email)
        if teacher:
            course: Course = Course.objects.create(
                name=name, course_code=course_code, ch=ch, teacher=Teacher.objects.get(email=email))

            course.save()
            return data
        else:
            raise serializers.ValidationError(NO_TEACHER_FOUND_MESSAGE)


class TimeTableSerializer(serializers.ModelSerializer):
    _class_ = serializers.UUIDField()

    class Meta:
        model = TimeTable
        exclude = ['_class']

    def validate(self, data):
        days = data.get('days')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        _class = data.get('_class_')
        is_class_exists = Classes.objects.filter(id=_class)

        if is_class_exists:
            timetable: TimeTable = TimeTable.objects.create(
                days=days, start_time=start_time, end_time=end_time, _class=Classes.objects.get(id=_class))

            timetable.save()
            return data
        else:
            raise serializers.ValidationError(NO_COURSE_FOUND_MESSAGE)
