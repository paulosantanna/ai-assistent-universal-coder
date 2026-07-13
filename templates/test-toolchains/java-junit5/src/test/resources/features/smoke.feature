Feature: AEOS Java Cucumber smoke

  Scenario: Java Cucumber runner is configured
    Given the AEOS Java test runner is configured
    Then the Java Cucumber smoke scenario passes
