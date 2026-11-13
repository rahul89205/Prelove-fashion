import csv, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "store-data", "products.csv")
COLS = ["Handle","Title","Body (HTML)","Vendor","Product Category","Type","Tags","Published","Option1 Name","Option1 Value","Variant SKU","Variant Grams","Variant Inventory Tracker","Variant Inventory Qty","Variant Inventory Policy","Variant Fulfillment Service","Variant Price","Variant Compare At Price","Variant Requires Shipping","Variant Taxable","Image Src","Image Position","Image Alt Text","Gift Card","SEO Title","SEO Description","Variant Weight Unit","Status"]
COAT = "Apparel & Accessories > Clothing > Outerwear > Coats & Jackets"
COND = {
 "Like new": "Worn once or twice with no visible flaws.",
 "Excellent": "Light signs of wear only; nothing that affects the look or use.",
 "Good": "Gently worn with minor signs of wear, as you'd expect from a well-loved piece.",
}
# handle, title, type, size, cond, price, compare, audience, category, colour, grams, fabric, blurb, new_in
P = [
 ("vintage-denim-jacket","Vintage Denim Jacket","Outerwear","M","Good",68,140,"Unisex",COAT,"Indigo",850,"Cotton denim","A vintage-style button-front denim jacket with chest pockets and a relaxed, boxy fit that layers over almost anything.",True),
 ("merino-knit-jumper","Merino Knit Jumper","Knitwear","S","Like new",45,120,"Women","Apparel & Accessories > Clothing > Clothing Tops > Sweaters","Terracotta",400,"Merino wool","A soft crew-neck jumper in warm terracotta with ribbed cuffs and hem and a subtle cable detail.",True),
 ("high-waist-straight-jeans","High-Waist Straight Jeans","Denim","W28","Good",52,130,"Women","Apparel & Accessories > Clothing > Pants","Blue",650,"Cotton denim with a little stretch","Classic high-waisted straight-leg jeans in a mid-blue wash with a button fly and a comfortable, easy-wearing cut.",False),
 ("linen-summer-dress","Linen Summer Dress","Dresses","12","Like new",58,150,"Women","Apparel & Accessories > Clothing > Dresses","Cream",380,"Linen blend","A light, airy strappy dress with a fitted button bodice and a gathered, flared skirt. Made for long Auckland summer days.",True),
 ("classic-trench-coat","Classic Trench Coat","Outerwear","L","Excellent",95,320,"Unisex",COAT,"Camel",1100,"Cotton-blend gabardine","A timeless double-breasted trench with a storm-flap collar, epaulettes and a belt to cinch the waist.",True),
 ("vintage-graphic-tee","Vintage Graphic Tee","Tops","M","Good",32,60,"Unisex","Apparel & Accessories > Clothing > Clothing Tops > T-Shirts","Charcoal",200,"Cotton jersey","A soft, broken-in charcoal tee with a faded retro sunset graphic on the chest.",False),
 ("pleated-midi-skirt","Pleated Midi Skirt","Skirts","S","Like new",38,95,"Women","Apparel & Accessories > Clothing > Skirts","Dusty blue",350,"Polyester crepe","A flowing dusty-blue pleated midi skirt with a button waistband that moves beautifully and doesn't crease.",False),
 ("leather-crossbody-bag","Leather Crossbody Bag","Accessories","One size","Excellent",64,180,"Unisex","Apparel & Accessories > Handbags, Wallets & Cases > Handbags","Tan",600,"Leather","A structured tan leather bag with a fold-over flap, gold-tone buckle and a sturdy strap you can wear crossbody or by hand.",True),
 ("wool-blend-scarf","Wool-Blend Scarf","Accessories","One size","Like new",24,70,"Unisex","Apparel & Accessories > Clothing Accessories > Scarves & Shawls","Rust and mustard",220,"Wool blend","A cosy striped scarf in rust, cream and mustard with fringed ends. Long enough to wrap twice.",False),
 ("oversized-fleece-hoodie","Oversized Fleece Hoodie","Tops","L","Good",40,100,"Unisex","Apparel & Accessories > Clothing > Clothing Tops > Hoodies","Sage",750,"Cotton-polyester fleece","A roomy sage-green hoodie with a kangaroo pocket, drawstring hood and ribbed cuffs. Warm and easy to throw on.",False),
 ("tailored-wool-blazer","Tailored Wool Blazer","Tailoring","10","Excellent",72,240,"Women",COAT,"Forest green",800,"Wool blend","A single-breasted forest-green blazer with notch lapels, flap pockets and a structured shoulder for work or weekends.",True),
 ("canvas-overshirt","Canvas Overshirt","Outerwear","M","Good",42,110,"Men",COAT,"Olive",600,"Cotton canvas","A sturdy olive overshirt with a spread collar, twin chest pockets and a full button placket. Wear it as a shirt or a light jacket.",False),
]
rows = []
for i,(h,t,typ,size,cond,price,comp,aud,cat,col,g,fab,blurb,new) in enumerate(P,1):
    tags = [f"Condition: {cond}", aud, f"Colour: {col}"] + (["New in"] if new else [])
    body = (f"<p>{blurb}</p><ul><li>Fabric: {fab}</li><li>Size: {size}</li>"
            f"<li>Condition: {cond}. {COND[cond]}</li><li>Measurements available on request</li></ul>"
            f"<p>Rehomed instead of landfilled: buying this piece keeps it in use and out of the waste stream.</p>")
    rows.append({
     "Handle":h,"Title":t,"Body (HTML)":body,"Vendor":"Thrice Loved","Product Category":cat,"Type":typ,
     "Tags":", ".join(tags),"Published":"TRUE","Option1 Name":"Size","Option1 Value":size,
     "Variant SKU":f"TL-{i:03d}","Variant Grams":g,"Variant Inventory Tracker":"shopify","Variant Inventory Qty":1,
     "Variant Inventory Policy":"deny","Variant Fulfillment Service":"manual","Variant Price":f"{price:.2f}",
     "Variant Compare At Price":f"{comp:.2f}","Variant Requires Shipping":"TRUE","Variant Taxable":"TRUE",
     "Image Src":"","Image Position":"","Image Alt Text":"","Gift Card":"FALSE",
     "SEO Title":f"{t} | Pre-loved fashion | Thrice Loved",
     "SEO Description":f"Pre-loved {t.lower()} in {cond.lower()} condition, size {size}. One-of-one, shipped plastic-free from Auckland.",
     "Variant Weight Unit":"g","Status":"active"})
with open(OUT,"w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL); w.writeheader(); w.writerows(rows)
# validate
with open(OUT,newline="",encoding="utf-8") as f:
    r = csv.DictReader(f); got = list(r)
    assert r.fieldnames == COLS and len(got)==12 and all(None not in x for x in got)
    assert len({x["Handle"] for x in got})==12
    assert all(sum(t.startswith("Condition: ") for t in x["Tags"].split(", "))==1 for x in got)
    print("OK rows:",len(got),"new-in:",sum("New in" in x["Tags"] for x in got))
