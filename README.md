# 🧪 Health Check Research and Development (R&D) Project

This R&D proof-of-concept project explores the development of a standardized health check system tailored for Python-based applications. Its purpose is to detect the availability and accessibility of application dependencies and support robust service monitoring.

While the immediate outcome is not the creation of a reusable library, the core objective is to inform and guide future efforts toward developing a generic Python library that developers can integrate to assess application status, performance metrics, and service availability.

The concept will be demonstrated using FastAPI—a modern, high-performance web framework compatible with Python 3.11—alongside a standalone HTML page that displays the health check results in a user-friendly format. This approach illustrates both backend integration and frontend visualization, offering a blueprint for future adoption across diverse Python environments.

## 🦯 Core Feature Implementation Checklist

- [ ] Implement diagnostic routine to verify TCP connectivity to external endpoints based on hostname or IP address and designated port.
- [ ] Validate presence of all Python packages specified in the `requirements.txt` manifest.
- [ ] Conduct availability checks for remote HTTP-based APIs, ensuring proper response status and latency bounds.
- [ ] Establish connectivity verification for dependent relational database management systems (RDBMS), confirming authentication and schema accessibility.
- [ ] Detect and confirm active mount status of filesystem targets essential to application runtime dependencies.

[📖 Core Features Description](howto/CORE_FEATURES.md "Core Features Description")

## Proof of Concept Implementation

### FastAPI Routes

### HTML Demo

## 🚀 Deployment and Usage Procedures

[🖥️ Deploy the application on a bare-metal or virtual server and perform testing](howto/BAREMETAL.md "Deploy the application on a bare-metal or virtual server and perform testing")

[📦 Deploy the application on a container engine (e.g., Docker, Podman) and conduct testing](howto/BAREMETAL.md "Deploy the application on a container engine (e.g., Docker, Podman) and conduct testing")

[📘 Follow the documented procedures for application usage and operation](howto/USAGE_OPERATION.md "Follow the documented procedures for application usage and operation")



## Libraries Used

### FastAPI Application


### HTML Demo Page

### Pytest