package com.aeos.telemetry.starter;

import org.junit.jupiter.api.Test;
import org.springframework.boot.autoconfigure.AutoConfigurations;
import org.springframework.boot.test.context.FilteredClassLoader;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;

import static org.assertj.core.api.Assertions.assertThat;

/** C11: properties oteltelemetry.* criam o bean Telemetry; C12: sem o core no classpath
 *  o autoconfig recua (@ConditionalOnClass) — e num app sem Spring o jar é inerte
 *  por construção (spring-boot-autoconfigure é provided). */
class StarterAutoConfigTest {

    private final ApplicationContextRunner runner = new ApplicationContextRunner()
            .withConfiguration(AutoConfigurations.of(OtelTelemetryAutoConfiguration.class))
            .withPropertyValues(
                    "oteltelemetry.service-name=svc-spring",
                    "oteltelemetry.preset=offline");

    @Test
    void autoconfiguresTelemetryFromProperties() {
        runner.run(context -> {
            assertThat(context).hasBean("telemetry");
            com.aeos.telemetry.core.Telemetry telemetry = context.getBean(
                    "telemetry", com.aeos.telemetry.core.Telemetry.class);
            // preset offline com sink default: runtime real, não no-op
            assertThat(telemetry.noop()).isFalse();
            assertThat(telemetry.openTelemetry()).isNotNull();
        });
    }

    @Test
    void inertWithoutSpring() {
        runner.withClassLoader(new FilteredClassLoader(com.aeos.telemetry.core.TelemetryBootstrap.class))
                .run(context -> {
                    assertThat(context).doesNotHaveBean("telemetry");
                    assertThat(context.getStartupFailure()).isNull();
                });
    }
}
