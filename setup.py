from setuptools import setup

setup(name='graphene-mongoengine',
      version='0.1',
      description='Adding graphene support for mongoengine Models, inspired in Django',
      url='https://github.com/tomasgarzon/graphene-mongoengine',
      author='Tomas Garzon',
      author_email='tomasgarzonhervas@gmail.com',
      license='MIT',
      packages=['graphene_mongoengine'],
      install_requires=[
          'mongoengine',
          'graphene',
          'django',
          'graphql_relay',
          'graphene_django'
      ],
      zip_safe=False)
