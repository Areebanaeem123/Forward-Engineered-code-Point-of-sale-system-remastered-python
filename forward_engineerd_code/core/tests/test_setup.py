"""
Test to verify Django project setup is working correctly.
"""
import pytest
from django.conf import settings


def test_django_settings_configured():
    """Test that Django settings are properly configured."""
    assert settings.configured
    assert 'core' in settings.INSTALLED_APPS
    assert settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'


def test_hypothesis_available():
    """Test that Hypothesis is available for property-based testing."""
    import hypothesis
    assert hypothesis is not None


def test_factory_boy_available():
    """Test that factory-boy is available for test fixtures."""
    import factory
    assert factory is not None
