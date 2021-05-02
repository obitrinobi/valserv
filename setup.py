from setuptools import find_packages, setup

setup(
    name="carla-service",
    version="0.0.1",
    install_requires=['Flask', 'Flask_restful', 'jsonpickle', 'pytest', 'mock'],
    extras_require=dict(test=['pytest']),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
