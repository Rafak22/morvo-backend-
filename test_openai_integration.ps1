# Test OpenAI Integration Script
$baseUrl = "https://morvo-backend-production.up.railway.app"

Write-Host "=== Testing OpenAI Integration ===" -ForegroundColor Green

# Test data
$chatData = @{
    message = "Give me a marketing strategy for a new product launch"
    user_id = "test_user_123"
    session_id = "test_session_456"
} | ConvertTo-Json

Write-Host "`nTesting OpenAI integration with marketing question..." -ForegroundColor Yellow
Write-Host "Message: Give me a marketing strategy for a new product launch" -ForegroundColor Gray

# Test 1: POST /chat
Write-Host "`nTesting POST /chat with OpenAI..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/chat" -Method POST -Body $chatData -ContentType "application/json"
    Write-Host "✅ SUCCESS: POST /chat" -ForegroundColor Green
    Write-Host "   Response: $($response.response)" -ForegroundColor Gray
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: POST /chat" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: POST /api/morvo/chat
Write-Host "`nTesting POST /api/morvo/chat with OpenAI..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/morvo/chat" -Method POST -Body $chatData -ContentType "application/json"
    Write-Host "✅ SUCCESS: POST /api/morvo/chat" -ForegroundColor Green
    Write-Host "   Response: $($response.response)" -ForegroundColor Gray
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: POST /api/morvo/chat" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Arabic message test
$arabicData = @{
    message = "اعطيني خطة تسويقية"
    user_id = "arabic_user"
    session_id = "arabic_session"
} | ConvertTo-Json

Write-Host "`nTesting Arabic message with OpenAI..." -ForegroundColor Yellow
Write-Host "Message: اعطيني خطة تسويقية (Give me a marketing plan)" -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/chat" -Method POST -Body $arabicData -ContentType "application/json"
    Write-Host "✅ SUCCESS: Arabic message" -ForegroundColor Green
    Write-Host "   Response: $($response.response)" -ForegroundColor Gray
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
} catch {
    Write-Host "❌ FAILED: Arabic message" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== OpenAI Integration Test Complete ===" -ForegroundColor Green
Write-Host "If you see AI-generated responses above, OpenAI is working!" -ForegroundColor Cyan
Write-Host "If you see error messages, check your OPENAI_API_KEY environment variable." -ForegroundColor Yellow 