#!/usr/bin/env npx ts-node
/**
 * sync-ai-instructions.ts
 * Profile-Based Module Assembly for AI instructions
 *
 * Usage:
 *   npx ts-node sync-ai-instructions.ts           # Generate all profiles
 *   npx ts-node sync-ai-instructions.ts alice     # Single profile
 *   npx ts-node sync-ai-instructions.ts --check   # Dry-run + drift detection
 *
 * Directory structure expected:
 *   profiles/          Developer YAML profiles
 *   modules/           Reusable markdown modules
 *   skeleton/claude.md Template with {{PLACEHOLDERS}}
 *   output/<dev>/      Generated CLAUDE.md files
 */

import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'fs'
import { join, basename } from 'path'
import { parse } from 'yaml'

// ─── Types ───────────────────────────────────────────────────────────────────

interface Profile {
  name: string
  os: 'macos' | 'linux' | 'windows'
  tools: string[]
  communication_style: 'verbose' | 'concise' | 'terse'
  modules: {
    core: string[]
    conditional: string[]
  }
  preferences?: {
    language?: string
    token_budget?: 'low' | 'medium' | 'high'
  }
}

// ─── Module Resolution ───────────────────────────────────────────────────────

function isModuleApplicable(moduleName: string, profile: Profile): boolean {
  // OS-specific modules
  if (moduleName.endsWith('-paths')) {
    return moduleName === `${profile.os}-paths`
  }

  // Tool-specific modules
  const toolModuleMap: Record<string, string> = {
    'cursor-rules': 'cursor',
    'windsurf-rules': 'windsurf',
  }
  if (toolModuleMap[moduleName]) {
    return profile.tools.includes(toolModuleMap[moduleName])
  }

  return true
}

function resolveModules(profile: Profile): string[] {
  const core = profile.modules.core
  const conditional = profile.modules.conditional.filter(m =>
    isModuleApplicable(m, profile)
  )
  return [...core, ...conditional]
}

// ─── Template Processing ─────────────────────────────────────────────────────

function processConditionalBlocks(content: string, profile: Profile): string {
  const hasTypescript = profile.modules.core.includes('typescript-rules') ||
    profile.modules.conditional.includes('typescript-rules')
  const hasPython = profile.modules.core.includes('python-rules') ||
    profile.modules.conditional.includes('python-rules')

  const flags: Record<string, boolean> = {
    typescript: hasTypescript,
    python: hasPython,
    cursor: profile.tools.includes('cursor'),
    windsurf: profile.tools.includes('windsurf'),
    verbose: profile.communication_style === 'verbose',
    concise: profile.communication_style === 'concise',
    terse: profile.communication_style === 'terse',
  }

  // Process {{#if flag}}...{{/if}} blocks
  return content.replace(
    /\{\{#if (\w+)\}\}([\s\S]*?)\{\{\/if\}\}/g,
    (_match, flag, block) => flags[flag] ? block : ''
  )
}

function injectModules(
  content: string,
  modules: string[],
  modulesDir: string
): string {
  // Inject named modules: {{MODULE:module-name}}
  let result = content.replace(/\{\{MODULE:([^}]+)\}\}/g, (_match, moduleName) => {
    const modulePath = join(modulesDir, `${moduleName}.md`)
    if (!existsSync(modulePath)) {
      console.warn(`  ⚠ Module not found: ${moduleName}`)
      return `<!-- MODULE NOT FOUND: ${moduleName} -->`
    }
    return readFileSync(modulePath, 'utf-8').trim()
  })

  return result
}

// ─── Assembler ───────────────────────────────────────────────────────────────

function assembleInstructions(
  profilePath: string,
  skeletonPath: string,
  modulesDir: string
): string {
  const profile = parse(readFileSync(profilePath, 'utf-8')) as Profile
  const skeleton = readFileSync(skeletonPath, 'utf-8')

  const slug = basename(profilePath, '.yaml')
  const modules = resolveModules(profile)

  // Replace simple placeholders
  let output = skeleton
    .replace(/\{\{DEVELOPER_NAME\}\}/g, profile.name)
    .replace(/\{\{DEVELOPER_SLUG\}\}/g, slug)
    .replace(/\{\{OS\}\}/g, profile.os)
    .replace(/\{\{TOOL\}\}/g, profile.tools[0] ?? 'claude-code')
    .replace(/\{\{GENERATED_DATE\}\}/g, new Date().toISOString().split('T')[0])

  // Process conditional blocks
  output = processConditionalBlocks(output, profile)

  // Inject module content
  output = injectModules(output, modules, modulesDir)

  // Clean up empty sections
  output = output.replace(/\n{3,}/g, '\n\n').trim()

  return output
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2)
  const isDryRun = args.includes('--check') || args.includes('--dry-run')
  const targetProfile = args.find(a => !a.startsWith('--'))

  const profilesDir = 'profiles'
  const skeletonPath = 'skeleton/claude.md'
  const modulesDir = 'modules'
  const outputDir = 'output'

  // Validate structure
  for (const dir of [profilesDir, modulesDir, 'skeleton']) {
    if (!existsSync(dir)) {
      console.error(`❌ Directory not found: ${dir}`)
      process.exit(1)
    }
  }

  // Collect profiles
  const profileFiles = targetProfile
    ? [`${targetProfile}.yaml`]
    : readdirSync(profilesDir).filter(f => f.endsWith('.yaml'))

  let driftDetected = false

  for (const profileFile of profileFiles) {
    const profilePath = join(profilesDir, profileFile)
    const slug = basename(profileFile, '.yaml')
    const outputPath = join(outputDir, slug, 'CLAUDE.md')

    console.log(`\n→ Processing: ${slug}`)

    const generated = assembleInstructions(profilePath, skeletonPath, modulesDir)

    if (isDryRun) {
      const existing = existsSync(outputPath)
        ? readFileSync(outputPath, 'utf-8')
        : null

      if (!existing) {
        console.log(`  ⚠ No existing file at ${outputPath}`)
        driftDetected = true
      } else if (existing !== generated) {
        console.log(`  ❌ Drift detected — ${outputPath} is out of sync`)
        driftDetected = true
      } else {
        console.log(`  ✓ In sync`)
      }
    } else {
      const devOutputDir = join(outputDir, slug)
      if (!existsSync(devOutputDir)) mkdirSync(devOutputDir, { recursive: true })

      writeFileSync(outputPath, generated)
      const lines = generated.split('\n').length
      console.log(`  ✓ Written: ${outputPath} (${lines} lines)`)
    }
  }

  if (isDryRun && driftDetected) {
    console.error('\n❌ Drift detected. Run: npx ts-node sync-ai-instructions.ts')
    process.exit(1)
  }

  if (!isDryRun) {
    console.log('\n✅ All profiles assembled successfully')
  }
}

main().catch(console.error)
