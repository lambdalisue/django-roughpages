try:
    # Python 3 have mock in unittest
    from unittest.mock import MagicMock, patch, DEFAULT
except ImportError:
    from mock import MagicMock, patch, DEFAULT

try:
    from django.test.utils import override_settings
except ImportError:
    from override_settings import override_settings

try:
    from unittest import skipIf
except ImportError:
    def skipIf(condition, message):
        def decorator(f):
            return None if condition else f
        return decorator
