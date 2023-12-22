# ClassroomAPI

ClassroomAPI is a Python library for accessing [Google Classroom's API](https://developers.google.com/classroom/reference/rest). It aims to be more Pythonic than Google's own [Classrom Python API](https://googleapis.github.io/google-api-python-client/docs/dyn/classroom_v1.html). It has been heavily influenced by (code copied from) [UCF Open's CanvasAPI](https://github.com/ucfopen/canvasapi).

Major changes from Google's Python API include accessing object details as attributes `class.name` instead of JSON dict entries like `class["name"]`. `courseWork` can be accessed by type, so `course.get_coursework()` gets everything, but `course.get_assignments()` only gets `ASSIGNMENT` objects.

## Installation

### Get From TestPyPI

```bash
py -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps classroomapi
```

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

### Create a new course
```python
course_information = {
    'name': 'New Course Name',
    'ownerId': 'me',
    'room': '105A',
    'description': 'Course description',
    'section': 'A',
    'descriptionHeading': 'This course created with classroomapi',
}
course = classroom.create_course(course_information)
```

## Documentation

Documentation is not available yet. So sorry.

### Additional Functionality

#### Get all courseWork or single courseWork by ID
```python
course.get_coursework()
course.get_coursework(coursework_id)
```

#### Get assignments or single assignment by ID
```python
course.get_assignments()
course.get_assignment(assignment_id)
```

#### Get short answer questions
```python
course.get_shortanswerquestions()
course.get_shortanswerquestion(question_id)
```

#### Get multiple choice questions
```python
course.get_multiplechoicequestions()
course.get_multiplechoicequestion(question_id)
```

#### Edit things (course, assignment, etc.)
Verb option instead of _patch_
```python
classroom.edit_course(course_id, body, update_mask)
assignment.edit(body, update_mask)
# etc.
```


## Contributing

This is a crude attempt to mirror canvasapi for Google Classroom. Pull requests are welcome. This is my first package, and it may need to be majorly restructured.

### Build

```bash
py -m pip install --upgrade build
py -m build
```

### Development Mode Install
```bash
pip install --editable .
```

### Upload, if you have edit rights on PyPI
```bash
py -m pip install --upgrade twine
py -m twine upload --skip-existing --repository testpypi dist/*
```

## To Do
- [ ]  Pagination
- [ ]  `pageSize` for requests to list classes, assignments, etc.
- [ ]  Unit tests
- [ ] Verify coverage of API endpoints
- [ ] Consider fetching information directly from Google Classroom API, rather than using Google's Python API
- [ ] Control scope of Classroom class, which currently requests all possible permissions

## Known Issues

The structure of Google Classroom's API prevents the user from modifying many things. Check the `associatedWithDeveloper` attribute to see if this is the issue. The best way to ensure you have access to edit everything is to create the course and all assignments with the API.

For example, the details of any course created with the web interface cannot be modified by the API. Any assignment created with the web interface or an external service (like [Desmos Classroom](https://teacher.desmos.com/)) cannot be modified by the API. This has something to do with the token used to create the item.

* [**StackOverflow:** Classroom.Courses.CourseWork.patch](https://stackoverflow.com/questions/69036227/classroom-courses-coursework-patch)
* [**StackOverflow:** Google Classroom API modifyAttachments](https://stackoverflow.com/questions/38313748/google-classroom-api-modifyattachments)
* [**StackOverflow:** Unable to grade student work via API if assignment was created in the Google Classroom UI](https://stackoverflow.com/questions/39302231/unable-to-grade-student-work-via-api-if-assignment-was-created-in-the-google-cla?noredirect=1&lq=1)
* [**Google Issue Tracker:** Allow to edit course work submission grade from developer project that did not create that coursework](https://issuetracker.google.com/issues/222811927)
* [**Google Issue Tracker:** Coursework: Modify assignments that were not created by the app](https://issuetracker.google.com/issues/36760149)

