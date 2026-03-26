# API Requirements

## Feature Name
User Registration API

## Objective
Implement a backend API endpoint that allows a new user to register with the system using name, email, and password.

## Endpoint
`POST /register`

## Request Payload
The request body must contain:
- `name` : string
- `email` : string
- `password` : string

## Functional Requirements
1. The API must accept a valid JSON request body.
2. The API must validate that all required fields are present.
3. The email must follow a valid email format.
4. The email must be unique in the system.
5. The password must be at least 8 characters long.
6. The password must be hashed before being stored.
7. The API must return a success response when registration is completed.
8. The API must return meaningful error messages for invalid input.

## Success Response
- HTTP Status: `201 Created`
- Response body:
```json
{
  "message": "User registered successfully"
}