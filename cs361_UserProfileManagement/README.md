# UserProfileManagement Microservice
 
UserProfileManagement is a Django REST Framework microservice that manages user profiles, file uploads, admin dashboards, and public features. It’s designed to integrate with external authentication services using JWT tokens.

---
# # Example of Request and Receive Data:

1. Login (via external authentication):
Request:
    POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username": "trong",
  "password": "cs361"
}

Response:
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "expiresAt": "2025-11-28T21:30:00Z"
}

2. Get User Profile:
Request:
GET http://127.0.0.1:8000/api/users/trong
Authorization: Bearer <accessToken>

Response:
{
  "id": 1,
  "username": "trong",
  "email": "trong@example.com",
  "roles": ["user"],
  "date_joined": "2025-11-15T12:00:00Z"
}

3. Upload File
Request:
POST http://127.0.0.1:8000/api/files/upload/
Authorization: Bearer <accessToken>
Content-Type: multipart/form-data

file=@cat.png
description="Profile avatar"

Response:
{
  "message": "File uploaded successfully",
  "filename": "cat.png",
  "owner": "trong"
}
# Project Structure Example

PROFILE-MANAGEMENT-CS361/
|--cs361_UserProfileManagement/
|   |--Project-Config/
|   |   |-- __init__.py
|   |   |-- settings.py
|   |   |-- urls.py
|   |   |--wsgi.py
|   |   |-- asgi.py
|   |
|   |--UserProfileManagement/
|   |   |-- __init__.py
|   |   |-- admin.py
|   |   |-- apps.py
|   |   |-- models.py
|   |   |-- serializers.py
|   |   |-- views.py
|   |   |-- rls.py
|   |   |-- tests.py
|   |   |-- migrations/
|   |--db.sqlite3
|   |--manage.py
|   |--.env.example.txt
|   |--README.md
|-venv/

# Request Flow:
[ Client Request ] ->

[ manage.py runserver ] ->

[ cs361_UserProfileManagement/urls.py ] ->

[ UserProfileManagement/urls.py ] ->

[ views.py ] ->

[ models.py ] ←→ [ db.sqlite3 ] ->

[ serializers.py ] ->
       
[ JSON Response to Client ] ->

## Features

- **Upload File**: Authenticated users can upload files (e.g., avatars, documents).
- **Edit User Profile**: Users can update their profile info.
- **Admin Dashboard**: Admins can view user and file statistics.
- **Global Features**: Public endpoints accessible without authentication.

---

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/ZirakJp/Profile-Management-CS361

cd CS361_UserProfileManagement

### 2. Create Virtual Environment

python3 -m venv venv

(If you're using Windows the command line is:
python -m venv venv
)

source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

If requirements.txt is missing, generate it with:

pip freeze > requirements.txt

### 4. Configure Environment Variables

Create a .env file based on .env.example.txt

### 5. Apply Migrations
python manage.py makemigrations
python manage.py migrate

### 6. Create SuperUser
python manage.py createsuperuser

### 7. Run Server
python manage.py runserver

Visit:
http://127.0.0.1:8000/admin/ – Django Admin
http://127.0.0.1:8000/api/global/features/ – Public API

