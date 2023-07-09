from .nira import Nira,NiraTest
from .ursb import URSBClient
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = os.getenv("DEBUG")

if DEBUG:
    nira = NiraTest()
else:
    nira = Nira()
    ursb = URSBClient()