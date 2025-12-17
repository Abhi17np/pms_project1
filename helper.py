"""
Helper functions module for Performance Management System
Contains utility functions, theme management, and UI components
"""

import streamlit as st
from datetime import datetime, date
from typing import List, Dict, Optional

# Add this import if not already present
from datetime import datetime, date
from typing import List, Dict, Optional

# Add this function to helper.py
def calculate_progress(achievement, target):
    """Calculate progress percentage - handle None values"""
    if achievement is None or target is None or target == 0:
        return 0.0
    return (float(achievement) / float(target)) * 100



# ============================================
# TIME & DATE UTILITIES
# ============================================

def get_quarter_months(quarter: int) -> List[int]:
    """
    Get list of month numbers for a given quarter
    
    Args:
        quarter: Quarter number (1-4)
        
    Returns:
        List of month numbers
    """
    quarter_map = {
        1: [4, 5, 6],      # Q1: April-June
        2: [7, 8, 9],      # Q2: July-September
        3: [10, 11, 12],   # Q3: October-December
        4: [1, 2, 3]       # Q4: January-March
    }
    return quarter_map.get(quarter, [])


def get_month_name(month_num: int) -> str:
    """
    Get month name from month number
    
    Args:
        month_num: Month number (1-12)
        
    Returns:
        Month name
    """
    months = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return months[month_num] if 1 <= month_num <= 12 else ""


def get_current_quarter() -> int:
    """Get current quarter based on current month"""
    month = datetime.now().month
    if 4 <= month <= 6:
        return 1
    elif 7 <= month <= 9:
        return 2
    elif 10 <= month <= 12:
        return 3
    else:
        return 4


def get_quarter_name(quarter: int) -> str:
    """Get quarter display name"""
    quarter_names = {
        1: "Q1 (April - June)",
        2: "Q2 (July - September)",
        3: "Q3 (October - December)",
        4: "Q4 (January - March)"
    }
    return quarter_names.get(quarter, f"Q{quarter}")


def get_financial_year(date_obj: date = None) -> int:
    """
    Get financial year for a given date (April to March)
    
    Args:
        date_obj: Date object, defaults to current date
        
    Returns:
        Financial year
    """
    if date_obj is None:
        date_obj = date.today()
    
    year = date_obj.year
    month = date_obj.month
    
    # If month is Jan-Mar, financial year is previous year
    if month < 4:
        return year - 1
    return year


# ============================================
# CALCULATION UTILITIES
# ============================================

def calculate_progress(achieved: float, target: float) -> float:
    """
    Calculate progress percentage
    
    Args:
        achieved: Achieved value
        target: Target value
        
    Returns:
        Progress percentage (capped at 100)
    """
    if target <= 0:
        return 0.0
    progress = (achieved / target) * 100
    return min(progress, 100.0)


def calculate_total_achievement(week1: float, week2: float, week3: float, week4: float) -> float:
    """Calculate total monthly achievement from weekly achievements"""
    return week1 + week2 + week3 + week4


def get_status_color(progress: float) -> str:
    """
    Get color based on progress percentage
    
    Args:
        progress: Progress percentage
        
    Returns:
        Color code
    """
    if progress >= 90:
        return "#10b981"  # Green
    elif progress >= 70:
        return "#f59e0b"  # Amber
    elif progress >= 50:
        return "#ef4444"  # Red
    else:
        return "#6b7280"  # Gray


def format_number(value: float, decimals: int = 2) -> str:
    """Format number with specified decimal places"""
    return f"{value:.{decimals}f}"


# ============================================
# THEME MANAGEMENT
# ============================================

