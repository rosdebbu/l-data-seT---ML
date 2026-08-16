param(
    [string]$ConversationId,
    [switch]$Latest,
    [switch]$List,
    [int]$Limit = 10,
    [switch]$ExportHtml
)

$brainDir = "C:\Users\ROSHNI\.gemini\antigravity-ide\brain"

if (-not (Test-Path $brainDir)) {
    Write-Error "Brain directory not found at $brainDir"
    exit 1
}

# Fetch conversations sorted by last write time
$conversations = Get-ChildItem -Path $brainDir -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName ".system_generated\logs\transcript.jsonl")
} | Sort-Object LastWriteTime -Descending

if ($conversations.Count -eq 0) {
    Write-Host "No conversation transcripts found." -ForegroundColor Yellow
    exit 0
}

function Get-ConversationSummary($convFolder) {
    $logPath = Join-Path $convFolder.FullName ".system_generated\logs\transcript.jsonl"
    $firstUserMsg = "No user prompt found"
    
    if (Test-Path $logPath) {
        $lines = Get-Content -Path $logPath -Encoding UTF8
        foreach ($line in $lines) {
            try {
                $obj = $line | ConvertFrom-Json
                if ($obj.type -eq "USER_INPUT" -and $obj.content) {
                    $content = $obj.content
                    if ($content -match '<USER_REQUEST>([\s\S]*?)</USER_REQUEST>') {
                        $content = $matches[1].Trim()
                    }
                    $firstUserMsg = ($content -replace '\s+', ' ').Trim()
                    if ($firstUserMsg.Length -gt 80) {
                        $firstUserMsg = $firstUserMsg.Substring(0, 77) + "..."
                    }
                    break
                }
            } catch {}
        }
    }
    return [PSCustomObject]@{
        Id = $convFolder.Name
        LastModified = $convFolder.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        Prompt = $firstUserMsg
        Folder = $convFolder.FullName
    }
}

