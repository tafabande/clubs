-- Row-Level Security (RLS) Policies for MSU Platform
-- This file enables RLS on organization tables and defines access policies

-- ============================================================================
-- ENABLE RLS ON TABLES
-- ============================================================================

-- Organizations
ALTER TABLE clubs ENABLE ROW LEVEL SECURITY;
ALTER TABLE churches ENABLE ROW LEVEL SECURITY;
ALTER TABLE sports_teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;

-- Memberships
ALTER TABLE club_memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE church_memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE sports_team_memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_registrations ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Function to get current user ID from session variable
CREATE OR REPLACE FUNCTION current_user_id() RETURNS UUID AS $$
BEGIN
    RETURN NULLIF(current_setting('app.current_user_id', TRUE), '')::UUID;
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql STABLE;

-- Function to check if user is staff/admin
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

-- Function to check if user has role for organization
CREATE OR REPLACE FUNCTION has_organization_role(
    org_table_name TEXT,
    org_id UUID,
    role_names TEXT[]
) RETURNS BOOLEAN AS $$
DECLARE
    has_role BOOLEAN;
    content_type_id INTEGER;
BEGIN
    -- Get content type ID for the organization table
    SELECT id INTO content_type_id
    FROM django_content_type
    WHERE app_label = 'organizations' 
    AND model = LOWER(REPLACE(org_table_name, '_', ''));
    
    -- Check if user has any of the specified roles for this organization
    SELECT EXISTS (
        SELECT 1
        FROM user_roles ur
        JOIN roles r ON ur.role_id = r.id
        WHERE ur.user_id = current_user_id()
        AND ur.content_type_id = content_type_id
        AND ur.object_id::TEXT = org_id::TEXT
        AND r.name = ANY(role_names)
        AND (ur.expires_at IS NULL OR ur.expires_at > NOW())
    ) INTO has_role;
    
    RETURN COALESCE(has_role, FALSE);
END;
$$ LANGUAGE plpgsql STABLE;

-- ============================================================================
-- CLUBS POLICIES
-- ============================================================================

-- Policy: Anyone can view active, approved clubs
CREATE POLICY select_approved_clubs ON clubs
    FOR SELECT
    USING (
        is_active = TRUE 
        AND is_approved = TRUE
    );

-- Policy: Staff can view all clubs
CREATE POLICY select_all_clubs_staff ON clubs
    FOR SELECT
    USING (is_staff_user());

-- Policy: Creators can view their own clubs
CREATE POLICY select_own_clubs ON clubs
    FOR SELECT
    USING (created_by_id = current_user_id());

-- Policy: Authenticated users can create clubs
CREATE POLICY insert_clubs ON clubs
    FOR INSERT
    WITH CHECK (
        created_by_id = current_user_id()
        AND current_user_id() IS NOT NULL
    );

-- Policy: Creators and admins can update their clubs
CREATE POLICY update_clubs ON clubs
    FOR UPDATE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('club', id, ARRAY['Club President', 'Club Admin'])
    );

-- Policy: Creators and admins can delete their clubs
CREATE POLICY delete_clubs ON clubs
    FOR DELETE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('club', id, ARRAY['Club President', 'Club Admin'])
    );

-- ============================================================================
-- CLUB MEMBERSHIPS POLICIES
-- ============================================================================

-- Policy: Members can view memberships of clubs they belong to
CREATE POLICY select_club_memberships ON club_memberships
    FOR SELECT
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('club', club_id, ARRAY['Club President', 'Club Officer', 'Club Admin'])
        OR club_id IN (
            SELECT club_id FROM club_memberships WHERE user_id = current_user_id()
        )
    );

-- Policy: Users can create their own memberships (join clubs)
CREATE POLICY insert_club_memberships ON club_memberships
    FOR INSERT
    WITH CHECK (
        user_id = current_user_id()
        AND current_user_id() IS NOT NULL
    );

-- Policy: Users can update their own memberships, admins can update any
CREATE POLICY update_club_memberships ON club_memberships
    FOR UPDATE
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('club', club_id, ARRAY['Club President', 'Club Admin'])
    );

-- ============================================================================
-- CHURCHES POLICIES
-- ============================================================================

CREATE POLICY select_approved_churches ON churches
    FOR SELECT
    USING (is_active = TRUE AND is_approved = TRUE);

CREATE POLICY select_all_churches_staff ON churches
    FOR SELECT
    USING (is_staff_user());

CREATE POLICY select_own_churches ON churches
    FOR SELECT
    USING (created_by_id = current_user_id());

CREATE POLICY insert_churches ON churches
    FOR INSERT
    WITH CHECK (created_by_id = current_user_id() AND current_user_id() IS NOT NULL);

CREATE POLICY update_churches ON churches
    FOR UPDATE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('church', id, ARRAY['Church Leader'])
    );

