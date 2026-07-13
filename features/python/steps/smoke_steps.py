from behave import given, then


@given("the AEOS Python BDD runner is installed")
def step_python_bdd_installed(context):
    context.python_bdd_installed = True


@then("the Python BDD smoke scenario passes")
def step_python_bdd_passes(context):
    assert context.python_bdd_installed is True
