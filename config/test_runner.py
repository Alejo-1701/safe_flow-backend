from django.db import connections
from django.test.runner import DiscoverRunner

from config.test_schema import preparar


class SeedRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        configuraciones = super().setup_databases(**kwargs)
        preparar(connections["default"].connection)
        return configuraciones
