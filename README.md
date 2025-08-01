# FastAPI Prototype

A comprehensive FastAPI prototype featuring authentication, CRUD operations, and modern API patterns. This project demonstrates best practices for building scalable REST APIs with FastAPI.

## Features

- 🔐 **JWT Authentication** - Secure user authentication with JWT tokens
- 👥 **User Management** - User registration, login, and profile management
- 📦 **CRUD Operations** - Complete Create, Read, Update, Delete operations for items
- 🛡️ **Security** - Password hashing, input validation, and authorization
- 📚 **Auto-generated Documentation** - Interactive API docs with Swagger UI
- 🔄 **CORS Support** - Cross-origin resource sharing enabled
- 🧪 **Testing Ready** - Structured for easy testing with pytest
- 📊 **Health Checks** - Built-in health monitoring endpoints

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   # If you have git
   git clone <repository-url>
   cd FastAPI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env with your configuration
   # At minimum, change the SECRET_KEY
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login and get access token

### Users
- `GET /users/me` - Get current user information (requires authentication)
- `GET /users` - Get all users

### Items (CRUD Operations)
- `POST /items/` - Create a new item (requires authentication)
- `GET /items/` - Get all items with pagination
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item (requires authentication)
- `DELETE /items/{item_id}` - Delete an item (requires authentication)

### System
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

## Usage Examples

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword123",
       "full_name": "John Doe"
     }'
```

### 2. Login and Get Token
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "securepassword123"
     }'
```

### 3. Create an Item (with authentication)
```bash
curl -X POST "http://localhost:8000/items/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Sample Item",
       "description": "This is a sample item",
       "price": 29.99
     }'
```

### 4. Get All Items
```bash
curl -X GET "http://localhost:8000/items/"
```

## Project Structure

```
FastAPI/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── env_example.txt     # Environment variables template
├── README.md          # This file
└── tests/             # Test files (to be added)
```

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests
```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest
```

### Code Quality
```bash
# Install linting tools
pip install black flake8 isort

# Format code
black main.py

# Check code style
flake8 main.py

# Sort imports
isort main.py
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with JSON Web Tokens
- **Input Validation**: Pydantic models ensure data integrity
- **Authorization**: Role-based access control for protected endpoints
- **CORS**: Configured for cross-origin requests

## Database

This prototype uses in-memory storage for simplicity. For production:

1. **Install SQLAlchemy and database driver**
   ```bash
   pip install sqlalchemy alembic psycopg2-binary
   ```

2. **Set up database models**
   ```python
   from sqlalchemy import create_engine, Column, Integer, String, DateTime
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker
   ```

3. **Configure database URL in .env**
   ```
   DATABASE_URL=postgresql://user:password@localhost/fastapi_db
   ```

## Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Environment Variables**: Set proper SECRET_KEY and other sensitive values
2. **Database**: Use PostgreSQL or similar production database
3. **HTTPS**: Configure SSL/TLS certificates
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Logging**: Add proper logging configuration
6. **Monitoring**: Set up health checks and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues:
- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Review the interactive API docs at `/docs`
- Open an issue in the repository

---

**Happy coding! 🚀** 