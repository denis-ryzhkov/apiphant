from distutils.core import setup

setup(
    name='apiphant',
    version='0.1.0',
    description='Simple Python Web API framework, based on Gevent, JSON, CRUD.',
    long_description='''
Please read complete description here:

https://github.com/denis-ryzhkov/apiphant/blob/master/README.md
''', # TODO: Update this rST from source MD. Maybe find autoconverter.
    url='https://github.com/denis-ryzhkov/apiphant',
    author='Denis Ryzhkov',
    author_email='denisr@denisr.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['apiphant'],
    scripts=['scripts/apiphant'],
    install_requires=[
        'adict',
        'gevent',
    ],
)
