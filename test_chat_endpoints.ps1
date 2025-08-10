# Test Chat Endpoints Script
$baseUrl = "https://morvo-backend-production.up.railway.app"

Write-Host "=== Testing Chat Endpoints ===" -ForegroundColor Green

# Test 1: POST /chat
Write-Host "`nTesting POST /chat..." -ForegroundColor Yellow
$chatData = @{
    message = "Hello, this is a test message"
    user_id = "test_user_123"
    session_id = "test_session_456"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/chat" -Method POST -Body $chatData -ContentType "application/json"
    Write-Host "✅ SUCCESS: POST /chat" -ForegroundColor Green
    Write-Host "   Response: $($response.response)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: POST /chat" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: POST /api/chat
Write-Host "`nTesting POST /api/chat..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/chat" -Method POST -Body $chatData -ContentType "application/json"
    Write-Host "✅ SUCCESS: POST /api/chat" -ForegroundColor Green
    Write-Host "   Response: $($response.response)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: POST /api/chat" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: POST /api/morvo/chat
Write-Host "`nTesting POST /api/morvo/chat..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/morvo/chat" -Method POST -Body $chatData -ContentType "application/json"
    Write-Host "✅ SUCCESS: POST /api/morvo/chat" -ForegroundColor Green
    Write-Host "   Response: $($response.response)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: POST /api/morvo/chat" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: POST /test-chat
Write-Host "`nTesting POST /test-chat..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/test-chat" -Method POST -Body $chatData -ContentType "application/json"
    Write-Host "✅ SUCCESS: POST /test-chat" -ForegroundColor Green
    Write-Host "   Response: $($response.response)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: POST /test-chat" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: POST / (root)
Write-Host "`nTesting POST / (root)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Method POST -Body $chatData -ContentType "application/json"
    Write-Host "✅ SUCCESS: POST / (root)" -ForegroundColor Green
    Write-Host "   Response: $($response.response)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: POST / (root)" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: GET /api/endpoints
Write-Host "`nTesting GET /api/endpoints..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/endpoints" -Method GET
    Write-Host "✅ SUCCESS: GET /api/endpoints" -ForegroundColor Green
    Write-Host "   Total endpoints: $($response.total_endpoints)" -ForegroundColor Gray
    Write-Host "   Chat endpoints: $($response.chat_endpoints -join ', ')" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: GET /api/endpoints" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Chat Endpoints Test Complete ===" -ForegroundColor Green
Write-Host "Your backend should now handle all chat requests properly!" -ForegroundColor Cyan 