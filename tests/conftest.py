"""Configuration des tests pytest.

Fixtures réutilisables pour tous les tests.
"""

# Marqueurs personnalisés
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
