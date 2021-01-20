from setuptools import setup, find_packages

setup(
    name = 'pydeck_h3',
    version = '0.0.1',
    description = 'Utils for working with H3 cells and Pydeck',
    author = 'AJ Friend',
    author_email = 'ajfriend@gmail.com',
    packages = find_packages(
        'src',
        exclude = ["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    package_dir = {'': 'src'},

    install_requires = ['pydeck','h3', 'pandas', 'toolz', 'matplotlib'],

    # extras_require={
    #     'numpy': ['numpy'],
    #     'test': ['pytest', 'pytest-cov', 'flake8'],
    #     'all': ['numpy', 'pytest', 'pytest-cov', 'flake8'],
    # },
)
