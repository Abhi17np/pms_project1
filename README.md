# Performance Management System (PMS)

A comprehensive Performance Management System built with **Streamlit** and **Supabase** for tracking goals, achievements, and feedback across yearly, quarterly, monthly, and weekly timeframes.

## 🎯 Features

- **Hierarchical Goal Management**: Year → Quarter → Month → Week structure
- **Excel-style Goal Sheets**: Easy tracking of targets and achievements
- **Multi-level Feedback System**: Self-appraisal, Manager, and HR feedback
- **Role-based Access**: Employee, Manager, and HR roles
- **Real-time Analytics**: Progress tracking and performance metrics
- **Dark/Light Theme**: Toggle between themes
- **Responsive Design**: Beautiful UI with smooth animations

## 📋 Prerequisites

- Python 3.8 or higher
- Supabase account (free tier works)
- pip package manager

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd pms-project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Supabase

1. Create a Supabase account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to **SQL Editor** in your Supabase dashboard
4. Copy and paste the contents of `schema.sql`
5. Run the SQL script to create all tables, indexes, and sample data

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

**To find these values:**
- Go to your Supabase project
- Click on **Settings** → **API**
- Copy the **Project URL** and **anon/public** key

### 5. Alternative: Use Streamlit Secrets

If deploying to Streamlit Cloud, create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "your_supabase_project_url"
SUPABASE_KEY = "your_supabase_anon_key"
```

## 🏃 Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 👥 Demo Accounts

The schema includes sample users:

| Role | Email | Password |
|------|-------|----------|
| HR | admin@company.com | admin |
| Manager | jane@company.com | jane |
| Employee | john@company.com | john |

## 📁 Project Structure

```
pms-project/
├── app.py              # Main application file
├── database.py         # Database operations
├── helper.py           # Helper functions and utilities
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # This file
```

## 🗂️ Database Schema

### Tables

1. **users**: User information and roles
2. **goals**: Goals with hierarchical time structure
3. **feedback**: Feedback and appraisals

### Key Features

- UUID primary keys
- Foreign key relationships
- Automatic timestamp updates
- Row Level Security (RLS) enabled
- Indexes for performance
- Sample data included

## 🎨 Customization

### Theme Colors

Edit `helper.py` in the `apply_theme()` function to customize colors.

### Role Permissions

Modify `database.py` to adjust role-based access controls.

### Financial Year

The system uses April-March financial year. Modify `helper.py` if you need a different fiscal year.

## 📊 Usage Guide

### For Employees

1. **Login** with your credentials
2. **Select Year** to view or create
3. **Navigate** through Quarters → Months
4. **Add Goals** with weekly targets
5. **Update Achievements** as you progress
6. **Submit Self-Appraisals**

### For Managers

1. All employee features, plus:
2. **View Team Goals** (if team members are assigned)
3. **Provide Manager Feedback** on team goals
4. **Track Team Performance**

### For HR

1. All features, plus:
2. **View All Users** and their goals
3. **Provide HR Feedback** on any goal
4. **Access Analytics** across the organization

## 🔧 Troubleshooting

### Database Connection Issues

- Verify your Supabase URL and key are correct
- Check if your Supabase project is active
- Ensure RLS policies allow your operations

### Import Errors

```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use

```bash
streamlit run app.py --server.port 8502
```

## 🚀 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in the Streamlit Cloud dashboard
5. Deploy!

### Other Platforms

- **Heroku**: Use `Procfile` with `web: streamlit run app.py`
- **AWS/GCP**: Deploy as containerized app
- **Azure**: Use Azure App Service

## 📝 Future Enhancements

- [ ] Email notifications for feedback
- [ ] Excel export functionality
- [ ] Advanced analytics dashboard
- [ ] Goal templates
- [ ] File attachments
- [ ] Mobile app
- [ ] Integration with HR systems

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 💬 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation
- Review Supabase docs at [supabase.com/docs](https://supabase.com/docs)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Database powered by [Supabase](https://supabase.com)
- Icons from various emoji sets

---

**Happy Goal Tracking! 🎯**