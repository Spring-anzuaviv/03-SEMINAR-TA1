namespace Qtkd.Api.Models;

public enum ContractStatus { Draft, PendingApproval, RevisionRequested, Approved, Active }

public sealed class Contract
{
    public int Id { get; set; }
    public string CustomerName { get; set; } = "";
    public DateOnly EffectiveDate { get; set; }
    public ContractStatus Status { get; set; } = ContractStatus.Draft;
    public int ApprovalRequestCount { get; set; }
    public bool HasCompletedApprovalStep { get; set; }
}

public record CreateContractRequest(string CustomerName, DateOnly EffectiveDate);
public record ApiError(string Code, string Message);
