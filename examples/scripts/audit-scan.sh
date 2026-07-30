#!/bin/bash
# claude-audit-scan.sh - Fast Claude Code setup scanner
#
# Scans your Claude Code configuration (global + project) and outputs
# a structured report of what's configured, what's missing, and quality patterns.
#
# Usage:
#   ./audit-scan.sh           # Human-readable output (default)
#   ./audit-scan.sh --json    # JSON output for Claude processing
#   ./audit-scan.sh --help    # Show this help

set -euo pipefail

# Colors for human output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Output mode (default: human)
OUTPUT_MODE="human"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      OUTPUT_MODE="json"
      shift
      ;;
    --help|-h)
      grep '^#' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

# Helper functions
check_file() {
  [[ -f "$1" ]] && echo "true" || echo "false"
}

count_md_files() {
  if [[ -d "$1" ]]; then
    # Count all .md files recursively (commands/skills can have subfolders)
    find "$1" -type f -name "*.md" ! -name "README.md" 2>/dev/null | wc -l | tr -d ' '
  else
    echo "0"
  fi
}

count_script_files() {
  if [[ -d "$1" ]]; then
    # Count hook scripts (.sh, .js, .py, .ts)
    find "$1" -type f \( -name "*.sh" -o -name "*.js" -o -name "*.py" -o -name "*.ts" \) 2>/dev/null | wc -l | tr -d ' '
  else
    echo "0"
  fi
}

check_pattern() {
  local file="$1"
  local pattern="$2"
  if [[ -f "$file" ]]; then
    grep -q "$pattern" "$file" 2>/dev/null && echo "true" || echo "false"
  else
    echo "false"
  fi
}

get_file_lines() {
  [[ -f "$1" ]] && wc -l < "$1" | tr -d ' ' || echo "0"
}

count_pattern() {
  if [[ -f "$1" ]]; then
    local count
    count=$(grep -c "$2" "$1" 2>/dev/null) || count="0"
    echo "$count"
  else
    echo "0"
  fi
}

# JSON helper - extract value without jq (fallback)
json_extract() {
  local file="$1"
  local key="$2"
  grep -oE "\"$key\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$file" 2>/dev/null | head -1 | sed 's/.*:[[:space:]]*"\([^"]*\)".*/\1/'
}

# JSON helper - extract keys from object (fallback)
json_keys() {
  local file="$1"
  grep -oE '"[a-zA-Z0-9_@/-]+"[[:space:]]*:' "$file" 2>/dev/null | sed 's/"//g;s/://g;s/[[:space:]]//g' | head -50
}

# Expand home directory
GLOBAL_DIR="${HOME}/.claude"

# === DATA COLLECTION ===

# Global config
GLOBAL_CLAUDE_MD=$(check_file "${GLOBAL_DIR}/CLAUDE.md")
GLOBAL_SETTINGS=$(check_file "${GLOBAL_DIR}/settings.json")
GLOBAL_MCP=$(check_file "${GLOBAL_DIR}/mcp.json")

# Project config
PROJECT_CLAUDE_MD=$(check_file "./CLAUDE.md")
LOCAL_CLAUDE_MD=$(check_file "./.claude/CLAUDE.md")
PROJECT_SETTINGS=$(check_file "./.claude/settings.json")
LOCAL_SETTINGS=$(check_file "./.claude/settings.local.json")

# Extensions (count .md files recursively, hooks are scripts)
AGENTS_COUNT=$(count_md_files "./.claude/agents")
COMMANDS_COUNT=$(count_md_files "./.claude/commands")
SKILLS_COUNT=$(count_md_files "./.claude/skills")
HOOKS_COUNT=$(count_script_files "./.claude/hooks")
RULES_COUNT=$(count_md_files "./.claude/rules")

# === ENHANCED STACK DETECTION ===

TECH_STACK="unknown"
STACK_FRAMEWORK=""
STACK_RUNTIME=""
STACK_TEST=""
STACK_BUNDLER=""
STACK_DB=""
STACK_INTEGRATIONS=""
ALL_DEPS=""  # Initialize to avoid unbound variable

