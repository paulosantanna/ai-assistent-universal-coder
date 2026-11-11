package com.aeos.telemetry.example.spring;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** Endpoint mínimo para gerar tráfego observável no dashboard. */
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello(@RequestParam(defaultValue = "mundo") String nome) {
        return "olá, " + nome + "!";
    }
}
