const assert = require("node:assert/strict");
const { Given, Then } = require("@cucumber/cucumber");

let installed = false;

Given("the AEOS JavaScript test runner is installed", function () {
  installed = true;
});

Then("the JavaScript Cucumber smoke scenario passes", function () {
  assert.equal(installed, true);
});
