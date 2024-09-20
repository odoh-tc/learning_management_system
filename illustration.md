# Models

## User

A User represents a person using the LMS. Users can have different roles such as Admin, Teacher, or Student.

### Attributes

- `id`: Unique identifier.
- `email`: Email of the user.
- `role`: Role of the user (admin, teacher, student).
- `is_active`: Boolean indicating if the user is active.
- `password`: User's password.

### Relationships

- `profile`: One-to-one relationship with Profile.
- `created_courses`: One-to-many relationship with Course (for teachers).
- `student_courses`: Many-to-many relationship with Course (for students).
- `student_content_blocks`: Many-to-many relationship with ContentBlock (for students).

## Profile

A Profile stores additional information about a user.

### Attributes

- `id`: Unique identifier.
- `first_name`: First name of the user.
- `last_name`: Last name of the user.
- `bio`: Biography of the user.
- `user_id`: Foreign key linking to the user.

### Relationships

- `owner`: One-to-one relationship with User.

## Course

A Course represents a course in the LMS.

### Attributes

- `id`: Unique identifier.
- `title`: Title of the course.
- `description`: Description of the course.
- `user_id`: Foreign key linking to the creator (teacher or admin).
- `category_id`: Foreign key linking to the category.

### Relationships

- `created_by`: Many-to-one relationship with User (creator).
- `sections`: One-to-many relationship with Section.
- `student_courses`: Many-to-many relationship with User (students).
- `category`: Many-to-one relationship with Category.

## Section

A Section represents a section within a course.

### Attributes

- `id`: Unique identifier.
- `title`: Title of the section.
- `description`: Description of the section.
- `course_id`: Foreign key linking to the course.

### Relationships

- `course`: Many-to-one relationship with Course.
- `content_blocks`: One-to-many relationship with ContentBlock.

## ContentBlock

A ContentBlock represents a piece of content within a section. This can be a video, text, or quiz.

### Attributes

- `id`: Unique identifier.
- `title`: Title of the content block.
- `description`: Description of the content block.
- `type`: Type of content (video, text, quiz).
- `url`: URL for video content.
- `content`: Text content.
- `section_id`: Foreign key linking the content block to its section.

### Relationships

- `section`: Many-to-one relationship with Section.
- `student_content_blocks`: One-to-many relationship with StudentContentBlock.

## StudentContentBlock

A StudentContentBlock tracks a student's progress on a specific content block. It includes information such as whether the content block is completed, the student's feedback, and their grade.

### Attributes

- `id`: Unique identifier.
- `student_id`: Foreign key linking to the student.
- `content_block_id`: Foreign key linking to the content block.
- `completed`: Boolean indicating if the content block is completed.
- `url`: URL for student-submitted content (e.g., assignment submissions).
- `feedback`: Feedback from the teacher.
- `grade`: Grade awarded by the teacher.

### Relationships

- `student`: Many-to-one relationship with User.
- `content_block`: Many-to-one relationship with ContentBlock.

## StudentCourse

A StudentCourse tracks a student's enrollment in a course.

### Attributes

- `id`: Unique identifier.
- `student_id`: Foreign key linking to the student.
- `course_id`: Foreign key linking to the course.
- `completed`: Boolean indicating if the course is completed.

### Relationships

- `student`: Many-to-one relationship with User.
- `course`: Many-to-one relationship with Course.

## Category

A Category groups courses into different categories.

### Attributes

- `id`: Unique identifier.
- `name`: Name of the category.

### Relationships

- `courses`: One-to-many relationship with Course.

## Announcement

An Announcement represents an announcement made by a user.

### Attributes

- `id`: Unique identifier.
- `title`: Title of the announcement.
- `message`: Message of the announcement.
- `user_id`: Foreign key linking to the user who made the announcement.

### Relationships

- `user`: Many-to-one relationship with User.

## Message

A Message represents a message between users.

### Attributes

- `id`: Unique identifier.
- `sender_id`: Foreign key linking to the sender.
- `receiver_id`: Foreign key linking to the receiver.
- `content`: Content of the message.

### Relationships

- `sender`: Many-to-one relationship with User (sender).
- `receiver`: Many-to-one relationship with User (receiver).
