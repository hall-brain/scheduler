from setuptools import setup, find_packages

with open('./requirements.txt', 'r') as f:
    req = f.readlines()


setup(
    name='scheduler',
    author='HallBregg',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    scripts=['src/scheduler/scherunner'],
    install_requires=req,
    python_requires='>=3.8',
)
