# Chạy trong Terminal thứ hai khi API đang chạy ở localhost:5080
$base = 'http://localhost:5080'
Write-Host '1. Kiểm tra API:'
Invoke-RestMethod "$base/"
Write-Host '2. Tạo hợp đồng:'
$future = (Get-Date).AddDays(30).ToString('yyyy-MM-dd')
$body = @{ customerName = 'ABC Logistics'; effectiveDate = $future } | ConvertTo-Json
$contract = Invoke-RestMethod -Uri "$base/api/contracts" -Method Post -ContentType 'application/json' -Body $body
$contract | ConvertTo-Json
Write-Host '3. Gửi trình duyệt lần 1:'
Invoke-RestMethod -Uri "$base/api/contracts/$($contract.id)/submit" -Method Post | ConvertTo-Json
Write-Host '4. Gửi lần 2 (dự kiến bị từ chối do trạng thái):'
try { Invoke-RestMethod -Uri "$base/api/contracts/$($contract.id)/submit" -Method Post | ConvertTo-Json } catch { Write-Host "HTTP error: $($_.Exception.Message)" }
