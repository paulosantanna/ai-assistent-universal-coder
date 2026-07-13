package ai.aeos;

import static org.junit.jupiter.api.Assertions.assertTrue;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;

public class CucumberSteps {
    private boolean configured;

    @Given("the AEOS Java test runner is configured")
    public void javaRunnerConfigured() {
        configured = true;
    }

    @Then("the Java Cucumber smoke scenario passes")
    public void javaCucumberSmokePasses() {
        assertTrue(configured);
    }
}
