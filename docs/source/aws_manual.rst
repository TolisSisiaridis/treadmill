Treadmill on AWS
==========================================================

Clone the treadmill repo and start the vagrant box:
::

  cd treadmill/vagrant
  vagrant up master

SSH in the vagrant machine:
::

  vagrant ssh master

Check treadmill exist:
::

  treadmill --help

----------------------------------------------------------

Set AWS Credentials and Region
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Assuming a user is present on AWS Account having AmazonEC2FullAccess, AmazonVPCFullAccess and AmazonRoute53FullAccess, there are two ways to set the credentials and region:

Either export them:

::

  export AWS_ACCESS_KEY_ID=<Access Key ID>
  export AWS_SECRET_ACCESS_KEY=<Secret Access Key>
  export AWS_DEFAULT_REGION=<aws_region>

Or create a credentials file ``~/.aws/credentials`` with following content:

::

  [default]
  aws_access_key_id=<access_key_id>
  aws_secret_access_key=<secret_access_key>
  region=us-east-1

----------------------------------------------------------

List treadmill AWS commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  treadmill cloud --help

----------------------------------------------------------

List VPC
^^^^^^^^
::

  treadmill cloud --domain <domain> list vpc --vpc-name <vpc_name>

This lists all the EC2 instances and subnets inside the vpc.

List Cell
^^^^^^^^^
::

  treadmill cloud --domain <domain> list cell --subnet-id <subnet_id>

This lists all the EC2 instances running inside a cell.

-----------------------------------------------------------

Initialize VPC
^^^^^^^^^^^^^^

::

  treadmill cloud --domain <domain> init vpc --name <vpc_name>

This creates a VPC, Internet Gateway, Security Group and Route53 Hosted Zone. Default values are used to create these resources. The values can be overwritten from command line.

List the options:

::

  treadmill cloud init --help


Initialize Domain
^^^^^^^^^^^^^^^^^

::

  treadmill cloud --domain <domain> init domain --vpc-name <vpc_name> --key <key_name> --image <image_name> --ipa-admin-password <password>

ipa-admin-password should be at least 8 characters long.

Other values can be overwritten if required.

This will spin up IPA Server.


Initialize Cell
^^^^^^^^^^^^^^^

::

  treadmill cloud --domain <domain> init cell --vpc-name <vpc_name> --key <key_name> --image <image_name>

This will setup 1 openldap, 3 masters and 3 zookeeper instances by default.

At this point all the hosts will be registered with IPA server.


SpinUp First Node
^^^^^^^^^^^^^^^^^

::

  treadmill cloud --domain <domain> init node --vpc-name <vpc_name> --key <key_name> --image <image_name> --subnet-id <subnet-id>
