package com.aeos.telemetry.starter;

import com.aeos.telemetry.core.Telemetry;
import com.aeos.telemetry.core.TelemetryBootstrap;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;

/** Auto-configuração da telemetria. Condicional à presença do core (AD-005): app sem
 *  Spring não tem o spring-boot-autoconfigure no classpath (scope provided) e o starter fica inerte. */
@AutoConfiguration
@ConditionalOnClass(TelemetryBootstrap.class)
@EnableConfigurationProperties(OtelTelemetryProperties.class)
public class OtelTelemetryAutoConfiguration {

    /** destroyMethod shutdown: flush com teto de 5 s antes do contexto fechar (AD-006). */
    @Bean(destroyMethod = "shutdown")
    public Telemetry telemetry(OtelTelemetryProperties properties) {
        return TelemetryBootstrap.start(builder -> builder
                .serviceName(properties.serviceName())
                .preset(properties.preset())
                .protocol(properties.protocol())
                .endpoint(properties.endpoint()));
    }
}
