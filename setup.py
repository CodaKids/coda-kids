"""setup file for coda-kids, a partial wrapper package for pygame."""
import setuptools

def readme():
    with open('README.rst') as file:
        return file.read()

setuptools.setup(name='coda_kids',
                 version='0.1',
                 description='Partial pygame wrapper and game programming framework.',
                 long_description=readme(),
                 classifiers=[
                     'Development Status :: 2 - Pre-Alpha',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python :: 3',
                     'Intended Audience :: Education'
                 ],
                 url='https://github.com/ADillon1/coda-kids',
                 author='Andrew Dillon',
                 author_email='AndrewDillon91@gmail.com',
                 license='MIT',
                 packages=['coda_Kids'],
                 install_requires=['pygame'],
                 include_package_data=True,
                 zip_safe=False)
