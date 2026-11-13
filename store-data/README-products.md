# Thrice Loved product data
1. In Shopify admin go to Products > Import, choose `products.csv`, and tick "Overwrite products with matching handles" if re-importing.
2. Each product is one-of-one: a single Size variant with inventory 1 (sold out once bought, which suits pre-loved stock).
3. Shopify CSV imports need public image URLs, so add pictures after import: open each product and drag the matching PNG from `product-images/` (filename = handle) into Media.
4. Swap in photos of real garments when you have them. These illustrations are placeholders. Upload `hero-flatlay.png` in the theme editor for the homepage hero.
5. Product Category values are best-effort Shopify taxonomy paths; if one is rejected, pick the category in the product page and re-save.
