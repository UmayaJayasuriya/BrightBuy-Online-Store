$content = Get-Content .env -Raw
$content = $content -replace 'DB_PASSWORD="JmyU#29791"', 'DB_PASSWORD="Himandhi@123"'
$content = $content -replace 'root:JmyU#29791@', 'root:Himandhi@123@'
Set-Content .env -Value $content -NoNewline
Write-Host "Password updated successfully"
