"""
Database operations module for Performance Management System
Handles all Supabase database interactions
"""
"""
Database operations for Performance Management System
Ensures single Supabase client instance (no caching or recursion)
"""

import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
import pytz
import secrets
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
IST = ZoneInfo("Asia/Kolkata")

load_dotenv()

# Initialize once globally
@st.cache_resource
def get_supabase_client() -> Client:
    """Initialize and return Supabase client safely"""
    url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

    if not url or not key:
        st.error("❌ Missing Supabase credentials. Add them in `.env` or Streamlit Secrets.")
        st.stop()

    return create_client(url, key)

# import streamlit as st
# from supabase import create_client, Client
# import os
# from dotenv import load_dotenv
# from typing import Dict, List, Optional, Any

# load_dotenv()

# # Global variable to store supabase client
# _supabase_client = None


# def get_supabase_client():
#     """Get or create Supabase client - NO CACHING to avoid recursion"""
#     global _supabase_client
    
#     if _supabase_client is None:
#         url = os.getenv("SUPABASE_URL", "")
#         key = os.getenv("SUPABASE_KEY", "")
        
#         # Try secrets if env vars not found
#         if not url or not key:
#             try:
#                 url = st.secrets.get("SUPABASE_URL", "")
#                 key = st.secrets.get("SUPABASE_KEY", "")
#             except:
#                 pass
        
#         if not url or not key:
#             st.error("⚠️ Supabase credentials not found!")
#             st.info("""
#             **Setup Instructions:**
            
#             Create a `.env` file in your project folder with:
# ```
#             SUPABASE_URL=your_supabase_url
#             SUPABASE_KEY=your_supabase_key
# ```
#             """)
#             st.stop()
        
#         _supabase_client = create_client(url, key)
    
#     return _supabase_client


