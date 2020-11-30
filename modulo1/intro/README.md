

# Creating Virtual Environments

There are three ways to install environments
conda, pipenv, virtualenv.

[Pipenv, virtualenv, conda](https://medium.com/@krishnaregmi/pipenv-vs-virtualenv-vs-conda-environment-3dde3f6869ed)

[more](https://stackoverflow.com/questions/51042589/conda-version-pip-install-r-requirements-txt-target-lib/51043636)


## Using conda


To create an environment call this command: <span style="color:red">(Don't do it)</span>.
```
conda create --name environment_name python=3.6
```
I our case we set the name as intro <span style="color:red">(Don't do it)</span>.
```
conda create --name intro python=3.6
```
You can save all the info necessary to recreate the environment in a file by calling <span style="color:red">(Don't do it)</span>.

```
conda env export > environment.yml 
```
To recreate the environment you can do the following: <span style="color:cyan">(Do it)</span>.

```
conda env create -f environment.yml
```





# Install python plugins to VSCode

pylance

## Testing

There are two popular tools for testing: [unittest](https://docs.python.org/3/library/unittest.html) and [pytest](https://docs.pytest.org/en/latest/getting-started.html). In this example we only use unittest, the way how execute is described bellow. Pytest wont be used this time, but there will be a documentation linked above if you know more about it.


[guide for more info](https://docs.python-guide.org/writing/tests/)

```
python -m unittest basics_test.py
```
For more detailes <span style="color:cyan">(recommended)</span>.
```
python -m unittest -v basics_test.py
```

For a list of all the command-line options
```
python -m unittest -h
```


## Exercise 

Write a function which return the factorial of number.