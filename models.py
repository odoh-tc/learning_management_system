from datetime import datetime
from sqlalchemy import Boolean, Float, String, ForeignKey, Column, Integer, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from mixins import Timestamp
from schema.content_block import ContentType
from schema.user import Role 
from database import Base  # Assuming Base is defined in database.py

class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)  # Add this line
    role = Column(Enum(Role), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)  # Default to False
    password = Column(String(255), nullable=False)


    profile = relationship("Profile", back_populates="owner", uselist=False)
    created_courses = relationship("Course", back_populates="created_by", foreign_keys="Course.user_id")
    student_courses = relationship("StudentCourse", back_populates="student")
    student_content_blocks = relationship("StudentContentBlock", back_populates="student")
    payments = relationship("Payment", back_populates="user")

class Profile(Timestamp, Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="profile")

# class Course(Timestamp, Base):
#     __tablename__ = "courses"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(100), nullable=False)
#     description = Column(Text, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

#     created_by = relationship("User", back_populates="created_courses", foreign_keys=[user_id])
#     sections = relationship("Section", back_populates="course")
#     student_courses = relationship("StudentCourse", back_populates="course")
#     category = relationship("Category", back_populates="courses")



class Course(Timestamp, Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    price = Column(Float, nullable=False, default=0.0)  # Price for the course
    is_paid_course = Column(Boolean, default=False)  # Paid course flag

    created_by = relationship("User", back_populates="created_courses", foreign_keys=[user_id])
    sections = relationship("Section", back_populates="course")
    student_courses = relationship("StudentCourse", back_populates="course")
    category = relationship("Category", back_populates="courses")
    payments = relationship("Payment", back_populates="course")

class Payment(Timestamp, Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    amount = Column(Float, nullable=False)  # Amount paid
    status = Column(String(50), nullable=False)  # payment status (pending, success, failed)
    stripe_payment_intent_id = Column(String(255), nullable=True)  # Store Stripe payment intent ID

    
    user = relationship("User", back_populates="payments")
    course = relationship("Course", back_populates="payments")

User.payments = relationship("Payment", back_populates="user")
Course.payments = relationship("Payment", back_populates="course")


class Section(Timestamp, Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", back_populates="sections")
    content_blocks = relationship("ContentBlock", back_populates="section")

class ContentBlock(Timestamp, Base):
    __tablename__ = "content_blocks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(ContentType))
    url = Column(URLType, nullable=True)
    content = Column(Text, nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)

    section = relationship("Section", back_populates="content_blocks")
    student_content_blocks = relationship("StudentContentBlock", back_populates="content_block")

class StudentCourse(Timestamp, Base):
    __tablename__ = "student_courses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    completed = Column(Boolean, default=False, server_default="False")  # Default to False

    student = relationship("User", back_populates="student_courses")
    course = relationship("Course", back_populates="student_courses")

class StudentContentBlock(Timestamp, Base):
    __tablename__ = "student_content_blocks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_block_id = Column(Integer, ForeignKey("content_blocks.id"), nullable=False)
    completed = Column(Boolean, default=False, server_default="False")  # Default to False
    url = Column(URLType, nullable=True)
    feedback = Column(Text, nullable=True)
    grade = Column(Integer, default=0, server_default="0")  # Default to 0
    optional = Column(Boolean, default=False)  # Field to mark optional blocks


    student = relationship("User", back_populates="student_content_blocks")
    content_block = relationship("ContentBlock", back_populates="student_content_blocks")

class Category(Timestamp, Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    courses = relationship("Course", back_populates="category")

class Announcement(Timestamp, Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User")

class Message(Timestamp, Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
