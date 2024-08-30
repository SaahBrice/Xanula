
# 📚 Xanula Interactive Learning Platform

Welcome to **Xanula**, an innovative and interactive learning platform designed to enhance educational engagement through structured workbooks and quizzes. **Xanula** offers a dynamic learning experience for students and provides powerful management tools for administrators and authors. 

## 🚀 Project Overview

**Xanula** is built to support the educational process by providing students with access to a wide range of learning materials, including quizzes and past exam papers, all organized within workbooks. The platform also integrates AI-driven feedback mechanisms and detailed performance tracking to create an enriching educational experience.

### Key Features:

- **User Roles**: Multiple user roles including Students, Administrators, and Authors with distinct permissions and capabilities.
- **Workbooks and Quizzes**: Structured learning materials with various quiz types such as multiple choice, drag-and-drop, and more.
- **Leaderboard and Badges**: Gamified learning experience with points, badges, and a leaderboard to encourage competition.
- **AI Integration**: Claude AI provides instant explanations to student queries with the option to escalate to an administrator.
- **Past Exam Papers**: Non-downloadable past exam papers with video explanations integrated via YouTube.
- **Real-Time Updates**: Instant updates to content, quizzes, and scores using Supabase's real-time features.
- **Author Dashboard**: Unique dashboard for authors to track interactions and revenue generated from their content.

## 🛠️ Technology Stack

### Backend

- **Django**: A powerful Python web framework used to build the backend logic, manage user authentication, and integrate third-party APIs.
- **Supabase**: A hosted backend service that provides a real-time database and API for managing data and user authentication.

### Frontend

- **Tailwind CSS**: A utility-first CSS framework used to build a responsive and modern interface.
- **Custom CSS**: Additional styling tailored to the specific needs of the platform.

### Third-Party Integrations

- **Claude AI**: Provides AI-assisted explanations for quiz questions.
- **YouTube API**: Embeds video explanations for past exam papers.
- **Supabase API**: Handles real-time data updates and secure user authentication.



## 🔧 Installation and Setup

### Prerequisites

Ensure you have the following installed:

- **Python 3.10**: Required for running Django.
- **PostgreSQL/MySQL**: Recommended SQL databases for production.
- **Supabase Account**: For managing the database and real-time features.
- **Git**: For version control.

### Installation

Follow these steps to get the project up and running on your local machine:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/saahbrice/xanula.git
   cd xanula
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Backend Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Frontend Dependencies**:


   ```bash
   pip install tailwindcss
   ```

5. **Database Setup**:

   Ensure your database is set up and configure the connection in `settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'xanula_db',
           'USER': 'yourusername',
           'PASSWORD': 'yourpassword',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

   Then, apply the migrations:

   ```bash
   python manage.py migrate
   ```

6. **Supabase Configuration**:

   Set up your Supabase account, and configure the API keys and URL in `settings.py` to handle real-time updates and authentication.

7. **Create a Superuser**:

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

   The app should now be running at `http://127.0.0.1:8000/`.

9. **Access the Admin Panel**:

   Visit `http://127.0.0.1:8000/admin/` and log in with the superuser credentials you created.

## 🛠️ Features and Implementation Details

### 1. **User Roles and Permissions**

**Students**: 

- Access workbooks and quizzes.
- Earn points and badges.
- View past exam papers and request further explanations.
- Receive AI-driven feedback and escalate queries to administrators.

**Administrators**: 

- Manage content, including workbooks, quizzes, and past exam papers.
- Handle student queries and feedback.
- Track student and author performance through detailed dashboards.

**Authors**: 

- Access a unique dashboard to monitor the performance of their content without needing a regular user account.
- Earn "Xans" based on student interactions, which are tracked for potential remuneration.

### 2. **Workbooks and Quizzes**

- **Workbook Creation**: Admins can create and organize workbooks by chapters, each containing quizzes.
- **Quiz Types**: Multiple choice, single choice, drag-and-drop, match-the-correct, and label the diagram.
- **Real-Time Updates**: Any changes made by admins are instantly reflected on the student's view thanks to Supabase's real-time capabilities.

### 3. **Leaderboard and Badges**

- **Gamification**: Students earn points and badges for completing quizzes and workbooks.
- **Leaderboard**: Displays the top-performing students, fostering a competitive learning environment.

### 4. **Feedback and Support System**

- **Claude AI Integration**: Provides instant, AI-driven explanations for student queries.
- **Admin Escalation**: Students can escalate their queries to an admin for detailed explanations if unsatisfied with the AI response.
- **Notification System**: Alerts students about new content, responses to queries, and achievements.

### 5. **Past Exam Papers and Solutions**

- **View-Only Access**: Students can view past exam papers in a non-downloadable format.
- **YouTube Integration**: Video explanations for each exam question are embedded within the platform.
- **Solution Feedback**: Students can request additional explanations for any part of the exam solutions.

### 6. **Author Dashboard**

- **Access via Unique Code**: Authors use a unique code to access their dashboard, where they can track student interactions, feedback, and revenue generation ("Xans").
- **Revenue Tracking**: Authors can monitor their earnings based on how frequently students engage with their workbooks.

## 🚀 Deployment

### Deployment Steps

1. **Configure Production Settings**: Update `settings.py` for production with secure settings, such as disabling `DEBUG`, setting `ALLOWED_HOSTS`, and configuring your production database.

2. **Collect Static Files**:

   ```bash
   python manage.py collectstatic
   ```

3. **Supabase and Cloud Deployment**: Ensure Supabase is properly configured for real-time updates, and deploy the application using a cloud service like **Heroku**, **AWS**, or **DigitalOcean**.

4. **CI/CD Pipeline**: Set up a Continuous Integration/Continuous Deployment pipeline to automate testing and deployment processes.

## 📄 License

This project is licensed under the MIT License 

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them

 (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## 📧 Contact

For any inquiries or support, please contact the project team at saahbrice98@gmail.com

