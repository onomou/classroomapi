from classroomapi.classroom import Classroom

# get token.json from Google Cloud console
# https://developers.google.com/classroom/quickstart/python
# https://console.cloud.google.com/apis/credentials
classroom = Classroom("token.json")
courses = classroom.get_courses()
print(courses)