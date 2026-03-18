#!/usr/bin/env ts-node
/**
 * Context Assembler
 *
 * Assembles CLAUDE.md from a developer profile YAML + shared module markdown files.
 * Supports @import resolution, module exclusions, and per-developer overrides.
 *
 * Usage:
 *   ts-node assembler.ts --profile .claude/profiles/alice.yaml --output CLAUDE.md
 *   ts-node assembler.ts --profile .claude/profiles/alice.yaml --modules .claude/modules --output CLAUDE.md --dry-run
 *
 * Dependencies:
 *   npm install js-yaml @types/js-yaml ts-node typescript
 */

import fs from 'fs'
import path from 'path'
import yaml from 'js-yaml'

// ── Types ────────────────────────────────────────────────────────────────────

interface ProfileTools {
  primary_lang: string
  frontend?: string
  backend?: string
  database?: string
  cloud?: string
  test_framework?: string
}

interface ProfileStyle {
  verbosity: 'verbose' | 'concise' | 'minimal'
  comment_style: 'none' | 'inline' | 'jsdoc'
  test_coverage: 'none' | 'optional' | 'required'
}

interface Profile {
  profile: {
    name: string
    role: string
    seniority: string
    tools: ProfileTools
    style: ProfileStyle
  }
  modules: {
    include: string[]
    exclude: string[]
  }
  overrides: {
    custom_rules: string[]
  }
}

interface AssemblyResult {
  content: string
  totalChars: number
  estimatedTokens: number
  modulesLoaded: number
  modulesMissing: string[]
  importsResolved: number
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function loadProfile(profilePath: string): Profile {
  if (!fs.existsSync(profilePath)) {
    throw new Error(`Profile not found: ${profilePath}`)
  }
  const content = fs.readFileSync(profilePath, 'utf8')
  return yaml.load(content) as Profile
}

function resolveImports(content: string, baseDir: string, depth = 0): string {
  if (depth > 5) {
    console.warn('  Warning: @import depth limit reached (5) — circular imports?')
    return content
  }
  return content.replace(/^@(.+)$/gm, (_, importPath) => {
    const fullPath = path.resolve(baseDir, importPath.trim())
    if (!fs.existsSync(fullPath)) {
      return `<!-- @import ${importPath} — FILE NOT FOUND -->`
    }
    const imported = fs.readFileSync(fullPath, 'utf8')
    return resolveImports(imported, path.dirname(fullPath), depth + 1)
  })
}

function loadModule(
  modulePath: string,
  modulesDir: string,
  result: AssemblyResult
): string {
  const fullPath = path.resolve(modulesDir, modulePath)
  if (!fs.existsSync(fullPath)) {
    console.warn(`  Warning: module not found — ${fullPath}`)
    result.modulesMissing.push(modulePath)
    return ''
  }
  const raw = fs.readFileSync(fullPath, 'utf8')
  const resolved = resolveImports(raw, path.dirname(fullPath))
  const importsInFile = (raw.match(/^@.+$/gm) || []).length
  result.importsResolved += importsInFile
  result.modulesLoaded++
  return resolved
}

function buildHeader(profile: Profile): string {
  const { name, role, seniority, tools, style } = profile.profile
  return [
    `# CLAUDE.md`,
    `# Assembled for: ${name} | Role: ${role} | Seniority: ${seniority}`,
    `# Generated: ${new Date().toISOString().split('T')[0]}`,
    `# Stack: ${tools.primary_lang}${tools.frontend !== 'none' ? ` + ${tools.frontend}` : ''}${tools.backend !== 'none' ? ` + ${tools.backend}` : ''}`,
    `# Style: verbosity=${style.verbosity}, comments=${style.comment_style}, tests=${style.test_coverage}`,
    '',
  ].join('\n')
}

function buildOverrides(rules: string[]): string {
  if (rules.length === 0) return ''
  return [
    '\n## Personal Rules',
    '',
    ...rules.map((r) => `- ${r}`),
    '',
  ].join('\n')
}

// ── Core ─────────────────────────────────────────────────────────────────────

function assemble(
  profilePath: string,
  outputPath: string,
  modulesDir: string,
  dryRun: boolean
): AssemblyResult {
  const profile = loadProfile(profilePath)
  const result: AssemblyResult = {
    content: '',
    totalChars: 0,
    estimatedTokens: 0,
    modulesLoaded: 0,
    modulesMissing: [],
    importsResolved: 0,
  }

  const sections: string[] = [buildHeader(profile)]

  for (const modulePath of profile.modules.include) {
    if (profile.modules.exclude.includes(modulePath)) {
      console.log(`  Skipped (excluded): ${modulePath}`)
      continue
    }
    const content = loadModule(modulePath, modulesDir, result)
    if (content) {
      sections.push(`\n<!-- ── Module: ${modulePath} ── -->\n`)
      sections.push(content.trim())
    }
  }

  const overrides = buildOverrides(profile.overrides.custom_rules)
  if (overrides) sections.push(overrides)

  result.content = sections.join('\n')
  result.totalChars = result.content.length
  result.estimatedTokens = Math.round(result.totalChars / 4)

  if (!dryRun) {
    fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true })
    fs.writeFileSync(outputPath, result.content)
  }

  return result
}

// ── CLI ───────────────────────────────────────────────────────────────────────

function parseArgs(): {
  profilePath: string
  outputPath: string
  modulesDir: string
  dryRun: boolean
} {
  const args = process.argv.slice(2)
  const get = (flag: string, fallback: string): string => {
    const idx = args.indexOf(flag)
    return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback
  }
  return {
    profilePath: get('--profile', '.claude/profiles/default.yaml'),
    outputPath: get('--output', 'CLAUDE.md'),
    modulesDir: get('--modules', '.claude/modules'),
    dryRun: args.includes('--dry-run'),
  }
}

function main() {
  const { profilePath, outputPath, modulesDir, dryRun } = parseArgs()

  console.log('Context Assembler')
  console.log('=================')
  console.log(`Profile:  ${profilePath}`)
  console.log(`Modules:  ${modulesDir}`)
  console.log(`Output:   ${outputPath}${dryRun ? ' (dry-run — not written)' : ''}`)
  console.log('')

  try {
    const result = assemble(profilePath, outputPath, modulesDir, dryRun)

    console.log('')
    console.log('Summary:')
    console.log(`  Modules loaded:    ${result.modulesLoaded}`)
    console.log(`  Modules missing:   ${result.modulesMissing.length}`)
    console.log(`  @imports resolved: ${result.importsResolved}`)
    console.log(`  Output size:       ${result.totalChars} chars (~${result.estimatedTokens} tokens)`)

    if (result.modulesMissing.length > 0) {
      console.log('')
      console.log('Missing modules (create these files or remove from profile):')
      for (const m of result.modulesMissing) {
        console.log(`  - ${m}`)
      }
    }

    if (result.estimatedTokens > 10000) {
      console.log('')
      console.log(
        `Warning: ~${result.estimatedTokens} tokens is on the heavy side (target <10K).`
      )
      console.log('         Consider splitting into per-task @imports instead of always-on.')
    }

    if (!dryRun) {
      console.log('')
      console.log(`Done: ${outputPath}`)
    }
  } catch (err) {
    console.error(`Error: ${(err as Error).message}`)
    process.exit(1)
  }
}

main()
