# Detailed CORS Test for magic.lovable.app
$baseUrl = "https://morvo-backend-production.up.railway.app"

Write-Host "=== Detailed CORS Test ===" -ForegroundColor Green
Write-Host "Testing from magic.lovable.app perspective" -ForegroundColor Yellow
Write-Host ""

# Test 1: Simple GET request (like a browser would make)
Write-Host "1. Testing simple GET request..." -ForegroundColor Cyan
try {
    $headers = @{
        "Origin" = "https://magic.lovable.app"
        "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    $response = Invoke-WebRequest -Uri "$baseUrl/cors-test" -Method GET -Headers $headers -TimeoutSec 10
    Write-Host "✅ GET request SUCCESS: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   CORS Headers:" -ForegroundColor Gray
    foreach ($header in $response.Headers.Keys) {
        Write-Host "   $header`: $($response.Headers[$header])" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ GET request FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 2: OPTIONS preflight request
Write-Host "2. Testing OPTIONS preflight request..." -ForegroundColor Cyan
try {
    $headers = @{
        "Origin" = "https://magic.lovable.app"
        "Access-Control-Request-Method" = "POST"
        "Access-Control-Request-Headers" = "Content-Type"
    }
    
    $response = Invoke-WebRequest -Uri "$baseUrl/cors-test" -Method OPTIONS -Headers $headers -TimeoutSec 10
    Write-Host "✅ OPTIONS request SUCCESS: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   CORS Headers:" -ForegroundColor Gray
    foreach ($header in $response.Headers.Keys) {
        Write-Host "   $header`: $($response.Headers[$header])" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ OPTIONS request FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: POST request with JSON
Write-Host "3. Testing POST request with JSON..." -ForegroundColor Cyan
try {
    $headers = @{
        "Origin" = "https://magic.lovable.app"
        "Content-Type" = "application/json"
    }
    
    $body = @{ test = "data" } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$baseUrl/cors-test" -Method POST -Headers $headers -Body $body -TimeoutSec 10
    Write-Host "✅ POST request SUCCESS: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ POST request FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== CORS Test Complete ===" -ForegroundColor Green
Write-Host "If all tests pass, the issue is likely in the frontend code." -ForegroundColor Yellow
Write-Host "If any fail, we need to fix the backend CORS configuration." -ForegroundColor Red 