package ai.aeos;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class CucumberSteps {
    private boolean runnerInstalled;

    @Given("the AEOS JVM BDD runner is installed by Gradle")
    public void runnerIsInstalled() {
        runnerInstalled = true;
    }

    @Then("the Gradle Cucumber smoke scenario passes")
    public void scenarioPasses() {
        assertTrue(runnerInstalled);
    }
}
