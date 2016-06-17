import pep8
import sys
import unittest
import os

from coverage import coverage, misc
from distutils import log
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


class SetupTestSuite(unittest.TestSuite):
    """
    Test Suite configuring Django settings and using
    DjangoTestSuiteRunner as test runner.
    Also runs PEP8 and Coverage checks.
    """
    def __init__(self, *args, **kwargs):
        self.configure()
        self.cov = coverage()
        self.cov.start()

        super(SetupTestSuite, self).__init__(*args, **kwargs)

        from django.conf import settings
        from django.test.utils import get_runner
        self.test_runner = get_runner(settings)()

    def configure(self):
        """
        Configures Django settings.
        """
        import django

        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
        django.setup()

    def coverage_report(self):
        """
        Outputs Coverage report to screen and coverage.xml.
        """
        verbose = '--quiet' not in sys.argv
        self.cov.stop()
        if verbose:
            log.info("\nCoverage Report:")
            try:
                include = ['embedded_media/*']
                omit = ['*tests*']
                self.cov.report(include=include, omit=omit)
                self.cov.xml_report(include=include, omit=omit)
            except misc.CoverageException as e:
                log.info("Coverage Exception: %s" % e)

    def pep8_report(self):
        """
        Outputs PEP8 report to screen and pep8.txt.
        """
        verbose = '--quiet' not in sys.argv
        if verbose:
            # Hook into stdout.
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()

            # Run Pep8 checks.
            pep8_style = pep8.StyleGuide(ignore=['E2', 'E3', 'E4', 'E501', 'W'])
            pep8_style.check_files(['embedded_media/media.py',
                                    'embedded_media/models.py'])

            # Restore stdout.
            sys.stdout = old_stdout

            # Save result to pep8.txt.
            result = mystdout.getvalue()
            output = open('pep8.txt', 'w')
            output.write(result)
            output.close()

            # Return Pep8 result
            if result:
                log.info("\nPEP8 Report:")
                log.info(result)

    def run(self, *args, **kwargs):
        """
        Run the test, teardown the environment and generate reports.
        """
        failures = self.test_runner.run_tests(["embedded_media"])
        self.coverage_report()
        self.pep8_report()
        return failures
