Feature: AEOS Gradle JVM BDD smoke

  Scenario: Gradle Cucumber JVM runner is configured
    Given the AEOS JVM BDD runner is installed by Gradle
    Then the Gradle Cucumber smoke scenario passes
