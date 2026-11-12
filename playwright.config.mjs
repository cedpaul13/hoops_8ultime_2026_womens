import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: 'site.spec.mjs',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: 2,
  reporter: process.env.CI
    ? [['github'], ['html', { open: 'never' }]]
    : 'list',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    viewport: { width: 1280, height: 900 },
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'node tests/serve.mjs',
    url: 'http://127.0.0.1:4173',
    reuseExistingServer: false,
  },
  projects: ['chromium', 'firefox', 'webkit'].map(browserName => ({
    name: browserName,
    use: { browserName },
  })),
});
