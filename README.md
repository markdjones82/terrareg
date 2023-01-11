# Terrareg

Open source Terraform Registry.

Provides features to aid usage and discovery of modules, providing:

 * Fully implemented Terraform modules API
 * Host Terraform modules internally or from an exteral Git source
 * Analytics about the usage of modules
 * All information about a module - README, inputs, outputs, provider requirements and managed resources
 * Security alerts for each module, submodule and examples
 * Cost estimation for each module example
 * Module example source code within the UI, with automatic rewriting of 'source' arguments
 * Interactive 'Usage builder', helping users build terraform to use the terraform modules
 * Hooks for git SCM applications to automatically index modules

If you like and use this project and are happy to let us know, please raise a Github issue, create a PR or contact [MatthewJohn](https://github.com/matthewjohn) so it can be added to the README :)

## Screenshots

![Homepage](./docs/screenshots/homepage.png)

![Search](./docs/screenshots/search.png)

![Module Provider](./docs/screenshots/module_provider.png)

![Example](./docs/screenshots/example.png)

## Getting started


    # Clone the repository
    git clone https://github.com/matthewJohn/terrareg
    cd terrareg

    # Builder docker image
    docker build . -t terrareg:latest

    # Create secret key for session data
    export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex())')

    # Run container, specifying secret key and admin password
    docker run -ti -p 5000:5000 -e MIGRATE_DATABASE=True -e SECRET_KEY=$SECRET_KEY -e ADMIN_AUTHENTICATION_TOKEN=MySuperSecretPassword terrareg:latest

The site can be accessed at http://localhost:5000, which will provide a 'Initial Setup' guide for getting started.

For information about running with docker-compose, SSL certificate generation or running without docker, see [docs/LOCAL_DEVELOPMENT.md](./docs/LOCAL_DEVELOPMENT.md).

## Upload a terraform module:

### From a git repo


