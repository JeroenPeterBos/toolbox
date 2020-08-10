from unittest import TestCase
from pathlib import Path
import os
import re


class ToolboxTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test environment. Written by Marco Rietveld"""
        TestCase.setUpClass()

        # base dir
        src_path_regex = "src/(main|unittest|integrationtest)/python.*"
        cwd_base = os.getcwd()
        if "/src/".format(sep=os.sep) in cwd_base:  # noqa F522
            cwd_base = re.sub(src_path_regex, "", cwd_base)

        if cwd_base[-1] == os.sep:
            cwd_base = cwd_base[:-1]

        cls.project_base_dir = Path(cwd_base)
        cls.test_data_dir = Path(os.path.join(cls.project_base_dir, 'src', 'unittest', 'data'))
