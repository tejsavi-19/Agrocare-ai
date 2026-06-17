# AgroCare-AI — AI Plant Disease Detection Platform

AgroCare-AI is a scalable, full-stack web application designed to help farmers and agricultural enthusiasts detect plant diseases using artificial intelligence. By uploading an image of a plant leaf or stem, users receive an instant diagnosis with confidence scores, risk levels, and actionable treatment advice.

## 🚀 Features

-   **Deep Learning Model**: Pre-trained MobileNetV3 model for high-accuracy detection of healthy vs. diseased plants.
-   **Instant Analysis**: Fast image processing and prediction.
-   **User Dashboard**: Secure area for users to upload images and view results.
-   **History Tracking**: Saves all past scans with timestamps and results for future reference.
-   **Statistics**: Visual analytics of scan history (Healthy vs. Diseased ratios).
-   **Responsive Design**: Modern UI/UX built with React and TailwindCSS, fully optimized for mobile and desktop.
-   **Secure Authentication**: JWT-based login and signup system.

## 🛠️ Tech Stack

### Frontend
-   **React (Vite)**: Fast and modern UI library.
-   **TailwindCSS**: Utility-first CSS framework for styling.
-   **Axios**: For API requests.
-   **Recharts**: For statistical data visualization.
-   **Lucide React**: For beautiful icons.

### Backend
-   **Python Flask**: Lightweight WSGI web application framework.
-   **TensorFlow/Keras**: For loading and running the AI model.
-   **MySQL**: Relational database for storing user data and scan history.
-   **SQLAlchemy**: ORM for database interactions.
-   **Flask-JWT-Extended**: For secure authentication.

## 📋 Prerequisites

-   **Python 3.8+**
-   **Node.js 16+** & **npm**
-   **MySQL Server** running on localhost (Default config: user `root`, password `rehan15`)

## ⚙️ Installation & Setup

### 1. Database Setup
Ensure your MySQL server is running. The application will automatically create the `agrocare_db` database and tables upon the first run of the backend.

### 2. Backend Setup
Navigate to the backend directory:
```bash
cd AgroCareAI/backend
```

Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Run the Backend Server:
```bash
python app.py
```
The backend will start on `http://localhost:5000`.

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory:
```bash
cd AgroCareAI/frontend
```

Install Node dependencies:
```bash
npm install
```

Run the Frontend Development Server:
```bash
npm run dev
```
The application will be accessible at `http://localhost:5173`.

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/signup` | Register a new user | No |
| `POST` | `/auth/login` | Login and get JWT token | No |
| `POST` | `/api/predict` | Upload image for diagnosis | Yes |
| `GET` | `/api/history` | Get user's scan history | Yes |
| `GET` | `/api/stats` | Get user's scan statistics | Yes |

## 📂 Project Structure

```
AgroCareAI/
├── backend/
│   ├── ai_models/          # TensorFlow .h5 models
│   ├── models/             # Database models (User, Scan)
│   ├── routes/             # API routes (Auth, Predict)
│   ├── uploads/            # Stored user uploaded images
│   ├── app.py              # Application entry point
│   ├── config.py           # Configuration settings
│   ├── ai_engine.py        # AI inference logic
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── src/
    │   ├── components/     # Reusable UI components
    │   ├── context/        # React Context (Auth)
    │   ├── pages/          # Application pages
    │   ├── services/       # API integration
    │   └── App.jsx         # Main React component
    ├── tailwind.config.js  # Tailwind configuration
    └── vite.config.js      # Vite configuration
```

## 🛡️ License
This project is for academic and educational purposes.
