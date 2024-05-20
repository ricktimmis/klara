# TODO 
Work items that need addressing

## Packaging
To package a Python application for other users, particularly for Linux, you might want to consider creating a distribution package. There are several ways to do this, but here is a brief explanation of how to do it using setuptools and wheel, and then creating a debian package:

 - Step 1: Prepare your Python application

Make sure the main functionality of your Python application can be triggered from a main file, e.g., main.py
Clean up and organize your project. Here is a typical project organization:

    Project/
       |-- your_package/
           |-- __init__.py
           |-- other_module.py
       |-- setup.py
       |-- setup.cfg
       |-- README.md
       |-- LICENSE.txt
       |-- main_script.sh

 - Step 2: Set up setuptools and create a distribution package
   - Install the necessary tools by running: 
 ```pip install setuptools wheel```
   - Create a setup.py file in your project directory and provide details about your project. 
  
 Below is a very basic example:

```python
    from setuptools import setup
    
    setup(
    name="Your-Application-Name",
    version="0.1",
    packages=["your_package"],
    entry_points={
    'console_scripts': [
    'your_command = your_package:main',
    ],
    },
    description="A short description about your project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    url="http://example.com/Your_Application_name/",
    author="Your Name",
    author_email="your_email@example.com",
    python_requires='>=3.6',
    )
```
- Once your `setup.py` is ready, you can create a distribution package with: 

```python setup.py sdist bdist_wheel``` 

This will create a `dist` directory with the distribution packages. 

- Step 3: Create a Debian Package
  - Install the required tools:
  
```sudo apt-get install python3-stdeb```

Run the following command:

```python3 setup.py --command-packages=stdeb.command bdist_deb```

This will create a .deb file in the deb_dist directory. This is your debian package.


Users can install your application using dpkg: sudo dpkg -i your-package.deb
Please keep in mind this is a very simplified overview and there are many options you can use in the setup.py file to customize the building of your distribution package according to your needs. For a very detailed guide, you should really look into the official
- 
https://packaging.python.org/en/latest/tutorials/packaging-projects/