class Database:
    """Handles all database operations for the PMS"""
    
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase = get_supabase_client()
    
    # ============================================
    # USER OPERATIONS
    # ============================================
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user with email and password"""
        try:
            response = self.supabase.table('users')\
                .select('*')\
                .eq('email', email.strip().lower())\
                .eq('password', password.strip())\
                .execute()
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            response = self.supabase.table('users')\
                .select('*')\
                .eq('id', user_id)\
                .single()\
                .execute()
            return response.data
        except:
            return None
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        try:
            response = self.supabase.table('users').select('*').execute()
            return response.data or []
        except:
            return []
    
    def get_team_members(self, manager_id: str) -> List[Dict]:
        """Get team members reporting to a manager"""
        try:
            response = self.supabase.table('users')\
                .select('*')\
                .eq('manager_id', manager_id)\
                .execute()
            return response.data or []
        except:
            return []
    
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Create a new user"""
        try:
            self.supabase.table('users').insert(user_data).execute()
            return True
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return False
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user information"""
        try:
            self.supabase.table('users')\
                .update(updates)\
                .eq('id', user_id)\
                .execute()
            return True
        except Exception as e:
            st.error(f"Error updating user: {e}")
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user and all associated data"""
        try:
            self.supabase.table('users')\
                .delete()\
                .eq('id', user_id)\
                .execute()
            return True
        except Exception as e:
            st.error(f"Error deleting user: {e}")
            return False
    
    # ============================================
    # YEAR OPERATIONS
    # ============================================
    
    def get_years(self, user_id: str) -> Dict[int, str]:
        """Get all years with summaries for a user"""
        try:
            response = self.supabase.table('goals')\
                .select('year, year_summary')\
                .eq('user_id', user_id)\
                .execute()
            
            years = {}
            if response.data:
                for item in response.data:
                    year = item['year']
                    if year not in years:
                        years[year] = item.get('year_summary', '')
            return years
        except Exception as e:
            st.error(f"Error fetching years: {e}")
            return {}
    
    def create_year(self, user_id: str, year: int, summary: str = "") -> bool:
        """Create a new year entry"""
        goal_data = {
            'user_id': user_id,
            'year': year,
            'goal_title': f'Year {year} Goals',
            'goal_description': 'Year planning',
            'start_date': f'{year}-01-01',
            'end_date': f'{year}-12-31',
            'year_summary': summary
        }
        return self.create_goal(goal_data)
    
    def delete_year(self, user_id: str, year: int) -> bool:
        """Delete all goals for a specific year"""
        try:
            self.supabase.table('goals')\
                .delete()\
                .eq('user_id', user_id)\
                .eq('year', year)\
                .execute()
            return True
        except Exception as e:
            st.error(f"Error deleting year: {e}")
            return False
    
    def update_year_summary(self, user_id: str, year: int, summary: str) -> bool:
        """Update year summary"""
        try:
            response = self.supabase.table('goals')\
                .select('goal_id')\
                .eq('user_id', user_id)\
                .eq('year', year)\
                .limit(1)\
                .execute()
            
            if response.data:
                return self.update_goal(response.data[0]['goal_id'], {'year_summary': summary})
            else:
                return self.create_year(user_id, year, summary)
        except Exception as e:
            st.error(f"Error updating year summary: {e}")
            return False
    
    # ============================================
    # QUARTER OPERATIONS
    # ============================================
    
    def get_quarters(self, user_id: str, year: int) -> Dict[int, str]:
        """Get all quarters with summaries for a year"""
        try:
            response = self.supabase.table('goals')\
                .select('quarter, quarter_summary')\
                .eq('user_id', user_id)\
                .eq('year', year)\
                .execute()
            
            quarters = {}
            if response.data:
                for item in response.data:
                    q = item.get('quarter')
                    if q and q not in quarters:
                        quarters[q] = item.get('quarter_summary', '')
            return quarters
        except Exception as e:
            st.error(f"Error fetching quarters: {e}")
            return {}
    
    def update_quarter_summary(self, user_id: str, year: int, quarter: int, summary: str) -> bool:
        """Update or create quarter summary"""
        try:
            from helper import get_quarter_months
            
            response = self.supabase.table('goals')\
                .select('goal_id')\
                .eq('user_id', user_id)\
                .eq('year', year)\
                .eq('quarter', quarter)\
                .limit(1)\
                .execute()
            
            if response.data:
                return self.update_goal(response.data[0]['goal_id'], {'quarter_summary': summary})
            else:
                months = get_quarter_months(quarter)
                goal_data = {
                    'user_id': user_id,
                    'year': year,
                    'quarter': quarter,
                    'goal_title': f'Q{quarter} Goals',
                    'goal_description': 'Quarter planning',
                    'start_date': f'{year}-{months[0]:02d}-01',
                    'end_date': f'{year}-{months[-1]:02d}-28',
                    'quarter_summary': summary
                }
                return self.create_goal(goal_data)
        except Exception as e:
            st.error(f"Error updating quarter: {e}")
            return False
    
    # ============================================
    # MONTH OPERATIONS
    # ============================================
    
    def get_months(self, user_id: str, year: int, quarter: int) -> Dict[int, str]:
        """Get all months with summaries for a quarter"""
        try:
            response = self.supabase.table('goals')\
                .select('month, month_summary')\
                .eq('user_id', user_id)\
                .eq('year', year)\
                .eq('quarter', quarter)\
                .execute()
            
            months = {}
            if response.data:
                for item in response.data:
                    m = item.get('month')
                    if m and m not in months:
                        months[m] = item.get('month_summary', '')
            return months
        except Exception as e:
            st.error(f"Error fetching months: {e}")
            return {}
    
    def update_month_summary(self, user_id: str, year: int, quarter: int, month: int, summary: str) -> bool:
        """Update or create month summary"""
        try:
            response = self.supabase.table('goals')\
                .select('goal_id')\
                .eq('user_id', user_id)\
                .eq('year', year)\
                .eq('quarter', quarter)\
                .eq('month', month)\
                .limit(1)\
                .execute()
            
            if response.data:
                return self.update_goal(response.data[0]['goal_id'], {'month_summary': summary})
            else:
                goal_data = {
                    'user_id': user_id,
                    'year': year,
                    'quarter': quarter,
                    'month': month,
                    'goal_title': f'Month {month} Goals',
                    'goal_description': 'Month planning',
                    'start_date': f'{year}-{month:02d}-01',
                    'end_date': f'{year}-{month:02d}-28',
                    'month_summary': summary
                }
                return self.create_goal(goal_data)
        except Exception as e:
            st.error(f"Error updating month: {e}")
            return False
    
    # ============================================
    # GOAL OPERATIONS
    # ============================================
    
    def get_month_goals(self, user_id: str, year: int, quarter: int, month: int) -> List[Dict]:
        """Get all goals for a specific month (excluding week-specific goals)"""
        try:
            response = self.supabase.table('goals')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('year', year)\
                .eq('quarter', quarter)\
                .eq('month', month)\
                .is_('week', 'null')\
                .order('created_at')\
                .execute()
            return response.data or []
        except Exception as e:
            st.error(f"Error fetching month goals: {e}")
            return []
    
    def get_week_goals(self, user_id: str, year: int, quarter: int, month: int, week: int) -> List[Dict]:
        """Get all goals for a specific week"""
        try:
            response = self.supabase.table('goals')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('year', year)\
                .eq('quarter', quarter)\
                .eq('month', month)\
                .eq('week', week)\
                .order('created_at')\
                .execute()
            return response.data or []
        except Exception as e:
            st.error(f"Error fetching week goals: {e}")
            return []
    
    def get_goal_by_id(self, goal_id: str) -> Optional[Dict]:
        """Get a specific goal by ID"""
        try:
            response = self.supabase.table('goals')\
                .select('*')\
                .eq('goal_id', goal_id)\
                .single()\
                .execute()
            return response.data
        except:
            return None
    
    def get_user_all_goals(self, user_id: str) -> List[Dict]:
        """Get all goals for a user"""
        try:
            response = self.supabase.table('goals')\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()
            return response.data or []
        except:
            return []
    
    def get_all_active_goals(self) -> List[Dict]:
        """Get all active goals in the system"""
        try:
            response = self.supabase.table('goals')\
                .select('*')\
                .eq('status', 'Active')\
                .execute()
            return response.data or []
        except:
            return []
    
    def get_goals_by_status(self) -> Dict[str, int]:
        """Get count of goals by status"""
        try:
            response = self.supabase.table('goals').select('status').execute()
            goals = response.data or []
            
            status_count = {}
            for goal in goals:
                status = goal.get('status', 'Active')
                status_count[status] = status_count.get(status, 0) + 1
            
            return status_count
        except:
            return {}
    
    def create_goal(self, goal_data: Dict[str, Any]) -> bool:
        """Create a new goal with proper defaults and safety"""
        try:
            # Ensure created_by is always set
            goal_data = goal_data.copy()  # don't mutate the original dict
            goal_data.setdefault('created_by', goal_data.get('user_id'))

            # Optional: automatically set created_at if your table has it
            if 'created_at' not in goal_data:
                goal_data['created_at'] = datetime.utcnow().isoformat()

            # Remove any keys that are None (except if you explicitly want to store NULL)
            cleaned_data = {
                k: v for k, v in goal_data.items()
                if v is not None or k in ['end_date', 'joining_date', 'some_other_nullable_field']
            }

            response = self.supabase.table('goals').insert(cleaned_data).execute()

            # Check if insert actually happened (supabase-py returns data + count)
            if hasattr(response, 'data') and response.data:
                return True
            else:
                st.error("Goal was not created – no data returned from database")
                return False

        except Exception as e:
            st.error(f"Error creating goal: {e}")
            if hasattr(e, 'details'):
                st.code(e.details)  # very helpful for debugging Supabase errors
            return False


    def update_goal(self, goal_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing goal – ONLY sends non-None values"""
        try:
            if not updates:
                st.warning("No updates provided.")
                return False

            # Critical safety: NEVER send None values in update()
            # because Supabase will turn None → NULL and overwrite your data!
            safe_updates = {k: v for k, v in updates.items() if v is not None}

            if not safe_updates:
                st.info("All provided values were empty – nothing to update.")
                return True  # not an error, just nothing changed

            response = (
                self.supabase.table('goals')
                .update(safe_updates)
                .eq('goal_id', goal_id)
                .execute()
            )

            # Check how many rows were affected
            if response.count == 0:
                st.warning(f"No goal found with goal_id = {goal_id}")
                return False

            return True

        except Exception as e:
            st.error(f"Error updating goal: {e}")
            if hasattr(e, 'details'):
                st.code(e.details)
            return False
    
    def delete_goal(self, goal_id: str) -> bool:
        """Delete a goal"""
        try:
            self.supabase.table('goals')\
                .delete()\
                .eq('goal_id', goal_id)\
                .execute()
            return True
        except Exception as e:
            st.error(f"Error deleting goal: {e}")
            return False
    
    # ============================================
    # FEEDBACK OPERATIONS
    # ============================================
    
    def get_goal_feedback(self, goal_id: str) -> List[Dict]:
        """Get all feedback for a specific goal"""
        try:
            response = self.supabase.table('feedback')\
                .select('*')\
                .eq('goal_id', goal_id)\
                .order('created_at', desc=True)\
                .execute()
            
            feedbacks = []
            for fb in response.data or []:
                user_info = self.get_user_by_id(fb['feedback_by'])
                fb['users'] = {'name': user_info['name'], 'role': user_info['role']} if user_info else {'name': 'Unknown', 'role': 'Unknown'}
                feedbacks.append(fb)
            
            return feedbacks
        except Exception as e:
            return []
    
    def get_all_feedback(self) -> List[Dict]:
        """Get all feedback in the system (HR only)"""
        try:
            response = self.supabase.table('feedback')\
                .select('*')\
                .order('created_at', desc=True)\
                .execute()
            
            feedbacks = []
            for fb in response.data or []:
                goal = self.get_goal_by_id(fb['goal_id'])
                user_info = self.get_user_by_id(fb['feedback_by'])
                
                feedbacks.append({
                    **fb,
                    'goal_title': goal['goal_title'] if goal else 'N/A',
                    'feedback_by_name': user_info['name'] if user_info else 'Unknown'
                })
            return feedbacks
        except Exception as e:
            return []
    
    def get_user_all_feedback(self, user_id: str) -> List[Dict]:
        """Get all feedback for a specific user"""
        try:
            response = self.supabase.table('feedback')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            
            feedbacks = []
            for fb in response.data or []:
                goal = self.get_goal_by_id(fb['goal_id'])
                user_info = self.get_user_by_id(fb['feedback_by'])
                
                feedbacks.append({
                    **fb,
                    'goal_title': goal['goal_title'] if goal else 'N/A',
                    'feedback_by_name': user_info['name'] if user_info else 'Unknown'
                })
            return feedbacks
        except Exception as e:
            return []
    
    def create_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """Create new feedback"""
        try:
            self.supabase.table('feedback').insert(feedback_data).execute()
            return True
        except Exception as e:
            st.error(f"Error creating feedback: {e}")
            return False
    
    def update_feedback(self, feedback_id: str, updates: Dict[str, Any]) -> bool:
        """Update existing feedback"""
        try:
            self.supabase.table('feedback')\
                .update(updates)\
                .eq('feedback_id', feedback_id)\
                .execute()
            return True
        except Exception as e:
            st.error(f"Error updating feedback: {e}")
            return False
    
    def delete_feedback(self, feedback_id: str) -> bool:
        """Delete feedback"""
        try:
            self.supabase.table('feedback')\
                .delete()\
                .eq('feedback_id', feedback_id)\
                .execute()
            return True
        except Exception as e:
            st.error(f"Error deleting feedback: {e}")
            return False
    
    # ============================================
    # FEEDBACK REPLIES (Optional)
    # ============================================
    
    def get_feedback_replies(self, feedback_id: str) -> List[Dict]:
        """Get all replies for a feedback - returns empty if table doesn't exist"""
        try:
            response = self.supabase.table('feedback_replies')\
                .select('*, users(name)')\
                .eq('feedback_id', feedback_id)\
                .order('created_at')\
                .execute()
            
            replies = []
            for reply in response.data or []:
                replies.append({
                    **reply,
                    'reply_by_name': reply.get('users', {}).get('name', 'Unknown')
                })
            return replies
        except:
            return []
    
    def create_feedback_reply(self, reply_data: Dict[str, Any]) -> bool:
        """Create a feedback reply - returns False if table doesn't exist"""
        try:
            self.supabase.table('feedback_replies').insert(reply_data).execute()
            return True
        except:
            return False
    
    # ============================================
    # NOTIFICATIONS & ANALYTICS
    # ============================================
    
    def get_notifications(self, user_id: str, role: str) -> List[Dict]:
        """Get notifications for user - simplified version"""
        return []
    
    def get_user_goal_stats(self, user_id):
        """Get user goal statistics - FILTERS TO APPROVED GOALS FOR EMPLOYEES"""
        try:
            # Get user to check role
            user = self.get_user_by_id(user_id)
            if not user:
                return {
                    'total_goals': 0,
                    'completed_goals': 0,
                    'active_goals': 0,
                    'avg_progress': 0
                }
            
            # Get all goals
            all_goals = self.get_user_all_goals(user_id)
            
            # ✅ CRITICAL FIX: Filter to approved goals if user is Employee
            if user['role'] == 'Employee':
                goals = [g for g in all_goals if g.get('approval_status') == 'approved']
            else:
                # Managers/HR/VP/CMD see all their goals
                goals = all_goals
            
            if not goals:
                return {
                    'total_goals': 0,
                    'completed_goals': 0,
                    'active_goals': 0,
                    'avg_progress': 0
                }
            
            total_goals = len(goals)
            completed_goals = len([g for g in goals if g.get('status') == 'Completed'])
            active_goals = len([g for g in goals if g.get('status') == 'Active'])
            
            # Calculate average progress
            total_progress = 0
            goals_with_progress = 0
            
            for goal in goals:
                monthly_achievement = goal.get('monthly_achievement')
                if monthly_achievement is not None:
                    monthly_target = goal.get('monthly_target', 1)
                    if monthly_target > 0:
                        progress = (monthly_achievement / monthly_target * 100)
                        total_progress += progress
                        goals_with_progress += 1
            
            avg_progress = (total_progress / goals_with_progress) if goals_with_progress > 0 else 0
            
            return {
                'total_goals': total_goals,
                'completed_goals': completed_goals,
                'active_goals': active_goals,
                'avg_progress': round(avg_progress, 2)
            }
        except Exception as e:
            print(f"Error getting user goal stats: {str(e)}")
            return {
                'total_goals': 0,
                'completed_goals': 0,
                'active_goals': 0,
                'avg_progress': 0
            }
    
    def get_team_performance(self, manager_id: str, year: Optional[int] = None) -> List[Dict]:
        """Get performance data for all team members"""
        try:
            team_members = self.get_team_members(manager_id)
            
            performance = []
            for member in team_members:
                stats = self.get_user_goal_stats(member['id'], year)
                performance.append({
                    'user': member,
                    'stats': stats
                })
            
            return performance
        except Exception as e:
            return []
    
    def get_user_permissions(self, user_id: str) -> List[str]:
        """Get user permissions"""
        try:
            response = self.supabase.table('user_permissions')\
                .select('permission')\
                .eq('user_id', user_id)\
                .execute()
            
            if response.data:
                return [p['permission'] for p in response.data]
            return []
        except:
            return []
    
    def update_user_permissions(self, user_id: str, permissions: List[str]) -> bool:
        """Update user permissions"""
        try:
            self.supabase.table('user_permissions')\
                .delete()\
                .eq('user_id', user_id)\
                .execute()
            
            if permissions:
                perm_data = [{'user_id': user_id, 'permission': p} for p in permissions]
                self.supabase.table('user_permissions').insert(perm_data).execute()
            
            return True
        except Exception as e:
            st.error(f"Error updating permissions: {e}")
            return False
    # Add after line ~50 in database.py (after class Database initialization)

    def add_remarks_columns(self):
        """Add remark columns to goals table"""
        try:
            # Check if columns exist, if not add them
            remarks_columns = [
                'week1_remarks TEXT',
                'week2_remarks TEXT', 
                'week3_remarks TEXT',
                'week4_remarks TEXT'
            ]
            
            for col in remarks_columns:
                try:
                    self.supabase.rpc('add_column_if_not_exists', {
                        'table_name': 'goals',
                        'column_definition': col
                    }).execute()
                except:
                    pass  # Column might already exist
            
            return True
        except Exception as e:
            print(f"Error adding remarks columns: {e}")
            return False
    
    def create_password_reset_token(self, email):
        """Create a password reset token for user"""
        try:
            # Generate token
            token = secrets.token_urlsafe(32)[:8].upper()  # 8 character token
            expires_at = (datetime.now(pytz.utc) + timedelta(hours=1)).isoformat()
            
            # Check if user exists
            result = self.supabase.table('users').select('id').eq('email', email).execute()
            
            if not result.data:
                return None
            
            user_id = result.data[0]['id']
            
            # Store token in database
            self.supabase.table('password_resets').insert({
                'user_id': user_id,
                'token': token,
                'expires_at': expires_at,
                'used': False
            }).execute()
            
            return token
        except Exception as e:
            print(f"Error creating reset token: {str(e)}")
            return None

    def verify_reset_token(self, token):
        """Verify if reset token is valid"""
        try:
            result = self.supabase.table('password_resets').select('*').eq('token', token).eq('used', False).execute()
            
            if not result.data:
                return None
            
            reset_data = result.data[0]
            
            # Check if expired
            expires_at = datetime.fromisoformat(reset_data['expires_at'].replace('Z', '+00:00'))
            if datetime.now(pytz.utc) > expires_at:
                return None
            
            return reset_data
        except Exception as e:
            print(f"Error verifying token: {str(e)}")
            return None

    def reset_password_with_token(self, token, new_password):
        """Reset password using token"""
        try:
            # Verify token
            reset_data = self.verify_reset_token(token)
            if not reset_data:
                return False
            
            user_id = reset_data['user_id']
            
            # Update password
            self.supabase.table('users').update({
                'password': new_password
            }).eq('id', user_id).execute()
            
            # Mark token as used
            self.supabase.table('password_resets').update({
                'used': True
            }).eq('token', token).execute()
            
            return True
        except Exception as e:
            print(f"Error resetting password: {str(e)}")
            return False

   
    # Add these methods to your Database class:

    def create_session(self, user_id):
        """Create a new session for user"""
        try:
            session_id = secrets.token_urlsafe(32)
            expires_at = (datetime.now() + timedelta(days=30)).isoformat()
            
            result = self.supabase.table('user_sessions').insert({
                'session_id': session_id,
                'user_id': str(user_id),  # Convert to string for UUID compatibility
                'expires_at': expires_at,
                'created_at': datetime.now().isoformat()
            }).execute()
            
            return session_id if result.data else None
        except Exception as e:
            print(f"Error creating session: {str(e)}")
            return None

    def get_session(self, session_id):
        """Get session data"""
        try:
            result = self.supabase.table('user_sessions').select('*').eq(
                'session_id', session_id
            ).execute()
            
            if result.data:
                session = result.data[0]
                # Check if session is expired
                expires_at = datetime.fromisoformat(session['expires_at'])
                if datetime.now() < expires_at:
                    return session
                else:
                    self.delete_session(session_id)
            return None
        except Exception as e:
            print(f"Error getting session: {str(e)}")
            return None

    def delete_session(self, session_id):
        """Delete a session"""
        try:
            self.supabase.table('user_sessions').delete().eq(
                'session_id', session_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting session: {str(e)}")
            return False

    def get_user_by_id(self, user_id):
        """Get user by ID - add this if you don't have it already"""
        try:
            result = self.supabase.table('users').select('*').eq(
                'id', str(user_id)
            ).execute()
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None    
    def update_goal_approval(self, goal_id, status, approved_by_id, rejection_reason=None):
        """Update goal approval status"""
        try:
            updates = {
                'approval_status': status,
                'approved_by': approved_by_id,
                'approved_at': datetime.now(IST).isoformat() if status == 'approved' else None
            }
            
            if rejection_reason:
                updates['rejection_reason'] = rejection_reason
            
            result = self.supabase.table('goals').update(updates).eq(
                'goal_id', goal_id
            ).execute()
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating goal approval: {str(e)}")
            return None

    def get_pending_approvals(self, manager_id):
        """Get all pending goals for manager's approval"""
        try:
            # Get team member IDs
            team_members = self.get_team_members(manager_id)
            member_ids = [m['id'] for m in team_members]
            
            if not member_ids:
                return []
            
            result = self.supabase.table('goals').select('*').eq(
                'approval_status', 'pending'
            ).in_('user_id', member_ids).execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting pending approvals: {str(e)}")
            return []    
    def store_approval_token(self, goal_id, token, action):
        """Store approval token"""
        try:
            data = {
                'goal_id': goal_id,
                'token': token,
                'action': action
            }
            result = self.supabase.table('approval_tokens').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error storing token: {str(e)}")
            return None

    def get_goal_by_token(self, token):
        """Get goal by approval token"""
        try:
            result = self.supabase.table('approval_tokens').select(
                '*, goals(*)'
            ).eq('token', token).eq('used', False).execute()
            
            if result.data and len(result.data) > 0:
                # Check if token expired
                expires_at = datetime.fromisoformat(result.data[0]['expires_at'].replace('Z', '+00:00'))
                if datetime.now(pytz.UTC) > expires_at:
                    return None
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error getting goal by token: {str(e)}")
            return None

    def mark_token_used(self, token):
        """Mark token as used"""
        try:
            result = self.supabase.table('approval_tokens').update({
                'used': True
            }).eq('token', token).execute()
            return True
        except Exception as e:
            print(f"Error marking token used: {str(e)}")
            return False