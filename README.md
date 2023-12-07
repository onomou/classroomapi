# ClassroomAPI

ClassroomAPI is a Python library for accessing [Google Classroom's API](https://developers.google.com/classroom/reference/rest). It aims to be more Pythonic than Google's own [Classrom Python API](https://googleapis.github.io/google-api-python-client/docs/dyn/classroom_v1.html). It has been heavily influenced by UCF Open's [CanvasAPI](https://github.com/ucfopen/canvasapi).

## Installation

Copy this repository to a folder and run your scripts in the root. Package listing on PyPI may come in the future.

## Documentation

Documentation is not available yet. So sorry.

## Contributing

This is a crude attempt to mirror canvasapi for Google Classroom.

## Quickstart

Download your own `token.json` from [Google Cloud console](https://console.cloud.google.com/apis/credentials), then put the following in a `script.py`.

```python
from classroomapi.classroom import Classroom 

classroom = Classroom("token.json")
```

### Working with Classroom Objects

```python
# list all courses
courses = classroom.get_courses()
print(courses)

# list all assignments in a course
course = courses[0]
assignments = course.get_assignments()
print(assignments)
```

### Known Issues

Pagination needs to be implemented. Requests to list classes, assignments, etc. still need to have `pageSize` implemented.

Coverage of all endpoints is not anywhere close to complete yet.

The structure of Google Classroom's API prevents the user from modifying many things. Check the `associatedWithDeveloper` attribute to see if this is the issue. The best way to ensure you have access to edit everything is to create the course and all assignments with the API.

For example, any course created with the web interface cannot be modified by the API. Any assignment created with the web interface or an external service (like [Desmos Classroom](https://teacher.desmos.com/)) cannot be modified by the API.

* [StackOverflow: Classroom.Courses.CourseWork.patch](https://stackoverflow.com/questions/69036227/classroom-courses-coursework-patch]
* [StackOverflow: Google Classroom API modifyAttachments](https://stackoverflow.com/questions/38313748/google-classroom-api-modifyattachments)
* [StackOverflow: Unable to grade student work via API if assignment was created in the Google Classroom UI](https://stackoverflow.com/questions/39302231/unable-to-grade-student-work-via-api-if-assignment-was-created-in-the-google-cla?noredirect=1&lq=1)
* [Issue Tracker: Allow to edit course work submission grade from developer project that did not create that coursework](https://issuetracker.google.com/issues/222811927)
* [Issue Tracker: Coursework: Modify assignments that were not created by the app](https://issuetracker.google.com/issues/36760149)

