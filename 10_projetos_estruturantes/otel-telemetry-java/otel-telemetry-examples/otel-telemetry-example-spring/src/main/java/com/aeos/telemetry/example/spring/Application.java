package com.aeos.telemetry.example.spring;

import com.aeos.telemetry.core.Telemetry;
import com.aeos.telemetry.adapters.Adapters;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

/** Exemplo Spring Boot: o starter autoconfigura o bean Telemetry a partir de
 *  oteltelemetry.* (application.properties, preset offline → sink local). */
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        ConfigurableApplicationContext context = SpringApplication.run(Application.class, args);
        Telemetry telemetry = context.getBean(Telemetry.class);
        // integrações opcionais: Logback → OTel e Micrometer → OTel (upstream)
        Adapters.installLogbackAppender(telemetry.openTelemetry());
        System.out.println("[demo-spring] pronto; telemetria ativa (noop=" + telemetry.noop() + ")");
    }
}
