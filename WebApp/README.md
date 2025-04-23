# Fire Detection Web App

This project is a full-stack fire detection system

- A **frontend UI** built with Next.js + React  
- A **backend inference service** using FastAPI + Docker  
- Default integration with **Hugging Face Spaces**

---

## Prerequisites
### Node.js (Frontend)
Install Node.js (LTS recommended — v20+):  
https://nodejs.org

### Docker (Backend)
Install Docker Desktop:  
https://www.docker.com/products/docker-desktop/

---

## Run the Frontend (Next.js UI)

1. Open your terminal and navigate to the frontend folder:

   ```bash
   cd app/frontend
   ```

2. Install project dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

4. Visit [http://localhost:3000](http://localhost:3000) to view the app.

---

## 🐳 Run the Backend with Docker

> `backend` and `backend_LUO` **both use port 7860** — only one can run at a time.

### Option 1: Run `backend`

```bash
cd backend
docker build -t backend .
docker run -p 7860:7860 backend
```

### Option 2: Run `backend_LUO`

```bash
cd backend_LUO
docker build -t backend_luo .
docker run -p 7860:7860 backend_luo
```
