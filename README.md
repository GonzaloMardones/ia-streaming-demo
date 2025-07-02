# IA Streaming Demo (Docker, GCP, Firestore, React)

This project demonstrates an end-to-end streaming AI architecture using **React (Vite)** as the frontend, **FastAPI** as the backend, a **worker** for processing AI requests, Google **Pub/Sub**, and **Firestore** for real-time persistence—all containerized with Docker.

---

## 🚀 How to Run the Project

1. **Clone this repository**
    ```bash
    git clone https://github.com/yourusername/ia-streaming-demo.git
    cd ia-streaming-demo
    ```

2. **Copy and configure environment variables**

    - Copy `.env.example` to `.env` in both `backend-api/` and `worker/`, and fill in your real keys:
      ```bash
      cp backend-api/.env.example backend-api/.env
      cp worker/.env.example worker/.env
      ```

    - Download your GCP Service Account JSON and place it where your `.env` files indicate (commonly `/app/your-credential.json`).

3. **Configure Firebase for the Frontend**

    - In the [Firebase Console](https://console.firebase.google.com/), go to your project settings and register a Web App if needed.
    - Copy the generated configuration block into `frontend-react/src/firebaseConfig.js`.

4. **Build and start all services with Docker Compose**

    ```bash
    docker-compose up --build
    ```

    This will start the backend, worker, and frontend containers.  
    - The frontend will be accessible at [http://localhost:3000](http://localhost:3000)
    - The backend API at [http://localhost:8000](http://localhost:8000)

---

## ⚡ Environment Files

- **Never commit** real `.env` or Service Account JSON files to the repository.
- Always use and share `.env.example` files and fill in your actual secrets locally.

---

## ⚙️ Firebase Frontend Setup

- Your `frontend-react/src/firebaseConfig.js` should look like:

    ```js
    import { initializeApp } from "firebase/app";
    import { getFirestore } from "firebase/firestore";
    const firebaseConfig = {
      apiKey: "YOUR_API_KEY",
      authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
      projectId: "YOUR_PROJECT_ID",
      storageBucket: "YOUR_PROJECT_ID.appspot.com",
      messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
      appId: "YOUR_APP_ID"
    };
    const app = initializeApp(firebaseConfig);
    export const db = getFirestore(app);
    ```

- Make sure your Firestore security rules allow reading/writing for testing, for example:

    ```
    service cloud.firestore {
      match /databases/{database}/documents {
        match /{document=**} {
          allow read, write: if true;
        }
      }
    }
    ```

    > **Note:** Never use open rules in production.

---

## 🔒 Security

- **Never commit** your real `.env` files, Service Account JSONs, or private API keys to GitHub.
- Only commit `.env.example` and `firebaseConfig.example.js` for documentation.
- If you accidentally push a secret, remove it immediately and rotate or revoke the key.

---

## 🧩 Project Structure

- **backend-api/** – FastAPI backend that publishes prompts to Google Pub/Sub.
- **worker/** – Python service consuming Pub/Sub, calling the AI model (OpenAI), and writing results to Firestore.
- **frontend-react/** – React app showing streaming responses and conversation history.
- **docker-compose.yml** – Container orchestration for local development.

---

## 💡 Useful Commands

- Build and run all services:
    ```bash
    docker-compose up --build
    ```
- Stop all services:
    ```bash
    docker-compose down
    ```
- Rebuild a single service:
    ```bash
    docker-compose build backend
    docker-compose up backend
    ```

---

## 📖 More

- For cost estimation, review the free tiers for [Google Cloud Pub/Sub](https://cloud.google.com/pubsub/pricing) and [Firestore](https://firebase.google.com/pricing).
- For OpenAI, monitor your API usage [here](https://platform.openai.com/usage).

---

**Happy hacking! If you have questions or want to contribute, open an issue or pull request.**
