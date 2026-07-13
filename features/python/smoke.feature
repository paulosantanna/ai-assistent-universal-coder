Feature: AEOS Python BDD smoke

  Scenario: Python behave runner is configured
    Given the AEOS Python BDD runner is installed
    Then the Python BDD smoke scenario passes
