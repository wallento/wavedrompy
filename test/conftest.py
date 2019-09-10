import os

collect_ignore = ["single_test.py"]
def pytest_report_header(config):
    if "WAVEDROMDIR" in os.environ:
        print("Using wavedrom in WAVEDROMDIR ({})".format(os.environ["WAVEDROMDIR"]))