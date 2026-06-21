import pandas as pd
from playwright.sync_api import sync_playwright
import os

def scrape_targeted_stars(company_base_url, target_pages=100):
    all_reviews = []
    target_stars = [5, 1] 
    auth_file = "auth.json"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        if os.path.exists(auth_file):
            print(f"[INFO] Loading existing session from {auth_file}")
            context = browser.new_context(
                storage_state=auth_file,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
        else:
            print("[INFO] No session found. Fresh context created.")
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )

        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(f"[INFO] Opening: {company_base_url}")
        page.goto(company_base_url)
        
        print("\n[ACTION REQUIRED]")
        print("[INFO] Playwright Inspector window opened.")
        print("[INFO] 1. Complete registration or login if required.")
        print("[INFO] 2. Navigate to the target page and click 'Resume' in the Inspector window.")
        
        page.pause() 

        context.storage_state(path=auth_file)
        print(f"[INFO] Session saved to {auth_file}")

        for star_rating in target_stars:
            print(f"\n[INFO] --- SCRAPING {star_rating}-STAR REVIEWS ---")
            
            for i in range(2, target_pages + 2):
                url = f"{company_base_url}?page={i}&stars={star_rating}"
                print(f"\n[INFO] Navigating to: {url}")
                
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(3000) 
                    
                    reviews = page.locator('article[data-service-review-card-paper="true"]').all()
                    print(f"[DEBUG] Page {i} has {len(reviews)} article containers.")
                    
                    added_on_page = 0
                    for idx, review in enumerate(reviews):
                        rating_element = review.locator('[data-service-review-rating]').first
                        
                        if rating_element.count() > 0:
                            rating_val = rating_element.get_attribute("data-service-review-rating")
                            
                            body = review.locator('p[data-service-review-text-typography="true"]').first
                            title = review.locator('h2[data-service-review-title-typography="true"]').first
                            
                            text = ""
                            if body.count() > 0:
                                text = body.inner_text().strip()
                            elif title.count() > 0:
                                text = title.inner_text().strip()

                            if text and rating_val and int(rating_val) == star_rating:
                                all_reviews.append({"rating": int(rating_val), "text": text})
                                added_on_page += 1
                        else:
                            if idx < 2:
                                print(f"  [DEBUG] Container {idx} skipped: No rating found.")
                    
                    print(f"[INFO] Page {i} result: Added {added_on_page} reviews. Total: {len(all_reviews)}")

                except Exception as e:
                    print(f"[ERROR] Page {i} failed: {e}")
                    print("[INFO] Execution paused. Resolve the issue and click Resume in the Inspector.")
                    page.pause()
                    continue
                    
        browser.close()

    if all_reviews:
        if not os.path.exists('data'): os.makedirs('data')
        df = pd.DataFrame(all_reviews)
        df.to_csv("data/raw_reviews.csv", index=False, encoding="utf-8")
        print(f"\n[SUCCESS] Final count: {len(all_reviews)} reviews saved.")

if __name__ == "__main__":
    BASE_URL = "https://www.trustpilot.com/review/www.revolut.com"
    scrape_targeted_stars(BASE_URL, target_pages=100)