import pytest

from datetime import date

from authentication.tests.conftest import *
from payments.tests.conftest import *
from main.models import Data, DataList, DataPackageBenefits, DataUpload, UploadedDataFile


@pytest.fixture
def create_subscribed_user(auto_login_user, create_active_subscription):
    def make(api=False):
        client, user = auto_login_user(api=api)
        subscription = create_active_subscription(user)
        DataPackageBenefits.objects.create(
            action_credits=100,
            add_to_list_credits=200,
            export_credits=5000,
            package=subscription.package
        )
        # Half-ass the attachment
        user.subscription = subscription
        return client, user
    return make



@pytest.fixture
def create_data_list():
    def make_data_list(user):
        return DataList.objects.create(
            creator=user,
            name='Test Data List',
            source='Test Source'
        )
    return make_data_list



@pytest.fixture
def create_data_upload():
    def make(**kwargs):
        if not kwargs.get('name'):
            kwargs['name'] = 'test upload'
        data_upload = DataUpload.objects.create(**kwargs)
        uploaded_data_file = UploadedDataFile.objects.create(data_upload=data_upload, file='test file', processed=True)
        return data_upload, uploaded_data_file
    return make


@pytest.fixture
def create_data():
    def make(uploaded_data_file, **kwargs):
        default_kwargs = {x[1]: x[0] for x in Data._header_field_mapping.items()}
        default_kwargs['founded_date'] = date.today()
        default_kwargs['ipo_date'] = date.today()
        default_kwargs['last_funding_date'] = date.today()

        for key, value in default_kwargs.items():
            kwargs.setdefault(key, value)

        return Data.objects.create(uploaded_data_file=uploaded_data_file, **kwargs)
    return make


@pytest.fixture
def created_data(create_data_upload):
    data_upload, uploaded_data_file = create_data_upload()

    for i in range(10):
        kwargs = {x[1]: x[0] + str(i) for x in Data._header_field_mapping.items()}
        kwargs['founded_date'] = date.today()
        kwargs['ipo_date'] = date.today()
        kwargs['last_funding_date'] = date.today()
        Data.objects.create(uploaded_data_file=uploaded_data_file, **kwargs)

    return data_upload
