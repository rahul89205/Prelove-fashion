# Thrice Loved – Shopify setup (about 20 minutes)

You get: `thrice-loved-theme.zip` (the website), `products.csv` (12 products), `product-images/` (photos).

## 1. Create the store
1. Go to shopify.com and start a free trial (or use a Shopify Partners development store, which is free for students/builds).
2. Store name = your business name. The theme shows the store name as the logo, so rename it under Settings > General if your group picks a different name.
3. Settings > Markets/Store details: set currency to NZD.

## 2. Install the theme
Online Store > Themes > Add theme > Upload zip file > choose `thrice-loved-theme.zip` > Publish.

## 3. Import products
Products > Import > choose `products.csv` > Import products.
Then open each product and drag its matching PNG from `product-images/` into Media (Shopify CSV needs public URLs, so photos are added by hand). Use real photos of real items if you have them.

## 4. Create three pages (Online Store > Pages > Add page)
| Page title | URL handle | Theme template |
|---|---|---|
| Sustainability | sustainability | page.sustainability |
| Sell with us | sell-with-us | page.sell-with-us |
| Contact | contact | page.contact |

## 5. Payments for testing
Settings > Payments > enable the Bogus Gateway / test mode (dev stores) or Shopify Payments test mode. Place a test order with card number 1 (Bogus Gateway) to screenshot the checkout for your report.

## 6. Customise (Online Store > Themes > Customize)
Edit text, colours (Theme settings), logo, hero image and the sustainability stats. Replace the stats' sources with your own if you change the numbers.

## Where the sustainability features live
- Condition grading: product tags like `Condition: Like new` become badges.
- One-of-one stock: inventory quantity 1 per item, "only 1 available" notice, sold badge.
- Plastic-free packaging, take-back/store-credit loop: home page, product page, cart, Sustainability and Sell with us pages.
