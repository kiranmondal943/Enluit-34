import streamlit as st
import zipfile
import io
import json
import datetime
import re
import requests

# --- 0. STATE MANAGEMENT (AI INTEGRATION) ---
# We initialize session state for all inputs so AI can overwrite them dynamically.
def init_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

init_state('hero_h', "Stop Paying Rent for Your Website.")
init_state('hero_sub', "The Titan Engine is the world’s first 0.1s website architecture. Pay once. Own it forever.")
init_state('about_h', "Control Your Empire from a Spreadsheet")
init_state('about_short', "No WordPress dashboard. No plugins to update. Just open your private Google Sheet.")
init_state('feat_data', "bolt | Speed | Loads in 0.1s\nwallet | Cost | $0 Monthly Fees\nshield | Secure | Unhackable Static Site")

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Titan v34.0 | AI & PWA Enabled", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED UI SYSTEM (CSS) ---
st.markdown("""
    <style>
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    .stTextInput input, .stTextArea textarea { border-radius: 8px !important; border: 1px solid #cbd5e1; }
    .stButton>button { border-radius: 8px; font-weight: 700; text-transform: uppercase; transition: 0.2s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    
    /* AI Badge */
    .ai-badge { background: linear-gradient(90deg, #6366f1, #a855f7); color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: THE CONTROL CENTER ---
with st.sidebar:
    st.title("⚡ Titan Architect")
    st.caption("v34.0 | AI, PWA & Commerce")
    
    # --- FEATURE 1: ROBOTIC AI CONTENT GENERATOR ---
    with st.expander("🤖 Titan AI Generator", expanded=True):
        st.info("Auto-write your website using AI.")
        groq_key = st.text_input("Groq API Key (Free)", type="password", help="Get free key at console.groq.com")
        biz_type = st.text_input("Business Description", placeholder="e.g., Luxury Dental Clinic in Dubai specializing in veneers")
        
        if st.button("✨ Generate Site Content"):
            if not groq_key or not biz_type:
                st.error("Please provide API Key and Description.")
            else:
                try:
                    with st.spinner("Titan AI is architecting your copy..."):
                        # PROMPT ENGINEERING
                        prompt = f"""
                        You are a high-conversion copywriter. Return ONLY a JSON object (no markdown) for a website for: {biz_type}.
                        Keys required:
                        - hero_h (Catchy 5-7 word headline)
                        - hero_sub (2 sentences explaining value)
                        - about_h (Engaging title)
                        - about_short (2-3 sentences summary)
                        - feat_data (3 lines format: iconname | Title | Description. Use icons: bolt, wallet, star, heart, shield, truck)
                        """
                        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                        payload = {
                            "messages": [{"role": "user", "content": prompt}],
                            "model": "llama3-8b-8192",
                            "response_format": {"type": "json_object"}
                        }
                        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                        data = response.json()['choices'][0]['message']['content']
                        js_res = json.loads(data)
                        
                        # UPDATE STATE
                        st.session_state.hero_h = js_res.get('hero_h', st.session_state.hero_h)
                        st.session_state.hero_sub = js_res.get('hero_sub', st.session_state.hero_sub)
                        st.session_state.about_h = js_res.get('about_h', st.session_state.about_h)
                        st.session_state.about_short = js_res.get('about_short', st.session_state.about_short)
                        st.session_state.feat_data = js_res.get('feat_data', st.session_state.feat_data)
                        st.success("AI Generation Complete! Check the tabs.")
                except Exception as e:
                    st.error(f"AI Error: {str(e)}")

    st.divider()
    
    # 3.1 VISUAL DNA
    with st.expander("🎨 Visual DNA", expanded=False):
        theme_mode = st.selectbox("Base Theme", ["Clean Corporate (Light)", "Midnight SaaS (Dark)", "Luxury Gold", "Forest Eco"])
        p_color = st.color_picker("Primary Brand", "#0F172A") 
        s_color = st.color_picker("Action (CTA)", "#EF4444")  
        h_font = st.selectbox("Headings", ["Montserrat", "Playfair Display", "Oswald", "Inter"])
        b_font = st.selectbox("Body Text", ["Inter", "Open Sans", "Roboto", "Lora"])

    # 3.2 MODULE MANAGER
    with st.expander("🧩 Section Manager", expanded=False):
        show_hero = st.checkbox("Hero Carousel", True)
        show_features = st.checkbox("Feature Grid", True)
        show_inventory = st.checkbox("Store / Inventory", True)
        show_booking = st.checkbox("Booking Engine", True) # NEW
        show_faq = st.checkbox("F.A.Q.", True)

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ Titan Site Builder v34")

tabs = st.tabs(["1. Identity & PWA", "2. Content (AI)", "3. Commerce & Cart", "4. Booking", "5. Portfolio", "6. Footer"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "StopWebRent.com")
        biz_phone = st.text_input("Phone (No +)", "966572562151")
        biz_email = st.text_input("Email", "hello@kaydiemscriptlab.com")
    with c2:
        prod_url = st.text_input("Website URL", "https://www.stopwebrent.com")
        logo_url = st.text_input("Logo URL")
        
    st.subheader("📱 PWA Configuration (App Install)")
    st.info("Titan will auto-generate manifest.json so users can install your site as an App.")
    pwa_short = st.text_input("App Short Name", biz_name[:12])
    pwa_desc = st.text_input("App Description", "Official App")
    pwa_icon = st.text_input("App Icon URL (PNG 512x512)", logo_url)

with tabs[1]:
    st.subheader("Hero Section (AI Editable)")
    hero_h = st.text_input("Hero Headline", key="hero_h")
    hero_sub = st.text_area("Hero Subtext", key="hero_sub")
    
    hc1, hc2 = st.columns(2)
    hero_img_1 = hc1.text_input("Hero Image 1", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1600")
    hero_img_2 = hc2.text_input("Hero Image 2", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1600")
    
    st.divider()
    st.subheader("Features & Value (AI Editable)")
    f_title = st.text_input("Features Title", "Why Choose Us")
    feat_data = st.text_area("Features List (icon | Title | Desc)", key="feat_data", height=150)
    
    st.subheader("About Section")
    about_h = st.text_input("About Title", key="about_h")
    about_short = st.text_area("About Text", key="about_short")
    about_img = st.text_input("About Side Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")

with tabs[2]:
    st.subheader("🛒 Commerce & Payments")
    st.markdown("Enable a Shopping Cart and Payment Links (Stripe/PayPal/UPI).")
    
    currency_sym = st.text_input("Currency Symbol", "$")
    
    col_pay1, col_pay2 = st.columns(2)
    paypal_me = col_pay1.text_input("PayPal.me Link (Optional)", "https://paypal.me/yourname")
    upi_id = col_pay2.text_input("UPI ID (India Only)", "")
    
    st.info("💡 **Pro Tip:** In your Inventory CSV, add a column named `StripeLink`. If filled, the 'Buy Now' button will go to Stripe. If empty, it adds to the WhatsApp Cart.")

with tabs[3]:
    st.subheader("📅 Booking Engine")
    st.markdown("Integrate Calendly, Cal.com, or Google Calendar.")
    booking_embed = st.text_area("Paste Embed Code (iframe)", height=150, placeholder='<iframe src="https://calendly.com/..." ...></iframe>')
    booking_title = st.text_input("Booking Page Title", "Book an Appointment")
    booking_sub = st.text_input("Booking Page Subtext", "Select a time slot that works for you.")

with tabs[4]:
    st.subheader("Portfolio/Inventory")
    sheet_url = st.text_input("Google Sheet CSV Link", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    custom_feat = st.text_input("Fallback Image URL", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800")
    st.caption("Required CSV Columns: Name, Price, Description, ImageURL. **Optional: StripeLink**")

with tabs[5]:
    st.subheader("Footer & Social")
    fb_link = st.text_input("Facebook URL")
    ig_link = st.text_input("Instagram URL")
    x_link = st.text_input("X (Twitter) URL")
    biz_addr = st.text_area("Address", "123 Business Rd, Tech City")

# --- 5. COMPILER ENGINE (ADVANCED GENERATORS) ---

def get_theme_css():
    # ... (Keep existing Theme Logic) ...
    bg_color, text_color, card_bg = "#ffffff", "#0f172a", "#ffffff"
    if "Midnight" in theme_mode:
        bg_color, text_color, card_bg = "#0f172a", "#f8fafc", "#1e293b"
    elif "Luxury" in theme_mode:
        bg_color, text_color, card_bg = "#1c1c1c", "#D4AF37", "#2a2a2a"
    
    return f"""
    :root {{ --p: {p_color}; --s: {s_color}; --bg: {bg_color}; --txt: {text_color}; --card: {card_bg}; --font-h: '{h_font}'; --font-b: '{b_font}'; }}
    body {{ background: var(--bg); color: var(--txt); font-family: var(--font-b), sans-serif; margin: 0; padding-bottom: 80px; }}
    h1, h2, h3 {{ font-family: var(--font-h), sans-serif; color: var(--p); }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    .btn {{ background: var(--p); color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold; border:none; cursor:pointer; }}
    .btn-accent {{ background: var(--s); }}
    .card {{ background: var(--card); padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid rgba(128,128,128,0.1); }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
    
    /* CART FLOATING BUTTON */
    #cart-float {{ position: fixed; bottom: 20px; left: 20px; background: var(--p); color: white; padding: 15px 20px; border-radius: 50px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); cursor: pointer; z-index: 999; display: flex; align-items: center; gap: 10px; font-weight: bold; }}
    #cart-modal {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); width: 90%; max-width: 500px; padding: 2rem; border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.3); z-index: 1000; border: 1px solid rgba(128,128,128,0.2); }}
    #cart-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999; }}
    .cart-item {{ display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0; }}
    
    /* NAV */
    nav {{ padding: 1rem 0; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 100; border-bottom: 1px solid rgba(128,128,128,0.1); }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    """

def gen_js_cart_system():
    """Generates the JavaScript for the Shopping Cart, Stripe, and WhatsApp Logic."""
    return f"""
    <script>
    // --- TITAN COMMERCE ENGINE v1.0 ---
    let cart = JSON.parse(localStorage.getItem('titanCart')) || [];
    const currency = "{currency_sym}";
    const waNumber = "{biz_phone}";
    
    function renderCart() {{
        const cartList = document.getElementById('cart-items');
        const cartCount = document.getElementById('cart-count');
        const cartTotal = document.getElementById('cart-total');
        
        if(!cartList) return;
        
        cartList.innerHTML = '';
        let total = 0;
        
        cart.forEach((item, index) => {{
            total += parseFloat(item.price);
            cartList.innerHTML += `
                <div class="cart-item">
                    <span>${{item.name}}</span>
                    <div style="display:flex; gap:10px; align-items:center;">
                        <span>${{currency}}${{item.price}}</span>
                        <button onclick="removeFromCart(${{index}})" style="color:red; background:none; border:none; cursor:pointer;">&times;</button>
                    </div>
                </div>`;
        }});
        
        cartCount.innerText = cart.length;
        cartTotal.innerText = currency + total.toFixed(2);
        localStorage.setItem('titanCart', JSON.stringify(cart));
        
        // Show/Hide Floating Button
        document.getElementById('cart-float').style.display = cart.length > 0 ? 'flex' : 'none';
    }}
    
    function addToCart(name, price, stripeLink) {{
        // If Stripe Link exists, redirect immediately (Single Product Checkout)
        if(stripeLink && stripeLink.length > 5) {{
            window.location.href = stripeLink;
            return;
        }}
        // Otherwise add to WhatsApp Cart
        cart.push({{name: name, price: price}});
        renderCart();
        alert(name + " added to cart!");
    }}
    
    function removeFromCart(index) {{
        cart.splice(index, 1);
        renderCart();
    }}
    
    function toggleCart() {{
        const modal = document.getElementById('cart-modal');
        const overlay = document.getElementById('cart-overlay');
        const display = modal.style.display === 'block' ? 'none' : 'block';
        modal.style.display = display;
        overlay.style.display = display;
    }}
    
    function checkoutWhatsApp() {{
        let msg = "Hi, I would like to place an order:%0A";
        let total = 0;
        cart.forEach(item => {{
            msg += "- " + item.name + " (" + currency + item.price + ")%0A";
            total += parseFloat(item.price);
        }});
        msg += "%0ATotal: " + currency + total.toFixed(2);
        
        // Add Payment Links if configured
        const upi = "{upi_id}";
        const paypal = "{paypal_me}";
        
        if(upi) msg += "%0A%0APayment via UPI: " + upi;
        if(paypal) msg += "%0A%0APayment via PayPal: " + paypal;
        
        window.open("https://wa.me/" + waNumber + "?text=" + msg, '_blank');
        localStorage.removeItem('titanCart');
        cart = [];
        renderCart();
        toggleCart();
    }}
    
    // Initial Render
    window.addEventListener('load', renderCart);
    </script>
    """

def gen_pwa_manifest():
    """Generates manifest.json for Installable App"""
    return json.dumps({
        "name": biz_name,
        "short_name": pwa_short,
        "start_url": "./index.html",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": p_color,
        "description": pwa_desc,
        "icons": [{
            "src": pwa_icon,
            "sizes": "512x512",
            "type": "image/png"
        }]
    })

def gen_service_worker():
    """Generates service-worker.js for Offline Capability"""
    return """
    self.addEventListener('install', (e) => {
      e.waitUntil(
        caches.open('titan-store').then((cache) => cache.addAll([
          './index.html',
        ])),
      );
    });
    self.addEventListener('fetch', (e) => {
      e.respondWith(
        caches.match(e.request).then((response) => response || fetch(e.request)),
      );
    });
    """

def gen_nav():
    return f"""
    <nav><div class="container nav-flex">
        <div style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</div>
        <div>
            <a href="index.html" class="btn" style="background:transparent; color:var(--txt)">Home</a>
            {f'<a href="booking.html" class="btn" style="background:transparent; color:var(--txt)">Book Now</a>' if show_booking else ''}
            <a href="#inventory" class="btn" style="background:transparent; color:var(--txt)">Store</a>
            <a href="tel:{biz_phone}" class="btn btn-accent">Call Us</a>
        </div>
    </div></nav>
    """

def gen_cart_html():
    return f"""
    <div id="cart-float" onclick="toggleCart()" style="display:none;">
        <span>🛒</span> <span id="cart-count">0</span>
    </div>
    <div id="cart-overlay" onclick="toggleCart()"></div>
    <div id="cart-modal">
        <h3>Your Cart</h3>
        <div id="cart-items" style="max-height:300px; overflow-y:auto; margin:1rem 0;"></div>
        <div style="font-weight:bold; font-size:1.2rem; margin-bottom:1rem; text-align:right;">Total: <span id="cart-total">0.00</span></div>
        <button onclick="checkoutWhatsApp()" class="btn btn-accent" style="width:100%">Checkout via WhatsApp</button>
    </div>
    """

def gen_inventory_section():
    if not show_inventory: return ""
    return f"""
    <section id="inventory" style="padding:4rem 0;"><div class="container">
        <h2 style="text-align:center; margin-bottom:3rem;">Our Inventory</h2>
        <div id="inv-grid" class="grid-3"><p>Loading Products...</p></div>
    </div></section>
    
    <script>
    async function loadInv() {{
        try {{
            const res = await fetch('{sheet_url}');
            const txt = await res.text();
            const lines = txt.split(/\\r\\n|\\n/);
            const box = document.getElementById('inv-grid');
            box.innerHTML = '';
            
            // CSV Parsing Logic
            for(let i=1; i<lines.length; i++) {{
                // Simple CSV split (handling commas inside quotes requires regex, keeping simple for demo)
                const row = lines[i].split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/); 
                if(row.length < 2) continue;
                
                const name = row[0].replace(/"/g, '');
                const price = row[1].replace(/"/g, '');
                const desc = row[2] ? row[2].replace(/"/g, '') : '';
                const img = row[3] ? row[3].replace(/"/g, '') : '{custom_feat}';
                const stripe = row.length > 4 ? row[4].replace(/"/g, '') : ''; // Check for Stripe Link
                
                box.innerHTML += `
                <div class="card">
                    <img src="${{img}}" style="width:100%; height:200px; object-fit:cover; border-radius:8px; margin-bottom:1rem;">
                    <h3>${{name}}</h3>
                    <p style="color:var(--s); font-weight:bold;">{currency_sym}${{price}}</p>
                    <p style="font-size:0.9rem; opacity:0.8;">${{desc}}</p>
                    <button onclick="addToCart('${{name}}', '${{price}}', '${{stripe}}')" class="btn" style="width:100%; margin-top:1rem;">
                        ${{stripe ? 'Buy Now (Stripe)' : 'Add to Cart'}}
                    </button>
                </div>
                `;
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    loadInv();
    </script>
    """

def build_page(title, content, extra_head=""):
    css = get_theme_css()
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | {biz_name}</title>
        <link rel="manifest" href="manifest.json">
        <meta name="theme-color" content="{p_color}">
        <link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}:wght@700&family={b_font.replace(' ','+')}:wght@400;600&display=swap" rel="stylesheet">
        <style>{css}</style>
        {extra_head}
    </head>
    <body>
        {gen_nav()}
        {content}
        {gen_cart_html()}
        {gen_js_cart_system()}
        <script>
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('service-worker.js');
        }}
        </script>
    </body>
    </html>
    """

# --- 6. PAGE LOGIC ---
home_content = ""
if show_hero:
    home_content += f"""
    <header style="background:var(--p); color:white; padding:80px 0; text-align:center;">
        <div class="container">
            <h1 style="color:white; font-size:3rem;">{hero_h}</h1>
            <p style="font-size:1.2rem; opacity:0.9; max-width:700px; margin:0 auto 2rem auto;">{hero_sub}</p>
            <a href="#inventory" class="btn btn-accent">Explore Offerings</a>
        </div>
    </header>
    """
if show_features:
    # Basic parser for the Feature text area
    feat_cards = ""
    for line in feat_data.split('\n'):
        if "|" in line:
            parts = line.split('|')
            feat_cards += f'<div class="card"><h3 style="font-size:1.2rem;">{parts[1]}</h3><p>{parts[2]}</p></div>'
    home_content += f'<section style="padding:4rem 0;"><div class="container"><h2 style="text-align:center; margin-bottom:2rem;">{f_title}</h2><div class="grid-3">{feat_cards}</div></div></section>'

home_content += f"""
<section style="background:#f1f5f9; padding:4rem 0;"><div class="container" style="display:flex; gap:3rem; align-items:center; flex-wrap:wrap;">
    <div style="flex:1;"><img src="{about_img}" style="width:100%; border-radius:12px;"></div>
    <div style="flex:1;"><h2>{about_h}</h2><p>{about_short}</p></div>
</div></section>
"""

home_content += gen_inventory_section()

home_content += f"""
<footer style="background:var(--p); color:white; padding:3rem 0; text-align:center; margin-top:auto;">
    <div class="container">
        <h3>{biz_name}</h3>
        <p>{biz_addr}</p>
        <div style="margin-top:1rem;">
            {f'<a href="{fb_link}" style="color:white; margin:0 10px;">Facebook</a>' if fb_link else ''}
            {f'<a href="{ig_link}" style="color:white; margin:0 10px;">Instagram</a>' if ig_link else ''}
        </div>
        <p style="opacity:0.5; font-size:0.8rem; margin-top:2rem;">&copy; 2026 {biz_name}. Powered by Titan Engine.</p>
    </div>
</footer>
"""

# --- 7. BOOKING PAGE ---
booking_content = f"""
<div class="container" style="padding:4rem 0; text-align:center; min-height:80vh;">
    <h1>{booking_title}</h1>
    <p>{booking_sub}</p>
    <div style="margin-top:2rem; background:white; padding:1rem; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.1);">
        {booking_embed}
    </div>
</div>
"""

# --- 8. PREVIEW & DOWNLOAD ---
st.divider()
c1, c2 = st.columns([3,1])

with c1:
    st.subheader("🖥️ Live Preview")
    preview_tabs = st.tabs(["Home", "Booking Page"])
    with preview_tabs[0]:
        st.components.v1.html(build_page("Home", home_content), height=600, scrolling=True)
    with preview_tabs[1]:
        st.components.v1.html(build_page("Booking", booking_content), height=600, scrolling=True)

with c2:
    st.subheader("🚀 Deployment")
    st.success("All Systems Go.")
    
    if st.button("DOWNLOAD FULL SITE (.ZIP)", type="primary"):
        z_b = io.BytesIO()
        with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
            # HTML Pages
            zf.writestr("index.html", build_page("Home", home_content))
            if show_booking:
                zf.writestr("booking.html", build_page("Booking", booking_content))
            
            # PWA Files
            zf.writestr("manifest.json", gen_pwa_manifest())
            zf.writestr("service-worker.js", gen_service_worker())
            
        st.download_button("📥 Save Website", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_titan_v34.zip", "application/zip")
