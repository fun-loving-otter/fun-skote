import pytest

from django.core.management import call_command


@pytest.fixture(autouse=True)
def load_email_templates():
    call_command('load_email_templates')


@pytest.fixture(autouse=True)
def load_admin_pages():
    call_command('load_admin_pages')
