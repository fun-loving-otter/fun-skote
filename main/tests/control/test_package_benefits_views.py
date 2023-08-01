import pytest

from django.urls import reverse

from control_panel.tests.conftest import AdminTemplateViewTestBase
from payments.models import SubscriptionPackage


class TestPackageWithBenefitsListView(AdminTemplateViewTestBase):
    url_name = 'control_panel:package-benefits'

    @pytest.fixture(autouse=True)
    def packages(self):
        self.packages = []
        self.packages.append(SubscriptionPackage.objects.create(name='Package 1', price=9.99))
        self.packages.append(SubscriptionPackage.objects.create(name='Package 2', price=19.99))
        self.packages.append(SubscriptionPackage.objects.create(name='Package 3', price=29.99))
        return self.packages


    def test_get_succeeds(self, url, admin_client):
        response = admin_client.get(url)
        assert response.status_code == 200
        assert all(package in response.context['object_list'] for package in self.packages)




class TestPackageWithBenefitsUpdateView(AdminTemplateViewTestBase):
    url_name = 'control_panel:package-benefits-edit'

    @pytest.fixture(autouse=True)
    def package(self):
        self.package = SubscriptionPackage.objects.create(name="Package 1", price=10)
        return self.package


    @pytest.fixture
    def url(self, package):
        return reverse(self.url_name, kwargs={'package_pk': package.pk})


    def test_get_succeeds(self, url, admin_client):
        response = admin_client.get(url)

        assert response.status_code == 200


    def test_post_update_succeeds(self, url, admin_client, package):
        # Define the new credits value
        data = {
            'action_credits': 927,
            'add_to_list_credits': 928,
            'export_credits': 929
        }

        # Make a POST request to update the data package benefits
        response = admin_client.post(url, data=data)

        # Assert the response status code is 302 (indicating a successful redirect)
        assert response.status_code == 302

        # Refresh the data package benefits object from the database
        package.datapackagebenefits.refresh_from_db()

        # Assert the credits value has been updated
        assert package.datapackagebenefits.action_credits == data['action_credits']
        assert package.datapackagebenefits.add_to_list_credits == data['add_to_list_credits']
        assert package.datapackagebenefits.export_credits == data['export_credits']
