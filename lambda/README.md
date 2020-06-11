# shelfCheck lambdas

Here are the lambda functions we are running as the shelfCheck backend

In addition to storing lambda functions, you may build them using the build script (usage below). The testing features has not yet been developed.

### Configure the lambda

Every lambda must have a handler.py file with a function lambda_handler. The lambda_handler function is what runs when the lambda is called. Additionally every lambda must have a config.py file that has three variables

```python
pip_dependencies = []
confidential_dependencies = []
shelfcheck_dependencies = []
```

If the lambda uses any pip packages, add them to the list as a string. They can be imported in the lambda normally. If the lambda uses any keys, add 'mapbox', 'aws' or 'mongo' to the confidential_dependencies list. These keys can be accessed within the lambda as shown below.

```python
import confidential

confidential.MAPBOX
confidential.AWS
confidential.MONGO
```

Finally if the lambda uses prop.py or shopper.so, add either 'prop' or shopper.so to the shelfcheck_dependencies list. These can be imported as so.

```python
import prop
import shopper
```

### Building a zipped lambda

To build a lambda, run the following command, where LAMBDA-NAME is the name of the lambda you are building

`python3 build.py LAMBDA-NAME`

A zip archive called LAMBDA-NAME-target.zip will be created. This can be directly uploaded to AWS Lambda.