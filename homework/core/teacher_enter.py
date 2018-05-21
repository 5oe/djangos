#!/usr/bin/env python
# coding=utf-8
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from lib import bin
from modules.schoool import School
from modules.teacher import Teacher
from modules.subject import Subject
from modules.classes import Class


def techaer_view():
    pass