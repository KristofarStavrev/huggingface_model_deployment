import nox


@nox.session
def security_scan(session):
    """Run Bandit security checks."""
    session.run("poetry", "run", "bandit", "-r", "src", external=True)


@nox.session
def dependency_security_scan(session):
    """Run security checks with pip-audit which checks dependencies against the Python Packaging Advisory Database."""
    session.run("poetry", "run", "pip-audit", external=True)


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
