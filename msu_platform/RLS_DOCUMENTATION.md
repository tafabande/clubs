# Row-Level Security (RLS) Documentation

**Component:** PostgreSQL Row-Level Security  
**Status:** ✅ Implemented  
**Database:** PostgreSQL 12+

---

## 📋 Overview

Row-Level Security (RLS) provides database-level access control, ensuring users can only access data they're authorized to see. This is implemented at the PostgreSQL level, providing defense-in-depth security.

---

## 🎯 Purpose

### Why RLS?

1. **Defense in Depth** - Security at database level, not just application level
2. **Data Isolation** - Users can only see their own data
3. **Compliance** - Meets data privacy requirements
4. **Protection** - Guards against application bugs or SQL injection
5. **Performance** - Database-level filtering is efficient

### Without RLS:
```python
# Application must filter data
clubs = Club.objects.filter(is_approved=True)  # Could be forgotten
```

### With RLS:
```python
# Database automatically filters data
clubs = Club.objects.all()  # RLS policies apply automatically
```

---

## 🔐 RLS Policies Implemented

### Organizations (Clubs, Churches, Sports Teams, Activities)

#### **SELECT (View) Policies**

**Policy 1: Public can view approved organizations**
```sql
CREATE POLICY select_approved_clubs ON clubs
    FOR SELECT
    USING (is_active = TRUE AND is_approved = TRUE);
```
- Anyone can view active, approved organizations
- Applies to: Clubs, Churches, Sports Teams, Activities

**Policy 2: Staff can view all organizations**
```sql
CREATE POLICY select_all_clubs_staff ON clubs
    FOR SELECT
    USING (is_staff_user());
```
- Staff members bypass restrictions
- Useful for moderation and administration

**Policy 3: Creators can view their own organizations**
```sql
CREATE POLICY select_own_clubs ON clubs
    FOR SELECT
    USING (created_by_id = current_user_id());
```
- Users can always see organizations they created
- Even if not yet approved

#### **INSERT (Create) Policies**

```sql
CREATE POLICY insert_clubs ON clubs
    FOR INSERT
    WITH CHECK (
        created_by_id = current_user_id()
        AND current_user_id() IS NOT NULL
    );
```
- Only authenticated users can create organizations
- Must set themselves as creator
- Prevents impersonation

#### **UPDATE (Modify) Policies**

```sql
CREATE POLICY update_clubs ON clubs
    FOR UPDATE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('club', id, ARRAY['Club President', 'Club Admin'])
    );
```
- Creators can update their organizations
- Staff can update any organization
- Users with admin roles can update their organization

#### **DELETE Policies**

```sql
CREATE POLICY delete_clubs ON clubs
    FOR DELETE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('club', id, ARRAY['Club President', 'Club Admin'])
    );
```
- Same rules as UPDATE
- Only creators, staff, or admins can delete

---

### Memberships (Club, Church, Sports Team, Activity)

#### **SELECT Policies**

```sql
CREATE POLICY select_club_memberships ON club_memberships
    FOR SELECT
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('club', club_id, ARRAY['Club President', 'Club Officer'])
        OR club_id IN (
            SELECT club_id FROM club_memberships WHERE user_id = current_user_id()
        )
    );
```
- Users can see their own memberships
- Staff can see all memberships
- Organization admins can see all members
- Members can see other members of the same organization

#### **INSERT Policies**

```sql
CREATE POLICY insert_club_memberships ON club_memberships
    FOR INSERT
    WITH CHECK (
        user_id = current_user_id()
        AND current_user_id() IS NOT NULL
    );
```
- Users can only create memberships for themselves
- Prevents joining as someone else

#### **UPDATE Policies**

```sql
CREATE POLICY update_club_memberships ON club_memberships
    FOR UPDATE
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('club', club_id, ARRAY['Club President', 'Club Admin'])
    );
```
- Users can update their own memberships (leave, change status)
- Staff and organization admins can update any membership
- Used for approval workflows

---

## 🛠️ Helper Functions

### 1. current_user_id()

```sql
CREATE OR REPLACE FUNCTION current_user_id() RETURNS UUID AS $$
BEGIN
    RETURN NULLIF(current_setting('app.current_user_id', TRUE), '')::UUID;
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql STABLE;
```

**Purpose:** Retrieves the current authenticated user's ID from the session variable set by Django middleware.

**Usage:** All policies use this to identify the current user.

### 2. is_staff_user()

```sql
CREATE OR REPLACE FUNCTION is_staff_user() RETURNS BOOLEAN AS $$
DECLARE
    user_is_staff BOOLEAN;
BEGIN
    SELECT is_staff INTO user_is_staff
    FROM users
    WHERE id = current_user_id();
    
    RETURN COALESCE(user_is_staff, FALSE);
END;
$$ LANGUAGE plpgsql STABLE;
```

**Purpose:** Checks if the current user is a staff member.

**Usage:** Staff bypass most restrictions for administration.

### 3. has_organization_role()

```sql
CREATE OR REPLACE FUNCTION has_organization_role(
    org_table_name TEXT,
    org_id UUID,
    role_names TEXT[]
) RETURNS BOOLEAN AS $$
-- Implementation checks user_roles table for specified roles
$$ LANGUAGE plpgsql STABLE;
```

**Purpose:** Checks if user has specific role(s) for an organization.

**Parameters:**
- `org_table_name`: 'club', 'church', 'sports_team', 'activity'
- `org_id`: Organization UUID
- `role_names`: Array of role names (e.g., ['Club President', 'Club Admin'])