CREATE POLICY delete_churches ON churches
    FOR DELETE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('church', id, ARRAY['Church Leader'])
    );

-- ============================================================================
-- CHURCH MEMBERSHIPS POLICIES
-- ============================================================================

CREATE POLICY select_church_memberships ON church_memberships
    FOR SELECT
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('church', church_id, ARRAY['Church Leader'])
        OR church_id IN (SELECT church_id FROM church_memberships WHERE user_id = current_user_id())
    );

CREATE POLICY insert_church_memberships ON church_memberships
    FOR INSERT
    WITH CHECK (user_id = current_user_id() AND current_user_id() IS NOT NULL);

CREATE POLICY update_church_memberships ON church_memberships
    FOR UPDATE
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('church', church_id, ARRAY['Church Leader'])
    );

-- ============================================================================
-- SPORTS TEAMS POLICIES
-- ============================================================================

CREATE POLICY select_approved_sports_teams ON sports_teams
    FOR SELECT
    USING (is_active = TRUE AND is_approved = TRUE);

CREATE POLICY select_all_sports_teams_staff ON sports_teams
    FOR SELECT
    USING (is_staff_user());

CREATE POLICY select_own_sports_teams ON sports_teams
    FOR SELECT
    USING (created_by_id = current_user_id());

CREATE POLICY insert_sports_teams ON sports_teams
    FOR INSERT
    WITH CHECK (created_by_id = current_user_id() AND current_user_id() IS NOT NULL);

CREATE POLICY update_sports_teams ON sports_teams
    FOR UPDATE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('sports_team', id, ARRAY['Team Captain', 'Team Coach'])
    );

CREATE POLICY delete_sports_teams ON sports_teams
    FOR DELETE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('sports_team', id, ARRAY['Team Captain'])
    );

-- ============================================================================
-- SPORTS TEAM MEMBERSHIPS POLICIES
-- ============================================================================

CREATE POLICY select_sports_team_memberships ON sports_team_memberships
    FOR SELECT
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('sports_team', sports_team_id, ARRAY['Team Captain', 'Team Coach'])
        OR sports_team_id IN (SELECT sports_team_id FROM sports_team_memberships WHERE user_id = current_user_id())
    );

CREATE POLICY insert_sports_team_memberships ON sports_team_memberships
    FOR INSERT
    WITH CHECK (user_id = current_user_id() AND current_user_id() IS NOT NULL);

CREATE POLICY update_sports_team_memberships ON sports_team_memberships
    FOR UPDATE
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('sports_team', sports_team_id, ARRAY['Team Captain', 'Team Coach'])
    );

-- ============================================================================
-- ACTIVITIES POLICIES
-- ============================================================================

CREATE POLICY select_approved_activities ON activities
    FOR SELECT
    USING (is_active = TRUE AND is_approved = TRUE);

CREATE POLICY select_all_activities_staff ON activities
    FOR SELECT
    USING (is_staff_user());

CREATE POLICY select_own_activities ON activities
    FOR SELECT
    USING (created_by_id = current_user_id());

CREATE POLICY insert_activities ON activities
    FOR INSERT
    WITH CHECK (created_by_id = current_user_id() AND current_user_id() IS NOT NULL);

CREATE POLICY update_activities ON activities
    FOR UPDATE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('activity', id, ARRAY['Activity Coordinator'])
    );

CREATE POLICY delete_activities ON activities
    FOR DELETE
    USING (
        created_by_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('activity', id, ARRAY['Activity Coordinator'])
    );

-- ============================================================================
-- ACTIVITY REGISTRATIONS POLICIES
-- ============================================================================

CREATE POLICY select_activity_registrations ON activity_registrations
    FOR SELECT
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('activity', activity_id, ARRAY['Activity Coordinator'])
    );

CREATE POLICY insert_activity_registrations ON activity_registrations
    FOR INSERT
    WITH CHECK (user_id = current_user_id() AND current_user_id() IS NOT NULL);

CREATE POLICY update_activity_registrations ON activity_registrations
    FOR UPDATE
    USING (
        user_id = current_user_id()
        OR is_staff_user()
        OR has_organization_role('activity', activity_id, ARRAY['Activity Coordinator'])
    );

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

-- Grant necessary permissions to the application user
-- Replace 'msu_user' with your actual database user
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO msu_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO msu_user;

-- ============================================================================
-- NOTES
-- ============================================================================

-- 1. The middleware sets app.current_user_id for each request
-- 2. Staff users (is_staff=true) can access all data
-- 3. Users can view approved organizations
-- 4. Users can only modify organizations they created or have admin roles for
-- 5. Users can view memberships for organizations they belong to
-- 6. All policies respect role expiration dates

-- To disable RLS for testing/development:
-- ALTER TABLE clubs DISABLE ROW LEVEL SECURITY;
-- (repeat for all tables)

-- To check active policies:
-- SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
-- FROM pg_policies
-- WHERE schemaname = 'public';
