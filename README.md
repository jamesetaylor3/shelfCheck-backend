# shelfCheck lambdas

Here are the lambda functions we are running as the shelfCheck backend

Currently this package simply stores the lambda functions source code. However, it will have the ability to test and build lambda functions in the future based on the config files by installing locally the correct dependencies and giving access to keys. As of right now, you must do manual installation.

Each of the handler.py files are missing a constant atlas_mondb_endpoint that specifies the mongodb endpoint. This will be automatically created when building and testing functionality is implemented.

Each each config.py file, the dependencies list is a list of strings of the pip packages that need to be installed locally for a lambda. uses_mongo (bool) indicates that the function needs access to mongodb, and uses_prop (bool) indicates that it uses the /src/prop.py file

The build.py and test.py are empty but will be created later