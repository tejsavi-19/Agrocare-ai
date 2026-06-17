# How to Run AgroCareAI

This guide provides step-by-step instructions on how to start both the backend and frontend for the AgroCareAI project.

You will need to open **two separate terminal windows** (or tabs): one for the backend and one for the frontend.

---

## 1. Running the Backend (Python/Flask)

1. **Open a terminal** and navigate to the backend folder:
   ```bash
   cd "AgroCareAI\backend"
   ```
   *(Or using the full path: `cd "c:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\AgroCareAI\backend"`)*

2. **(Optional but recommended) Create a virtual environment** to isolate dependencies:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows (Command Prompt or PowerShell):
     ```bash
     .\venv\Scripts\activate
     ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the Flask application**:
   ```bash
   python app.py
   ```
   *The backend will start running, usually on `http://127.0.0.1:5000`.*

---

## 2. Running the Frontend (React/Vite)

1. **Open a NEW, second terminal window** and navigate to the frontend folder:
   ```bash
   cd "AgroCareAI\frontend"
   ```
   *(Or using the full path: `cd "c:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\AgroCareAI\frontend"`)*

2. **Install the Node.js modules** (you only need to do this the first time or if `package.json` changes):
   ```bash
   npm install
   ```

3. **Start the Vite development server**:
   ```bash
   npm run dev
   ```
   *The frontend will start running. You will see a target address (usually `http://localhost:5173`) in the terminal. **Ctrl + Click** the link or copy and paste it into your web browser to open the application.*
