# Coding Standards

## Objective
Ensure generated and human-written code follow a clear and maintainable project structure.

## General Rules
1. Use meaningful and descriptive function names.
2. Keep route handlers lightweight.
3. Business logic must live in the service layer.
4. Utility functions must be reusable and isolated.
5. Return JSON responses for API endpoints.
6. Use consistent naming conventions across files.

## File Organization
- `routes/` should contain HTTP route handlers.
- `services/` should contain feature logic.
- `models/` should represent data structures.
- `utils/` should contain helpers and validators.
- `tests/` should contain pytest test files.

## Style Guidelines
- Follow PEP 8 formatting.
- Prefer small, readable functions.
- Add docstrings for important functions.
- Handle errors explicitly.
- Do not mix validation, hashing, and persistence inside route functions.

## Response Handling
- Always return structured JSON responses.
- Use proper HTTP status codes.
- Keep error responses consistent.

## LLM Code Generation Preference
Generated code should:
- be modular
- be readable
- avoid unnecessary complexity
- align with the project folder structure