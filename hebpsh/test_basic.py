"""Simple tests to verify the application structure."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        # Test config imports
        from app.config import settings
        from app.config.database import Base, get_db
        print("✅ Config modules imported successfully")
        
        # Test model imports
        from app.models.url import URL
        print("✅ Model modules imported successfully")
        
        # Test schema imports
        from app.schemas.url import URLCreate, URLResponse, APIResponse
        print("✅ Schema modules imported successfully")
        
        # Test repository imports
        from app.repositories.url_repository import URLRepository
        print("✅ Repository modules imported successfully")
        
        # Test service imports
        from app.services.url_service import URLService
        from app.services.utils import generate_short_code
        print("✅ Service modules imported successfully")
        
        # Test controller imports
        from app.controllers.url_controller import router
        print("✅ Controller modules imported successfully")
        
        # Test main app
        from app.main import app
        print("✅ Main application imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        return False


def test_short_code_generation():
    """Test short code generation utility."""
    print("\nTesting short code generation...")
    
    try:
        from app.services.utils import generate_short_code
        
        # Generate multiple codes
        codes = [generate_short_code() for _ in range(10)]
        
        # Check length
        assert all(len(code) == 6 for code in codes), "All codes should be 6 characters"
        print("✅ All codes have correct length (6 characters)")
        
        # Check uniqueness (probabilistic)
        assert len(set(codes)) == len(codes), "Codes should be unique"
        print("✅ Generated codes are unique")
        
        # Check characters (Base62)
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        for code in codes:
            assert all(c in valid_chars for c in code), f"Code {code} contains invalid characters"
        print("✅ All codes use valid Base62 characters")
        
        return True
    except Exception as e:
        print(f"❌ Short code generation test failed: {str(e)}")
        return False


def test_pydantic_schemas():
    """Test Pydantic schema validation."""
    print("\nTesting Pydantic schemas...")
    
    try:
        from app.schemas.url import URLCreate, URLResponse, APIResponse
        from datetime import datetime
        
        # Test URLCreate
        url_create = URLCreate(original_url="https://example.com")
        assert url_create.original_url == "https://example.com"
        print("✅ URLCreate schema works correctly")
        
        # Test APIResponse
        api_response = APIResponse(status="success", message="Test")
        assert api_response.status == "success"
        assert api_response.message == "Test"
        print("✅ APIResponse schema works correctly")
        
        return True
    except Exception as e:
        print(f"❌ Pydantic schema test failed: {str(e)}")
        return False


def test_fastapi_app():
    """Test FastAPI application setup."""
    print("\nTesting FastAPI application...")
    
    try:
        from app.main import app
        
        # Check that app is a FastAPI instance
        from fastapi import FastAPI
        assert isinstance(app, FastAPI), "app should be a FastAPI instance"
        print("✅ FastAPI app is properly initialized")
        
        # Check routes
        routes = [route.path for route in app.routes]
        assert "/" in routes, "Root route should exist"
        assert "/health" in routes, "Health route should exist"
        assert "/urls" in routes, "URLs route should exist"
        print("✅ All expected routes are registered")
        
        return True
    except Exception as e:
        print(f"❌ FastAPI app test failed: {str(e)}")
        return False


def test_settings():
    """Test configuration settings."""
    print("\nTesting configuration settings...")
    
    try:
        from app.config.settings import settings
        
        # Check that settings are loaded
        assert hasattr(settings, 'DATABASE_URL'), "DATABASE_URL should exist"
        assert hasattr(settings, 'APP_HOST'), "APP_HOST should exist"
        assert hasattr(settings, 'APP_PORT'), "APP_PORT should exist"
        assert hasattr(settings, 'APP_TTL_MINUTES'), "APP_TTL_MINUTES should exist"
        print("✅ All configuration settings are present")
        
        # Check types
        assert isinstance(settings.APP_PORT, int), "APP_PORT should be integer"
        assert isinstance(settings.APP_TTL_MINUTES, int), "APP_TTL_MINUTES should be integer"
        print("✅ Configuration types are correct")
        
        return True
    except Exception as e:
        print(f"❌ Settings test failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("URL Shortener - Basic Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_short_code_generation,
        test_pydantic_schemas,
        test_fastapi_app,
        test_settings
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit(main())
