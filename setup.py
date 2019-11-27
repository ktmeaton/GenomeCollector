import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as r:
    require_list = r.read().strip().split("\n")

setuptools.setup(
   name='NCBImeta',
   version='0.4.1',
   description='Efficient and comprehensive metadata acquisition from the NCBI databases (includes SRA).',
   python_requires='>=3',
   license="MIT",
   long_description=long_description,
   author='Katherine Eaton',
   author_email='ktmeaton@gmail.com',
   url="https://github.com/ktmeaton/NCBImeta",
   #packages=setuptools.find_packages(),
   packages=['ncbimeta'],
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
   ],
   install_requires=require_list, #external packages as dependencies
   scripts=[
      'ncbimeta/NCBImeta.py',
      'ncbimeta/NCBImetaExport.py',
      'ncbimeta/NCBImetaJoin.py',
      'ncbimeta/NCBImetaAnnotateReplace.py',
      'ncbimeta/NCBImetaAnnotateConcatenate.py']
)