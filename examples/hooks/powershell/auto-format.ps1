# PostToolUse hook - Auto-format files after editing
# Place in: .claude\hooks\auto-format.ps1
# Register in: .claude\settings.json (PostToolUse, matcher "Edit|Write"), running in PowerShell:
#   {
#     "hooks": {
#       "PostToolUse": [{
#         "matcher": "Edit|Write",
#         "hooks": [{
#           "type": "command",
#           "shell": "powershell",
#           "command": "& \"$env:CLAUDE_PROJECT_DIR\\.claude\\hooks\\auto-format.ps1\""
#         }]
#       }]
#     }
#   }
# Use the `$env:CLAUDE_PROJECT_DIR` spelling: the bare `$CLAUDE_PROJECT_DIR` resolves
# to $null in PowerShell.

$inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json
$tool = $inputJson.tool_name

# Only run after Write or Edit operations
if ($tool -eq "Write" -or $tool -eq "Edit") {
    $file = $inputJson.tool_input.file_path
    if (-not $file) {
        $file = $inputJson.tool_input.path
    }

    if (-not $file -or $file -eq "null") {
        exit 0
    }

    # Get file extension
    $ext = [System.IO.Path]::GetExtension($file).TrimStart('.')

    switch ($ext) {
        { $_ -in @("js", "jsx", "ts", "tsx", "json", "css", "scss", "md", "html", "vue") } {
            # Format with Prettier if available
            if (Test-Path "node_modules\.bin\prettier.cmd") {
                & npx prettier --write $file 2>$null
            }
        }
        "py" {
            # Format with Black if available
            if (Get-Command black -ErrorAction SilentlyContinue) {
                & black $file 2>$null
            }
        }
        "go" {
            # Format with gofmt
            if (Get-Command gofmt -ErrorAction SilentlyContinue) {
                & gofmt -w $file 2>$null
            }
        }
        "rs" {
            # Format with rustfmt
            if (Get-Command rustfmt -ErrorAction SilentlyContinue) {
                & rustfmt $file 2>$null
            }
        }
    }
}

exit 0
