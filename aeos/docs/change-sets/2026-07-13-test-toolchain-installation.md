# Change Set: Test Toolchain Installation

Date: 2026-07-13
Scope: Python, Node.js, BDD, Robot Framework, Maven, Gradle, JDK, Java test templates, AEOS test matrix

## Objective

Install and configure the project test toolchain for immediate validation across Python, Node.js, and Java, with reusable Maven and Gradle templates for JUnit 5 and Cucumber-JVM.

## Installed Runtime Tooling

Python tools were installed into `/tmp/aeos-venv`:

- pytest 9.1.1
- pytest-cov 7.1.0
- pytest-timeout 2.4.0
- pytest-asyncio 1.4.0
- pytest-xdist 3.8.0
- hypothesis 6.156.6
- behave 1.3.3
- robotframework 7.4.2
- coverage 7.15.1
- PyYAML 6.0.3

Local Python packages were installed in editable mode into `/tmp/aeos-venv`:

- continuous-training-mcp
- medical-research-mcp
- complete-docs-mcp
- language-docs-mcp
- universal-project-mcp
- aeos-lsp

Node.js dev dependencies were installed into the root project:

- jest
- vitest
- mocha
- @cucumber/cucumber
- c8
- tsx
- typescript
- @types/node
- @types/jest

Java tooling was installed locally under `.tools`:

- Apache Maven 3.9.11
- Gradle 9.2.1
- Eclipse Temurin JDK 17.0.19+10

The tracked wrappers are:

- `.tools/bin/mvn`
- `.tools/bin/gradle`

The large downloaded tool distributions under `.tools` are intentionally ignored by git. The wrappers configure:

- local JDK through `JAVA_HOME=.tools/jdk-17.0.19+10`
- Maven local repository at `/tmp/aeos-m2`
- Gradle user home at `/tmp/aeos-gradle`
- Java proxy properties from the current `HTTP_PROXY`/`HTTPS_PROXY`
- local Java truststore at `.tools/aeos-java-truststore.p12`

## Host Limitations

The host still does not provide global `go`, `cargo`, or `dotnet`; those optional matrix entries are skipped when `--include-optional` is used.

## Files Added Or Updated

- `.npmrc`
- `.gitignore`
- `requirements-dev.txt`
- `package.json`
- `package-lock.json`
- `behave.ini`
- `jest.config.cjs`
- `vitest.config.ts`
- `cucumber.js`
- `.tools/bin/mvn`
- `.tools/bin/gradle`
- `aeos/config/maven-settings.xml`
- `aeos/config/test-toolchain.config.yaml`
- `aeos/scripts/test_matrix.py`
- `tests/node/smoke.test.cjs`
- `features/js/smoke.feature`
- `features/js/step_definitions/smoke.steps.cjs`
- `features/python/smoke.feature`
- `features/python/steps/smoke_steps.py`
- `tests/robot/smoke.robot`
- `templates/test-toolchains/java-junit5/pom.xml`
- `templates/test-toolchains/java-junit5/src/test/java/ai/aeos/SmokeTest.java`
- `templates/test-toolchains/java-junit5/src/test/java/ai/aeos/CucumberSteps.java`
- `templates/test-toolchains/java-junit5/src/test/java/ai/aeos/RunCucumberTest.java`
- `templates/test-toolchains/java-junit5/src/test/resources/features/smoke.feature`
- `templates/test-toolchains/java-gradle-junit5/settings.gradle.kts`
- `templates/test-toolchains/java-gradle-junit5/build.gradle.kts`
- `templates/test-toolchains/java-gradle-junit5/src/test/java/ai/aeos/SmokeTest.java`
- `templates/test-toolchains/java-gradle-junit5/src/test/java/ai/aeos/CucumberSteps.java`
- `templates/test-toolchains/java-gradle-junit5/src/test/java/ai/aeos/RunCucumberTest.java`
- `templates/test-toolchains/java-gradle-junit5/src/test/resources/features/smoke.feature`

## NPM Scripts Added

- `test:python`
- `test:python:cov`
- `test:python:bdd`
- `test:robot`
- `test:node:jest`
- `test:node:vitest`
- `test:node:mocha`
- `test:node:cucumber`
- `test:java:maven`
- `test:java:gradle`
- `test:java`
- `test:matrix`
- `test:matrix:full`
- `test:all`

The existing AEOS verification scripts now call `/tmp/aeos-venv/bin/python` explicitly.

## Validation

Executed successfully:

```bash
/tmp/aeos-venv/bin/python aeos/scripts/verify.py --suite full --python /tmp/aeos-venv/bin/python
npm run test:matrix
npm run test:java
npm run test:matrix -- --include-optional
```

Validation result:

- AEOS doctor: PASS
- AEOS registry: PASS
- AEOS performance benchmark: PASS
- AEOS core tests: 438 passed
- AEOS skills tests: 13 passed
- AEOS MCP tests: 69 passed, 1 skipped
- AEOS universal project MCP tests: 8 passed
- AEOS LSP tests: 518 passed
- AEOS LSP doctor: PASS
- AEOS LSP validate: PASS
- AEOS LSP index: PASS
- AEOS runtime build: PASS
- Python Behave smoke: PASS
- Robot Framework smoke: PASS
- Jest smoke: PASS
- Vitest smoke: PASS
- Mocha smoke: PASS
- Cucumber.js smoke: PASS
- Maven JUnit 5 + Cucumber-JVM template: PASS
- Gradle JUnit 5 + Cucumber-JVM template: PASS
- Full matrix optional Java entries: PASS
- Optional Go/Rust/.NET entries: SKIP, host tools missing

## File Hashes

