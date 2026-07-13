using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource.AddService("aeos-dotnet-service"))
    .WithTracing(tracing => tracing.AddAspNetCoreInstrumentation().AddOtlpExporter());

var app = builder.Build();
app.MapGet("/", () => "hello aeos");
app.Run();
