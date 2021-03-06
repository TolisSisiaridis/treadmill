from treadmill.infra.setup import base_provision
from treadmill.infra import configuration, constants


class Master(base_provision.BaseProvision):
    def setup(
            self,
            image,
            count,
            cidr_block,
            ldap_hostname,
            tm_release,
            key,
            instance_type,
            app_root,
            ipa_admin_password,
            subnet_id=None,
    ):
        self.configuration = configuration.Master(
            name=self.name,
            subnet_id=subnet_id,
            ldap_hostname=ldap_hostname,
            tm_release=tm_release,
            app_root=app_root,
            ipa_admin_password=ipa_admin_password
        )
        self.subnet_name = constants.TREADMILL_CELL_SUBNET_NAME
        super().setup(
            image=image,
            count=count,
            cidr_block=cidr_block,
            subnet_id=subnet_id,
            key=key,
            instance_type=instance_type
        )
