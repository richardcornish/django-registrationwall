from setuptools import setup


setup(
    name='django-paywall',
    version='0.1.0',
    description='A Django app to raise a paywall for content websites',
    long_description=open('README.md').read(),
    license='BSD License',
    author='Richard Cornish',
    author_email='rich@richardcornish.com',
    url='https://github.com/richardcornish/django-paywall',
    zip_safe=False,
    platforms=[
        'OS Independent'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=[
        'paywall',
        'paywall.tests'
    ],
    include_package_data=True,
    install_requires=[
        'django>=1.9'
    ],
)
