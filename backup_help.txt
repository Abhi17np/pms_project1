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
    """Apply custom theme based on user preference with full styling"""
    theme = st.session_state.get('theme', 'light')
    """Apply custom theme based on user preference"""
    theme = st.session_state.get('theme', 'light')

    
    if theme == 'dark':
        st.markdown("""
        <style>
        /* Dark Mode Styles */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        .stMarkdown, .stText {
            color: #fafafa !important;
        }
        
        /* Sidebar Dark Mode */
        section[data-testid="stSidebar"] {
            background-color: #262730 !important;
        }
        
        section[data-testid="stSidebar"] .stMarkdown {
            color: #fafafa !important;
        }
        
        /* Cards Dark Mode */
        .metric-card, .hierarchy-card, .month-card {
            background: #1e1e1e !important;
            color: #fafafa !important;
            border: 1px solid #333 !important;
        }
        
        /* Input fields Dark Mode */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #262730 !important;
            color: #fafafa !important;
            border-color: #444 !important;
        }
        
        /* Buttons Dark Mode */
        .stButton button {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #444 !important;
        }
        
        .stButton button:hover {
            background-color: #333 !important;
            border-color: #666 !important;
        }
        
        /* DataFrames Dark Mode */
        .stDataFrame, [data-testid="stDataFrame"] {
            background-color: #1e1e1e !important;
        }
        
        /* Expanders Dark Mode */
        .streamlit-expanderHeader {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        
        /* Tables Dark Mode */
        table {
            background-color: #1e1e1e !important;
            color: #fafafa !important;
        }
        
        th {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        
        td {
            background-color: #1e1e1e !important;
            color: #fafafa !important;
            border-color: #444 !important;
        }
        
        /* Info/Warning/Success boxes */
        .stAlert {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        """Apply clean professional light blue theme across the app"""
        st.markdown("""
        <style>
            /* ------------------ FONT & BACKGROUND ------------------ */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            html, body, [class*="css"]  {
                font-family: 'Inter', sans-serif;
                background-color: #F8FAFC; /* very light grey-blue background */
            }

            /* ------------------ SIDEBAR ------------------ */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #FFFFFF 0%, #F0F9FF 100%);
                border-right: 1px solid #E2E8F0;
            }

            /* ------------------ HEADINGS ------------------ */
            h1, h2, h3, h4, h5, h6 {
                color: #1E3A8A;
                font-weight: 700;
            }

            /* ------------------ BUTTONS ------------------ */
            .stButton>button {
            background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 6px 0;              /* ✅ smaller vertical padding */
            height: 42px;                /* ✅ fixed consistent height */
            font-size: 0.95rem;
            font-weight: 600;
            transition: 0.3s ease;
            box-shadow: 0 3px 8px rgba(59,130,246,0.15);
        }

            .stButton>button:hover {
                background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%);
                box-shadow: 0 6px 16px rgba(59,130,246,0.35);
                transform: translateY(-2px);
            }

            /* ------------------ INPUTS ------------------ */
            input, textarea, select {
                background-color: #FFFFFF !important;
                border: 1px solid #CBD5E1 !important;
                border-radius: 8px !important;
                color: #0F172A !important;
                padding: 0.5rem !important;
            }

            /* ------------------ TABS ------------------ */
            .stTabs [data-baseweb="tab"] {
                background: #E0F2FE;
                border-radius: 8px;
                color: #1E3A8A;
                padding: 10px 16px;
                font-weight: 600;
            }

            .stTabs [aria-selected="true"] {
                background: #3B82F6;
                color: white;
            }

            /* ------------------ METRICS ------------------ */
            [data-testid="stMetricValue"] {
                color: #1E3A8A !important;
            }

            /* ------------------ PROGRESS BAR ------------------ */
            .stProgress > div > div > div > div {
                background: linear-gradient(90deg, #3B82F6, #60A5FA);
            }

            /* ------------------ BLUE CARDS (YEAR / QUARTER / MONTH) ------------------ */
            .hierarchy-card {
                background: linear-gradient(180deg, #DBEAFE 0%, #BFDBFE 100%);
                
                border-radius: 20px;
                padding: 28px;
                margin-bottom: 20px;
                transition: all 0.3s ease;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(59,130,246,0.15);
                text-align: center;
            }

            .hierarchy-card:hover {
                background: linear-gradient(180deg, #BFDBFE 0%, #93C5FD 100%);
                border-color: #3B82F6;
                box-shadow: 0 8px 18px rgba(59,130,246,0.25);
                transform: translateY(-5px);
            }

            .hierarchy-card h2 {
                color: #1E3A8A;
                font-size: 1.5rem;
                font-weight: 700;
                margin: 0;
            }

            .hierarchy-card p {
                color: #1E40AF;
                font-size: 0.95rem;
                margin-top: 8px;
                font-weight: 500;
            }

            /* ------------------ MONTH CARDS ------------------ */
            .month-card {
                background: linear-gradient(180deg, #DBEAFE 0%, #BFDBFE 100%);
                
                border-radius: 20px;
                padding: 24px;
                text-align: center;
                height: 200px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 10px rgba(59,130,246,0.15);
            }

            .month-card:hover {
                background: linear-gradient(180deg, #BFDBFE 0%, #93C5FD 100%);
                border-color: #2563EB;
                box-shadow: 0 8px 18px rgba(59,130,246,0.3);
                transform: translateY(-5px);
            }

            .month-card-content h2 {
                color: #1E3A8A;
                font-size: 1.4rem;
                font-weight: 700;
                margin: 0;
            }

            .month-card-content p {
                color: #1E40AF;
                margin-top: 8px;
                font-size: 1rem;
                font-weight: 500;
            }

            /* ------------------ BLUE HOVER GLOW ------------------ */
            .hierarchy-card:hover, .month-card:hover {
                box-shadow: 0 0 12px rgba(59,130,246,0.4);
            }

            /* ------------------ SCROLLBAR ------------------ */
            ::-webkit-scrollbar {
                width: 8px;
            }
            ::-webkit-scrollbar-thumb {
                background: #93C5FD;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #3B82F6;
            }
            /* ✅ Make all metric rows stay single-line and shrink evenly */
            section[data-testid="stHorizontalBlock"],
            div[data-testid="stHorizontalBlock"],
            div[data-testid="column"],
            section[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-wrap: nowrap !important;           /* don't wrap */
                justify-content: space-between !important;
                align-items: stretch !important;
                gap: 18px !important;
            }

            /* Make all columns inside those blocks flexible */
            section[data-testid="stHorizontalBlock"] > div,
            div[data-testid="stHorizontalBlock"] > div,
            div[data-testid="column"] > div {
                flex: 1 1 auto !important;
                min-width: 0 !important;                /* allow shrinking */
                max-width: 100% !important;
            }

            /* Handle cards inside expanders or containers (like employee / analytics) */
            div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] > div {
                flex: 1 1 auto !important;
                min-width: 0 !important;
            }

            /* Keep metrics consistent height */
            [data-testid="stMetricValue"] {
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
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
        <div style='width: 80px; height: 80px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; 
                    justify-content: center; color: white; font-size: 32px; font-weight: bold;'>
            {user['name'][0].upper()}
        </div>
        <h3 style='margin: 0;'>{user['name']}</h3>
        <p style='color: #64748b; margin: 5px 0;'>{user.get('designation', 'Employee')}</p>
        <span style='background: #dbeafe; color: #1e40af; padding: 5px 15px; 
                     border-radius: 15px; font-size: 12px; font-weight: 600;'>
            {user['role']}
        </span>
    </div>
    """, unsafe_allow_html=True)


def render_card(title: str, subtitle: str = "", icon: str = "📊"):
    """
    Render a card component
    
    Args:
        title: Card title
        subtitle: Card subtitle
        icon: Emoji icon
    """
    st.markdown(f"""
    <div class='hierarchy-card'>
        <h2 style='margin:0;'>{icon} {title}</h2>
        <p style='color: #64748b; margin-top: 8px;'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: Optional[str] = None, color: str = "#3b82f6"):
    """Render a metric card with optional delta"""
    delta_html = f"<p style='color: {color}; font-size: 14px; margin: 5px 0 0 0;'>{delta}</p>" if delta else ""
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {color}15 0%, {color}05 100%); 
                padding: 24px; border-radius: 16px; font-family: 'Inter', sans-serif;
                border-left: 4px solid {color};'>
        <p style='color: #64748b; font-size: 14px; margin: 0;'>{label}</p>
        <h2 style='margin: 10px 0 0 0;'>{value}</h2>
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


