import { test as base, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const test = base.extend({
  pageErrors: [async ({ page }, use) => {
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await use();
    expect(errors, 'No unhandled browser errors').toEqual([]);
  }, { auto: true }],
});

test.beforeEach(async ({ page }) => {
  await page.route('https://**/*', route => {
    expect(route.request().resourceType()).toBe('image');
    return route.fulfill({
      contentType: 'image/svg+xml',
      body: '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"/>',
    });
  });
});

test('mobile menu supports keyboard entry, exit and short viewports', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 256 });
  await page.goto('/');
  const menu = page.locator('#menuToggle');
  const links = page.locator('#navLinks a');
  await menu.focus();
  await page.keyboard.press('Enter');
  await expect(menu).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Tab');
  await expect(links.first()).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(menu).toBeFocused();
  await page.keyboard.press('Tab');
  await page.keyboard.press('Escape');
  await expect(menu).toBeFocused();
  await expect(menu).toHaveAttribute('aria-expanded', 'false');
  await menu.click();
  await links.last().focus();
  const bounds = await links.last().boundingBox();
  expect(bounds.y + bounds.height).toBeLessThanOrEqual(256);
  await page.keyboard.press('Tab');
  await expect(menu).toHaveAttribute('aria-expanded', 'false');
  await menu.click();
  await links.nth(1).click();
  await expect(page.locator('#picks')).toBeFocused();
  await expect(menu).toHaveAttribute('aria-expanded', 'false');
});

test('language and theme survive reload; numeric formatting follows the language', async ({ page }) => {
  await page.goto('/');
  await page.locator('#langToggle').click();
  await page.locator('#themeToggle').click();
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('lang', 'fr');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  await expect(page).toHaveTitle(/terrain/);
  await expect(page.locator('#picks .hbar-val').first()).toHaveText(/75,7\s%/);
  await page.locator('#whiteboard summary').click();
  await expect(page.locator('#whiteboard tbody tr').nth(6).locator('td').nth(2)).toHaveText('82,7');
  await page.locator('#langToggle').click();
  await expect(page.locator('#picks .hbar-val').first()).toHaveText('75.7%');
  await expect(page.locator('#whiteboard tbody tr').nth(6).locator('td').nth(2)).toHaveText('82.7');
});

test('denied preference storage does not break navigation', async ({ page }) => {
  const warnings = [];
  page.on('console', message => {
    if (message.type() === 'warning') warnings.push(message.text());
  });
  await page.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', {
      get() { throw new DOMException('Storage blocked', 'SecurityError'); },
    });
  });
  await page.goto('/');
  await page.locator('#langToggle').click();
  await page.locator('#themeToggle').click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'fr');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  expect(warnings.some(text => /preferences/i.test(text))).toBe(true);
});

test('failed remote images retain names, layout and an explicit photo notice', async ({ page }) => {
  await page.route('https://**/*', route => route.abort());
  await page.goto('/');
  await page.locator('.photo').scrollIntoViewIfNeeded();
  await expect(page.locator('.photo [role="status"]')).toBeVisible();
  await expect(page.locator('.photo')).toBeVisible();
  await page.locator('#eyetest').scrollIntoViewIfNeeded();
  await expect(page.locator('.star img:visible')).toHaveCount(0);
  for (const initials of ['KB', 'GG', 'KO', 'SK']) {
    await expect(page.locator('.star .mono', { hasText: initials })).toBeVisible();
  }
  await expect(page.locator('.byline-pic .mono')).toBeVisible();
  expect(await page.locator('.photo-media').evaluate(node => node.clientHeight)).toBeGreaterThan(0);
});

test('layout reflows and chart geometry matches the displayed probabilities', async ({ page }) => {
  await page.goto('/');
  await page.locator('details').evaluateAll(nodes => nodes.forEach(node => { node.open = true; }));
  for (const width of [320, 390, 768, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const lang of ['en', 'fr']) {
      if (await page.locator('html').getAttribute('lang') !== lang) {
        await page.locator('#langToggle').click();
      }
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      const bars = await page.locator('.hbar-track').evaluateAll(nodes => nodes.map(node => {
        const style = getComputedStyle(node);
        const available = node.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
        return {
          expected: parseFloat(node.style.getPropertyValue('--w')) / 100 * available,
          actual: node.querySelector('.hbar-fill').getBoundingClientRect().width,
        };
      }));
      for (const bar of bars) expect(Math.abs(bar.actual - bar.expected)).toBeLessThan(1);
    }
  }
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.addStyleTag({ content: 'html { font-size: 200% !important; }' });
  const resized = await page.evaluate(() => ({
    overflow: document.documentElement.scrollWidth > innerWidth,
    offenders: [...document.querySelectorAll('body *')]
      .filter(node => node.getBoundingClientRect().right > innerWidth)
      .map(node => ({ tag: node.tagName, class: node.className, text: node.textContent.slice(0, 80) })),
  }));
  expect(resized.overflow, JSON.stringify(resized.offenders)).toBe(false);
});

for (const lang of ['en', 'fr']) {
  for (const theme of ['dark', 'light']) {
    test(`accessibility scan: ${lang}, ${theme}`, async ({ page }) => {
      test.setTimeout(60_000);
      await page.addInitScript(({ lang, theme }) => {
        localStorage.setItem('f8-26-lang', lang);
        localStorage.setItem('f8-26-theme', theme);
      }, { lang, theme });
      await page.goto('/');
      await page.locator('details').evaluateAll(nodes => nodes.forEach(node => { node.open = true; }));
      for (const width of [1280, 390]) {
        await page.setViewportSize({ width, height: 900 });
        if (width === 390) await page.locator('#menuToggle').click();
        const result = await new AxeBuilder({ page }).analyze();
        expect(result.violations, `${width}px`).toEqual([]);
      }
    });
  }
}

test('skip link and data tables remain keyboard accessible', async ({ page, browserName }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  // Safari uses Option+Tab for links when macOS Full Keyboard Access is off.
  await page.keyboard.press(browserName === 'webkit' && process.platform === 'darwin' ? 'Alt+Tab' : 'Tab');
  await expect(page.locator('.skip-link')).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('main')).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(page.locator('#whiteboard summary')).toBeFocused();
  await page.keyboard.press('Enter');
  const table = page.locator('.tablewrap').first();
  await table.focus();
  await page.keyboard.press('ArrowRight');
  await expect.poll(() => table.evaluate(node => node.scrollLeft)).toBeGreaterThan(0);
  await expect(table.locator('thead')).toBeVisible();
});

test('reduced motion disables smooth scrolling', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');
});

test.describe('without JavaScript', () => {
  test.use({ javaScriptEnabled: false });
  test('navigation, disclosures and charts remain available on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/');
    await expect(page.locator('#navLinks a:visible')).toHaveCount(5);
    await expect(page.locator('.topbar button:visible')).toHaveCount(0);
    await page.locator('#whiteboard summary').click();
    await expect(page.locator('#whiteboard table').first()).toBeVisible();
    expect(await page.locator('.hbar-fill').first().evaluate(node => node.clientWidth)).toBeGreaterThan(0);
  });
});
