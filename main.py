import pytest


def run_tests():
    """
    Pytest exit codes:
      EXIT_OK = 0
      EXIT_TESTSFAILED = 1
      EXIT_INTERRUPTED = 2
      EXIT_INTERNALERROR = 3
      EXIT_USAGEERROR = 4
      EXIT_NOTESTSCOLLECTED = 5
    """
    exit_code = pytest.main([
        './tests',
        # '--junitxml', './nosetests.xml',
        '--html', 'report.html',
        '--self-contained-html'
        # '--sm', 'config'
    ])

    if exit_code not in (0, 1,):
        exit(1)


if __name__ == '__main__':
    run_tests()
