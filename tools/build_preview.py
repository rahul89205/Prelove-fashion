#!/usr/bin/env python3
"""Builds preview/index.html: a self-contained, clickable preview of the Thrice Loved theme.
Uses the theme's own theme.css, the product CSV and the product images."""
import base64, csv, io, json, pathlib
from PIL import Image

ROOT = pathlib.Path('/home/claude/thrice-loved')
css = (ROOT / 'theme/assets/theme.css').read_text()
rows = list(csv.DictReader(open(ROOT / 'store-data/products.csv', encoding='utf-8')))


def data_uri(path, size, q=78):
    im = Image.open(path).convert('RGB')
    im.thumbnail(size)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


products = []
for r in rows:
    tags = [t.strip() for t in r['Tags'].split(',')]
    cond = next((t.split(':', 1)[1].strip() for t in tags if t.startswith('Condition:')), '')
    colour = next((t.split(':', 1)[1].strip() for t in tags if t.startswith('Colour:')), '')
    products.append({
        'handle': r['Handle'], 'title': r['Title'], 'body': r['Body (HTML)'], 'type': r['Type'],
        'size': r['Option1 Value'], 'price': float(r['Variant Price']),
        'was': float(r['Variant Compare At Price'] or 0), 'condition': cond, 'colour': colour,
        'new': 'New in' in tags, 'sku': r['Variant SKU'],
        'img': data_uri(ROOT / f"store-data/product-images/{r['Handle']}.png", (560, 700)),
        'imgLarge': data_uri(ROOT / f"store-data/product-images/{r['Handle']}.png", (900, 1125), 80),
    })

hero = data_uri(ROOT / 'theme/assets/hero-flatlay.png', (1200, 900), 80)

html = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Thrice Loved – pre-loved fashion (theme preview)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#F6F1E7;--ink:#1B1B1B;--primary:#1F3D2F;--accent:#C65D3B;--sand:#E8DCC8;--sage:#A9B8A0}
__CSS__
.preview-pill{position:fixed;left:12px;bottom:12px;z-index:90;background:#1B1B1B;color:#fff;font-size:.72rem;padding:.35rem .8rem;border-radius:999px;opacity:.85}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:var(--primary);color:#fff;padding:.8rem 1.2rem;border-radius:14px;z-index:95;max-width:92vw;font-size:.92rem;box-shadow:0 12px 30px rgba(0,0,0,.25)}
button.link{background:none;border:0;padding:0;cursor:pointer;text-decoration:underline}
</style></head>
<body>
<div id="app"></div>
<div class="preview-pill">Design preview &middot; the real store runs on Shopify</div>
<script>
const P = __PRODUCTS__;
const HERO = "__HERO__";
const money = n => '$' + n.toFixed(2).replace(/\.00$/, '');
let bag = [];
const byHandle = h => P.find(p => p.handle === h);
const pct = p => Math.round((p.was - p.price) * 100 / p.was);
const icon = {
 bag:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
 search:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>',
 menu:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 recycle:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7h8l-2-2M15 7l-2 2"/><path d="M17 12l3 5h-5M20 17l-4 1"/><path d="M10 18H4l3-5M4 18l3 1"/></svg>',
 box:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8l9-5 9 5v8l-9 5-9-5V8z"/><path d="M3 8l9 5 9-5M12 13v8"/></svg>',
 tag:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12V4h8l10 10-8 8L3 12z"/><circle cx="7.5" cy="8.5" r="1.2"/></svg>',
 truck:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M2 6h12v10H2zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/></svg>',
 leaf:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19c3-5 6-8 10-10"/></svg>',
 heart:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/></svg>'
};
const links = [['Shop all','#/shop'],['New in','#/shop/new'],['Sustainability','#/sustainability'],['Sell with us','#/sell']];

const header = () => `
<div class="announcement"><p>Every piece is one-of-one &nbsp;·&nbsp; Free NZ shipping over $100 &nbsp;·&nbsp; Plastic-free packaging</p></div>
<header class="header"><div class="container header__inner">
 <details class="mobile-nav"><summary aria-label="Menu">${icon.menu}</summary><nav class="mobile-nav__panel">${links.map(l=>`<a href="${l[1]}">${l[0]}</a>`).join('')}</nav></details>
 <nav class="nav">${links.map(l=>`<a href="${l[1]}">${l[0]}</a>`).join('')}</nav>
 <a class="logo" href="#/"><span class="logo__dot"></span><span>Thrice Loved</span></a>
 <div class="header__icons"><a class="icon-btn" href="#/shop" aria-label="Search">${icon.search}</a>
 <a class="icon-btn" href="#/bag" aria-label="Bag">${icon.bag}<span class="cart-count" data-empty="${bag.length===0}">${bag.length}</span></a></div>
</div></header>`;

const footer = () => `
<footer class="footer"><div class="container"><div class="footer__grid">
 <div><a class="logo" href="#/"><span class="logo__dot"></span><span>Thrice Loved</span></a><p class="footer__about">Pre-loved fashion from Auckland. Every piece is hand-picked, honestly graded and given a third life.</p></div>
 <div><h4>Shop</h4><ul><li><a href="#/shop">Shop all</a></li><li><a href="#/shop/new">New in</a></li><li><a href="#/shop/Outerwear">Outerwear</a></li><li><a href="#/shop/Denim">Denim</a></li></ul></div>
 <div><h4>Thrice Loved</h4><ul><li><a href="#/sustainability">Our promise</a></li><li><a href="#/sell">Sell with us</a></li></ul></div>
 <div><h4>Help</h4><ul><li><a href="#/bag">Your bag</a></li></ul></div>
 <div><h4>Join the loop</h4><p style="font-size:.92rem">New arrivals, drops and sustainability tips. No spam.</p><form onsubmit="event.preventDefault();toast('Thanks for subscribing!')"><input type="email" placeholder="you@email.com" required><button class="btn">Subscribe</button></form></div>
</div><div class="footer__bottom"><span>&copy; 2026 Thrice Loved. Pre-loved, never wasted.</span><span>Secure checkout by Shopify</span></div></div></footer>`;

const card = p => `
<article class="card"><div class="card__badges"><span class="badge badge--${p.condition.toLowerCase().replace(/ /g,'-')}">${p.condition}</span><span class="badge badge--sale">${pct(p)}% off new</span></div>
<a class="card__media" href="#/product/${p.handle}"><img src="${p.img}" alt="${p.title}" loading="lazy"></a>
<div class="card__body"><h3 class="card__title"><a href="#/product/${p.handle}">${p.title}</a></h3><p class="card__meta">Size ${p.size}</p>
<div class="price price--sale"><span class="price__now">${money(p.price)}</span><s class="price__was">${money(p.was)}</s></div></div></article>`;

const grid = list => `<ul class="grid">${list.map(p=>`<li>${card(p)}</li>`).join('')}</ul>`;

const impact = (eyebrow, heading, text) => `
<section class="section impact"><div class="container"><span class="eyebrow">${eyebrow}</span><h2>${heading}</h2><p class="lead">${text}</p>
<div class="impact__grid">
 <div class="stat"><div class="stat__num">220,000 t</div><p class="stat__label">of textiles are thrown away in New Zealand every year</p><p class="stat__src">Estimate: WasteMINZ</p></div>
 <div class="stat"><div class="stat__num">1 of 1</div><p class="stat__label">every piece is a one-off, so nothing is made that does not need to be</p><p class="stat__src">Our model</p></div>
 <div class="stat"><div class="stat__num">100%</div><p class="stat__label">of orders ship in recycled or compostable packaging</p><p class="stat__src">Our promise</p></div>
</div></div></section>`;

const how = (h, steps) => `
<section class="section"><div class="container"><div class="section-head"><h2>${h}</h2></div><ol class="steps">${steps.map((s,i)=>`<li class="step"><span class="step__num">${i+1}</span><h3>${s[0]}</h3><p>${s[1]}</p></li>`).join('')}</ol></div></section>`;

const cta = () => `
<section class="section section--tight"><div class="container"><div class="cta cta--terracotta"><span class="eyebrow">Sell with us</span><h2>Got good clothes you no longer wear?</h2><p>Send us your pre-loved pieces and earn store credit. We handle the photos, listing and packing, and your clothes find a new home.</p><a class="btn btn--light" href="#/sell">Start selling</a></div></div></section>`;

const views = {
 home: () => `
<section class="hero"><div class="container hero__grid"><div class="hero__text"><span class="eyebrow">Pre-loved fashion · Auckland</span><h1>Good clothes deserve a third life.</h1>
<p class="lead">Hand-picked, honestly graded second-hand fashion. Every piece is one-of-one, shipped plastic-free, and kept out of landfill.</p>
<div class="hero__actions"><a class="btn" href="#/shop/new">Shop new arrivals</a><a class="btn btn--ghost" href="#/sustainability">Our promise</a></div></div>
<div class="hero__media"><img src="${HERO}" alt="Flat lay of pre-loved clothing"><span class="hero__badge">100% pre-loved</span></div></div></section>
<div class="values"><div class="container"><ul class="values__list">
 <li class="values__item">${icon.recycle}<span>100% pre-loved</span></li><li class="values__item">${icon.box}<span>Plastic-free packaging</span></li>
 <li class="values__item">${icon.tag}<span>Honest condition grading</span></li><li class="values__item">${icon.truck}<span>Free NZ shipping over $100</span></li></ul></div></div>
<section class="section"><div class="container"><div class="section-head"><h2>Shop by category</h2><a class="link-arrow" href="#/shop">Shop everything</a></div><div class="tiles">
 <a class="tile tile--sage" href="#/shop/Outerwear"><span class="tile__arrow">&nearr;</span><h3>Outerwear</h3><p>Jackets, coats &amp; overshirts</p></a>
 <a class="tile tile--terracotta" href="#/shop/Knitwear"><span class="tile__arrow">&nearr;</span><h3>Knitwear</h3><p>Merino &amp; wool-blend</p></a>
 <a class="tile tile--blue" href="#/shop/Denim"><span class="tile__arrow">&nearr;</span><h3>Denim</h3><p>Jeans that already have a story</p></a>
 <a class="tile tile--mustard" href="#/shop/Accessories"><span class="tile__arrow">&nearr;</span><h3>Accessories</h3><p>Bags, scarves &amp; more</p></a></div></div></section>
<section class="section" style="padding-top:0"><div class="container"><div class="section-head"><h2>Just rehomed</h2><a class="link-arrow" href="#/shop">View all</a></div>${grid(P.filter(p=>p.new).slice(0,8))}</div></section>
${impact('Why pre-loved','The most sustainable garment is the one that already exists.','Buying second-hand extends the life of clothing that has already been made, and keeps it out of the landfill.')}
${how('How a piece gets its third life',[['Sourced','We collect quality garments from Auckland closets, so they never reach landfill.'],['Checked &amp; graded','Each piece is inspected, cleaned and given an honest grade: Like new, Excellent or Good.'],['Packed plastic-free','Orders go out in recycled paper mailers with paper tape. No bubble wrap, no plastic bags.'],['Loved again','Finished with it? Send it back for store credit and it enters the loop again.']])}
${cta()}
<section class="section newsletter center"><div class="container"><h2>Be first to see new arrivals</h2><p class="lead">Every piece is one-of-one, so the good stuff goes fast. Get a heads-up when new drops land.</p>
<form onsubmit="event.preventDefault();toast('Thanks for subscribing – check your inbox!')"><input type="email" placeholder="you@email.com" required><button class="btn">Subscribe</button></form></div></section>`,

 shop: (arg) => {
   let list = P.slice(), title = 'All pieces';
   if (arg === 'new') { list = P.filter(p=>p.new); title = 'New in'; }
   else if (arg) { list = P.filter(p=>p.type === arg); title = arg; }
   const sort = sortMode;
   if (sort === 'low') list.sort((a,b)=>a.price-b.price); else if (sort === 'high') list.sort((a,b)=>b.price-a.price);
   const types = [...new Set(P.map(p=>p.type))];
   return `<div class="container"><header class="collection-head"><h1>${title}</h1><p>Every piece is one-of-one. When it's gone, it's gone.</p></header>
   <div class="toolbar"><div class="filters"><a class="filter summary" style="text-decoration:none"></a>${['All',...types].map(t=>`<a class="btn ${((arg||'All')===t)?'':'btn--ghost'}" style="padding:.4rem .9rem;font-size:.85rem" href="#/shop${t==='All'?'':'/'+t}">${t}</a>`).join('')}</div>
   <span class="toolbar__count">${list.length} pieces</span>
   <div class="toolbar__controls"><select onchange="sortMode=this.value;render()" aria-label="Sort"><option value="new" ${sort==='new'?'selected':''}>Newest</option><option value="low" ${sort==='low'?'selected':''}>Price: low to high</option><option value="high" ${sort==='high'?'selected':''}>Price: high to low</option></select></div></div>
   ${grid(list)}<div style="height:72px"></div></div>`;
 },

 product: (handle) => {
   const p = byHandle(handle); if (!p) return views.shop();
   const inBag = bag.includes(p.handle);
   const related = P.filter(x=>x.handle!==p.handle).slice(0,4);
   return `<div class="container product"><div class="product__gallery gallery"><div class="gallery__main"><img src="${p.imgLarge}" alt="${p.title}"></div></div>
   <div class="product__info"><p class="product__vendor">Thrice Loved</p><h1 class="product__title">${p.title}</h1>
   <div class="product__price"><div class="price price--sale"><span class="price__now">${money(p.price)}</span><s class="price__was">${money(p.was)}</s><span class="save-pill">${pct(p)}% off new</span></div>
   <p style="font-size:.8rem;font-weight:400;color:rgba(0,0,0,.55);margin:.3rem 0 0">Crossed-out price is the estimated price when new.</p></div>
   <div class="chips"><span class="chip">${icon.tag} Condition: ${p.condition}</span><span class="chip">${icon.recycle} Pre-loved</span><span class="chip">${icon.heart} One-of-one</span></div>
   <p class="stock-note">Only 1 available – once it is gone, it is gone.</p>
   <div class="product__buy"><div class="field"><label>Size</label><select disabled><option>${p.size}</option></select></div>
   <button class="btn btn--block" ${inBag?'disabled':''} onclick="addBag('${p.handle}')">${inBag?'In your bag':'Add to bag'}</button></div>
   <div class="product__eco">${icon.leaf}<p><strong>Saved from landfill</strong><br>Buying this pre-loved piece extends the life of a garment that already exists. It ships in recycled, plastic-free packaging.</p></div>
   <div class="accordion"><details open><summary>Details</summary><div class="accordion__body">${p.body}</div></details>
   <details><summary>Condition guide</summary><div class="accordion__body"><p><strong>Like new:</strong> worn once or twice, no visible wear.</p><p><strong>Excellent:</strong> lightly worn with minor signs of use only.</p><p><strong>Good:</strong> clearly worn but sound. Any flaws are described in the details.</p></div></details>
   <details><summary>Shipping &amp; returns</summary><div class="accordion__body"><p>Free NZ shipping over $100, otherwise flat-rate courier. Orders are packed in recycled paper mailers within 2 business days.</p><p>Returns accepted within 7 days of delivery for unworn items in the condition they were sent.</p></div></details></div></div></div>
   <section class="section section--tight"><div class="container"><div class="section-head"><h2>You might also love</h2><a class="link-arrow" href="#/shop">Shop all</a></div>${grid(related)}</div></section>`;
 },

 bag: () => {
   if (!bag.length) return `<div class="container cart"><h1>Your bag</h1><div class="empty"><p class="lead" style="margin-inline:auto">Your bag is empty – but there are plenty of one-of-one pieces waiting for a new home.</p><a class="btn" href="#/shop">Start shopping</a></div></div>`;
   const items = bag.map(byHandle); const total = items.reduce((s,p)=>s+p.price,0);
   return `<div class="container cart"><h1>Your bag</h1><div class="cart__layout"><ul class="cart__items">${items.map(p=>`
   <li class="cart__item"><a href="#/product/${p.handle}"><img src="${p.img}" alt=""></a><div><a href="#/product/${p.handle}" style="font-weight:600;text-decoration:none">${p.title}</a><p class="card__meta">Size ${p.size}</p><div class="price"><span class="price__now">${money(p.price)}</span></div></div>
   <div class="cart__line"><span class="cart__qty" style="padding:.5rem 0">Qty 1</span><button class="link cart__remove" onclick="removeBag('${p.handle}')">Remove</button><strong>${money(p.price)}</strong></div></li>`).join('')}</ul>
   <div class="cart__summary"><div class="cart__total"><span>Subtotal</span><span>${money(total)}</span></div><p class="cart__note">Taxes included where applicable. Shipping is calculated at checkout.</p>
   <button class="btn btn--accent btn--block" onclick="toast('In the live store this opens Shopify’s secure checkout.')">Checkout</button>
   <p class="cart__note" style="display:flex;gap:.5rem;align-items:center;margin:0"><span style="width:20px;color:var(--primary)">${icon.box}</span>Ships in recycled, plastic-free packaging.</p></div></div></div>`;
 },

 sustainability: () => `
<section class="section section--tight"><div class="container"><span class="eyebrow">Our promise</span><h1>Fashion without the footprint</h1><div class="lead"><p>Making a brand-new garment takes land, water, energy and labour. The most sustainable piece in your wardrobe is the one that already exists. That is the whole idea behind our store.</p></div></div></section>
${impact('The problem','Too many good clothes end up in landfill.',"Most of New Zealand's discarded clothing is still wearable. We give it somewhere better to go.")}
${how('What we do differently',[['Source locally','Pieces come from Auckland closets and clear-outs, with no overseas shipping of stock.'],['Clean &amp; repair','Items are washed and given small repairs before listing.'],['Pack with care','Recycled paper mailers, paper tape and recycled-card labels. Nothing plastic.'],['Close the loop','Customers can return pieces for store credit, so garments keep circulating.']])}
<section class="section"><div class="container"><h2>Good questions</h2><div class="accordion" style="max-width:820px">
 <details><summary>Is buying second-hand really more sustainable?</summary><div class="accordion__body"><p>Yes. Every garment you buy pre-loved is one that does not need to be made from scratch, and one that does not go to landfill.</p></div></details>
 <details><summary>How do you grade condition?</summary><div class="accordion__body"><p>Like new: worn once or twice. Excellent: lightly worn. Good: clearly worn but sound; flaws are listed on the product page.</p></div></details>
 <details><summary>What happens to items you cannot sell?</summary><div class="accordion__body"><p>Unsold pieces are donated to local charity shops or passed on to a textile recycler.</p></div></details></div></div></section>`,

 sell: () => `
<section class="section section--tight"><div class="container"><span class="eyebrow">Sell with us</span><h1>Turn your wardrobe into store credit</h1><div class="lead"><p>Have good-quality clothes you no longer wear? Send them our way. We photograph, list and pack each piece, and you earn store credit when it sells.</p></div></div></section>
${how('How it works',[['Tell us what you have','Fill in the form below with a short description of your items.'],['We review','We reply within 2 business days with what we can accept and the credit on offer.'],['Send or drop off','Post your parcel in reused packaging, or arrange a drop-off in Auckland.'],['Earn credit','When your pieces sell, store credit lands in your account.']])}
<section class="section section--tight"><div class="container" style="max-width:620px"><h2>Tell us what you would like to sell</h2>
<form onsubmit="event.preventDefault();toast('Thanks – we will reply within 2 business days.')"><div class="field"><label>Name</label><input type="text" required></div><div class="field"><label>Email</label><input type="email" required></div><div class="field"><label>What would you like to sell?</label><input type="text" placeholder="e.g. 8 tops, 2 coats, 3 pairs of jeans"></div><div class="field"><label>Message</label><textarea></textarea></div><button class="btn">Send message</button></form></div></section>`
};

function toast(msg){ const t=document.createElement('div'); t.className='toast'; t.textContent=msg; document.body.appendChild(t); setTimeout(()=>t.remove(),3200); }
function addBag(h){ if(!bag.includes(h)) bag.push(h); render(); toast('Added to your bag'); }
function removeBag(h){ bag = bag.filter(x=>x!==h); render(); }

let route = '', sortMode = 'new';
function go(r){ route = r; render(); window.scrollTo(0,0); }
document.addEventListener('click', e => {
  const a = e.target.closest('a[href^="#/"]');
  if (!a) return;
  e.preventDefault(); go(a.getAttribute('href').slice(2));
});
function render(){
  const raw = route;
  const [view, arg] = raw.split('/');
  const v = view || 'home';
  const fn = views[v] || views.home;
  document.getElementById('app').innerHTML = header() + '<main>' + fn(arg ? decodeURIComponent(arg) : undefined) + '</main>' + footer();
}
render();
</script></body></html>"""

html = (html.replace('__CSS__', css)
            .replace('__PRODUCTS__', json.dumps(products, ensure_ascii=False))
            .replace('__HERO__', hero))
out = ROOT / 'preview'
out.mkdir(exist_ok=True)
(out / 'index.html').write_text(html, encoding='utf-8')
print('preview size KB:', len(html) // 1024)
