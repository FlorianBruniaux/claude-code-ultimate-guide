import { readFileSync } from 'node:fs';
import { defineConfig } from 'tsup';

const packageJson = JSON.parse(
  readFileSync(new URL('./package.json', import.meta.url), 'utf8'),
) as { version: string };
const packageUserAgent = `claude-code-ultimate-guide-mcp/${packageJson.version}`;

export default defineConfig({
  entry: {
    index: 'src/index.ts',
    'product-metrics': 'src/lib/product-metrics.ts',
  },
  format: ['esm'],
  target: 'es2022',
  outDir: 'dist',
  clean: true,
  dts: true,
  sourcemap: true,
  define: {
    __PACKAGE_VERSION__: JSON.stringify(packageJson.version),
    __USER_AGENT__: JSON.stringify(packageUserAgent),
  },
  banner: {
    js: '#!/usr/bin/env node',
  },
});