function Display-Transcript($convFolder, [switch]$AsHtml) {
    $logPath = Join-Path $convFolder.FullName ".system_generated\logs\transcript.jsonl"
    if (-not (Test-Path $logPath)) {
        Write-Host "Log file not found for $($convFolder.Name)" -ForegroundColor Red
        return
    }

    $lines = Get-Content -Path $logPath -Encoding UTF8
    $entries = @()

    foreach ($line in $lines) {
        try {
            $obj = $line | ConvertFrom-Json
            if ($obj.type -eq "USER_INPUT" -or $obj.type -eq "PLANNER_RESPONSE") {
                $role = if ($obj.type -eq "USER_INPUT") { "User" } else { "AI Assistant" }
                $text = $obj.content
                if ($role -eq "User" -and $text -match '<USER_REQUEST>([\s\S]*?)</USER_REQUEST>') {
                    $text = $matches[1].Trim()
                }
                if ($text) {
                    $entries += [PSCustomObject]@{
                        Role = $role
                        Time = $obj.created_at
                        Text = $text
                    }
                }
            }
        } catch {}
    }

    if ($AsHtml) {
        $htmlFile = Join-Path $env:TEMP "chat_history_$($convFolder.Name).html"
        $htmlBuilder = [System.Text.StringBuilder]::new()
        [void]$htmlBuilder.AppendLine("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Chat History - $($convFolder.Name)</title>")
        [void]$htmlBuilder.AppendLine("<style>
            body { font-family: 'Segoe UI', Arial, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 24px; }
            .container { max-width: 900px; margin: 0 auto; }
            h1 { color: #38bdf8; font-size: 24px; border-bottom: 1px solid #334155; padding-bottom: 12px; }
            .meta { color: #94a3b8; font-size: 13px; margin-bottom: 20px; }
            .msg { padding: 16px 20px; border-radius: 12px; margin-bottom: 16px; line-height: 1.6; white-space: pre-wrap; font-size: 14px; }
            .user { background: #1e293b; border-left: 4px solid #38bdf8; }
            .assistant { background: #1e1e38; border-left: 4px solid #a855f7; }
            .badge { font-weight: bold; margin-bottom: 8px; display: inline-block; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
            .user .badge { color: #38bdf8; }
            .assistant .badge { color: #c084fc; }
            .time { float: right; font-size: 11px; color: #64748b; font-weight: normal; }
        </style></head><body><div class='container'>")
        [void]$htmlBuilder.AppendLine("<h1>Conversation History</h1><div class='meta'>ID: $($convFolder.Name) | Modified: $($convFolder.LastWriteTime)</div>")
        
        foreach ($e in $entries) {
            $cssClass = if ($e.Role -eq "User") { "user" } else { "assistant" }
            $encodedText = [System.Web.HttpUtility]::HtmlEncode($e.Text)
            [void]$htmlBuilder.AppendLine("<div class='msg $cssClass'><div class='badge'>$($e.Role) <span class='time'>$($e.Time)</span></div><div>$encodedText</div></div>")
        }
        
        [void]$htmlBuilder.AppendLine("</div></body></html>")
        
        Add-Type -AssemblyName System.Web
        [System.IO.File]::WriteAllText($htmlFile, $htmlBuilder.ToString(), [System.Text.Encoding]::UTF8)
        Write-Host "Opening chat history in browser: $htmlFile" -ForegroundColor Green
        Start-Process $htmlFile
        return
    }

    Write-Host "`n========================================================" -ForegroundColor Cyan
    Write-Host " Conversation: $($convFolder.Name)" -ForegroundColor Cyan
    Write-Host " Last Modified: $($convFolder.LastWriteTime)" -ForegroundColor Gray
    Write-Host "========================================================`n" -ForegroundColor Cyan

    foreach ($e in $entries) {
        if ($e.Role -eq "User") {
            Write-Host "[$($e.Time)] USER:" -ForegroundColor Yellow -NoNewline
            Write-Host "`n$($e.Text)`n" -ForegroundColor White
        } else {
            Write-Host "[$($e.Time)] ASSISTANT:" -ForegroundColor Magenta -NoNewline
            Write-Host "`n$($e.Text)`n" -ForegroundColor Gray
        }
        Write-Host "--------------------------------------------------------" -ForegroundColor DarkGray
    }
}

# Determine action
if ($ConversationId) {
    $target = $conversations | Where-Object { $_.Name -like "*$ConversationId*" } | Select-Object -First 1
    if ($target) {
        Display-Transcript -convFolder $target -AsHtml:$ExportHtml
    } else {
        Write-Host "No conversation found matching ID '$ConversationId'" -ForegroundColor Red
    }
    exit 0
}

if ($Latest) {
    Display-Transcript -convFolder $conversations[0] -AsHtml:$ExportHtml
    exit 0
}

# Default or -List: Show list of recent chats
Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " RECENT CHAT HISTORIES (Top $($Limit))" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$summaries = @()
$count = 1
foreach ($c in ($conversations | Select-Object -First $Limit)) {
    $s = Get-ConversationSummary -convFolder $c
    $summaries += [PSCustomObject]@{
        "#" = $count
        "Date Modified" = $s.LastModified
        "Conversation ID" = $s.Id
        "First Prompt" = $s.Prompt
    }
    $count++
}

$summaries | Format-Table -AutoSize

Write-Host "Usage Tips:" -ForegroundColor DarkCyan
Write-Host "  View latest chat:       powershell -ExecutionPolicy Bypass -File .\view_chat_history.ps1 -Latest" -ForegroundColor Gray
Write-Host "  Open latest in browser: powershell -ExecutionPolicy Bypass -File .\view_chat_history.ps1 -Latest -ExportHtml" -ForegroundColor Gray
Write-Host "  View specific chat:     powershell -ExecutionPolicy Bypass -File .\view_chat_history.ps1 -ConversationId <ID>" -ForegroundColor Gray
