# MORVO Backend Deployment Test
# Replace YOUR_RAILWAY_URL with your actual Railway URL

$baseUrl = "https://morvo-backend-production.up.railway.app"

Write-Host "=== MORVO Backend Deployment Test ===" -ForegroundColor Green
Write-Host "Testing URL: $baseUrl" -ForegroundColor Yellow
Write-Host ""

# Test endpoints
$endpoints = @(
    @{Path="/health"; Name="Health Check"},
    @{Path="/ping"; Name="Ping"},
    @{Path="/api-status"; Name="API Status"},
    @{Path="/cors-test"; Name="CORS Test"},
    @{Path="/test"; Name="Test Endpoint"},
    @{Path="/"; Name="Root Endpoint"}
)

$successCount = 0
$totalCount = $endpoints.Count

foreach ($endpoint in $endpoints) {
    $url = $baseUrl + $endpoint.Path
    Write-Host "Testing $($endpoint.Name): $url" -ForegroundColor Cyan
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 10
        Write-Host "✅ SUCCESS: $($response.StatusCode)" -ForegroundColor Green
        
        # Try to parse JSON response
        try {
            $jsonResponse = $response.Content | ConvertFrom-Json
            Write-Host "   Response: $($jsonResponse | ConvertTo-Json -Compress)" -ForegroundColor Gray
        } catch {
            Write-Host "   Response: $($response.Content)" -ForegroundColor Gray
        }
        $successCount++
    } catch {
        Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
}

Write-Host "=== Test Results ===" -ForegroundColor Green
Write-Host "✅ $successCount/$totalCount endpoints working" -ForegroundColor Yellow

if ($successCount -eq $totalCount) {
    Write-Host "🎉 All tests passed! Your backend is ready for your partner!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some tests failed. Check Railway logs before sharing." -ForegroundColor Red
}

Write-Host ""
Write-Host "To use this script:" -ForegroundColor Yellow
Write-Host "1. Replace 'YOUR_RAILWAY_URL' with your actual Railway URL" -ForegroundColor White
Write-Host "2. Run: .\test_deployment.ps1" -ForegroundColor White 