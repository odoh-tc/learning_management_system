from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.user import router as user_router
from routers.profile import router as profile_router
from routers.category import router as category_router
from routers.course import router as course_router
from routers.section import router as section_router
from routers.content_block import router as content_block_router
from routers.student_content_block import router as student_content_block_router
from routers.enrollment import router as enrollment_router
from routers.student_course import router as student_course_router
from routers.message import router as message_router
from routers.announcement import router as announcement_router
from database import engine
import models

app = FastAPI()

# Include the auth router under the /auth prefix with "auth" tags
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(profile_router, prefix="/profile", tags=["profile"])
app.include_router(enrollment_router, prefix="/enrollment", tags=["enrollment"])
app.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(course_router, prefix="/course", tags=["course"])
app.include_router(section_router, prefix="/section", tags=["section"])
app.include_router(content_block_router, prefix="/content_block", tags=["content_block"])
app.include_router(student_content_block_router, prefix="/student_content_block", tags=["student_content_block"])
app.include_router(student_course_router, prefix="/student_course", tags=["student_course"])
app.include_router(message_router, prefix="/message", tags=["message"])
app.include_router(announcement_router, prefix="/announcement", tags=["announcement"])

# Create database tables when the application starts
models.Base.metadata.create_all(bind=engine)

# Example route
@app.get("/")
async def home():
    return {"message": "Hello World!"}


