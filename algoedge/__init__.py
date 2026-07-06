import pymysql
pymysql.install_as_MySQLdb()

# Allow older MariaDB versions (XAMPP compatibility)
from django.db.backends.base.base import BaseDatabaseWrapper
_orig_check = BaseDatabaseWrapper.check_database_version_supported
def _patched_check(self):
    try:
        _orig_check(self)
    except Exception:
        pass
BaseDatabaseWrapper.check_database_version_supported = _patched_check
