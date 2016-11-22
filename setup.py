from distutils.core import setup
from pip.req import parse_requirements

setup(
    name='django-traffic',
    packages=['django_traffic'],
    version='1.2.2',
    description='Django middleware that helps visualize your app\'s traffic in Kibana',
    author='Konstantinos Livieratos',
    author_email='livieratos.konstantinos@gmail.com',
    install_requires=parse_requirements('requirements.txt'),
    url='https://github.com/koslibpro/django-traffic',
    download_url='https://github.com/koslibpro/django-traffic/tarball/1.2.2',
    keywords=['django', 'kibana', 'elasticsearch', 'traffic'],
    classifiers=[],
)