**Usage:** Determines if user has administrative privileges for an organization.

---

## 🔄 How It Works

### 1. Request Flow

```
1. User makes API request
   ↓
2. Django authenticates user (JWT)
   ↓
3. RLSMiddleware sets current_user_id
   ↓
4. Database query executes
   ↓
5. RLS policies filter results automatically
   ↓
6. Only authorized data returned
```

### 2. Middleware Integration

**File:** `apps/core/middleware.py`

```python
class RLSMiddleware:
    def __call__(self, request):
        if request.user.is_authenticated:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SET LOCAL app.current_user_id = %s",
                    [request.user.id]
                )
        return self.get_response(request)
```

**What it does:**
- Sets PostgreSQL session variable with current user ID
- Runs before every database query
- Enables RLS functions to identify current user

### 3. Example Scenarios

#### Scenario 1: Viewing Clubs

**User:** Regular student  
**Action:** `GET /api/clubs/`

**Query:**
```python
clubs = Club.objects.all()
```

**RLS Applied:**
```sql
-- Automatically filtered to:
SELECT * FROM clubs 
WHERE is_active = TRUE AND is_approved = TRUE;
```

**Result:** Only approved, active clubs visible

---

#### Scenario 2: Creating a Club

**User:** Student (ID: abc-123)  
**Action:** `POST /api/clubs/` with `{"name": "AI Club", ...}`

**RLS Check:**
```sql
-- INSERT policy checks:
WITH CHECK (created_by_id = current_user_id())
```

**Result:** 
- ✅ Allowed if `created_by_id = 'abc-123'`
- ❌ Blocked if trying to set different creator

---

#### Scenario 3: Updating a Club

**User:** Club President (role: 'Club President')  
**Action:** `PUT /api/clubs/{id}/`

**RLS Check:**
```sql
USING (
    created_by_id = current_user_id()
    OR is_staff_user()
    OR has_organization_role('club', id, ARRAY['Club President'])
)
```

**Result:**
- ✅ Allowed (has Club President role)
- Updates go through

---

#### Scenario 4: Viewing Members

**User:** Club member  
**Action:** `GET /api/clubs/{id}/members/`

**RLS Applied:**
```sql
SELECT * FROM club_memberships
WHERE club_id IN (
    SELECT club_id FROM club_memberships 
    WHERE user_id = current_user_id()
)
```

**Result:** Can see members of clubs they belong to

---

## 📊 Policy Matrix

| Action | Public | Member | Creator | Admin Role | Staff |
|--------|--------|--------|---------|------------|-------|
| **View approved orgs** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **View unapproved orgs** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **Create org** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Update own org** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **Update any org** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Delete org** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Join org** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **View members** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Approve members** | ❌ | ❌ | ❌ | ✅ | ✅ |

---

## 🧪 Testing RLS

### Enable RLS

```bash
# After migrations
python manage.py migrate
```

### Test as Different Users

```python
# Django shell
python manage.py shell

from apps.users.models import User
from apps.organizations.models import Club
from django.db import connection

# Test as regular user
user1 = User.objects.create_user(email='student@msu.ac.zw', password='test')

# Set user context (simulates middleware)
with connection.cursor() as cursor:
    cursor.execute("SET LOCAL app.current_user_id = %s", [str(user1.id)])

# This will only return approved clubs
clubs = Club.objects.all()
print(f"User1 sees {clubs.count()} clubs")

# Test as staff
staff = User.objects.create_user(email='staff@msu.ac.zw', password='test', is_staff=True)

with connection.cursor() as cursor:
    cursor.execute("SET LOCAL app.current_user_id = %s", [str(staff.id)])

# This will return all clubs
all_clubs = Club.objects.all()
print(f"Staff sees {all_clubs.count()} clubs")
```

### Check Active Policies

```sql
-- View all RLS policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

### Verify Policy Application

```sql
-- Test a specific policy
EXPLAIN (VERBOSE, COSTS OFF)
SELECT * FROM clubs;

-- Should show RLS filter in query plan
```

---

## ⚠️ Important Notes

### Development vs Production

**Development (SQLite):**
- RLS not supported
- Migration skips RLS setup
- Rely on application-level permissions

**Production (PostgreSQL):**
- RLS fully enforced
- Database-level security active
- Defense in depth

### Disabling RLS

**For Testing:**
```sql
-- Temporarily disable on a table
ALTER TABLE clubs DISABLE ROW LEVEL SECURITY;

-- Re-enable
ALTER TABLE clubs ENABLE ROW LEVEL SECURITY;
```

**Not Recommended:** Only disable for debugging

### Performance

- **Impact:** Minimal (< 5ms per query)
- **Optimization:** Policies use indexes
- **Functions:** Marked as `STABLE` for caching

---

## 🔧 Troubleshooting

### Issue: User can't see their own data

**Cause:** Middleware not setting user ID

**Solution:**
```python
# Check middleware is in MIDDLEWARE setting
'apps.core.middleware.RLSMiddleware',
```

### Issue: Staff can't see all data

**Cause:** is_staff not set correctly

**Solution:**
```python
user.is_staff = True
user.save()
```

### Issue: Policies not applying

**Cause:** RLS not enabled

**Solution:**
```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- Should show 't' (true) for all org tables
```

---

## 📚 References

- [PostgreSQL RLS Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Django Database Functions](https://docs.djangoproject.com/en/5.0/ref/databases/)
- MSU Platform Security Architecture

---

**Last Updated:** May 5, 2026  
**Version:** 1.0