def apply_theme():
    """Updated premium dashboard theme (refined colors based on reference file)"""
    st.markdown("""
    <style>
     /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    /* ------------------------------
       GLOBAL COLORS (UPDATED)
    ------------------------------ */
        :root {
            --primary-bg: #f1f5f9;
            --card-bg: #f8fafc;
            --sidebar-bg: #1e293b;
            --sidebar-hover: #334155;

            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #94a3b8;

            --border-color: #e2e8f0;

            --accent-blue: #9BBCE0;     /* Soft pastel blue */
            --accent-green: #A7D7C5;    /* Pastel mint */
            --accent-orange: #F6D8A8;   /* Pastel yellow-orange */
            --accent-red: #E8A8A8;      /* Pastel red */
            --accent-purple: #C7B8E6;  

            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
                
            --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.06);
            --shadow-xl: 0 12px 32px rgba(0, 0, 0, 0.16), 0 6px 12px rgba(0, 0, 0, 0.08);
        }

       

    /* ------------------------------
       BACKGROUND
    ------------------------------ */
                
    /* GLOBAL STYLES */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        }
    html, body {
        background-color: var(--primary-bg) !important;
        color: var(--text-primary);
    }

    .block-container {
        padding: 2.2rem 2.8rem 3rem 2.8rem;
    }
                
    /* HEADINGS */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
            font-weight: 700;
            letter-spacing: -0.03em;
        }

        h1 {
            font-size: 32px;
            margin-bottom: 12px;
            line-height: 1.2;
        }

        h2 {
            font-size: 24px;
            margin-bottom: 16px;
            line-height: 1.3;
        }

        h3 {
            font-size: 20px;
            margin-bottom: 12px;
            font-weight: 600;
            line-height: 1.4;
        }

    /* ------------------------------
       SIDEBAR
    ------------------------------ */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
            box-shadow: 4px 0 12px rgba(0, 0, 0, 0.1);
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }

        /* Sidebar buttons */
        section[data-testid="stSidebar"] button {
            background-color: rgba(51, 65, 85, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            color: #cbd5e1 !important;
            padding: 12px 18px !important;
            border-radius: 10px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            width: 100% !important;
            text-align: left !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            letter-spacing: 0.01em !important;
        }

        section[data-testid="stSidebar"] button:hover {
            background-color: #2dccff !important;
            border-color: rgba(45, 204, 255, 0.3) !important;
            color: white !important;
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(45, 204, 255, 0.15);
        }

    /* ------------------------------
       BUTTONS
    ------------------------------ */
    .stButton > button {
            background: linear-gradient(135deg, #2dccff 0%, #1ea8d9 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 28px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            letter-spacing: 0.02em !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(45, 204, 255, 0.25) !important;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #1bb8e6 0%, #1896c4 100%) !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(45, 204, 255, 0.35) !important;
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Form submit buttons */
        button[type="submit"] {
            background: linear-gradient(135deg, #2dccff 0%, #1ea8d9 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 28px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            letter-spacing: 0.02em !important;
            box-shadow: 0 4px 12px rgba(45, 204, 255, 0.25) !important;
            transition: all 0.3s ease !important;
        }

        button[type="submit"]:hover {
            background: linear-gradient(135deg, #1bb8e6 0%, #1896c4 100%) !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(45, 204, 255, 0.35) !important;
        }

        /* Secondary buttons */
        button[kind="secondary"] {
            background: white !important;
            color: var(--text-primary) !important;
            border: 1.5px solid var(--border-color) !important;
            box-shadow: var(--shadow-xs) !important;
        }

        button[kind="secondary"]:hover {
            border-color: var(--accent-blue) !important;
            background: #34d8fb !important;
        }
    /* ------------------------------
       METRIC CARDS
    ------------------------------ */
        /* METRIC CARDS */
        [data-testid="stMetricValue"] {
            font-size: 36px;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }

        [data-testid="stMetricLabel"] {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        /* CUSTOM CARD STYLES */
        .metric-card {
            background: background: var(--card-bg) !important;
            border-radius: 12px;
            padding: 28px 24px;
            box-shadow: var(--shadow-sm);
            border: 1px solid rgba(226, 232, 240, 0.8);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: background: var(--accent-blue) !important;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .metric-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
            border-color: rgba(45, 204, 255, 0.3);
        }

        .metric-card:hover::before {
            opacity: 1;
        }

        .metric-card-title {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 16px;
            display: block;
            color: var(--text-secondary);
        }

        .metric-card-value {
            font-size: 48px;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
            line-height: 1;
            letter-spacing: -0.03em;
        }

        .metric-card-delta {
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 12px;
            font-weight: 500;
        }

        /* ICON CONTAINER IN METRIC CARDS */
        .metric-icon {
            width: 52px;
            height: 52px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
            box-shadow: var(--shadow-sm);
            transition: transform 0.3s ease;
        }

        .metric-card:hover .metric-icon {
            transform: scale(1.05);
        }

        .metric-icon svg {
            width: 26px;
            height: 26px;
        }




    /* ------------------------------
       TABLES
    ------------------------------ */
    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-soft);
    }

    thead tr th {
        background: #F8FAFC !important;
        color: #475569 !important;
    }

    tbody tr:hover {
        background: #F1F5F9 !important;
    }

    /* ------------------------------
       PROGRESS BAR
    ------------------------------ */
    .pms-progress-container {
            background-color: #e2e8f0;
            height: 8px;
            border-radius: 999px;
            overflow: hidden;
            margin: 12px 0;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
        }

        .pms-progress-bar {
            height: 100%;
            border-radius: 999px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(90deg, var(--accent-blue), #BFD4EA) !important;
            box-shadow: 0 0 4px rgba(155,188,224,0.35);
            position: relative;
        }

        .pms-progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

    /* ------------------------------
       HIERARCHY CARDS
    ------------------------------ */
    .hierarchy-card, .month-card {
        background: white;
        border-radius: 14px;
        padding: 26px;
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-color);
        transition: 0.25s;
    }

    .hierarchy-card:hover, .month-card:hover {
        transform: translateY(-6px);
        border-color: var(--accent-blue);
        box-shadow: var(--shadow-medium);
    }

    .hierarchy-card h2, .month-card h2 {
        color: #13206e !important;
    }

    .hierarchy-card p, .month-card p {
        color: #0b1890 !important;
    }
                
    /* SCROLLBAR */
    ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }

    ::-webkit-scrollbar-track {
            background: var(--primary-bg);
            border-radius: 10px;
        }

    ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #cbd5e1, #94a3b8);
            border-radius: 10px;
            border: 2px solid var(--primary-bg);
        }

    ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #94a3b8, #64748b);
        }

    </style>
    """, unsafe_allow_html=True)



