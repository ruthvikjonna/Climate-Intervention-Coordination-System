import os
import pytest
from supabase import create_client, Client
from app.core.database import get_supabase
from app.main import app
from fastapi.testclient import TestClient

# Use Supabase test project for testing
TEST_SUPABASE_URL = os.getenv("TEST_SUPABASE_URL", "your_test_supabase_url")
TEST_SUPABASE_KEY = os.getenv("TEST_SUPABASE_KEY", "your_test_supabase_key")

@pytest.fixture(scope="session")
def test_supabase():
    """Create a test Supabase client"""
    return create_client(TEST_SUPABASE_URL, TEST_SUPABASE_KEY)

@pytest.fixture(autouse=True)
def cleanup_test_data(test_supabase):
    """Clean up test data before each test"""
    # Clean up interventions table
    test_supabase.table("interventions").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    yield

@pytest.fixture()
def supabase():
    """Provide Supabase client for tests"""
    return test_supabase()

@pytest.fixture()
def client():
    """Provide test client with Supabase dependency override"""
    def override_get_supabase():
        return test_supabase()
    
    app.dependency_overrides = {}
    app.dependency_overrides[get_supabase] = override_get_supabase
    
    with TestClient(app) as c:
        yield c 