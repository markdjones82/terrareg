
from terrareg.server.error_catching_resource import ErrorCatchingResource
from terrareg.models import Example


class ApiTerraregExampleDetails(ErrorCatchingResource):
    """Interface to obtain example details."""

    def _get(self, namespace, name, provider, version, example):
        """Return details of example."""
        _, _, _, module_version, error = self.get_module_version_by_name(namespace, name, provider, version)
        if error:
            return error

        example_obj = Example.get(module_version=module_version, module_path=example)

        return example_obj.get_terrareg_api_details()
