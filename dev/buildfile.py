"""
buildfile.py

Running this file will build PyActy locally so that it can be tested properly before being uploading to PyPi.
All files used for this type of testing should be contained inside /dev/.
"""
import os

os.chdir("..")
os.system("pip install .")
