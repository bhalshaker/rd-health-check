# 🧪 Health Check Research and Development (R&D) Project

This R&D proof-of-concept project explores the development of a standardized health check system tailored for Python-based applications. Its purpose is to detect the availability and accessibility of application dependencies and support robust service monitoring.

While the immediate outcome is not the creation of a reusable library, the core objective is to inform and guide future efforts toward developing a generic Python library that developers can integrate to assess application status, performance metrics, and service availability.

The concept will be demonstrated using FastAPI—a modern, high-performance web framework compatible with Python 3.11—alongside a standalone HTML page that displays the health check results in a user-friendly format. This approach illustrates both backend integration and frontend visualization, offering a blueprint for future adoption across diverse Python environments.

## 🦯 Core Feature Implementation Checklist

- [75%] Implement diagnostic routine to verify TCP connectivity to external endpoints based on hostname or IP address and designated port.
- [50%] Validate presence of all Python packages specified in the `requirements.txt` manifest.
- [25%] Conduct availability checks for remote HTTP-based APIs, ensuring availability of the service.
- [75%] Detect and confirm active mount status of filesystem targets essential to application runtime dependencies.

[📖 Core Features Description](howto/CORE_FEATURES.md "Core Features Description")

## ✨ Proof of Concept Implementation

### ⚙️ FastAPI Routes

| HTTP Method | Endpoint         | Description                       | Who Can Access? | 
|-------------|------------------|-----------------------------------|------------------|
| GET         | /health        | Returns overall health status of the health checks with a details list of each category       | Public  |
| GET         | /health/databases        | Returns overall health status of databases checklist a details list of each database       | Admin User  |
| GET         | /health/mountpoints        | Returns overall health status of the mount points health checks with a details list of each mount point       | Admin User   |
| GET         | /health/webservices        | Returns overall health status of the health checks of registered webservice api with a details list of each webservice       | Admin User   |

### 🌐 HTML Demo

* A **dropdown menu** with the following options: [All,Databases, Webservices, Mount points].
* A **submit button** that triggers the display of the selected category.
* A **status view** that shows the health status of the selected option.

## 🚀 Deployment and Usage Procedures

[🖥️ Deploy the application on a bare-metal or virtual server and perform testing](howto/BAREMETAL.md "Deploy the application on a bare-metal or virtual server and perform testing")

[📦 Deploy the application on a container engine (e.g., Docker, Podman) and conduct testing](howto/BAREMETAL.md "Deploy the application on a container engine (e.g., Docker, Podman) and conduct testing")

[📘 Follow the documented procedures for application usage and operation](howto/USAGE_OPERATION.md "Follow the documented procedures for application usage and operation")


## 📋 Run environemnt prerequisites

* 🐍 Python 3.11
* 🐳 Docker/ 🦭 Podman (Recommended to automate testing, otherwise allocating databases should be done manually)

## 📦 Libraries Used

### 🐍 Python Backend Application

| Tool/Library       | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **FastAPI**         | Web framework for building RESTful APIs using Python type hints.        |
| **Uvicorn**         | ASGI server for running FastAPI apps in production.                     |
| **Pydantic**        | Data validation and parsing of JSON bodies and query parameters.        |
| **prometheus_client** | Exposes metrics for Prometheus monitoring and alerting.                |
| **jsonschema** | Validates JSON data against a JSON Schema, which is a declarative way to describe the structure and constraints of JSON data. |

### 🌐 Frontend (HTML Demo Page)

| Tool/Library       | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **Tailwind CSS**    | Utility-first CSS framework for responsive design.                      |
| **React**           | JavaScript library for building interactive UIs.                        |
| **Babel**           | Transpiles modern JavaScript for browser compatibility.                 |
| **fetch API**       | Native JavaScript method for making RESTful API calls to FastAPI.       |

### 🧪 Testing & CI/CD

| Tool/Library       | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **Pytest**          | Framework for writing and running tests.                                |
| **pytest-html**     | Generates HTML reports from Pytest results.                             |
| **Selenium**        | Automates browser-based UI testing.                                     |
| **TestClient (FastAPI)** | Tests FastAPI routes without running a live server.               |
| **GitHub Actions**  | Automates testing, linting, and deployment workflows.                   |