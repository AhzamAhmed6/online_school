# @REM MIGRATION AND MIGRATE
python3 manage.py makemigrations classes
python3 manage.py makemigrations accounts
python3 manage.py migrate


# @REM CREATE SUPER USER
echo "User.objects.create_superuser(email='superuser@test.com',name='ahzam',password='1234')" | python3 manage.py shell_plus


# @REM CREATE 3 ADMINS
echo "Admin.objects.create_user(email='admin1@test.com', name='Admin1', password='1234')" | python3 manage.py shell_plus
echo "Admin.objects.create_user(email='admin2@test.com', name='Admin2', password='1234')" | python3 manage.py shell_plus
echo "Admin.objects.create_user(email='admin3@test.com', name='Admin3', password='1234')" | python3 manage.py shell_plus


# @REM CREATE 3 TEACHERS
echo "Teacher.objects.create_user(email='teacher1@test.com', name='Teacher1', password='1234')" | python3 manage.py shell_plus
echo "Teacher.objects.create_user(email='teacher2@test.com', name='Teacher2', password='1234')" | python3 manage.py shell_plus
echo "Teacher.objects.create_user(email='teacher3@test.com', name='Teacher3', password='1234')" | python3 manage.py shell_plus


# @REM CREATE 3 STUDENTS
echo "Student.objects.create_user(email='student1@test.com', name='Student1', password='1234')" | python3 manage.py shell_plus
echo "Student.objects.create_user(email='student2@test.com', name='Student2', password='1234')" | python3 manage.py shell_plus
echo "Student.objects.create_user(email='student3@test.com', name='Student3', password='1234')" | python3 manage.py shell_plus


# @REM CREATE 4 COURSES
echo "course1=Course.objects.create(name='Test Course 1',course_code='TC123 1',ch=Course.CH.FOUR); course1.save(); course2=Course.objects.create(name='Test Course 2',course_code='TC123 2',ch=Course.CH.FOUR); course2.save(); course3=Course.objects.create(name='Test Course 3',course_code='TC123 3',ch=Course.CH.FOUR); course3.save(); course4=Course.objects.create(name='Test Course 4',course_code='TC123 4',ch=Course.CH.FOUR); course4.save(); course5=Course.objects.create(name='Test Course 5',course_code='TC123 5',ch=Course.CH.FOUR); course5.save(); course = Course.objects.create(name='Test Course 101',course_code='TC123 101',ch=Course.CH.FOUR); course.pre_req_courses.add(course1, course2, course3, course4, course5); course.save()" | python3 manage.py shell_plus


# @REM CREATE 4 CLASSES
echo "from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code='TC123 1'),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save()" | python3 manage.py shell_plus
echo "from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code='TC123 2'),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save()" | python3 manage.py shell_plus
echo "from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code='TC123 3'),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save()" | python3 manage.py shell_plus
echo "from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code='TC123 4'),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save()" | python3 manage.py shell_plus


# @REM CREATE 4 ATTENDENCES
echo "import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 1')),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save()" | python3 manage.py shell_plus
echo "import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 2')),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save()" | python3 manage.py shell_plus
echo "import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 3')),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save()" | python3 manage.py shell_plus
echo "import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 4')),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save()" | python3 manage.py shell_plus
# echo "import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 5')),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save()" | python3 manage.py shell_plus


# @REM CREATE 4 TimeTables
echo "import datetime; TimeTable.objects.create(days=TimeTable.DAYS.MONDAY,start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),room_no=TimeTable.ROOM_NO.ROOM_1,_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 1')))" | python3 manage.py shell_plus
echo "import datetime; TimeTable.objects.create(days=TimeTable.DAYS.MONDAY,start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),room_no=TimeTable.ROOM_NO.ROOM_1,_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 2')))" | python3 manage.py shell_plus
echo "import datetime; TimeTable.objects.create(days=TimeTable.DAYS.MONDAY,start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),room_no=TimeTable.ROOM_NO.ROOM_1,_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 3')))" | python3 manage.py shell_plus
echo "import datetime; TimeTable.objects.create(days=TimeTable.DAYS.MONDAY,start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),room_no=TimeTable.ROOM_NO.ROOM_1,_class=Classes.objects.get(course=Course.objects.get(course_code='TC123 4')))" | python3 manage.py shell_plus

# @REM RUN SERVER
python3 manage.py runserver
