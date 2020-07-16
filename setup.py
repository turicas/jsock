import setuptools

with open("README.md", "r") as fobj:
    long_description = fobj.read()


setuptools.setup(
    name="jsock",
    version="0.1.0",
    author="Álvaro Justen",
    author_email="alvarojusten@gmail.com",
    description="Key-value-based, HMAC-signed, non-blocking sockets for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/turicas/jsock",
    py_modules=["jsock"],
    install_requires=["simplejson"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