```text
463e0bd1b4fb0aecd91ad8737819efc691ca801056103fdaf69eac27bfa1f155  .npmrc
34f26e5a082cabb45b2040e761094c80fe9570a860ee2806e4c68f5608252f87  .gitignore
9d3019c10396c1717fff2b0bb6162621a352843919d081b046ed3cdf8ff6ac17  requirements-dev.txt
8625213f071b9c63ff904a060db61bae6f1eebe48eeea67ef5dcfe91544e503e  package.json
826192901e236a5b96a1b909d220c0e52975faead71a72b060fbeac9b40e214a  package-lock.json
97ace3da21588f909c4b5690dcc408cc7adf4b6e577524b4dc83d60cc33bca2b  behave.ini
92db712095c677afa2b2b1db8a1b819de0a76e17eadfd8682bc705c2b1585687  jest.config.cjs
5eff1a5e367bd9baaab01c24fc7177046479284980aa3c3ea01c9d36db6795c1  vitest.config.ts
1eca89ce73fe271cc5ff479e26b1a84303ce92a39f9677534b7cdc2e7b2eef1b  cucumber.js
79caad45305a5d133975da7a59f43f0816f47620ddc73450026c0836d08f01ed  .tools/bin/mvn
3b44b9ea543eddf91e423dce550c47ed4dbaddeb58603a7846e56b32d32ef70f  .tools/bin/gradle
681a731e2ae6be419a57f81da2f0fa8a2bb6d8e708dfa404b4aae73823e66985  aeos/config/test-toolchain.config.yaml
0193bedd74c71b53ddfef0952f6f4cfacd61ed9e184f500010fbd19344d0c4f7  aeos/config/maven-settings.xml
c74421b7b274cece02f5636f18dc9558ca0d25c1a93884ba733fcf9f299f0641  aeos/scripts/test_matrix.py
4eca52c32e873d640d09500099f52e94aaaebcae9d0fd725b252818b62e7b3fd  tests/node/smoke.test.cjs
b9f76034afcd649436947b537bd476653ad1c0c6aa9bba52953e15f6715b11d8  features/js/smoke.feature
c8a8cf3498599b83e08ca88fcede6c5f64b75d9869243d15b9530a05fde482d3  features/js/step_definitions/smoke.steps.cjs
5a26d3a313d9a37db56ff21ce9351f64eafeaeaa057b1ecd531ce4f31008eb3a  features/python/smoke.feature
8d920e73ffb45a29f3313b65f949472295b9f0d6ead405002f76b172f01854bf  features/python/steps/smoke_steps.py
f74c1c8423a4a2e06e0117d8ec04ef766d7ed378becde0e163e4ddbedaf49170  tests/robot/smoke.robot
fbff149856017a72973153d4c1db1ddffb30289bc5381f64e8eae57130820920  templates/test-toolchains/java-junit5/pom.xml
e91763e46e289a2e6c81cd5d026581c027b862e706eb7869c2fc4316b11adc9c  templates/test-toolchains/java-junit5/src/test/java/ai/aeos/SmokeTest.java
4693bf80d0e4f6882351c81072b479185e749ae49c7abc0ebec54b6a5a82fba9  templates/test-toolchains/java-junit5/src/test/java/ai/aeos/CucumberSteps.java
db8338a8b9093ad9fb5cef1639efcf37d06db5576fff2ab7dd7ed4a6e8841653  templates/test-toolchains/java-junit5/src/test/java/ai/aeos/RunCucumberTest.java
2a2ef4696ad2eecb351437a0d339456325f7a1a37dc313c0af8ffd0556315f27  templates/test-toolchains/java-junit5/src/test/resources/features/smoke.feature
b830a655660acfa574e317a17b20d1770de113c03443bc6143a01c3f73017fd0  templates/test-toolchains/java-gradle-junit5/settings.gradle.kts
9368167fa39c46eac7d672bd8839024f92485f5e24d16fc2896dd1ffe80b0bb4  templates/test-toolchains/java-gradle-junit5/build.gradle.kts
02ca1569563c5511a8c6911357661ed189dffb88c8259b1ae24f4d1753c34b65  templates/test-toolchains/java-gradle-junit5/src/test/java/ai/aeos/SmokeTest.java
fa3392202a7dc294078ecb57dadd6605d725394a71c7535ab6452ec050ee6d0d  templates/test-toolchains/java-gradle-junit5/src/test/java/ai/aeos/CucumberSteps.java
db8338a8b9093ad9fb5cef1639efcf37d06db5576fff2ab7dd7ed4a6e8841653  templates/test-toolchains/java-gradle-junit5/src/test/java/ai/aeos/RunCucumberTest.java
68efeae3f86c8b26bacf90135ea68bd23869178b3d55b4480101bc3be1fa90cb  templates/test-toolchains/java-gradle-junit5/src/test/resources/features/smoke.feature
```

## Rollback

To rollback this change set only:

1. Remove the files listed in "Files Added Or Updated" that were newly introduced by this change set.
2. Revert the `package.json` script/dependency additions and restore `package-lock.json` from the previous revision.
3. Remove `.tools/apache-maven-3.9.11`, `.tools/gradle-9.2.1`, `.tools/jdk-17.0.19+10`, `.tools/downloads`, and `.tools/aeos-java-truststore.p12` if the local Java toolchain should also be discarded.
4. Remove `/tmp/aeos-venv` if the local Python test environment should also be discarded.
5. Remove `/tmp/aeos-robot-results`, `/tmp/aeos-m2`, `/tmp/aeos-gradle`, and `/tmp/aeos-maven-settings.xml` if generated reports/caches are not needed.

Do not rollback unrelated AEOS changes from earlier change sets unless explicitly requested.
