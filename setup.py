from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-suit5',
    version=__import__('suit5').VERSION,
    description='Modern theme for Django admin interface built with Bootstrap 5.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Naved Rangwala (navedr)',
    author_email='info@djangosuit.com',
    url='http://djangosuit.com',
    packages=['suit5', 'suit5.templatetags'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ]
)
