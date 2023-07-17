from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'flownet-ai',
    version = '0.0.1',
    author = 'Shashank',
    author_email = 'savvy.shashank@gmail.com',
    license = 'MIT',
    description = 'CLI tool to pick AI tasks from blockchain and perform them',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = '<github url where the tool code will remain>',
    py_modules = ['main', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        flownetai=main:cli
    '''
)