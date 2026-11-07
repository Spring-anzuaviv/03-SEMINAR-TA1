using System.Text.Json.Serialization;
using Qtkd.Api.Models;
using Qtkd.Api.Services;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<ContractService>();
builder.Services.ConfigureHttpJsonOptions(options =>
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter()));

var app = builder.Build();
app.MapGet("/", () => Results.Ok(new { application = "QTKD Demo API", version = "1.0" }));
app.MapGet("/api/contracts", (ContractService service) => Results.Ok(service.List()));
app.MapGet("/api/contracts/{id:int}", (int id, ContractService service) =>
    service.Get(id) is { } contract ? Results.Ok(contract) : Results.NotFound(new ApiError("NOT_FOUND", "Khong tim thay hop dong.")));
app.MapPost("/api/contracts", (CreateContractRequest request, ContractService service) =>
{
    if (string.IsNullOrWhiteSpace(request.CustomerName) || request.EffectiveDate == default)
        return Results.BadRequest(new ApiError("INVALID_INPUT", "Khach hang va ngay hieu luc la bat buoc."));
    var contract = service.Create(request);
    return Results.Created($"/api/contracts/{contract.Id}", contract);
});
app.MapPost("/api/contracts/{id:int}/submit", (int id, ContractService service) =>
{
    var (contract, error) = service.Submit(id);
    if (error is null) return Results.Ok(contract);
    return error.Code == "NOT_FOUND" ? Results.NotFound(error) : Results.Conflict(error);
});
app.Run();
