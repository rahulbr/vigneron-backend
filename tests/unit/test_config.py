"""
Unit tests for configuration module.
"""
import pytest
from app.core.config import Settings


class TestSettings:
    """Test Settings class."""

    def test_settings_initialization(self):
        """Test that settings can be initialized."""
        settings = Settings()
        assert settings.PROJECT_NAME == "Vigneron AI Backend"
        assert settings.VERSION == "1.0.0"
        assert settings.API_V1_STR == "/api/v1"

    def test_database_url_default(self):
        """Test default database URL."""
        settings = Settings()
        assert "postgresql://" in settings.DATABASE_URL

    def test_supabase_url_default(self):
        """Test default Supabase URL."""
        settings = Settings()
        assert "localhost:54321" in settings.SUPABASE_URL