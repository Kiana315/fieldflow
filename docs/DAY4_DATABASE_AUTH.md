
# Day 4 — Database Models & Authentication

## Completed Features

### Database
- SQLAlchemy 2.0 ORM models
- User, WorkOrder, CompletionRecord
- PostgreSQL Enum types
- Foreign keys and relationships
- Completion notes check constraint
- Alembic initial migration

### Authentication
- Argon2 password hashing
- JWT access token (HS256)
- POST /auth/login
- GET /auth/me
- Database session dependency
- Role-based access control (RBAC)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login | Authenticate user |
| GET | /auth/me | Get current user |

## Security

- Passwords stored as Argon2 hashes
- JWT expires after 30 minutes by default
- Inactive users cannot authenticate
- Invalid tokens return HTTP 401
- Insufficient permissions return HTTP 403
- JWT secret stored in environment variables

## Testing

31 automated tests passed.

Tests cover:
- ORM model metadata
- Password hashing and verification
- JWT generation and validation
- Login success and failure cases
- Protected endpoint authorization
- Role-based permissions

## Database Migration

Revision: acf52ea2fbb5

Apply migration:

    python -m alembic upgrade head

## Next Steps

Day 5 — Work Order API
- Create work orders
- List and retrieve work orders
- Assign technicians
- Implement status transitions
