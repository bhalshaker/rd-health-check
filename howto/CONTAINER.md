# 🛠️ RC Healthcheck Demo App: Setup & Testing Guide

This guide walks you through cloning the project, building a container image, running the container, executing test suites, and managing the container lifecycle using **Docker** or **Podman**.

---

## 📥 Step 1: Clone the Project Repository

```bash
git clone https://github.com/bhalshaker/rd-health-check.git
```

---

## 📂 Step 2: Navigate to the Project Directory

```bash
cd rd-health-check
```

---

## 🐳 Step 3: Build the Container Image

### Using Docker

```bash
docker build -t rc-healthcheck-demo-app docker/.
```

### Using Podman

```bash
podman build -t rc-healthcheck-demo-app docker/.
```

---

## 🚀 Step 4: Run the Container

### Using Docker

```bash
docker run -d -p 8000:8000 --name rc-healthcheck-demo rc-healthcheck-demo-app
```

### Using Podman

```bash
podman run -d -p 8000:8000 --name rc-healthcheck-demo rc-healthcheck-demo-app
```

---

## 🧪 Step 5: Run Tests Inside the Container

### Integration Tests

#### Using Docker

```bash
docker exec -it rc-healthcheck-demo .venv/bin/pytest app/tests/integration
```
#### Using Podman

```bash
podman exec -it rc-healthcheck-demo .venv/bin/pytest app/tests/integration
```

### Unit Tests

#### Using Docker

```bash
docker exec -it rc-healthcheck-demo .venv/bin/pytest app/tests/unit
```

#### Using Podman

```bash
podman exec -it rc-healthcheck-demo .venv/bin/pytest app/tests/unit
```

### End-to-End Tests


#### Using Docker

```bash
docker exec -it rc-healthcheck-demo .venv/bin/pytest app/tests/e2e
```

#### Using Podman

```bash
podman exec -it rc-healthcheck-demo .venv/bin/pytest app/tests/e2e
```

---

## 🔄 Step 6: Manage Container Lifecycle

### Stop the Container

#### Using Docker

```bash
docker stop rc-healthcheck-demo
```

#### Using Podman

```bash
podman stop rc-healthcheck-demo
```

### Start the Container Again

#### Using Docker

```bash
docker start rc-healthcheck-demo
```

#### Using Podman

```bash
podman start rc-healthcheck-demo
```


### View Container Logs

#### Using Docker

```bash
docker logs rc-healthcheck-demo
```

#### Using Podman

```bash
podman logs rc-healthcheck-demo
```

---

## ✅ Notes

- Ensure Docker or Podman is installed and running.
- You can replace `docker` with `podman` in most commands—they're CLI-compatible for basic usage.

---