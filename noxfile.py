import nox
import subprocess
import sys


@nox.session
def security_scan(session):
    """Run Bandit security checks."""
    session.run("poetry", "run", "bandit", "-r", "src", external=True)


@nox.session
def dependency_security_scan(session):
    """Run security checks with pip-audit which checks dependencies against the Python Packaging Advisory Database."""
    #session.run("poetry", "run", "pip-audit", external=True)

    # Run pip-audit using poetry
    result = subprocess.run(
        ["poetry", "run", "pip-audit"],
        capture_output=True,
        text=True
    )

    # Split the result into lines
    lines = result.stdout.splitlines()

    # Add any keywords that should be excluded from the checks below
    # First two are pytorch and the thrid is h11
    excl_list = ["GHSA-3749-ghw9-m3mg", "GHSA-887c-mr87-cxwp", "GHSA-vqfr-h8mv-ghfj", "GHSA-fpwr-67px-3qhx", "GHSA-8jw3-6x8j-v96g",
                 "GHSA-5rjg-fvgr-3xxf", "PYSEC-2025-40", "GHSA-wmjh-cpqj-4v6x", "GHSA-9hjg-9r4m-mvj7", "PYSEC-2025-49"]

    # Filter out lines that contain any of the excluded libraries
    potential_fix = [line for line in lines if not any(word.lower() in line.lower() for word in excl_list)]
    no_fix = [line for line in lines if any(word.lower() in line.lower() for word in excl_list)]

    # Add headers to the output
    no_fix = ['Name  Version ID                  Fix Versions', '----- ------- ------------------- ------------', *no_fix]

    if len(lines) <= 2:
        print("No vulnerabilities found.")
    else:
        if len(potential_fix) > 2:
            print("Vulnerabilities with a potential fix found:")
            for line in potential_fix:
                print(line)
            print("")
            sys.exit(1)

        if len(no_fix) > 2:
            print("Vulnerabilities without a known fix found:")
            for line in no_fix:
                print(line)


@nox.session
def pytest_scan(session):
    """Run all Pytest unit and integration tests"""
    session.run("poetry", "run", "pytest", "tests/", external=True)


@nox.session
def mypy_type_checking(session):
    """Run MyPy static type checking."""
    session.run("poetry", "run", "mypy", "src/", external=True)


@nox.session
def code_linting(session):
    """Run all code linting checks."""
    session.run("poetry", "run", "ruff", "check", "src", external=True)
    session.run("poetry", "run", "ruff", "check", "tests", external=True)
