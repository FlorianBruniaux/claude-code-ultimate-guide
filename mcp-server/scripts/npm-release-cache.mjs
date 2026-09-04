import { isAbsolute, resolve } from 'node:path'

export const RELEASE_NPM_CACHE_ENV = 'MCP_RELEASE_NPM_CACHE'

export function npmReleaseEnvironment(cacheDirectory, baseEnvironment = process.env) {
  if (typeof cacheDirectory !== 'string' || cacheDirectory.trim() === '') {
    throw new Error('release npm cache must be a non-empty path')
  }
  const cache = resolve(cacheDirectory)
  if (!isAbsolute(cache)) throw new Error('release npm cache must resolve to an absolute path')
  return {
    ...baseEnvironment,
    [RELEASE_NPM_CACHE_ENV]: cache,
    npm_config_cache: cache,
    npm_config_audit: 'false',
    npm_config_fund: 'false',
  }
}
