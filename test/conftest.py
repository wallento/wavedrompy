import os

def pytest_report_header(config):
    if "WAVEDROMDIR" in os.environ:
        print("Using wavedrom in WAVEDROMDIR ({})".format(os.environ["WAVEDROMDIR"]))