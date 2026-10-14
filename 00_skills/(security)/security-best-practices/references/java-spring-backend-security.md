# Spring Boot and Apache Camel security

Updated: 2026-10-13
Entry point: ../SKILL.md. Read with java-general-backend-security.md for Spring/Camel. Source: IMG_2740–IMG_2748.

- Resolve exact Spring Boot/Security/Camel versions and inherited configuration before recommending APIs; Boot 2 and Boot 3 are distinct contracts. Inspect filter-chain matching/order, authenticated routes and sensitive actuator endpoints.
- Locate authorization at request, method and object/tenant boundaries; verify gateway isolation if code trusts the gateway. Never require @PreAuthorize just for stylistic consistency, and never waive a missing authorization boundary because a photo mentions a gateway.
- Validate inbound DTO/contract constraints at the generated delegate boundary and verify malformed input behavior. Preserve OpenAPI-generated APIs and avoid parallel controller contracts.
- Configure CORS to the required origins/methods; inspect CSRF against actual cookie/session/browser use. Stateless naming alone does not justify disabling CSRF.
- Camel dynamic endpoints (toD/recipientList) require demonstrated untrusted destination control before an SSRF finding; constrain destinations, protocols and redirects when untrusted. Review route logs for credentials/PII and error/retry amplification.
- Keep secret values outside repository and logs. Verify mounting, entrypoint materialization and property lookup by name. Protect generated secret files in runtime and redact diagnostic output.

Official [Spring request authorization](https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html), [method authorization](https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html), [Camel dynamic endpoints](https://camel.apache.org/manual/faq/how-to-use-a-dynamic-uri-in-to.html). Select documentation matching the target's verified version before applying code.
