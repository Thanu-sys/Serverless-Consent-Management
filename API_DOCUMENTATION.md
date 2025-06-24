# Consent Management API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API doesn't require authentication. In a production environment, you should implement proper authentication and authorization.

## Endpoints

### Health Check
**GET** `/health`
- **Description**: Check if the API is running
- **Response**: 
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### Purposes

#### Get All Purposes
**GET** `/purposes`
- **Description**: Retrieve all available consent purposes
- **Response**:
```json
[
  {
    "id": 1,
    "name": "Marketing Communications",
    "description": "Receive marketing emails and promotional offers",
    "created_at": "2024-01-01T12:00:00.000000"
  }
]
```

#### Get Specific Purpose
**GET** `/purposes/{purpose_id}`
- **Description**: Get a specific purpose by ID
- **Parameters**: `purpose_id` (integer, path parameter)
- **Response**: Same as above but single object

### Consent Management

#### Get User Consents
**GET** `/consent?user_id={user_id}&purpose_id={purpose_id}`
- **Description**: Get consent records for a user
- **Parameters**: 
  - `user_id` (string, required): The user's unique identifier
  - `purpose_id` (integer, optional): Filter by specific purpose
- **Response**:
```json
[
  {
    "id": 1,
    "user_id": "user123",
    "purpose_id": 1,
    "purpose_name": "Marketing Communications",
    "status": true,
    "ip_address": "192.168.1.1",
    "created_at": "2024-01-01T12:00:00.000000",
    "updated_at": "2024-01-01T12:00:00.000000"
  }
]
```

#### Get Specific Consent
**GET** `/consent/{consent_id}`
- **Description**: Get a specific consent record by ID
- **Parameters**: `consent_id` (integer, path parameter)
- **Response**: Single consent object

#### Update/Create Consent
**POST** `/consent`
- **Description**: Update or create a consent record
- **Request Body**:
```json
{
  "user_id": "user123",
  "purpose_id": 1,
  "status": true
}
```
- **Response**: Updated/created consent object

#### Bulk Update Consents
**POST** `/consent/bulk`
- **Description**: Update multiple consent records at once
- **Request Body**:
```json
{
  "user_id": "user123",
  "consents": [
    {
      "purpose_id": 1,
      "status": true
    },
    {
      "purpose_id": 2,
      "status": false
    }
  ]
}
```
- **Response**:
```json
{
  "message": "Bulk update successful",
  "consents": [...]
}
```

#### Delete Consent
**DELETE** `/consent/{consent_id}`
- **Description**: Delete a specific consent record
- **Parameters**: `consent_id` (integer, path parameter)
- **Response**:
```json
{
  "message": "Consent record deleted successfully"
}
```

#### Delete User Consents
**DELETE** `/consent/user/{user_id}`
- **Description**: Delete all consent records for a user
- **Parameters**: `user_id` (string, path parameter)
- **Response**:
```json
{
  "message": "All consent records for user user123 deleted successfully"
}
```

### Analytics & Statistics

#### Get Consent Statistics
**GET** `/consent/stats`
- **Description**: Get overall consent statistics
- **Response**:
```json
{
  "total_consents": 100,
  "active_consents": 75,
  "inactive_consents": 25,
  "consent_rate": 75.0,
  "by_purpose": [
    {
      "purpose_name": "Marketing Communications",
      "total": 50,
      "active": 40,
      "rate": 80.0
    }
  ]
}
```

#### Get User Consent History
**GET** `/consent/user/{user_id}/history`
- **Description**: Get consent history for a specific user
- **Parameters**: `user_id` (string, path parameter)
- **Response**:
```json
{
  "user_id": "user123",
  "consent_history": {
    "Marketing Communications": [
      {
        "status": true,
        "ip_address": "192.168.1.1",
        "updated_at": "2024-01-01T12:00:00.000000"
      }
    ]
  }
}
```

#### Check Consent Status
**POST** `/consent/check`
- **Description**: Check if a user has given consent for specific purposes
- **Request Body**:
```json
{
  "user_id": "user123",
  "purpose_ids": [1, 2, 3]
}
```
- **Response**:
```json
{
  "user_id": "user123",
  "consent_status": {
    "Marketing Communications": {
      "has_consent": true,
      "status": true,
      "last_updated": "2024-01-01T12:00:00.000000"
    },
    "Analytics": {
      "has_consent": false,
      "status": null,
      "last_updated": null
    }
  }
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Error message",
  "message": "Detailed error description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing required parameters)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error

## Example Usage

### Setting up a new user's consents:
```bash
# Get available purposes
curl http://localhost:5000/api/purposes

# Set multiple consents at once
curl -X POST http://localhost:5000/api/consent/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "consents": [
      {"purpose_id": 1, "status": true},
      {"purpose_id": 2, "status": false}
    ]
  }'
```

### Checking user consent status:
```bash
curl -X POST http://localhost:5000/api/consent/check \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "purpose_ids": [1, 2, 3, 4]
  }'
```

### Getting consent statistics:
```bash
curl http://localhost:5000/api/consent/stats
```

## Database Schema

### Purposes Table
- `id` (Primary Key)
- `name` (String, 100 chars)
- `description` (Text)
- `created_at` (DateTime)

### Consents Table
- `id` (Primary Key)
- `user_id` (String, 36 chars)
- `purpose_id` (Foreign Key to purposes.id)
- `status` (Boolean)
- `ip_address` (String, 45 chars)
- `created_at` (DateTime)
- `updated_at` (DateTime) 