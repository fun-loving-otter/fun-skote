import pytest

from django.core.management import call_command


@pytest.fixture(autouse=True)
def load_email_templates():
    call_command('load_email_templates')


@pytest.fixture(autouse=True)
def load_admin_pages():
    call_command('load_admin_pages')


@pytest.fixture(autouse=True)
def load_data_columns():
    call_command('load_data_column_visibility')


@pytest.fixture(autouse=True)
def patch_celery(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
