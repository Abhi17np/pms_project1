-- ============================================
-- PERFORMANCE MANAGEMENT SYSTEM - COMPLETE DATABASE SCHEMA
-- ============================================

-- Drop existing tables if they exist (clean slate)
DROP TABLE IF EXISTS user_permissions CASCADE;
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS goals CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP VIEW IF EXISTS goal_progress_summary CASCADE;
DROP FUNCTION IF EXISTS calculate_monthly_achievement(UUID) CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    designation VARCHAR(255),
    role VARCHAR(50) NOT NULL CHECK (role IN ('Employee', 'Manager', 'HR')),
    manager_id UUID,
    department VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_manager FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ============================================
-- GOALS TABLE
-- ============================================
CREATE TABLE goals (
    goal_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    
    -- Time hierarchy
    year INTEGER NOT NULL,
    quarter INTEGER CHECK (quarter >= 1 AND quarter <= 4),
    month INTEGER CHECK (month >= 1 AND month <= 12),
    week INTEGER CHECK (week >= 1 AND week <= 4),
    
    -- Goal details
    vertical VARCHAR(255),
    goal_title VARCHAR(500) NOT NULL,
    goal_description TEXT,
    kpi VARCHAR(255),
    
    -- Dates
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    -- Targets and Achievements
    monthly_target DECIMAL(10, 2) DEFAULT 0,
    monthly_achievement DECIMAL(10, 2) DEFAULT 0,
    
    week1_target DECIMAL(10, 2) DEFAULT 0,
    week2_target DECIMAL(10, 2) DEFAULT 0,
    week3_target DECIMAL(10, 2) DEFAULT 0,
    week4_target DECIMAL(10, 2) DEFAULT 0,
    
    week1_achievement DECIMAL(10, 2) DEFAULT 0,
    week2_achievement DECIMAL(10, 2) DEFAULT 0,
    week3_achievement DECIMAL(10, 2) DEFAULT 0,
    week4_achievement DECIMAL(10, 2) DEFAULT 0,
    
    weekly_target DECIMAL(10, 2) DEFAULT 0,
    weekly_achievement DECIMAL(10, 2) DEFAULT 0,
    
    -- Summaries
    year_summary TEXT,
    quarter_summary TEXT,
    month_summary TEXT,
    
    -- Status
    status VARCHAR(50) DEFAULT 'Active' CHECK (status IN ('Active', 'Completed', 'On Hold', 'Cancelled')),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- FEEDBACK TABLE
-- ============================================
CREATE TABLE feedback (
    feedback_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    goal_id UUID NOT NULL,
    user_id UUID NOT NULL,
    feedback_by UUID NOT NULL,
    
    feedback_type VARCHAR(50) NOT NULL CHECK (feedback_type IN ('Self Appraisal', 'Manager', 'HR')),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT NOT NULL,
    level VARCHAR(50),
    date DATE DEFAULT CURRENT_DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT fk_goal FOREIGN KEY (goal_id) REFERENCES goals(goal_id) ON DELETE CASCADE,
    CONSTRAINT fk_feedback_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_feedback_by FOREIGN KEY (feedback_by) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- USER PERMISSIONS TABLE
-- ============================================
CREATE TABLE user_permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    permission VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, permission),
    CONSTRAINT fk_permission_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_manager ON users(manager_id);
CREATE INDEX idx_users_department ON users(department);

-- Goals indexes
CREATE INDEX idx_goals_user ON goals(user_id);
CREATE INDEX idx_goals_year ON goals(year);
CREATE INDEX idx_goals_quarter ON goals(year, quarter);
CREATE INDEX idx_goals_month ON goals(year, quarter, month);
CREATE INDEX idx_goals_week ON goals(year, quarter, month, week);
CREATE INDEX idx_goals_status ON goals(status);
CREATE INDEX idx_goals_dates ON goals(start_date, end_date);
CREATE INDEX idx_goals_vertical ON goals(vertical);

-- Feedback indexes
CREATE INDEX idx_feedback_goal ON feedback(goal_id);
CREATE INDEX idx_feedback_user ON feedback(user_id);
CREATE INDEX idx_feedback_by ON feedback(feedback_by);
CREATE INDEX idx_feedback_type ON feedback(feedback_type);
CREATE INDEX idx_feedback_date ON feedback(date);

-- Permissions indexes
CREATE INDEX idx_user_permissions_user ON user_permissions(user_id);
CREATE INDEX idx_user_permissions_permission ON user_permissions(permission);

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_goals_updated_at 
    BEFORE UPDATE ON goals
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_feedback_updated_at 
    BEFORE UPDATE ON feedback
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_permissions ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY users_select_policy ON users
    FOR SELECT USING (true);

CREATE POLICY users_insert_policy ON users
    FOR INSERT WITH CHECK (true);

CREATE POLICY users_update_policy ON users
    FOR UPDATE USING (true);

CREATE POLICY users_delete_policy ON users
    FOR DELETE USING (true);

-- Goals policies
CREATE POLICY goals_select_policy ON goals
    FOR SELECT USING (true);

CREATE POLICY goals_insert_policy ON goals
    FOR INSERT WITH CHECK (true);

CREATE POLICY goals_update_policy ON goals
    FOR UPDATE USING (true);

CREATE POLICY goals_delete_policy ON goals
    FOR DELETE USING (true);

-- Feedback policies
CREATE POLICY feedback_select_policy ON feedback
    FOR SELECT USING (true);

CREATE POLICY feedback_insert_policy ON feedback
    FOR INSERT WITH CHECK (true);

CREATE POLICY feedback_update_policy ON feedback
    FOR UPDATE USING (true);

CREATE POLICY feedback_delete_policy ON feedback
    FOR DELETE USING (true);

-- Permissions policies
CREATE POLICY permissions_select_policy ON user_permissions
    FOR SELECT USING (true);

CREATE POLICY permissions_insert_policy ON user_permissions
    FOR INSERT WITH CHECK (true);

CREATE POLICY permissions_update_policy ON user_permissions
    FOR UPDATE USING (true);

CREATE POLICY permissions_delete_policy ON user_permissions
    FOR DELETE USING (true);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Insert HR Admin
INSERT INTO users (email, password, name, designation, role, department)
VALUES ('admin@company.com', 'admin', 'HR Admin', 'HR Manager', 'HR', 'Human Resources');

-- Insert Managers
INSERT INTO users (email, password, name, designation, role, department)
VALUES 
    ('jane@company.com', 'jane', 'Jane Smith', 'Engineering Manager', 'Manager', 'Engineering'),
    ('mike@company.com', 'mike', 'Mike Johnson', 'Product Manager', 'Manager', 'Product');

-- Insert Employees
INSERT INTO users (email, password, name, designation, role, department)
VALUES 
    ('john@company.com', 'john', 'John Doe', 'Senior Developer', 'Employee', 'Engineering'),
    ('sarah@company.com', 'sarah', 'Sarah Williams', 'Junior Developer', 'Employee', 'Engineering'),
    ('alex@company.com', 'alex', 'Alex Brown', 'Product Analyst', 'Employee', 'Product'),
    ('emma@company.com', 'emma', 'Emma Davis', 'UX Designer', 'Employee', 'Design');

-- Update manager relationships
UPDATE users 
SET manager_id = (SELECT id FROM users WHERE email = 'jane@company.com')
WHERE email IN ('john@company.com', 'sarah@company.com');

UPDATE users 
SET manager_id = (SELECT id FROM users WHERE email = 'mike@company.com')
WHERE email IN ('alex@company.com');

-- Insert sample goals for John
INSERT INTO goals (
    user_id, 
    year, 
    quarter, 
    month,
    vertical,
    goal_title, 
    goal_description,
    kpi,
    start_date, 
    end_date,
    monthly_target,
    week1_target,
    week2_target,
    week3_target,
    week4_target,
    year_summary,
    quarter_summary,
    month_summary,
    status
)
SELECT 
    (SELECT id FROM users WHERE email = 'john@company.com'),
    EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER,
    CASE 
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 4 AND 6 THEN 1
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 7 AND 9 THEN 2
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END,
    EXTRACT(MONTH FROM CURRENT_DATE)::INTEGER,
    'Development',
    'Complete Feature Module',
    'Develop and deploy new user authentication module',
    'Story Points Completed',
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '30 days',
    40.0,
    10.0,
    10.0,
    10.0,
    10.0,
    'Focus on technical excellence and team collaboration',
    'Q1 priorities: Authentication system and API improvements',
    'Complete authentication module with comprehensive testing',
    'Active';

-- Insert another goal for John
INSERT INTO goals (
    user_id, 
    year, 
    quarter, 
    month,
    vertical,
    goal_title, 
    goal_description,
    kpi,
    start_date, 
    end_date,
    monthly_target,
    week1_target,
    week2_target,
    week3_target,
    week4_target,
    status
)
SELECT 
    (SELECT id FROM users WHERE email = 'john@company.com'),
    EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER,
    CASE 
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 4 AND 6 THEN 1
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 7 AND 9 THEN 2
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END,
    EXTRACT(MONTH FROM CURRENT_DATE)::INTEGER,
    'Development',
    'API Performance Optimization',
    'Optimize API response time and reduce server load',
    'API Response Time (ms)',
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '30 days',
    30.0,
    8.0,
    8.0,
    7.0,
    7.0,
    'Active';

-- Insert sample goal for Sarah
INSERT INTO goals (
    user_id, 
    year, 
    quarter, 
    month,
    vertical,
    goal_title, 
    goal_description,
    kpi,
    start_date, 
    end_date,
    monthly_target,
    week1_target,
    week2_target,
    week3_target,
    week4_target,
    status
)
SELECT 
    (SELECT id FROM users WHERE email = 'sarah@company.com'),
    EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER,
    CASE 
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 4 AND 6 THEN 1
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 7 AND 9 THEN 2
        WHEN EXTRACT(MONTH FROM CURRENT_DATE) BETWEEN 10 AND 12 THEN 3
        ELSE 4
    END,
    EXTRACT(MONTH FROM CURRENT_DATE)::INTEGER,
    'Development',
    'Learn React and Build Dashboard',
    'Complete React course and build analytics dashboard',
    'Learning Hours',
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '30 days',
    20.0,
    5.0,
    5.0,
    5.0,
    5.0,
    'Active';

-- Insert sample feedback
INSERT INTO feedback (
    goal_id,
    user_id,
    feedback_by,
    feedback_type,
    rating,
    comment,
    level
)
SELECT 
    g.goal_id,
    (SELECT id FROM users WHERE email = 'john@company.com'),
    (SELECT id FROM users WHERE email = 'jane@company.com'),
    'Manager',
    4,
    'Great progress on the authentication module. Keep up the good work! Your code quality is excellent.',
    'month'
FROM goals g
WHERE g.user_id = (SELECT id FROM users WHERE email = 'john@company.com')
AND g.goal_title = 'Complete Feature Module'
LIMIT 1;

-- Insert HR feedback
INSERT INTO feedback (
    goal_id,
    user_id,
    feedback_by,
    feedback_type,
    rating,
    comment,
    level
)
SELECT 
    g.goal_id,
    (SELECT id FROM users WHERE email = 'john@company.com'),
    (SELECT id FROM users WHERE email = 'admin@company.com'),
    'HR',
    5,
    'Exceptional performance! Your dedication and technical skills are commendable.',
    'month'
FROM goals g
WHERE g.user_id = (SELECT id FROM users WHERE email = 'john@company.com')
AND g.goal_title = 'Complete Feature Module'
LIMIT 1;

-- Insert self appraisal
INSERT INTO feedback (
    goal_id,
    user_id,
    feedback_by,
    feedback_type,
    rating,
    comment,
    level
)
SELECT 
    g.goal_id,
    (SELECT id FROM users WHERE email = 'sarah@company.com'),
    (SELECT id FROM users WHERE email = 'sarah@company.com'),
    'Self Appraisal',
    3,
    'Making steady progress. Need to dedicate more focused time to complete the React course.',
    'month'
FROM goals g
WHERE g.user_id = (SELECT id FROM users WHERE email = 'sarah@company.com')
LIMIT 1;

-- Insert sample permissions for testing
INSERT INTO user_permissions (user_id, permission)
SELECT 
    (SELECT id FROM users WHERE email = 'mike@company.com'),
    unnest(ARRAY['view_analytics', 'export_data', 'manage_teams']);

-- ============================================
-- USEFUL VIEWS
-- ============================================

CREATE VIEW goal_progress_summary AS
SELECT 
    g.goal_id,
    g.user_id,
    u.name as user_name,
    u.email as user_email,
    u.role as user_role,
    u.department,
    g.year,
    g.quarter,
    g.month,
    g.vertical,
    g.goal_title,
    g.monthly_target,
    g.monthly_achievement,
    CASE 
        WHEN g.monthly_target > 0 THEN 
            ROUND((g.monthly_achievement / g.monthly_target * 100)::NUMERIC, 2)
        ELSE 0 
    END as progress_percentage,
    g.status,
    g.start_date,
    g.end_date,
    COUNT(f.feedback_id) as feedback_count,
    AVG(f.rating) as avg_rating
FROM goals g
LEFT JOIN users u ON g.user_id = u.id
LEFT JOIN feedback f ON g.goal_id = f.goal_id
GROUP BY g.goal_id, u.name, u.email, u.role, u.department;

-- View for team summary
CREATE VIEW team_summary AS
SELECT 
    m.id as manager_id,
    m.name as manager_name,
    m.email as manager_email,
    m.department,
    COUNT(DISTINCT e.id) as team_size,
    COUNT(DISTINCT g.goal_id) as total_goals,
    COUNT(DISTINCT CASE WHEN g.status = 'Active' THEN g.goal_id END) as active_goals,
    COUNT(DISTINCT CASE WHEN g.status = 'Completed' THEN g.goal_id END) as completed_goals,
    ROUND(AVG(CASE 
        WHEN g.monthly_target > 0 THEN 
            (g.monthly_achievement / g.monthly_target * 100)
        ELSE 0 
    END)::NUMERIC, 2) as avg_team_progress
FROM users m
LEFT JOIN users e ON e.manager_id = m.id
LEFT JOIN goals g ON g.user_id = e.id
WHERE m.role = 'Manager'
GROUP BY m.id, m.name, m.email, m.department;

-- ============================================
-- FUNCTIONS FOR COMMON OPERATIONS
-- ============================================

CREATE OR REPLACE FUNCTION calculate_monthly_achievement(p_goal_id UUID)
RETURNS DECIMAL AS $$
DECLARE
    v_total DECIMAL;
BEGIN
    SELECT 
        COALESCE(week1_achievement, 0) + 
        COALESCE(week2_achievement, 0) + 
        COALESCE(week3_achievement, 0) + 
        COALESCE(week4_achievement, 0)
    INTO v_total
    FROM goals
    WHERE goal_id = p_goal_id;
    
    RETURN COALESCE(v_total, 0);
END;
$$ LANGUAGE plpgsql;

-- Function to get user statistics
CREATE OR REPLACE FUNCTION get_user_stats(p_user_id UUID)
RETURNS TABLE(
    total_goals BIGINT,
    active_goals BIGINT,
    completed_goals BIGINT,
    avg_progress NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT as total_goals,
        COUNT(CASE WHEN status = 'Active' THEN 1 END)::BIGINT as active_goals,
        COUNT(CASE WHEN status = 'Completed' THEN 1 END)::BIGINT as completed_goals,
        ROUND(AVG(
            CASE 
                WHEN monthly_target > 0 THEN 
                    (monthly_achievement / monthly_target * 100)
                ELSE 0 
            END
        )::NUMERIC, 2) as avg_progress
    FROM goals
    WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

DO $$
DECLARE
    user_count INTEGER;
    goal_count INTEGER;
    feedback_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO user_count FROM users;
    SELECT COUNT(*) INTO goal_count FROM goals;
    SELECT COUNT(*) INTO feedback_count FROM feedback;
    
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ PMS Database Schema Installation Complete!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Tables created: users, goals, feedback, user_permissions';
    RAISE NOTICE 'Users created: % (3 Managers + 4 Employees + 1 HR)', user_count;
    RAISE NOTICE 'Sample goals: %', goal_count;
    RAISE NOTICE 'Sample feedback: %', feedback_count;
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Test Logins:';
    RAISE NOTICE '  HR: admin@company.com / admin';
    RAISE NOTICE '  Manager: jane@company.com / jane';
    RAISE NOTICE '  Employee: john@company.com / john';
    RAISE NOTICE '========================================';
END $$;

-- ============================================
-- ADDITIONAL HELPFUL QUERIES
-- ============================================

-- Query to see all users with their managers
-- SELECT u.name, u.email, u.role, u.department, m.name as manager_name
-- FROM users u
-- LEFT JOIN users m ON u.manager_id = m.id
-- ORDER BY u.role, u.name;

-- Query to see all active goals with progress
-- SELECT * FROM goal_progress_summary
-- WHERE status = 'Active'
-- ORDER BY progress_percentage DESC;

-- Query to see team summaries
-- SELECT * FROM team_summary;