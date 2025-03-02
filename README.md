# Globetrotter Project - Backend

## Overview
The backend for the Globetrotter Challenge, a travel guessing game with AI integration, score tracking, and social challenge features. This Django-based backend interacts with MongoDB for data storage and provides APIs for the frontend.

## Features
- User authentication and score tracking
- AI-based travel challenge generation
- "Challenge a Friend" functionality
- MongoDB integration via PyMongo
- RESTful APIs for frontend interaction

## Technologies Used
- **Framework:** Django
- **Database:** MongoDB (via PyMongo)
- **Server:** Gunicorn
- **Deployment:** AWS EC2

## Installation
### Prerequisites
- Python 3.12+
- MongoDB installed and running
- Virtual environment setup

### Steps to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/sachidanandsde/Globetrotter-Project.git
   cd Globetrotter-Project
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Configure environment variables (e.g., `.env` file for MongoDB connection, secret keys, etc.).

4. Run database migrations (if needed for any SQL components):
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Running in Production
### Gunicorn Setup
Run the backend using Gunicorn:
```bash
cd /home/ubuntu/Globetrotter-Project/globetrotter-backend
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 globetrotter.wsgi:application
```

### PM2 Process Management
For running Gunicorn in the background:
```bash
pm2 start "gunicorn --bind 0.0.0.0:8000 globetrotter.wsgi:application" --name globetrotter-backend
```

## API Endpoints
| Method | Endpoint                      | Description |
|--------|--------------------------------|-------------|
| POST   | `/api/game/create-user`       | Create a new user |
| GET    | `/api/game/get-score`         | Fetch user score |
| POST   | `/api/game/start-challenge`   | Start a new challenge |
| POST   | `/api/game/submit-answer`     | Submit an answer |
| GET    | `/api/game/leaderboard`       | Get leaderboard |

## Environment Variables
- `MONGO_URI`: MongoDB connection string
- `SECRET_KEY`: Django secret key

## Deployment on AWS EC2
1. Pull the latest code:
   ```bash
   git pull origin main
   ```
2. Restart the backend process:
   ```bash
   pm2 restart globetrotter-backend
   ```

## License
This project is licensed under the MIT License.

## Contributors
- **[Sachidanand SDE](https://github.com/sachidanandsde)**

