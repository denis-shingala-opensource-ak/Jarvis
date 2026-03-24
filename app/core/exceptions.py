"""Custom exception hierarchy for Jarvis."""


class JarvisError(Exception):
    """Base exception for all Jarvis errors."""
    pass


class LLMServiceError(JarvisError):
    """Error communicating with the LLM API."""
    pass


class SpeechServiceError(JarvisError):
    """Error in speech-to-text or text-to-speech."""
    pass


class ConfigurationError(JarvisError):
    """Invalid or missing configuration."""
    pass


class AuthRedirectException(Exception):
    """Raised when user is not authenticated and should be redirected to login."""
    pass