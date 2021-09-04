import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='paparse',
    version='0.1.0a1',
    license='',
    description='Python utility for creating configs from settings files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wulu473/paparse',
    author='Lukas Wutschitz',
    packages=['paparse'],
    package_dir={'': 'src'},
    python_requires='>=3.9.0',
    include_package_data=True,
    install_requires=[
        'multimethod',
        'seval',
        'pyyaml'
    ],
    scripts=[],
    test_suite="tests",
    zip_safe=False)
