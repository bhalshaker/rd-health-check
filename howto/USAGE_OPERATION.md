# Health Check System – Operations Guide

This guide outlines how to operate, configure, and interact with the health check system hosted at `http://localhost:8000`.

---

## System Overview

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  
  Use this to explore and test API endpoints interactively.

- **Frontend App**: [http://localhost:8000](http://localhost:8000)  
  Provides a demo visual interface for monitoring health check results.

---

## Configuration File: `health_check_config.json`

This file defines which health checks to run. Each entry includes:

| Field | Description |
|-------|-------------|
| `check_type` | Type of check: `database`, `webservice`, `mount_point`, `requirements` |
| `details.synonym` | Friendly name for the check |
| `details` | Parameters specific to the check type |

### Example Configuration
```json
[
  {
    "check_type": "database",
    "details": {
      "synonym": "Core Database",
      "hostname": "mozilla.cloudflare-dns.com",
      "port": 443,
      "database_type": "mysql"
    }
  },
  {
    "check_type": "webservice",
    "details": {
      "synonym": "example API",
      "hostname": "example.com",
      "port": 443,
      "protocol": "https"
    }
  },
  {
    "check_type": "mount_point",
    "details": {
      "synonym": "Root partition",
      "mount_point": "/",
      "threshold_percentage": 45
    }
  },
  {
    "check_type":"requirements",
    "details":{
      "synonym":"Requirements Files",
      "requirements_file_path":"requirements.txt"
    }
  }
]
```

---

## Running Health Checks thought Web APIs

### 1. **Run All Checks**
```bash
curl -X GET http://localhost:8000/healthcheck \
  -H 'accept: application/json'
```

### 2. **Run Specific Checks**

#### Databases
```bash
curl -X GET http://localhost:8000/healthcheck/databases \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer rd-healthcheck'
```  
#### Webservices
```bash
curl -X GET http://localhost:8000/healthcheck/webservices \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer rd-healthcheck'
```  
#### Mount Points
```bash
curl -X GET http://localhost:8000/healthcheck/mountpoints \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer rd-healthcheck'
```  
#### Requirements
```bash
curl -X GET http://localhost:8000/healthcheck/requirements \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer rd-healthcheck'
```  