# Detect by manifest file
if [[ -f "package.json" ]]; then
  TECH_STACK="nodejs"
  STACK_RUNTIME="Node.js"

  # Extract dependencies (with or without jq)
  DEPS=""
  DEV_DEPS=""
  if command -v jq &> /dev/null; then
    DEPS=$(jq -r '.dependencies // {} | keys[]' package.json 2>/dev/null | tr '\n' ' ')
    DEV_DEPS=$(jq -r '.devDependencies // {} | keys[]' package.json 2>/dev/null | tr '\n' ' ')
  else
    # Fallback: grep-based extraction
    DEPS=$(grep -A 1000 '"dependencies"' package.json 2>/dev/null | grep -B 1000 -m 1 '}' | grep -oE '"[^"]+":' | sed 's/"//g;s/://g' | tr '\n' ' ')
    DEV_DEPS=$(grep -A 1000 '"devDependencies"' package.json 2>/dev/null | grep -B 1000 -m 1 '}' | grep -oE '"[^"]+":' | sed 's/"//g;s/://g' | tr '\n' ' ')
  fi
  ALL_DEPS="$DEPS $DEV_DEPS"

  # Framework detection
  [[ "$ALL_DEPS" == *"next"* ]] && STACK_FRAMEWORK="Next.js"
  [[ "$ALL_DEPS" == *"nuxt"* ]] && STACK_FRAMEWORK="Nuxt"
  [[ "$ALL_DEPS" == *"@angular/core"* ]] && STACK_FRAMEWORK="Angular"
  [[ "$ALL_DEPS" == *"vue"* && -z "$STACK_FRAMEWORK" ]] && STACK_FRAMEWORK="Vue"
  [[ "$ALL_DEPS" == *"react"* && -z "$STACK_FRAMEWORK" ]] && STACK_FRAMEWORK="React"
  [[ "$ALL_DEPS" == *"express"* && -z "$STACK_FRAMEWORK" ]] && STACK_FRAMEWORK="Express"
  [[ "$ALL_DEPS" == *"fastify"* && -z "$STACK_FRAMEWORK" ]] && STACK_FRAMEWORK="Fastify"
  [[ "$ALL_DEPS" == *"nestjs"* || "$ALL_DEPS" == *"@nestjs/core"* ]] && STACK_FRAMEWORK="NestJS"
  [[ "$ALL_DEPS" == *"svelte"* ]] && STACK_FRAMEWORK="Svelte"
  [[ "$ALL_DEPS" == *"astro"* ]] && STACK_FRAMEWORK="Astro"
  [[ "$ALL_DEPS" == *"remix"* ]] && STACK_FRAMEWORK="Remix"

  # Test framework detection
  [[ "$ALL_DEPS" == *"vitest"* ]] && STACK_TEST="Vitest"
  [[ "$ALL_DEPS" == *"jest"* && -z "$STACK_TEST" ]] && STACK_TEST="Jest"
  [[ "$ALL_DEPS" == *"mocha"* && -z "$STACK_TEST" ]] && STACK_TEST="Mocha"
  [[ "$ALL_DEPS" == *"playwright"* ]] && STACK_TEST="${STACK_TEST:+$STACK_TEST + }Playwright"
  [[ "$ALL_DEPS" == *"cypress"* ]] && STACK_TEST="${STACK_TEST:+$STACK_TEST + }Cypress"

  # Bundler detection
  [[ "$ALL_DEPS" == *"vite"* ]] && STACK_BUNDLER="Vite"
  [[ "$ALL_DEPS" == *"webpack"* && -z "$STACK_BUNDLER" ]] && STACK_BUNDLER="Webpack"
  [[ "$ALL_DEPS" == *"esbuild"* && -z "$STACK_BUNDLER" ]] && STACK_BUNDLER="esbuild"
  [[ "$ALL_DEPS" == *"turbo"* ]] && STACK_BUNDLER="${STACK_BUNDLER:+$STACK_BUNDLER + }Turborepo"

  # Database/ORM detection
  [[ "$ALL_DEPS" == *"prisma"* || "$ALL_DEPS" == *"@prisma/client"* ]] && STACK_DB="Prisma"
  [[ "$ALL_DEPS" == *"drizzle"* ]] && STACK_DB="Drizzle"
  [[ "$ALL_DEPS" == *"typeorm"* ]] && STACK_DB="TypeORM"
  [[ "$ALL_DEPS" == *"mongoose"* ]] && STACK_DB="Mongoose (MongoDB)"
  [[ "$ALL_DEPS" == *"sequelize"* ]] && STACK_DB="Sequelize"

  # Key integrations detection (generic - look for notable packages)
  INTEGRATIONS_LIST=""
  # Auth
  [[ "$ALL_DEPS" == *"@clerk"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Clerk, "
  [[ "$ALL_DEPS" == *"next-auth"* || "$ALL_DEPS" == *"@auth/"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}NextAuth, "
  [[ "$ALL_DEPS" == *"@supabase"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Supabase, "
  [[ "$ALL_DEPS" == *"firebase"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Firebase, "
  [[ "$ALL_DEPS" == *"@kinde"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Kinde, "
  # Payments
  [[ "$ALL_DEPS" == *"stripe"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Stripe, "
  [[ "$ALL_DEPS" == *"@lemonsqueezy"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}LemonSqueezy, "
  # AI/ML
  [[ "$ALL_DEPS" == *"openai"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}OpenAI, "
  [[ "$ALL_DEPS" == *"@anthropic"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Anthropic, "
  [[ "$ALL_DEPS" == *"langchain"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}LangChain, "
  [[ "$ALL_DEPS" == *"@ai-sdk"* || "$ALL_DEPS" == *"ai "* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Vercel AI SDK, "
  # Communication / Chat
  [[ "$ALL_DEPS" == *"@daily-co"* || "$ALL_DEPS" == *"daily-js"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Daily.co, "
  [[ "$ALL_DEPS" == *"twilio"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Twilio, "
  [[ "$ALL_DEPS" == *"sendgrid"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}SendGrid, "
  [[ "$ALL_DEPS" == *"resend"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Resend, "
  [[ "$ALL_DEPS" == *"talkjs"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}TalkJS, "
  [[ "$ALL_DEPS" == *"@knocklabs"* || "$ALL_DEPS" == *"knock"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Knock, "
  [[ "$ALL_DEPS" == *"stream-chat"* || "$ALL_DEPS" == *"@stream-io"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Stream, "
  # Maps
  [[ "$ALL_DEPS" == *"maplibre"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}MapLibre, "
  [[ "$ALL_DEPS" == *"mapbox"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Mapbox, "
  [[ "$ALL_DEPS" == *"@react-google-maps"* || "$ALL_DEPS" == *"google-maps"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Google Maps, "
  # File Upload
  [[ "$ALL_DEPS" == *"bytescale"* || "$ALL_DEPS" == *"@bytescale"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Bytescale, "
  [[ "$ALL_DEPS" == *"uploadthing"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}UploadThing, "
  [[ "$ALL_DEPS" == *"cloudinary"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Cloudinary, "
  # Admin Panels
  [[ "$ALL_DEPS" == *"forest-admin"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Forest Admin, "
  [[ "$ALL_DEPS" == *"@refinedev"* || "$ALL_DEPS" == *"refine"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Refine, "
  # Monitoring / Analytics
  [[ "$ALL_DEPS" == *"@sentry"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Sentry, "
  [[ "$ALL_DEPS" == *"posthog"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}PostHog, "
  [[ "$ALL_DEPS" == *"@vercel/analytics"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Vercel Analytics, "
  [[ "$ALL_DEPS" == *"mixpanel"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Mixpanel, "
  [[ "$ALL_DEPS" == *"@hotjar"* || "$ALL_DEPS" == *"hotjar"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Hotjar, "
  [[ "$ALL_DEPS" == *"@amplitude"* || "$ALL_DEPS" == *"amplitude"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Amplitude, "
  # CMS/Content
  [[ "$ALL_DEPS" == *"sanity"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Sanity, "
  [[ "$ALL_DEPS" == *"contentful"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Contentful, "
  [[ "$ALL_DEPS" == *"@payloadcms"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Payload CMS, "
  # State management
  [[ "$ALL_DEPS" == *"zustand"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Zustand, "
  [[ "$ALL_DEPS" == *"@tanstack/react-query"* || "$ALL_DEPS" == *"react-query"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}TanStack Query, "
  [[ "$ALL_DEPS" == *"trpc"* || "$ALL_DEPS" == *"@trpc"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}tRPC, "
  [[ "$ALL_DEPS" == *"jotai"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Jotai, "
  # Validation
  [[ "$ALL_DEPS" == *"zod"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Zod, "
  [[ "$ALL_DEPS" == *"yup"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Yup, "
  [[ "$ALL_DEPS" == *"valibot"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Valibot, "
  # UI Libraries
  [[ "$ALL_DEPS" == *"tailwindcss"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Tailwind, "
  [[ "$ALL_DEPS" == *"@radix-ui"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Radix UI, "
  [[ "$ALL_DEPS" == *"@chakra-ui"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Chakra UI, "
  [[ "$ALL_DEPS" == *"@mui"* || "$ALL_DEPS" == *"@material-ui"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Material UI, "
  [[ "$ALL_DEPS" == *"daisyui"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}DaisyUI, "
  [[ "$ALL_DEPS" == *"@mantine"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Mantine, "
  # shadcn/ui special case: not in package.json, check for components/ui folder
  if [[ "$ALL_DEPS" == *"shadcn"* ]] || [[ -d "components/ui" ]] || [[ -d "src/components/ui" ]]; then
    echo "$INTEGRATIONS_LIST" | grep -q "shadcn" || INTEGRATIONS_LIST="${INTEGRATIONS_LIST}shadcn/ui, "
  fi
  # Database providers (extends existing DB detection)
  [[ "$ALL_DEPS" == *"@neondatabase"* || "$ALL_DEPS" == *"@neon"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Neon, "
  [[ "$ALL_DEPS" == *"@planetscale"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}PlanetScale, "
  [[ "$ALL_DEPS" == *"@vercel/postgres"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Vercel Postgres, "
  [[ "$ALL_DEPS" == *"@upstash"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Upstash, "
  [[ "$ALL_DEPS" == *"@libsql"* || "$ALL_DEPS" == *"turso"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Turso, "
  # Feature flags
  [[ "$ALL_DEPS" == *"@vercel/flags"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Vercel Flags, "
  [[ "$ALL_DEPS" == *"launchdarkly"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}LaunchDarkly, "
  # Forms
  [[ "$ALL_DEPS" == *"react-hook-form"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}React Hook Form, "
  [[ "$ALL_DEPS" == *"formik"* ]] && INTEGRATIONS_LIST="${INTEGRATIONS_LIST}Formik, "

  # Clean up trailing comma
  STACK_INTEGRATIONS=$(echo "$INTEGRATIONS_LIST" | sed 's/, $//')

elif [[ -f "pyproject.toml" ]] || [[ -f "requirements.txt" ]]; then
  TECH_STACK="python"
  STACK_RUNTIME="Python"

  # Python framework detection
  PYTHON_DEPS=""
  if [[ -f "requirements.txt" ]]; then
    PYTHON_DEPS=$(cat requirements.txt 2>/dev/null | tr '\n' ' ')
  fi
  if [[ -f "pyproject.toml" ]]; then
    PYTHON_DEPS="$PYTHON_DEPS $(cat pyproject.toml 2>/dev/null | tr '\n' ' ')"
  fi

  [[ "$PYTHON_DEPS" == *"django"* ]] && STACK_FRAMEWORK="Django"
  [[ "$PYTHON_DEPS" == *"fastapi"* ]] && STACK_FRAMEWORK="FastAPI"
  [[ "$PYTHON_DEPS" == *"flask"* && -z "$STACK_FRAMEWORK" ]] && STACK_FRAMEWORK="Flask"
  [[ "$PYTHON_DEPS" == *"pytest"* ]] && STACK_TEST="pytest"
  [[ "$PYTHON_DEPS" == *"sqlalchemy"* ]] && STACK_DB="SQLAlchemy"
  [[ "$PYTHON_DEPS" == *"prisma"* ]] && STACK_DB="Prisma"

elif [[ -f "go.mod" ]]; then
  TECH_STACK="go"
  STACK_RUNTIME="Go"
  [[ -f "go.mod" ]] && grep -q "gin-gonic" go.mod 2>/dev/null && STACK_FRAMEWORK="Gin"
  [[ -f "go.mod" ]] && grep -q "echo" go.mod 2>/dev/null && STACK_FRAMEWORK="Echo"

elif [[ -f "Cargo.toml" ]]; then
  TECH_STACK="rust"
  STACK_RUNTIME="Rust"
  [[ -f "Cargo.toml" ]] && grep -q "actix" Cargo.toml 2>/dev/null && STACK_FRAMEWORK="Actix"
  [[ -f "Cargo.toml" ]] && grep -q "axum" Cargo.toml 2>/dev/null && STACK_FRAMEWORK="Axum"

elif [[ -f "composer.json" ]]; then
  TECH_STACK="php"
  STACK_RUNTIME="PHP"
  [[ -f "composer.json" ]] && grep -q "laravel" composer.json 2>/dev/null && STACK_FRAMEWORK="Laravel"
  [[ -f "composer.json" ]] && grep -q "symfony" composer.json 2>/dev/null && STACK_FRAMEWORK="Symfony"
fi

# Quality patterns
HAS_SECURITY_HOOKS="false"
if [[ -d "./.claude/hooks" ]]; then
  grep -l "PreToolUse" ./.claude/hooks/* 2>/dev/null >/dev/null && HAS_SECURITY_HOOKS="true"
fi

# P1.2: Test framework detection (also detect absence)
HAS_TEST_FRAMEWORK="false"
if [[ -n "$STACK_TEST" ]]; then
  HAS_TEST_FRAMEWORK="true"
elif [[ -f "jest.config.js" ]] || [[ -f "jest.config.ts" ]] || [[ -f "jest.config.mjs" ]]; then
  HAS_TEST_FRAMEWORK="true"
  STACK_TEST="Jest"
elif [[ -f "vitest.config.ts" ]] || [[ -f "vitest.config.js" ]] || [[ -f "vitest.config.mts" ]]; then
  HAS_TEST_FRAMEWORK="true"
  STACK_TEST="Vitest"
elif [[ -f "playwright.config.ts" ]] || [[ -f "playwright.config.js" ]]; then
  HAS_TEST_FRAMEWORK="true"
  STACK_TEST="Playwright"
elif [[ -f "cypress.config.ts" ]] || [[ -f "cypress.config.js" ]]; then
  HAS_TEST_FRAMEWORK="true"
  STACK_TEST="Cypress"
else
  # Last resort: check for test files
  TEST_FILES=$(find . -maxdepth 4 \( -name "*.test.*" -o -name "*.spec.*" -o -name "__tests__" \) 2>/dev/null | head -1)
  if [[ -n "$TEST_FILES" ]]; then
    HAS_TEST_FRAMEWORK="true"
    STACK_TEST="(detected from test files)"
  fi
fi

# MCP servers detection
# Claude Code stores MCP config in multiple locations:
# 1. ~/.claude.json under projects.<cwd>.mcpServers (per-project)
# 2. ~/.claude.json under mcpServers (global - applies to ALL projects)
# 3. ./.claude/mcp.json (project-level)
# 4. ~/.claude/mcp.json (legacy global)
MCP_PROJECT_SERVERS=""
MCP_GLOBAL_SERVERS=""
MCP_PROJECT_SOURCE=""
MCP_GLOBAL_SOURCE=""
CURRENT_DIR=$(pwd)

# Check 1: ~/.claude.json (project-specific AND global)
if [[ -f "${HOME}/.claude.json" ]]; then
  if command -v jq &> /dev/null; then
    # Get project-specific MCP servers
    MCP_PROJECT_SERVERS=$(jq -r --arg path "$CURRENT_DIR" '.projects[$path].mcpServers // {} | keys[]' "${HOME}/.claude.json" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
    if [[ -n "$MCP_PROJECT_SERVERS" ]]; then
      MCP_PROJECT_SOURCE="~/.claude.json (project)"
    fi
    # Get global MCP servers (top-level mcpServers key)
    MCP_GLOBAL_SERVERS=$(jq -r '.mcpServers // {} | keys[]' "${HOME}/.claude.json" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
    if [[ -n "$MCP_GLOBAL_SERVERS" ]]; then
      MCP_GLOBAL_SOURCE="~/.claude.json (global)"
    fi
  else
    # Fallback grep for project-specific
    if grep -q "\"$CURRENT_DIR\"" "${HOME}/.claude.json" 2>/dev/null; then
      MCP_PROJECT_SERVERS=$(grep -A 100 "\"$CURRENT_DIR\"" "${HOME}/.claude.json" 2>/dev/null | grep -A 50 "mcpServers" | grep -oE '"[a-zA-Z0-9_-]+"[[:space:]]*:' | head -10 | sed 's/"//g;s/://g' | tr '\n' ',' | sed 's/,$//')
      if [[ -n "$MCP_PROJECT_SERVERS" ]]; then
        MCP_PROJECT_SOURCE="~/.claude.json (project)"
      fi
    fi
    # Fallback grep for global (look for mcpServers before "projects" key)
    MCP_GLOBAL_SERVERS=$(sed -n '1,/"projects"/p' "${HOME}/.claude.json" 2>/dev/null | grep -A 50 '"mcpServers"' | grep -oE '"[a-zA-Z0-9_-]+"[[:space:]]*:[[:space:]]*\{' | head -10 | sed 's/"//g;s/://g;s/{//g' | tr '\n' ',' | sed 's/,$//')
    if [[ -n "$MCP_GLOBAL_SERVERS" ]]; then
      MCP_GLOBAL_SOURCE="~/.claude.json (global)"
    fi
  fi
fi

# Check 2: Project-level .claude/mcp.json
if [[ -z "$MCP_PROJECT_SERVERS" && -f "./.claude/mcp.json" ]]; then
  if command -v jq &> /dev/null; then
    MCP_PROJECT_SERVERS=$(jq -r '.mcpServers // {} | keys[]' "./.claude/mcp.json" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
    if [[ -n "$MCP_PROJECT_SERVERS" ]]; then
      MCP_PROJECT_SOURCE=".claude/mcp.json (project)"
    fi
  else
    MCP_PROJECT_SERVERS=$(grep -oE '"[a-zA-Z0-9_-]+"[[:space:]]*:' "./.claude/mcp.json" 2>/dev/null | head -20 | sed 's/"//g;s/://g' | tr '\n' ',' | sed 's/,$//')
    if [[ -n "$MCP_PROJECT_SERVERS" ]]; then
      MCP_PROJECT_SOURCE=".claude/mcp.json (project)"
    fi
  fi
fi

# Check 3: Legacy global ~/.claude/mcp.json
if [[ -z "$MCP_GLOBAL_SERVERS" && -f "${GLOBAL_DIR}/mcp.json" ]]; then
  if command -v jq &> /dev/null; then
    MCP_GLOBAL_SERVERS=$(jq -r '.mcpServers // {} | keys[]' "${GLOBAL_DIR}/mcp.json" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
    if [[ -n "$MCP_GLOBAL_SERVERS" ]]; then
      MCP_GLOBAL_SOURCE="~/.claude/mcp.json (legacy global)"
    fi
  else
    MCP_GLOBAL_SERVERS=$(grep -oE '"[a-zA-Z0-9_-]+"[[:space:]]*:' "${GLOBAL_DIR}/mcp.json" 2>/dev/null | head -20 | sed 's/"//g;s/://g' | tr '\n' ',' | sed 's/,$//')
    if [[ -n "$MCP_GLOBAL_SERVERS" ]]; then
      MCP_GLOBAL_SOURCE="~/.claude/mcp.json (legacy global)"
    fi
  fi
fi

# Merge all MCP servers (project + global)
MCP_ALL_SERVERS=""
if [[ -n "$MCP_PROJECT_SERVERS" && -n "$MCP_GLOBAL_SERVERS" ]]; then
  MCP_ALL_SERVERS="$MCP_PROJECT_SERVERS,$MCP_GLOBAL_SERVERS"
elif [[ -n "$MCP_PROJECT_SERVERS" ]]; then
  MCP_ALL_SERVERS="$MCP_PROJECT_SERVERS"
elif [[ -n "$MCP_GLOBAL_SERVERS" ]]; then
  MCP_ALL_SERVERS="$MCP_GLOBAL_SERVERS"
fi

# For backward compatibility
MCP_SERVERS="$MCP_ALL_SERVERS"
MCP_SOURCE=""
if [[ -n "$MCP_PROJECT_SOURCE" && -n "$MCP_GLOBAL_SOURCE" ]]; then
  MCP_SOURCE="$MCP_PROJECT_SOURCE + $MCP_GLOBAL_SOURCE"
elif [[ -n "$MCP_PROJECT_SOURCE" ]]; then
  MCP_SOURCE="$MCP_PROJECT_SOURCE"
elif [[ -n "$MCP_GLOBAL_SOURCE" ]]; then
  MCP_SOURCE="$MCP_GLOBAL_SOURCE"
fi

# Count MCP servers (unique)
MCP_COUNT=0
MCP_PROJECT_COUNT=0
MCP_GLOBAL_COUNT=0
if [[ -n "$MCP_ALL_SERVERS" ]]; then
  MCP_COUNT=$(echo "$MCP_ALL_SERVERS" | tr ',' '\n' | sort -u | grep -c . || echo "0")
fi
if [[ -n "$MCP_PROJECT_SERVERS" ]]; then
  MCP_PROJECT_COUNT=$(echo "$MCP_PROJECT_SERVERS" | tr ',' '\n' | grep -c . || echo "0")
fi
if [[ -n "$MCP_GLOBAL_SERVERS" ]]; then
  MCP_GLOBAL_COUNT=$(echo "$MCP_GLOBAL_SERVERS" | tr ',' '\n' | grep -c . || echo "0")
fi

# === P0.2: Detect MCPs mentioned in CLAUDE.md but not configured ===
MCP_DOCUMENTED=""
MCP_MISSING=""
KNOWN_MCPS="serena context7 sequential playwright morphllm magic filesystem"

# Scan CLAUDE.md files for MCP mentions
scan_for_mcps() {
  local file="$1"
  if [[ -f "$file" ]]; then
    for mcp in $KNOWN_MCPS; do
      if grep -qi "$mcp" "$file" 2>/dev/null; then
        if [[ -z "$MCP_DOCUMENTED" ]]; then
          MCP_DOCUMENTED="$mcp"
        else
          echo "$MCP_DOCUMENTED" | grep -q "$mcp" || MCP_DOCUMENTED="$MCP_DOCUMENTED,$mcp"
        fi
      fi
    done
  fi
}

scan_for_mcps "./CLAUDE.md"
scan_for_mcps "./.claude/CLAUDE.md"
scan_for_mcps "${GLOBAL_DIR}/CLAUDE.md"

# Find MCPs documented but not configured
if [[ -n "$MCP_DOCUMENTED" ]]; then
  for mcp in $(echo "$MCP_DOCUMENTED" | tr ',' '\n'); do
    if ! echo "$MCP_ALL_SERVERS" | grep -qi "$mcp" 2>/dev/null; then
      if [[ -z "$MCP_MISSING" ]]; then
        MCP_MISSING="$mcp"
      else
        MCP_MISSING="$MCP_MISSING,$mcp"
      fi
    fi
  done
fi

# P1.3: MCP Recommendations based on detected stack
MCP_RECOMMENDATIONS=""

# Context7 for modern frameworks (official docs lookup)
if [[ -n "$STACK_FRAMEWORK" ]]; then
  if ! echo "$MCP_ALL_SERVERS" | grep -qi "context7" 2>/dev/null; then
    MCP_RECOMMENDATIONS="${MCP_RECOMMENDATIONS}context7 ($STACK_FRAMEWORK docs), "
  fi
fi

# Sequential for complex architectures (reasoning)
if [[ -n "$STACK_DB" ]] || [[ "$STACK_FRAMEWORK" == "NestJS" ]] || [[ "$STACK_FRAMEWORK" == "Next.js" ]]; then
  if ! echo "$MCP_ALL_SERVERS" | grep -qi "sequential" 2>/dev/null; then
    MCP_RECOMMENDATIONS="${MCP_RECOMMENDATIONS}sequential-thinking (complex reasoning), "
  fi
fi

# Playwright for E2E testing (if no E2E framework)
if [[ "$HAS_TEST_FRAMEWORK" == "false" ]] || [[ -z "$STACK_TEST" ]]; then
  if ! echo "$MCP_ALL_SERVERS" | grep -qi "playwright" 2>/dev/null; then
    MCP_RECOMMENDATIONS="${MCP_RECOMMENDATIONS}playwright (E2E testing), "
  fi
fi

# Serena for large TypeScript projects (symbol navigation)
if [[ "$ALL_DEPS" == *"typescript"* ]] || [[ -f "tsconfig.json" ]]; then
  if ! echo "$MCP_ALL_SERVERS" | grep -qi "serena" 2>/dev/null; then
    MCP_RECOMMENDATIONS="${MCP_RECOMMENDATIONS}serena (TypeScript symbols), "
  fi
fi

# Clean up trailing comma
MCP_RECOMMENDATIONS=$(echo "$MCP_RECOMMENDATIONS" | sed 's/, $//')

# Memory file quality (if exists)
CLAUDE_MD_LINES="0"
CLAUDE_MD_REFS="0"
if [[ -f "./CLAUDE.md" ]]; then
  CLAUDE_MD_LINES=$(get_file_lines "./CLAUDE.md")
  CLAUDE_MD_REFS=$(count_pattern "./CLAUDE.md" "@")
fi

# Single Source of Truth pattern
HAS_SSOT="false"
NEEDS_SSOT_REFACTOR="false"
CODEBASE_REFS="0"

if [[ -f "./CLAUDE.md" ]]; then
  grep -qE "^@|/docs/|/conventions/" "./CLAUDE.md" 2>/dev/null && HAS_SSOT="true"
  # Warning: large CLAUDE.md without @references should use SSoT pattern
  if [[ $CLAUDE_MD_LINES -gt 100 && $CLAUDE_MD_REFS -eq 0 ]]; then
    NEEDS_SSOT_REFACTOR="true"
  fi
fi

# P2.1: Also check for implicit SSoT in codebase (even without CLAUDE.md)
# Look for @file.md references in code comments or markdown files
if [[ "$HAS_SSOT" == "false" ]]; then
  CODEBASE_REFS=$(find . -maxdepth 3 \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.md" \) \
    -exec grep -l "@[a-zA-Z0-9_/-]*\.md" {} \; 2>/dev/null | wc -l | tr -d ' ')
  if [[ $CODEBASE_REFS -gt 5 ]]; then
    HAS_SSOT="true"
  fi
fi

# === OUTPUT ===

if [[ "$OUTPUT_MODE" == "json" ]]; then
  # JSON output - ensure all values are properly formatted
  cat <<EOF
{
  "global": {
    "claude_md": $GLOBAL_CLAUDE_MD,
    "settings": $GLOBAL_SETTINGS,
    "mcp_json": $GLOBAL_MCP
  },
  "project": {
    "claude_md": $PROJECT_CLAUDE_MD,
    "local_claude_md": $LOCAL_CLAUDE_MD,
    "settings": $PROJECT_SETTINGS,
    "local_settings": $LOCAL_SETTINGS
  },
  "extensions": {
    "agents": $AGENTS_COUNT,
    "commands": $COMMANDS_COUNT,
    "skills": $SKILLS_COUNT,
    "hooks": $HOOKS_COUNT,
    "rules": $RULES_COUNT
  },
  "stack": {
    "type": "$TECH_STACK",
    "runtime": "$STACK_RUNTIME",
    "framework": "$STACK_FRAMEWORK",
    "test": "$STACK_TEST",
    "bundler": "$STACK_BUNDLER",
    "database": "$STACK_DB",
    "integrations": "$STACK_INTEGRATIONS"
  },
  "quality": {
    "has_security_hooks": $HAS_SECURITY_HOOKS,
    "has_test_framework": $HAS_TEST_FRAMEWORK,
    "has_ssot_references": $HAS_SSOT,
    "needs_ssot_refactor": $NEEDS_SSOT_REFACTOR,
    "claude_md_lines": $CLAUDE_MD_LINES,
    "claude_md_refs": $CLAUDE_MD_REFS
  },
  "privacy": {
    "env_excluded": $([ -f "./.claude/settings.json" ] && grep -q '\.env' "./.claude/settings.json" 2>/dev/null && echo "true" || echo "false"),
    "has_db_mcp": $(echo "$MCP_ALL_SERVERS" | grep -qiE "postgres|neon|supabase|mysql|database" 2>/dev/null && echo "true" || echo "false"),
    "opt_out_link": "https://claude.ai/settings/data-privacy-controls",
    "guide_link": "guide/security/data-privacy.md"
  },
  "mcp": {
    "configured": $([ -n "$MCP_SERVERS" ] && echo "true" || echo "false"),
    "count": $MCP_COUNT,
    "servers": "$MCP_SERVERS",
    "source": "$MCP_SOURCE",
    "project_servers": "$MCP_PROJECT_SERVERS",
    "global_servers": "$MCP_GLOBAL_SERVERS",
    "documented": "$MCP_DOCUMENTED",
    "missing": "$MCP_MISSING",
    "recommendations": "$MCP_RECOMMENDATIONS"
  }
}
EOF
else
  # Human-readable output
  echo -e "${BLUE}=== CLAUDE CODE SETUP AUDIT ===${NC}\n"

  # Stack recap at the top
  echo -e "${CYAN}💻 STACK DETECTED${NC}"
  if [[ "$TECH_STACK" != "unknown" ]]; then
    echo -e "  Runtime:      ${GREEN}$STACK_RUNTIME${NC}"
    [[ -n "$STACK_FRAMEWORK" ]] && echo -e "  Framework:    ${GREEN}$STACK_FRAMEWORK${NC}"
    [[ -n "$STACK_TEST" ]] && echo -e "  Testing:      $STACK_TEST"
    [[ -n "$STACK_BUNDLER" ]] && echo -e "  Bundler:      $STACK_BUNDLER"
    [[ -n "$STACK_DB" ]] && echo -e "  Database:     $STACK_DB"
    [[ -n "$STACK_INTEGRATIONS" ]] && echo -e "  Integrations: $STACK_INTEGRATIONS"
  else
    echo -e "  ${YELLOW}⚠️${NC}  Could not detect stack (no package.json, pyproject.toml, etc.)"
  fi

  echo -e "\n${BLUE}📁 GLOBAL CONFIG${NC} (~/.claude/)"
  [[ "$GLOBAL_CLAUDE_MD" == "true" ]] && echo -e "  ${GREEN}✅${NC} CLAUDE.md" || echo -e "  ${RED}❌${NC} CLAUDE.md"
  [[ "$GLOBAL_SETTINGS" == "true" ]] && echo -e "  ${GREEN}✅${NC} settings.json" || echo -e "  ${RED}❌${NC} settings.json"
  [[ "$GLOBAL_MCP" == "true" ]] && echo -e "  ${GREEN}✅${NC} mcp.json (legacy)" || echo -e "  ${YELLOW}⚠️${NC}  mcp.json (not required, MCP in ~/.claude.json)"

  echo -e "\n${BLUE}📁 PROJECT CONFIG${NC} (./)"
  [[ "$PROJECT_CLAUDE_MD" == "true" ]] && echo -e "  ${GREEN}✅${NC} CLAUDE.md" || echo -e "  ${YELLOW}⚠️${NC}  CLAUDE.md (recommended)"
  [[ "$LOCAL_CLAUDE_MD" == "true" ]] && echo -e "  ${GREEN}✅${NC} .claude/CLAUDE.md (local)" || echo -e "  ${YELLOW}⚠️${NC}  .claude/CLAUDE.md (optional)"
  [[ "$PROJECT_SETTINGS" == "true" ]] && echo -e "  ${GREEN}✅${NC} .claude/settings.json" || echo -e "  ${YELLOW}⚠️${NC}  .claude/settings.json (optional)"

  echo -e "\n${BLUE}🔧 EXTENSIONS${NC} (.claude/)"
  echo -e "  Agents:   $AGENTS_COUNT"
  echo -e "  Commands: $COMMANDS_COUNT"
  echo -e "  Skills:   $SKILLS_COUNT"
  echo -e "  Hooks:    $HOOKS_COUNT"
  echo -e "  Rules:    $RULES_COUNT"

  echo -e "\n${BLUE}✨ QUALITY PATTERNS${NC}"
  [[ "$HAS_SECURITY_HOOKS" == "true" ]] && echo -e "  ${GREEN}✅${NC} Security hooks (PreToolUse)" || echo -e "  ${RED}❌${NC} Security hooks (recommended)"
  [[ "$HAS_TEST_FRAMEWORK" == "true" ]] && echo -e "  ${GREEN}✅${NC} Test framework: $STACK_TEST" || echo -e "  ${RED}❌${NC} No test framework detected"
  [[ "$HAS_SSOT" == "true" ]] && echo -e "  ${GREEN}✅${NC} Single Source of Truth (@refs)" || echo -e "  ${YELLOW}⚠️${NC}  SSoT pattern (recommended)"

  if [[ "$PROJECT_CLAUDE_MD" == "true" ]]; then
    echo -e "  ${BLUE}ℹ️${NC}  CLAUDE.md: $CLAUDE_MD_LINES lines, $CLAUDE_MD_REFS @references"
    if [[ "$NEEDS_SSOT_REFACTOR" == "true" ]]; then
      echo -e "    ${RED}⚠️${NC}  Large file without @refs → Consider SSoT pattern (split into @docs/)"
    elif [[ $CLAUDE_MD_LINES -gt 200 ]]; then
      echo -e "    ${YELLOW}⚠️${NC}  Consider shortening (>200 lines)"
    fi
  fi

  echo -e "\n${BLUE}🔐 PRIVACY CHECK${NC}"
  # Check permissions.deny for sensitive files
  HAS_ENV_EXCLUSION="false"
  if [[ -f "./.claude/settings.json" ]]; then
    grep -q 'Read.*\.env' "./.claude/settings.json" 2>/dev/null && HAS_ENV_EXCLUSION="true"
  fi

  [[ "$HAS_ENV_EXCLUSION" == "true" ]] && echo -e "  ${GREEN}✅${NC} .env blocked via permissions.deny" || echo -e "  ${RED}⚠️${NC}  .env NOT blocked (add Read(./.env*) to permissions.deny)"

  # Check for database MCP servers (production risk)
  if echo "$MCP_ALL_SERVERS" | grep -qiE "postgres|neon|supabase|mysql|database" 2>/dev/null; then
    echo -e "  ${YELLOW}⚠️${NC}  Database MCP detected → ensure NOT production data"
  fi

  # Privacy reminders
  echo -e "  ${CYAN}💡${NC} Opt-out training: https://claude.ai/settings/data-privacy-controls"
  echo -e "  ${CYAN}💡${NC} Full guide: guide/security/data-privacy.md"

  echo -e "\n${BLUE}🔌 MCP SERVERS${NC}"
  if [[ -n "$MCP_ALL_SERVERS" ]]; then
    echo -e "  ${GREEN}✅${NC} Configured ($MCP_COUNT total): $MCP_ALL_SERVERS"
    [[ -n "$MCP_PROJECT_SERVERS" ]] && echo -e "      ${BLUE}Project:${NC} $MCP_PROJECT_SERVERS (from $MCP_PROJECT_SOURCE)"
    [[ -n "$MCP_GLOBAL_SERVERS" ]] && echo -e "      ${BLUE}Global:${NC} $MCP_GLOBAL_SERVERS (from $MCP_GLOBAL_SOURCE)"
  else
    echo -e "  ${YELLOW}⚠️${NC}  No MCP servers configured"
  fi

  # Show MCPs documented but not configured
  if [[ -n "$MCP_MISSING" ]]; then
    echo -e "  ${RED}⚠️${NC}  Documented but NOT configured: ${YELLOW}$MCP_MISSING${NC}"
    echo -e "      Add to ~/.claude.json or .claude/mcp.json to use them"
  fi

  # Show MCP recommendations
  if [[ -n "$MCP_RECOMMENDATIONS" ]]; then
    echo -e "  ${CYAN}💡${NC} Recommended for your stack: $MCP_RECOMMENDATIONS"
  fi

  echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "Scan complete! Use ${YELLOW}--json${NC} flag for machine-readable output."
fi
