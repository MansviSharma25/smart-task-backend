>>>>>>> **Smart Task & Team Management System (Backend APIs)** <<<<<<<

**DESCRIPTION** >>>  A Django REST Framework-based backend system for managing tasks, teams, and user roles.
This project provides secure APIs for user authentication (signup, login, logout), task management (create, update, delete, mark complete), and team collaboration (create teams, add members, view team tasks).
Perfect for small teams or individuals who want to organize their work efficiently.


**TECH STACK** >>>  • Backend: Django + Django REST Framework
                    • Database: SQLite or PostgreSQL
                    • Authentication: Custom Token Authentication / JWT Authentication
                    • Testing: Postman / Django Test Framework
                    • Deployment: Render/Heroku (Optional)


**API Endpoints List** >>> • Authentication APIs:
                               - POST /api/auth/signup
                               - POST /api/auth/login
                               - POST /api/auth/logout
                            
                            • Task APIs:
                               - GET /api/tasks/ (list tasks)
                               - POST /api/tasks/ (create task)
                               - PUT /api/tasks/{id}/ (update task)
                               - DELETE /api/tasks/{id}/ (delete task)
                               - PATCH /api/tasks/{id}/complete/ (mark as complete)
                            
                            • Team APIs:
                               - POST /api/teams/ (create team)
                               - POST /api/teams/{id}/add-member/ (add member)
                               - GET /api/teams/{id}/tasks/ (view team tasks)
                            
                            • Reporting APIs:
                               - GET /api/reports/summary (overview of pending, completed, overdue tasks)


**Setup Instructions** >>>      
1️⃣ Clone the Repository
______________________________________________________________________
git clone https://github.com/your-username/smarttask-backend.git   
cd smarttask-backend                                                
______________________________________________________________________

2️⃣ Create & Activate Virtual Environment
______________________________________________________________________
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
                                                
______________________________________________________________________

3️⃣ Install Dependencies
______________________________________________________________________
pip install -r requirements.txt                                             
______________________________________________________________________

4️⃣ Apply Migrations
______________________________________________________________________
python manage.py makemigrations
python manage.py migrate                                               
______________________________________________________________________

5️⃣ Create Superuser (Optional - for Admin Panel)
______________________________________________________________________
python manage.py createsuperuser                                              
______________________________________________________________________

6️⃣ Run the Development Server
______________________________________________________________________
python manage.py runserver                                              
______________________________________________________________________

**Backend will be available at:
➡ http://127.0.0.1:8000/**



                    



