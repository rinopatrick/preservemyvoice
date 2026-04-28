from preservemyvoice.config import Settings


def test_settings():
    """Test that settings load correctly."""
    settings = Settings()
    assert settings.APP_NAME == "PreserveMyVoice"
    assert settings.DEBUG is False
    assert settings.SAMPLE_RATE == 22050


def test_settings_debug_mode():
    """Test debug mode setting."""
    import os

    os.environ["DEBUG"] = "true"
    settings = Settings()
    assert settings.DEBUG is True
    del os.environ["DEBUG"]
