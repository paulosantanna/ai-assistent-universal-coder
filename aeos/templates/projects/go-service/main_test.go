package main

import (
	"context"
	"testing"
)

func TestGreeting(t *testing.T) {
	if got := greeting(context.Background(), "aeos"); got != "hello aeos" {
		t.Fatalf("unexpected greeting: %s", got)
	}
}
