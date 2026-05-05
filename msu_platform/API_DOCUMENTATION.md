# MSU Platform - API Documentation

**Base URL:** `http://localhost:8000/api/`  
**Authentication:** JWT Bearer Token

---

## Table of Contents

1. [Authentication](#authentication)
2. [Clubs](#clubs)
3. [Churches](#churches)
4. [Sports Teams](#sports-teams)
5. [Activities](#activities)
6. [Common Patterns](#common-patterns)

---

## Authentication

All authenticated endpoints require a JWT Bearer token in the Authorization header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Endpoints

#### Register User
```http
POST /api/auth/register/
```

**Request:**
```json
{
  "email": "student@msu.ac.zw",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "student_id": "MSU000001234",
  "faculty": "science",
  "department": "Computer Science",
  "year_of_study": 3
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully...",
  "user": { ... }
}
```

#### Login
```http
POST /api/auth/login/
```

**Request:**
```json
{
  "email": "student@msu.ac.zw",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "email": "student@msu.ac.zw",
    "first_name": "John",
    "last_name": "Doe",
    "student_id": "MSU000001234",
    "faculty": "science",
    "is_verified": false
  }
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
```

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Get Current User
```http
GET /api/auth/me/
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "email": "student@msu.ac.zw",
  "first_name": "John",
  "last_name": "Doe",
  ...
}
```

#### Logout
```http
POST /api/auth/logout/
```

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Clubs

### List Clubs
```http
GET /api/clubs/
```

**Query Parameters:**
- `search` - Search by name or description
- `category` - Filter by category
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20)

**Response:** `200 OK`
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/clubs/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "name": "Robotics Club",
      "description": "Build and program robots...",
      "email": "robotics@msu.edu",
      "website": "https://robotics.msu.edu",
      "logo": null,
      "category": "technology",
      "faculty_advisor": { ... },
      "meeting_location": "Room 301",
      "meeting_schedule": "Tuesdays 4-6 PM",
      "max_members": 50,
      "member_count": 25,
      "is_active": true,
      "is_approved": true,
      "created_by": { ... },
      "created_at": "2026-01-15T10:00:00Z",
      "user_membership": null
    }
  ]
}
```

### Create Club
```http
POST /api/clubs/
```

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "name": "AI & ML Club",
  "description": "Explore artificial intelligence...",
  "email": "ai@msu.edu",
  "website": "",
  "category": "technology",
  "meeting_location": "Lab 205",
  "meeting_schedule": "Fridays 3-5 PM",
  "max_members": 40
}
```

**Response:** `201 Created`

### Get Club Detail
```http
GET /api/clubs/{id}/
```

**Response:** `200 OK`

### Update Club
```http
PUT /api/clubs/{id}/
PATCH /api/clubs/{id}/
```

**Headers:** `Authorization: Bearer <token>`  
**Permissions:** Club admin only

### Delete Club
```http
DELETE /api/clubs/{id}/
```

**Headers:** `Authorization: Bearer <token>`  
**Permissions:** Club admin only

**Response:** `204 No Content`

### Join Club
```http
POST /api/clubs/{id}/join/
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "user": { ... },
  "club": "uuid",
  "status": "pending",
  "position": "",
  "joined_at": "2026-05-05T14:00:00Z"
}
```

### Leave Club
```http
POST /api/clubs/{id}/leave/
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Successfully left the club"
}
```

### List Club Members
```http
GET /api/clubs/{id}/members/
```

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "user": {
      "id": "uuid",
      "email": "member@msu.ac.zw",
      "first_name": "Jane",
      "last_name": "Smith"
    },
    "club": "uuid",
    "status": "active",
    "position": "Officer",
    "joined_at": "2026-01-20T10:00:00Z"
  }
]
```

### Approve Club Member
```http
POST /api/clubs/{id}/approve_member/
```

**Headers:** `Authorization: Bearer <token>`  
**Permissions:** Club admin only

**Request:**
```json
{
  "membership_id": "uuid"
}
```

**Response:** `200 OK`

### Get Club History
```http
GET /api/clubs/{id}/history/
```

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "date": "2026-05-01",
    "member_count": 25,
    "event_count": 3,
    "engagement_score": 8.5
  }
]
```

---

## Churches

Similar to Clubs, with the following differences:

**Base URL:** `/api/churches/`

**Join:** No approval required (status immediately set to "active")

**Additional Fields:**
- `denomination` - Protestant, Catholic, Orthodox, etc.
- `service_times` - JSON object with service schedule
- `pastor_name` - Name of pastor/leader
- `pastor_contact` - Contact information

---

## Sports Teams

**Base URL:** `/api/sports-teams/`

**Additional Fields:**
- `sport_type` - Football, Basketball, etc.
- `division` - Men's, Women's, Mixed
- `coach` - Coach name
- `practice_schedule` - Practice times
- `max_roster_size` - Maximum team size

**Membership Fields:**
- `position` - Player position
- `jersey_number` - Jersey number
- `status` - active, injured, inactive

---

## Activities

**Base URL:** `/api/activities/`

**Actions:**
- `POST /api/activities/{id}/register/` - Register for activity
- `POST /api/activities/{id}/cancel/` - Cancel registration
- `GET /api/activities/{id}/participants/` - List participants

**Additional Fields:**
- `activity_type` - Workshop, Conference, Competition, etc.
- `start_date` - Activity start date/time
- `end_date` - Activity end date/time
- `location` - Activity location
- `max_participants` - Maximum participants
- `registration_deadline` - Registration cutoff date
- `is_recurring` - Whether activity repeats

**Register Request:**
```json
{
  "registration_data": {
    "dietary_requirements": "Vegetarian",
    "t_shirt_size": "M"
  }
}
```

---

## Common Patterns

### Pagination

All list endpoints support pagination:

```http
GET /api/clubs/?page=2&page_size=10
```

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/clubs/?page=3",
  "previous": "http://localhost:8000/api/clubs/?page=1",
  "results": [...]
}
```

### Filtering

Use query parameters for filtering:

```http
GET /api/clubs/?category=technology&is_active=true
```

### Search

Use the `search` parameter:

```http
GET /api/clubs/?search=robotics
```

### Ordering

Use `ordering` parameter:

```http
GET /api/clubs/?ordering=-created_at  # Newest first
GET /api/clubs/?ordering=name         # Alphabetical
```

### Error Responses

**400 Bad Request:**
```json
{
  "error": "Validation error message"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

**429 Too Many Requests:**
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

---

## Rate Limiting

- **API Endpoints:** 500 requests/hour per user
- **Auth Endpoints:** 10 requests/minute per user

---

## Testing with cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@msu.ac.zw",
    "password": "Pass123!",
    "password_confirm": "Pass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@msu.ac.zw",
    "password": "Pass123!"
  }'
```

**List Clubs:**
```bash
curl http://localhost:8000/api/clubs/
```

**Create Club:**
```bash
curl -X POST http://localhost:8000/api/clubs/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Test Club",
    "description": "Testing",
    "email": "test@msu.edu",
    "category": "technology",
    "max_members": 50
  }'
```

---

**Last Updated:** 2026-05-05  
**Version:** 1.0
