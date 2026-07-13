package main

import (
	"context"
	"fmt"

	"go.opentelemetry.io/otel"
)

func greeting(ctx context.Context, name string) string {
	_, span := otel.Tracer("aeos-go-service").Start(ctx, "greeting")
	defer span.End()
	return fmt.Sprintf("hello %s", name)
}

func main() {
	fmt.Println(greeting(context.Background(), "aeos"))
}
