using System.Collections.Concurrent;
using Qtkd.Api.Models;

namespace Qtkd.Api.Services;

public sealed class ContractService
{
    private readonly ConcurrentDictionary<int, Contract> _contracts = new();
    private int _nextId;
    private readonly object _gate = new();

    public IReadOnlyCollection<Contract> List() => _contracts.Values.OrderBy(c => c.Id).ToArray();
    public Contract? Get(int id) => _contracts.TryGetValue(id, out var c) ? c : null;

    public Contract Create(CreateContractRequest request)
    {
        var contract = new Contract
        {
            Id = Interlocked.Increment(ref _nextId),
            CustomerName = request.CustomerName.Trim(),
            EffectiveDate = request.EffectiveDate
        };
        _contracts[contract.Id] = contract;
        return contract;
    }

    public (Contract? Contract, ApiError? Error) Submit(int id)
    {
        lock (_gate)
        {
            if (!_contracts.TryGetValue(id, out var contract))
                return (null, new("NOT_FOUND", "Khong tim thay hop dong."));
            if (contract.Status != ContractStatus.Draft && contract.Status != ContractStatus.RevisionRequested)
                return (null, new("INVALID_STATE", "Hop dong khong o trang thai cho phep gui duyet."));
            if (string.IsNullOrWhiteSpace(contract.CustomerName) || contract.EffectiveDate == default)
                return (null, new("INVALID_CONTRACT", "Thieu thong tin bat buoc."));
            if (contract.EffectiveDate < DateOnly.FromDateTime(DateTime.UtcNow.Date))
                return (null, new("INVALID_DATE", "Ngay hieu luc phai tu ngay hien tai tro di."));
            contract.Status = ContractStatus.PendingApproval;
            contract.ApprovalRequestCount += 1;
            return (contract, null);
        }
    }

    // TODO Week 10: Add Withdraw(id, requester) with authorization and audit trail.
}
