import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self):
        """Test user registration"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        response = client.post("/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "password" not in data  # Password should not be returned
    
    def test_register_duplicate_username(self):
        """Test registration with duplicate username"""
        user_data = {
            "username": "duplicateuser",
            "email": "duplicate@example.com",
            "password": "testpassword123",
            "full_name": "Duplicate User"
        }
        # Register first user
        client.post("/register", json=user_data)
        
        # Try to register with same username
        response = client.post("/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_login_success(self):
        """Test successful login"""
        # First register a user
        user_data = {
            "username": "logintest",
            "email": "login@example.com",
            "password": "testpassword123",
            "full_name": "Login Test"
        }
        client.post("/register", json=user_data)
        
        # Then login
        login_data = {
            "username": "logintest",
            "password": "testpassword123"
        }
        response = client.post("/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        response = client.post("/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

class TestUsers:
    """Test user-related endpoints"""
    
    def test_get_users(self):
        """Test getting all users"""
        response = client.get("/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_current_user_without_token(self):
        """Test getting current user without authentication"""
        response = client.get("/users/me")
        assert response.status_code == 403
    
    def test_get_current_user_with_token(self):
        """Test getting current user with valid token"""
        # First register and login to get token
        user_data = {
            "username": "currentusertest",
            "email": "current@example.com",
            "password": "testpassword123",
            "full_name": "Current User Test"
        }
        client.post("/register", json=user_data)
        
        login_data = {
            "username": "currentusertest",
            "password": "testpassword123"
        }
        login_response = client.post("/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Get current user with token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "currentusertest"

class TestItems:
    """Test item-related endpoints"""
    
    def test_create_item_without_auth(self):
        """Test creating item without authentication"""
        item_data = {
            "title": "Test Item",
            "description": "Test description",
            "price": 29.99
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 403
    
    def test_create_item_with_auth(self):
        """Test creating item with authentication"""
        # First register and login
        user_data = {
            "username": "itemcreator",
            "email": "item@example.com",
            "password": "testpassword123",
            "full_name": "Item Creator"
        }
        client.post("/register", json=user_data)
        
        login_data = {
            "username": "itemcreator",
            "password": "testpassword123"
        }
        login_response = client.post("/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Create item
        item_data = {
            "title": "Test Item",
            "description": "Test description",
            "price": 29.99
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/items/", json=item_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == item_data["title"]
        assert data["price"] == item_data["price"]
    
    def test_get_items(self):
        """Test getting all items"""
        response = client.get("/items/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_item_by_id(self):
        """Test getting item by ID"""
        # First create an item
        user_data = {
            "username": "itemgetter",
            "email": "getter@example.com",
            "password": "testpassword123",
            "full_name": "Item Getter"
        }
        client.post("/register", json=user_data)
        
        login_data = {
            "username": "itemgetter",
            "password": "testpassword123"
        }
        login_response = client.post("/login", json=login_data)
        token = login_response.json()["access_token"]
        
        item_data = {
            "title": "Get Test Item",
            "description": "Test description",
            "price": 19.99
        }
        headers = {"Authorization": f"Bearer {token}"}
        create_response = client.post("/items/", json=item_data, headers=headers)
        item_id = create_response.json()["id"]
        
        # Get item by ID
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["title"] == item_data["title"]
    
    def test_get_nonexistent_item(self):
        """Test getting item that doesn't exist"""
        response = client.get("/items/99999")
        assert response.status_code == 404
        assert "Item not found" in response.json()["detail"]
    
    def test_update_item_with_auth(self):
        """Test updating item with authentication"""
        # First create an item
        user_data = {
            "username": "itemupdater",
            "email": "updater@example.com",
            "password": "testpassword123",
            "full_name": "Item Updater"
        }
        client.post("/register", json=user_data)
        
        login_data = {
            "username": "itemupdater",
            "password": "testpassword123"
        }
        login_response = client.post("/login", json=login_data)
        token = login_response.json()["access_token"]
        
        item_data = {
            "title": "Original Title",
            "description": "Original description",
            "price": 25.00
        }
        headers = {"Authorization": f"Bearer {token}"}
        create_response = client.post("/items/", json=item_data, headers=headers)
        item_id = create_response.json()["id"]
        
        # Update item
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "price": 35.00
        }
        response = client.put(f"/items/{item_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["price"] == update_data["price"]
    
    def test_delete_item_with_auth(self):
        """Test deleting item with authentication"""
        # First create an item
        user_data = {
            "username": "itemdeleter",
            "email": "deleter@example.com",
            "password": "testpassword123",
            "full_name": "Item Deleter"
        }
        client.post("/register", json=user_data)
        
        login_data = {
            "username": "itemdeleter",
            "password": "testpassword123"
        }
        login_response = client.post("/login", json=login_data)
        token = login_response.json()["access_token"]
        
        item_data = {
            "title": "Item to Delete",
            "description": "Will be deleted",
            "price": 15.00
        }
        headers = {"Authorization": f"Bearer {token}"}
        create_response = client.post("/items/", json=item_data, headers=headers)
        item_id = create_response.json()["id"]
        
        # Delete item
        response = client.delete(f"/items/{item_id}", headers=headers)
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify item is deleted
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404

class TestSystem:
    """Test system endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

class TestValidation:
    """Test input validation"""
    
    def test_register_invalid_email(self):
        """Test registration with invalid email"""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        response = client.post("/register", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_register_short_password(self):
        """Test registration with short password"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "short",
            "full_name": "Test User"
        }
        response = client.post("/register", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_item_invalid_price(self):
        """Test creating item with invalid price"""
        # First get a token
        user_data = {
            "username": "validationtest",
            "email": "validation@example.com",
            "password": "testpassword123",
            "full_name": "Validation Test"
        }
        client.post("/register", json=user_data)
        
        login_data = {
            "username": "validationtest",
            "password": "testpassword123"
        }
        login_response = client.post("/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Try to create item with negative price
        item_data = {
            "title": "Test Item",
            "description": "Test description",
            "price": -10.00
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/items/", json=item_data, headers=headers)
        assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main([__file__]) 