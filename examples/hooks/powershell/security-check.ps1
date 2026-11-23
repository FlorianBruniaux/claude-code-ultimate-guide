# PreToolUse hook - Block commands containing secrets
# Place in: .claude\hooks\security-check.ps1
# Register in: .claude\settings.json (PreToolUse, matcher "Bash"), running in PowerShell:
#   {
#     "hooks": {
#       "PreToolUse": [{
#         "matcher": "Bash",
#         "hooks": [{
#           "type": "command",
#           "shell": "powershell",
#           "command": "& \"$env:CLAUDE_PROJECT_DIR\\.claude\\hooks\\security-check.ps1\""
#         }]
#       }]
#     }
#   }
# Use the `$env:CLAUDE_PROJECT_DIR` spelling: the bare `$CLAUDE_PROJECT_DIR` resolves
# to $null in PowerShell. Blocking uses exit 2 plus a message on stderr, like the
# bash twin (security-check.sh).

$inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
$tool = $inputJson.tool_name

if ($tool -eq "Bash") {
    $command = $inputJson.tool_input.command

    # Check for common secret patterns
    $patterns = @(
        "password=",
        "PASSWORD=",
        "secret=",
        "SECRET=",
        "api_key=",
        "API_KEY=",
        "apikey=",
        "token=",
        "TOKEN=",
        "aws_access_key",
        "AWS_ACCESS_KEY",
        "aws_secret",
        "AWS_SECRET",
        "private_key",
        "PRIVATE_KEY"
    )

    foreach ($pattern in $patterns) {
        if ($command -match [regex]::Escape($pattern)) {
            [Console]::Error.WriteLine("Blocked: potential secret detected in command: $pattern")
            exit 2
        }
    }

    # Check for hardcoded API keys
    if ($command -match "(sk-[a-zA-Z0-9]{20,}|pk_[a-zA-Z0-9]{20,}|[a-f0-9]{32,})") {
        [Console]::Error.WriteLine("Blocked: potential API key or hash detected in command")
        exit 2
    }
}

# Allow the command
exit 0