# ============================================
# UI COMPONENTS
# ============================================

def render_user_avatar(user: Dict):
    """
    Render user avatar and info in sidebar
    
    Args:
        user: User dictionary
    """
    st.markdown(f"""
    <div style='text-align: center; padding: 20px;'>
        <div style='width: 80px; height: 80px; background: linear-gradient(135deg, #2dccff 0%, #1ea8d9 100%);
                    border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; 
                    justify-content: center; color: white; font-size: 32px; font-weight: bold;'>
            {user['name'][0].upper()}
        </div>
        <h3 style='margin: 0; color: white'>{user['name']}</h3>
        <p style='color: #64748b; margin: 5px 0;'>{user.get('designation', 'Employee')}</p>
        <span style='background: #dbeafe; color: #1e40af; padding: 5px 15px; 
                     border-radius: 15px; font-size: 12px; font-weight: 600;'>
            {user['role']}
        </span>
    </div>
    """, unsafe_allow_html=True)

def render_card(title: str, subtitle: str = "", icon: str = ""):
    """Professional standalone card component"""

    # Icon HTML (optional)
    icon_html = (
        f"<span style='margin-right: 10px; color: #2dccff; font-size: 20px;'>{icon}</span>"
        if icon else ""
    )

    st.markdown(f"""
    <div style='background: white; border-radius: 12px; padding: 28px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.06); border: 1px solid #e2e8f0; transition: box-shadow 0.3s ease;'>
        <div style='font-size: 18px; font-weight: 600; color: #0f172a; display: flex; align-items: center; margin-bottom: 12px;'>
            {icon_html}{title}
        </div>
        <div style='color: #475569; font-size: 14px; line-height: 1.6;'>
            {subtitle}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(
    label: str,
    value: str,
    color: str = "#2dccff",
    delta: Optional[str] = None,
):
    """Clean, professional metric card without icons"""
    
    delta_html = ""
    if delta:
        delta_color = "#10b981" if "+" in str(delta) else "#ef4444"
        delta_html = f"<div style='font-size: 13px; color: {delta_color}; margin-top: 12px; font-weight: 500;'>{delta}</div>"

    st.markdown(f"""
    <div style='background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%); border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.06); border: 1px solid rgba(226, 232, 240, 0.8); transition: all 0.3s ease; position: relative; overflow: hidden;'>
        <div style='position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: {color};'></div>
        <div style='color: {color}; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>{label}</div>
        <div style='color: #1e293b; font-size: 36px; font-weight: 700; line-height: 1; margin-bottom: 8px;'>{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(progress: float, label: str = ""):
    """Render a custom progress bar"""
    color = get_status_color(progress)
    
    st.markdown(f"""
    <div style='margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
            <span>{label}</span>
            <span style='font-weight: 600;'>{progress:.1f}%</span>
        </div>
        <div style='background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;'>
            <div style='background: {color}; height: 100%; width: {progress}%; transition: width 0.3s;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_feedback_card(feedback: Dict, feedback_type: str):
    """
    Render a feedback card
    
    Args:
        feedback: Feedback dictionary
        feedback_type: Type of feedback (Manager, HR, Self Appraisal)
    """
    color_map = {
        'Manager': '#3b82f6',
        'HR': '#10b981',
        'Self Appraisal': '#f59e0b'
    }
    
    color = color_map.get(feedback_type, '#6b7280')
    stars = '⭐' * feedback.get('rating', 3)
    
    user_name = feedback.get('users', {}).get('name', 'Unknown')
    date_str = feedback.get('date', '')
    comment = feedback.get('comment', '')
    
    st.markdown(f"""
    <div style='background: {color}15; padding: 15px; border-radius: 12px; 
                border-left: 4px solid {color}; margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <strong>{user_name}</strong>
            <span style='color: #64748b; font-size: 12px;'>{date_str}</span>
        </div>
        <p style='margin: 10px 0;'>{comment}</p>
        <div style='margin-top: 10px;'>{stars}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# VALIDATION UTILITIES
# ============================================

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_date_range(start_date: date, end_date: date) -> bool:
    """Validate that end date is after start date"""
    return end_date >= start_date


def validate_goal_data(goal_data: Dict) -> tuple[bool, str]:
    """
    Validate goal data before submission
    
    Returns:
        (is_valid, error_message)
    """
    required_fields = ['goal_title', 'start_date', 'end_date']
    
    for field in required_fields:
        if not goal_data.get(field):
            return False, f"Missing required field: {field}"
    
    if not validate_date_range(goal_data['start_date'], goal_data['end_date']):
        return False, "End date must be after start date"
    
    return True, ""


# ============================================
# DATA FORMATTING UTILITIES
# ============================================

def format_goal_table_data(goals: List[Dict]) -> List[Dict]:
    """
    Format goals data for table display
    
    Args:
        goals: List of goal dictionaries
        
    Returns:
        Formatted list for DataFrame
    """
    table_data = []
    for goal in goals:
        table_data.append({
            'Vertical': goal.get('vertical', ''),
            'Title': goal['goal_title'],
            'KPI': goal.get('kpi', ''),
            'Monthly Target': goal.get('monthly_target', 0),
            'Start Date': goal['start_date'],
            'End Date': goal['end_date'],
            'W1 Target': goal.get('week1_target', 0),
            'W2 Target': goal.get('week2_target', 0),
            'W3 Target': goal.get('week3_target', 0),
            'W4 Target': goal.get('week4_target', 0),
            'W1 Achievement': goal.get('week1_achievement', 0),
            'W2 Achievement': goal.get('week2_achievement', 0),
            'W3 Achievement': goal.get('week3_achievement', 0),
            'W4 Achievement': goal.get('week4_achievement', 0),
            'Monthly Achievement': goal.get('monthly_achievement', 0)
        })
    return table_data


def export_to_csv(data: List[Dict], filename: str) -> str:
    """
    Export data to CSV format
    
    Args:
        data: List of dictionaries
        filename: Output filename
        
    Returns:
        CSV string
    """
    import pandas as pd
    df = pd.DataFrame(data)
    return df.to_csv(index=False)


# ============================================
# SESSION STATE UTILITIES
# ============================================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'user': None,
        'page': 'year_selection',
        'theme': 'light',
        'selected_year': datetime.now().year,
        'selected_quarter': None,
        'selected_month': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_navigation():
    """Reset navigation to home page"""
    st.session_state.page = 'year_selection'
    st.session_state.selected_year = datetime.now().year
    st.session_state.selected_quarter = None
    st.session_state.selected_month = None


