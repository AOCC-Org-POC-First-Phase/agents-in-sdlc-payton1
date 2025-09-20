import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should display the correct title', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page title is correct
    await expect(page).toHaveTitle('Tailspin Toys - Crowdfunding your new favorite game!');
  });

  test('should display the main heading', async ({ page }) => {
    await page.goto('/');
    
    // Check that the main heading is present
    const mainHeading = page.locator('h1').first();
    await expect(mainHeading).toHaveText('Tailspin Toys');
  });

  test('should display the welcome message', async ({ page }) => {
    await page.goto('/');
    
    // Check that the welcome message is present
    const welcomeMessage = page.locator('p').first();
    await expect(welcomeMessage).toHaveText('Find your next game! And maybe even back one! Explore our collection!');
  });

  test('should have functional navigation in header', async ({ page }) => {
    await page.goto('/');
    
    // Check that the header is present
    const header = page.locator('header');
    await expect(header).toBeVisible();
    
    // Check that the Tailspin Toys logo/link is present and functional
    const logoLink = header.locator('a:has-text("Tailspin Toys")');
    await expect(logoLink).toBeVisible();
    await expect(logoLink).toHaveAttribute('href', '/');
  });

  test('should display games list section', async ({ page }) => {
    await page.goto('/');
    
    // Check that the Featured Games heading is present
    const featuredGamesHeading = page.locator('h2:has-text("Featured Games")');
    await expect(featuredGamesHeading).toBeVisible();
    
    // Ensure the games grid appears (may be loading or loaded)
    await page.waitForSelector('[data-testid="games-grid"], .animate-pulse', { timeout: 10000 });
  });
});