* Goto http://localhost:5000
* Login, using the button in the top-right hand corner
* Goto Modules -> Create (http://localhost:5000/create-module)
* Fill in the details for your module and 'Create'
* Use the 'Manually index version' form of your module, filling out the verison and select 'Publish' and then press 'Index Version'

### From source

    terrareg_root=$PWD
    
    cd source/of/my/module
    
    # OPTIONAL: Create an terrareg meta-data file
    echo '{ "description": "My first module", "owner": "ME!", "source": "https://github.com/me/my-tf-module" }' > ./terrareg.json
    
    # Zip up module
    zip -r ../my-tf-module.zip *
    
    # Upload to terrareg
    bash $terrareg_root/scripts/upload_module.sh http://localhost:5000 helloworld my-tf-module aws 1.0.0 ../my-tf-module.zip

  Navigate to http://localhost:5000 to get started, or http://localhost/modules/helloworld/my-tf-module to see the uploaded example!


**NOTE:** To use modules from the registry in Terraform, a valid SSL certificate must be used. Terraform will not work if you supply `http://` as a protocol for the module URL, as it will treat this as a direct HTTP download, rather than treating it as a registry.

## Docker environment variables

The following environment variables are available to configure the docker container

### MIGRATE_DATABASE

Whether to perform a database migration on container startup.

Set to `True` to enable database migration

*Note:* Be very careful when scaling the application. There should never be more than one instance of Terrareg running with `MIGRATE_DATABASE` set to `True` during an upgrade.

When upgrading, scale the application to a single instance before upgrading to a newer version.

Alternatively, set `MIGRATE_DATABASE` to `False` and run a dedicated instance for performing database upgrades.
Use `MIGRATE_DATABASE_ONLY` to run an instance that will perform the necessary database migrations and immediately exit.

Default: `False`

### MIGRATE_DATABASE_ONLY

Whether to perform database migration and exit immediately.

This is useful for scheduling migrations by starting a 'migration' instance of the application.

Set to `True` to exit after migration.

The `MIGRATE_DATABASE` environment variable must also be set to `True` to perform the migration, otherwise nothing will be performed and the container will exit.

Default: `False`

### SSH_PRIVATE_KEY

Provide the contents of the SSH key to perform git clones.

This is an alternative to mounting the '.ssh' directory of the root user.

Default: ''

## Application environment variables

For a list of available application configuration environment variables, please see [docs/CONFIG.md](./docs/CONFIG.md)


## Terrareg module metadata

A metadata file can be provided each an uploaded module's archive to provide additional metadata to terrareg.

For an example, please see: [docs/example-terrareg-module-metadata.json](./docs/example-terrareg-module-metadata.json)

The following attributes are available at the root of the JSON object:

|Key |Description|
--- | --- |
|owner|Name of the owner of the module|
|description|Description of the module|
|variable_template|Structure holding required input variables for module, used for 'Usage Builder'. See table below|
|repo_clone_url|Url to clone the repository. Optional placeholders `{namespace}`, `{module}` and `{provider}` can be used. E.g. `ssh://gitlab.corporate.com/scm/{namespace}/{module}.git`|
|repo_base_url|Formatted base URL for project's repo. E.g. `https://gitlab.corporate.com/{namespace}/{module}`|
|repo_browse_url|Formatted URL for user-viewable source code. Must contain `{tag}` and `{path}` placeholders. E.g. `https://github.com/{namespace}/{module}-{provider}/blob/{tag}/{path}`|

### Usage builder configuration

The usage builder requires an array of objects, which define the name, type and description of the variable.

In the following the 'config input' refers to the HTML inputs that provide the user with the ability to select/enter values. The 'terraform input' refers to the value used for the variable in the outputted terraform example.

There are common attributes that can be added to each of variable objects, which include:

|Attribute |Description |Default|
--- | --- | ---|
|name|The name of the 'config input'. This is also used as the module variable in the 'terraform input'.|Required|
|type|The type of the input variable, see table below.|Required|
|required|Boolean flag to determine whether the variable is Required.|`true`|
|quote_value|Boolean flag to determine whether the value generated is quoted for the 'terraform input'.|`false`|
|additional_help|A description that is provided, along with the terraform variable description in the usage builder|`""`|
|default_value|The default value if required is false|`null`|



|Variable type|Description|Type specific attributes|
--- | --- | ---|
|text|A plain input text box for users to provide a value that it directly used as the 'terraform input'||
|boolean|Provides a checkbox that results in a true/false value as the 'terraform input'||
|static|This does not appear in the 'Usage Builder' 'config input' table, but provides a static value in the 'terraform input'||
|select|Provides a dropdown for the user to select from a list of choices|"choices" must be added to the object, which may either be a list of strings, or a list of objects. If using a list of objects, a "name" and "value" must be provided. Optionally an "additional_content" attribute can be added to the choice, which provides additional terraform to be added to the top of the terraform example. The main variable object may also contain a "allow_custom" boolean attribute, which allows the user to enter a custom text input.|

## Single Sign-On

For information about setting up Single Sign-on, please see [docs/SSO.md](./docs/SSO.md)

## Changelog

See [CHANGELOG.md](CHANGELOG.md)


## Local development

Since terraform requires HTTPS with a valid SSL cert, this must be provided in local development

On linux, by default, non-privileged users cannot listen on privileged ports, so the following can be used to route requests locally to port 5000:

```
sudo iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 443 -j REDIRECT --to-ports 5000
```

Example to run in local development environment:
```
virtualenv -ppython3.8 venv
. venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Without SSL cert
ALLOW_CUSTOM_GIT_URL_MODULE_PROVIDER=False ALLOW_CUSTOM_GIT_URL_MODULE_VERSION=False GIT_PROVIDER_CONFIG='[{"name": "Github", "base_url": "https://github.com/{namespace}/{module}", "clone_url": "ssh://git@github.com:{namespace}/{module}.git", "browse_url": "https://github.com/{namespace}/{module}/tree/{tag}/{path}"}, {"name": "Bitbucket", "base_url": "https://bitbucket.org/{namespace}/{module}", "clone_url": "ssh://git@bitbucket.org:{namespace}/{module}-{provider}.git", "browse_url": "https://bitbucket.org/{namespace}/{module}-{provider}/src/{tag}/{path}"}, {"name": "Gitlab", "base_url": "https://gitlab.com/{namespace}/{module}", "clone_url": "ssh://git@gitlab.com:{namespace}/{module}-{provider}.git", "browse_url": "https://gitlab.com/{namespace}/{module}-{provider}/-/tree/{tag}/{path}"}]' SECRET_KEY=ec9b8cc5ed0404acb3983b7836844d828728c22c28ecbed9095edef9b7489e85 ADMIN_AUTHENTICATION_TOKEN=password ANALYTICS_AUTH_KEYS=xxxxxx.atlasv1.zzzzzzzzzzzzz:dev,xxxxxx.atlasv1.xxxxxxxxxx:prod VERIFIED_MODULE_NAMESPACES=hashicorp TRUSTED_NAMESPACES=test DEBUG=True AUTO_PUBLISH_MODULE_VERSIONS=False LISTEN_PORT=5001 python ./terrareg.py

# With SSL Cert
# Add the following argument
#  --ssl-cert-private-key ./example/ssl-certs/private.pem --ssl-cert-public-key ./example/ssl-certs/public.pem

```

## Generating DB changes

```
alembic revision --autogenerate
```

## Applying DB changes

```
alembic upgrade head
```

## Running tests

```
# Run all tests
pytest

# Running unit/integration/selenium tests individually
pytest ./test/unit
pytest ./test/integration
pytest ./test/selenium

# Running a specific test
pytest -k test_setup_page
```

# License

This project and all associated code is covered by GNU General Public License v3.0.

For full license, see [LICENSE](LICENSE)

# Contributors

 * Matt Comben <matthew@dockstudios.co.uk>

## Special thanks

 *  David Soff <david@soff.nl> for implementing Github hook support

