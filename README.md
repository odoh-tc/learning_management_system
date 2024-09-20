# FastAPI Learning Management System (LMS)

## Overview

This Learning Management System (LMS) is built using FastAPI and SQLAlchemy. It includes functionalities for managing users, courses, sections, content blocks, student progress, announcements, and messages. The system is designed with role-based access control, allowing different levels of access for admins, teachers, and students.

## Features

- **User Management**: Registration, authentication, and profile management.
- **Course Management**: Creation, update, and deletion of courses and sections.
- **Content Blocks**: Adding and managing content blocks (videos, text, quizzes) within sections.
- **Student Progress**: Tracking student progress through sections and content blocks.
- **Announcements**: Admins and teachers can post announcements.
- **Messages**: Admins, teachers, and students can send and receive messages.
- **Role-Based Access Control**: Ensures secure access based on user roles.
- **Enrollment**: Students can enroll in courses, which initializes their progress tracking.

## Models

### User

Attributes:

- `id`: Unique identifier.
- `username`: User's username.
- `email`: User's email address.
- `role`: User's role (admin, teacher, student).

### Course

Attributes:

- `id`: Unique identifier.
- `title`: Title of the course.
- `description`: Description of the course.
- `category_id`: Foreign key linking the course to its category.

### Section

Attributes:

- `id`: Unique identifier.
- `title`: Title of the section.
- `course_id`: Foreign key linking the section to its course.

### ContentBlock

A `ContentBlock` represents a piece of content within a section. This can be a video, text, or quiz.

Attributes:

- `id`: Unique identifier.
- `title`: Title of the content block.
- `description`: Description of the content block.
- `type`: Type of content (video, text, quiz).
- `url`: URL for video content.
- `content`: Text content.
- `section_id`: Foreign key linking the content block to its section.

### StudentContentBlock

A `StudentContentBlock` tracks a student's progress on a specific content block. It includes information such as whether the content block is completed, the student's feedback, and their grade.

Attributes:

- `id`: Unique identifier.
- `student_id`: Foreign key linking to the student.
- `content_block_id`: Foreign key linking to the content block.
- `completed`: Boolean indicating if the content block is completed.
- `url`: URL for student-submitted content (e.g., assignment submissions).
- `feedback`: Feedback from the teacher.
- `grade`: Grade awarded by the teacher.

### Category

Attributes:

- `id`: Unique identifier.
- `name`: Name of the category.

### Announcement

Attributes:

- `id`: Unique identifier.
- `title`: Title of the announcement.
- `message`: Message content.
- `user_id`: Foreign key linking the announcement to the user who created it.

### Message

Attributes:

- `id`: Unique identifier.
- `sender_id`: Foreign key linking to the sender user.
- `receiver_id`: Foreign key linking to the receiver user.
- `content`: Message content.

## Roles and Responsibilities

### Admin

- Can create, update, or delete courses and sections.
- Can manage announcements and messages.
- Has access to all user profiles and can manage user roles.

### Teacher

- Can create courses and sections.
- Can add content blocks to sections and manage them.
- Can view and manage student enrollments in their courses.
- Can post announcements related to their courses.

### Student

- Can enroll in courses.
- Can view course content and progress through sections and content blocks.
- Can submit completed content blocks and receive grades and feedback.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/your-repo-name.git
   ```

2. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```sh
   alembic upgrade head
   ```

4. Run the application:
   ```sh
   uvicorn main:app --reload
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- SQLAlchemy: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)

## Contact

- Portfolio: [https://odoh-tc.github.io/portfolio/](https://odoh-tc.github.io/portfolio/)

<!--

"This Learning Management System (LMS) empowers administrators, teachers, and students with robust features. It facilitates comprehensive management of users, courses, sections, content blocks, student progress tracking, announcements, and messaging. Built-in role-based access control ensures secure and tailored access levels for administrators, teachers, and students, fostering efficient educational administration and engagement." -->
