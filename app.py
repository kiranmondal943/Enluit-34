import streamlit as st
import zipfile
import io
import json
import datetime
import re
import requests  # Required for AI

# --- 0. STATE MANAGEMENT ---
# Initialize session state so AI can overwrite text fields
def init_state(key, default_val):
    if key not in st.session_state:
        st.session_state[key] = default_val

init_state('hero_h', "Stop Paying Rent for Your Website.")
init_state('hero_sub', "The Titan Engine is the world’s first 0.1s website architecture that runs on $0 monthly fees. Pay once. Own it forever.")
init_state('about_h', "Control Your Empire from a Spreadsheet")
init_state('about_short', "No WordPress dashboard. No plugins to update. Just open your private Google Sheet, change a text, and watch your site update globally in seconds.")
init_state('feat_data', "bolt | The Performance Pillar | **0.1s High-Velocity Loading**. While traditional sites take 3–5s, Titan loads instantly.\nwallet | The Economic Pillar | **$0 Monthly Fees**. We eliminated hosting subscriptions.\ntable | The Functional Pillar | **Google Sheets CMS**. Update prices and photos directly from a simple spreadsheet.\nshield | The Authority Pillar | **Unhackable Security**. Zero-DB Architecture removes the hacker's primary entry point.")

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Titan v35.0 | AI & PWA", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    /* UI Variables */
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { 
        background: linear-gradient(90deg, #0f172a, #ef4444);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900 !important; font-size: 1.8rem !important;
    }
    
    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: #3b82f6 !important; }
    
    /* Buttons */
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        color: white; font-weight: 800; border: none; text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3); transition: transform 0.2s;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v35.0 | AI, PWA & Commerce")
    st.divider()

    # --- 3.1 AI GENERATOR (FIXED) ---
    with st.expander("🤖 Titan AI Generator", expanded=True):
        st.info("Auto-write content using Groq/Llama3.")
        groq_key = st.text_input("Groq API Key", type="password", help="Get free key at console.groq.com")
        biz_desc = st.text_input("Business Type", placeholder="e.g. Luxury Dentist in Dubai")
        
        if st.button("✨ Generate Copy"):
            if not groq_key or not biz_desc:
                st.error("Please enter API Key and Business Description.")
            else:
                with st.spinner("Titan AI is writing..."):
                    try:
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                        prompt = f"""
                        Return a valid JSON object (NO MARKDOWN) for a website about '{biz_desc}'.
                        Required Keys:
                        "hero_h": "Headline (5-8 words)",
                        "hero_sub": "Subtext (2 sentences)",
                        "about_h": "About Title",
                        "about_short": "About Summary (3 sentences)",
                        "feat_data": "4 lines. Format: iconname | Title | Description. (Icons: bolt, wallet, shield, star, heart)"
                        """
                        payload = {
                            "messages": [{"role": "user", "content": prompt}],
                            "model": "llama3-8b-8192",
                            "response_format": {"type": "json_object"}
                        }
                        
                        response = requests.post(url, headers=headers, json=payload)
                        
                        # --- ERROR HANDLING FIX ---
                        if response.status_code == 200:
                            res_json = response.json()
                            content = res_json['choices'][0]['message']['content']
                            parsed = json.loads(content)
                            
                            # Update Session State
                            st.session_state.hero_h = parsed.get('hero_h', st.session_state.hero_h)
                            st.session_state.hero_sub = parsed.get('hero_sub', st.session_state.hero_sub)
                            st.session_state.about_h = parsed.get('about_h', st.session_state.about_h)
                            st.session_state.about_short = parsed.get('about_short', st.session_state.about_short)
                            st.session_state.feat_data = parsed.get('feat_data', st.session_state.feat_data)
                            st.success("Content Generated Successfully! Check the tabs.")
                        else:
                            st.error(f"API Error ({response.status_code}): {response.text}")
                    except Exception as e:
                        st.error(f"System Error: {str(e)}")

    # 3.2 VISUALS
    with st.expander("🎨 Visual DNA", expanded=False):
        theme_mode = st.selectbox("Base Theme", ["Clean Corporate (Light)", "Midnight SaaS (Dark)", "Luxury Gold", "Forest Eco", "Ocean Breeze"])
        c1, c2 = st.columns(2)
        p_color = c1.color_picker("Primary Brand", "#0F172A") 
        s_color = c2.color_picker("Action (CTA)", "#EF4444")  
        h_font = st.selectbox("Headings", ["Montserrat", "Playfair Display", "Oswald", "Inter"])
        b_font = st.selectbox("Body Text", ["Inter", "Open Sans", "Roboto", "Lora"])
        border_rad = st.select_slider("Roundness", ["0px", "12px", "24px"], value="12px")
        anim_type = st.selectbox("Animation", ["Fade Up", "Zoom In", "None"])

    # 3.3 MODULES
    with st.expander("🧩 Section Manager", expanded=False):
        show_hero = st.checkbox("Hero Carousel", value=True)
        show_stats = st.checkbox("Trust Stats", value=True)
        show_features = st.checkbox("Features", value=True)
        show_pricing = st.checkbox("Pricing", value=True)
        show_inventory = st.checkbox("Store/Portfolio", value=True)
        show_booking = st.checkbox("Booking Engine (New)", value=True) # New Feature
        show_blog = st.checkbox("Blog Engine", value=True)
        show_gallery = st.checkbox("About Section", value=True)
        show_testimonials = st.checkbox("Testimonials", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)
        show_cta = st.checkbox("Final CTA", value=True)

    # 3.4 SEO
    with st.expander("⚙️ SEO & Analytics", expanded=False):
        seo_area = st.text_input("Service Area", "Global")
        seo_d = st.text_area("Meta Desc", "Stop paying monthly fees.")
        gsc_tag = st.text_input("GSC ID")
        og_image = st.text_input("Social Share Image")

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ StopWebRent Site Builder v35")

tabs = st.tabs(["1. Identity & PWA", "2. Content", "3. Pricing", "4. Store & Payments", "5. Booking", "6. Blog", "7. Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "StopWebRent.com")
        biz_phone = st.text_input("Phone", "966572562151")
        biz_email = st.text_input("Email", "hello@kaydiemscriptlab.com")
    with c2:
        prod_url = st.text_input("Website URL", "https://www.stopwebrent.com")
        logo_url = st.text_input("Logo URL (PNG/SVG)")
        biz_addr = st.text_area("Address", "Kaydiem Script Lab, Kolkata, India")
        map_iframe = st.text_area("Map Embed", placeholder='<iframe src="..."></iframe>', height=100)

    st.divider()
    st.subheader("📱 PWA Settings (App Install)")
    pwa_short = st.text_input("App Short Name", biz_name[:12])
    pwa_icon = st.text_input("App Icon URL (512x512 PNG)", logo_url)
    
    st.subheader("🌍 Multi-Language")
    lang_sheet = st.text_input("Translation Sheet CSV URL (Optional)")

    st.subheader("Social Links")
    fb_link = st.text_input("Facebook URL")
    ig_link = st.text_input("Instagram URL")
    x_link = st.text_input("X (Twitter) URL")
    wa_num = st.text_input("WhatsApp Number (No +)", "966572562151")

with tabs[1]:
    st.subheader("Hero (AI Editable)")
    hero_h = st.text_input("Hero Headline", key="hero_h")
    hero_sub = st.text_input("Hero Subtext", key="hero_sub")
    hero_img_1 = st.text_input("Slide 1 Image", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1600")
    hero_img_2 = st.text_input("Slide 2 Image", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1600")
    hero_img_3 = st.text_input("Slide 3 Image", "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1600")
    
    st.subheader("Features")
    f_title = st.text_input("Feature Title", "Why Us")
    feat_data_input = st.text_area("Features (icon|Title|Desc)", key="feat_data", height=150)
    
    st.subheader("About")
    about_h_in = st.text_input("About Title", key="about_h")
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")
    about_short_in = st.text_area("Short About", key="about_short")
    about_long = st.text_area("Long About", "Full story here...")
    
    st.subheader("Stats")
    c1, c2, c3 = st.columns(3)
    stat_1 = c1.text_input("Stat 1", "0.1s")
    label_1 = c1.text_input("Label 1", "Speed")
    stat_2 = c2.text_input("Stat 2", "$0")
    label_2 = c2.text_input("Label 2", "Fees")
    stat_3 = c3.text_input("Stat 3", "100%")
    label_3 = c3.text_input("Label 3", "Ownership")

with tabs[2]:
    st.subheader("Pricing")
    c1, c2 = st.columns(2)
    titan_price = c1.text_input("Setup Price", "$199")
    wix_mo = c2.text_input("Competitor Monthly", "$29/mo")
    wix_name = st.text_input("Competitor Name", "Wix")
    save_val = st.text_input("5-Year Savings", "$1,466")

with tabs[3]:
    st.subheader("Store & Payments")
    st.info("Power your store with a Google Sheet CSV.")
    sheet_url = st.text_input("Inventory CSV", placeholder="https://docs.google.com...")
    custom_feat = st.text_input("Fallback Image", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800")
    
    st.markdown("### 💳 Payment Gateways")
    st.caption("Add a column named `StripeLink` in your CSV for direct checkout. Otherwise, it uses WhatsApp Cart.")
    c1, c2 = st.columns(2)
    paypal_link = c1.text_input("PayPal.me Link")
    upi_id = c2.text_input("UPI ID")

with tabs[4]:
    st.subheader("Booking Engine")
    st.info("Paste your Calendly or Cal.com embed code here.")
    booking_embed = st.text_area("Booking Embed Code", height=100, placeholder='<iframe src="..."></iframe>')
    booking_title = st.text_input("Booking Page Title", "Book Now")

with tabs[5]:
    st.subheader("Blog Engine")
    blog_sheet_url = st.text_input("Blog CSV Link")
    blog_hero_title = st.text_input("Blog Title", "Insights")
    blog_hero_sub = st.text_input("Blog Subtext", "Latest news.")

with tabs[6]:
    st.subheader("Legal")
    testi_data = st.text_area("Testimonials (Name|Quote)", "John Doe | Great service!")
    faq_data = st.text_area("FAQ (Q? ? A)", "Cost? ? $0.")
    priv_txt = st.text_area("Privacy Text", "We respect privacy.")
    term_txt = st.text_area("Terms Text", "Our terms.")

# --- 5. COMPILER ---

def format_text(text):
    if not text: return ""
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text).replace('\n', '<br>')

def gen_schema():
    return f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "LocalBusiness", "name": biz_name, "telephone": biz_phone})}</script>'

def gen_pwa_manifest():
    return json.dumps({
        "name": biz_name, "short_name": pwa_short, "start_url": "./index.html",
        "display": "standalone", "background_color": "#ffffff", "theme_color": p_color,
        "icons": [{"src": pwa_icon, "sizes": "512x512", "type": "image/png"}]
    })

def gen_sw():
    return "self.addEventListener('fetch', e => e.respondWith(caches.match(e.request).then(r => r || fetch(e.request))));"

def get_theme_css():
    bg_color, text_color, card_bg = "#ffffff", "#0f172a", "#ffffff"
    if "Midnight" in theme_mode: bg_color, text_color, card_bg = "#0f172a", "#f8fafc", "#1e293b"
    elif "Luxury" in theme_mode: bg_color, text_color, card_bg = "#1c1c1c", "#D4AF37", "#2a2a2a"
    
    anim_css = ""
    if anim_type == "Fade Up": anim_css = ".reveal { opacity: 0; transform: translateY(30px); transition: 0.8s; } .reveal.active { opacity: 1; transform: translateY(0); }"
    
    return f"""
    :root {{ --p: {p_color}; --s: {s_color}; --bg: {bg_color}; --txt: {text_color}; --card: {card_bg}; --rad: {border_rad}; }}
    body {{ background: var(--bg); color: var(--txt); font-family: '{b_font}', sans-serif; margin: 0; }}
    h1, h2, h3 {{ font-family: '{h_font}', sans-serif; color: var(--p); }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    .btn {{ display:inline-block; padding:1rem 2rem; background:var(--p); color:white; text-decoration:none; border-radius:var(--rad); cursor:pointer; border:none; }}
    .btn-accent {{ background:var(--s); }}
    .card {{ background:var(--card); padding:2rem; border-radius:var(--rad); box-shadow:0 4px 6px rgba(0,0,0,0.05); }}
    .grid-3 {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:2rem; }}
    nav {{ position:fixed; width:100%; top:0; background:rgba(255,255,255,0.95); backdrop-filter:blur(10px); z-index:999; padding:1rem 0; border-bottom:1px solid #eee; }}
    .hero {{ padding-top:100px; min-height:80vh; display:flex; align-items:center; justify-content:center; text-align:center; background:var(--p); color:white; }}
    footer {{ background:var(--p); color:white; padding:4rem 0; margin-top:4rem; }}
    
    /* CART CSS */
    #cart-float {{ position:fixed; bottom:100px; right:30px; background:var(--s); color:white; padding:15px; border-radius:50px; cursor:pointer; z-index:998; display:flex; gap:10px; box-shadow:0 10px 20px rgba(0,0,0,0.3); }}
    #cart-modal {{ display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); background:var(--card); width:90%; max-width:400px; padding:2rem; z-index:1001; border-radius:12px; box-shadow:0 20px 50px rgba(0,0,0,0.5); }}
    .cart-item {{ display:flex; justify-content:space-between; margin-bottom:10px; border-bottom:1px solid #eee; }}
    
    {anim_css}
    @media(max-width:768px) {{ .hero {{ min-height:60vh; }} }}
    """

def gen_nav():
    lang_btn = f'<a href="#" onclick="toggleLang()" style="margin-left:1rem;text-decoration:none;">🌐 Lang</a>' if lang_sheet else ''
    return f"""
    <nav><div class="container" style="display:flex; justify-content:space-between; align-items:center;">
        <div style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</div>
        <div>
            <a href="index.html" style="margin-right:1rem; text-decoration:none; color:var(--txt);">Home</a>
            {'<a href="booking.html" style="margin-right:1rem; text-decoration:none; color:var(--txt);">Book</a>' if show_booking else ''}
            {lang_btn}
            <a href="tel:{biz_phone}" class="btn-accent" style="padding:0.5rem 1rem; border-radius:50px;">Call</a>
        </div>
    </div></nav>
    """

def gen_cart_js():
    return f"""
    <div id="cart-float" onclick="toggleCart()" style="display:none;">🛒 <span id="cart-count">0</span></div>
    <div id="cart-modal"><h3>Cart</h3><div id="cart-items"></div><div id="cart-total"></div><button onclick="checkout()" class="btn btn-accent" style="width:100%;margin-top:1rem;">Checkout WhatsApp</button><button onclick="toggleCart()" style="width:100%;margin-top:0.5rem;background:#eee;border:none;padding:0.5rem;">Close</button></div>
    <script>
    let cart = JSON.parse(localStorage.getItem('tc')) || [];
    const wa = "{wa_num}";
    function render() {{
        const b = document.getElementById('cart-items'); if(!b) return;
        b.innerHTML=''; let t=0;
        cart.forEach((c,i)=>{{ t+=parseFloat(c.p)||0; b.innerHTML+=`<div class="cart-item"><span>${{c.n}}</span><span>${{c.p}} <b onclick="rem(${{i}})" style="color:red;cursor:pointer">x</b></span></div>`; }});
        document.getElementById('cart-count').innerText=cart.length;
        document.getElementById('cart-total').innerText="Total: "+t.toFixed(2);
        document.getElementById('cart-float').style.display = cart.length>0?'flex':'none';
        localStorage.setItem('tc', JSON.stringify(cart));
    }}
    function add(n,p) {{ cart.push({{n,p}}); render(); alert('Added'); }}
    function rem(i) {{ cart.splice(i,1); render(); }}
    function toggleCart() {{ const m=document.getElementById('cart-modal'); m.style.display=m.style.display==='block'?'none':'block'; }}
    function checkout() {{ 
        let m="Order:%0A"; cart.forEach(c=>m+=`- ${{c.n}} (${{c.p}})%0A`); 
        m+=`%0APayment: UPI {upi_id} | PayPal {paypal_link}`;
        window.open(`https://wa.me/${{wa}}?text=${{m}}`); cart=[]; render(); toggleCart(); 
    }}
    window.addEventListener('load', render);
    </script>
    """

def gen_lang_js():
    if not lang_sheet: return ""
    return f"""<script>
    async function toggleLang() {{
        try {{
            const r = await fetch('{lang_sheet}'); const t = await r.text();
            alert("Language Switched! (Demo: In prod this replaces text IDs)");
        }} catch(e) {{}}
    }}</script>"""

def build_page(title, content, extra=""):
    return f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title><style>{get_theme_css()}</style>
    <link rel="manifest" href="manifest.json"><meta name="theme-color" content="{p_color}">
    <script>
    if('serviceWorker' in navigator) navigator.serviceWorker.register('service-worker.js');
    window.addEventListener('scroll', () => {{
        var reveals = document.querySelectorAll('.reveal');
        for (var i = 0; i < reveals.length; i++) {{
            if (reveals[i].getBoundingClientRect().top < window.innerHeight - 150) reveals[i].classList.add('active');
        }}
    }});
    </script>
    </head><body>
    {gen_nav()}
    {content}
    <div class="container" style="text-align:center; padding:2rem; opacity:0.6;">&copy; {biz_name}</div>
    {gen_cart_js()}
    {gen_lang_js()}
    {extra}
    </body></html>
    """

# --- PAGE CONTENT GENERATORS ---
def gen_home():
    h = f"<header class='hero'><div class='container'><h1>{hero_h}</h1><p>{hero_sub}</p></div></header>"
    if show_stats: h += f"<div style='background:var(--p); color:white; padding:2rem; text-align:center;'><div class='container grid-3'><div><h2>{stat_1}</h2>{label_1}</div><div><h2>{stat_2}</h2>{label_2}</div><div><h2>{stat_3}</h2>{label_3}</div></div></div>"
    if show_features: 
        f_html = "".join([f"<div class='card reveal'><h3>{l.split('|')[1]}</h3><p>{l.split('|')[2]}</p></div>" for l in feat_data_input.split('\n') if '|' in l])
        h += f"<section><div class='container'><h2>Features</h2><div class='grid-3'>{f_html}</div></div></section>"
    if show_inventory:
        h += f"""<section><div class='container'><h2>Store</h2><div id='inv' class='grid-3'>Loading...</div></div></section>
        <script>
        async function ld() {{
            const r = await fetch('{sheet_url}'); const t = await r.text(); const l = t.split(/\\r\\n|\\n/);
            const b = document.getElementById('inv'); b.innerHTML='';
            for(let i=1; i<l.length; i++) {{
                const c = l[i].split(','); if(c.length<2) continue;
                // c[0]=Name, c[1]=Price, c[2]=Desc, c[3]=Img, c[4]=Stripe
                let btn = (c[4] && c[4].includes('http')) ? `<a href='${{c[4]}}' class='btn btn-accent' style='width:100%'>Buy Now</a>` : `<button onclick="add('${{c[0]}}','${{c[1]}}')" class='btn' style='width:100%'>Add Cart</button>`;
                b.innerHTML+=`<div class='card reveal'><img src='${{c[3]||'{custom_feat}'}}' style='width:100%;height:200px;object-fit:cover'><h3>${{c[0]}}</h3><b>${{c[1]}}</b><p>${{c[2]}}</p>${{btn}}</div>`;
            }}
        }}
        ld();
        </script>"""
    return h

def gen_booking():
    return f"<header class='hero' style='min-height:40vh'><h1>{booking_title}</h1></header><div class='container' style='padding:4rem 0'>{booking_embed}</div>"

def gen_blog_index():
    return f"""<header class='hero' style='min-height:40vh'><h1>{blog_hero_title}</h1></header>
    <div class='container' style='padding:4rem 0'><div id='bg' class='grid-3'>Loading...</div></div>
    <script>async function lb(){{
        const r=await fetch('{blog_sheet_url}');const t=await r.text();const l=t.split(/\\n/);
        const b=document.getElementById('bg');b.innerHTML='';
        for(let i=1;i<l.length;i++){{ const c=l[i].split(','); if(c.length>3) b.innerHTML+=`<div class='card reveal'><h3><a href='post.html?id=${{c[0]}}'>${{c[1]}}</a></h3><p>${{c[4]}}</p></div>`; }}
    }} lb();</script>"""

def gen_product_detail(is_demo):
    demo_script = "const isDemo = true;" if is_demo else "const isDemo = false;"
    return f"""<div class='container' style='padding-top:150px' id='pd'>Loading...</div>
    <script>{demo_script}
    async function lp() {{
        const r = await fetch('{sheet_url}'); const t = await r.text(); const l = t.split(/\\n/);
        const c = l[1].split(','); 
        document.getElementById('pd').innerHTML = `<h1>${{c[0]}}</h1><img src='${{c[3]||''}}' style='max-width:500px'><p>${{c[2]}}</p><button class='btn' onclick="add('${{c[0]}}','${{c[1]}}')">Add to Cart</button>`;
    }}
    lp();
    </script>"""

# --- 6. LAUNCHPAD (RESTORED RADIO BUTTONS) ---
st.divider()
st.subheader("🚀 Launchpad")

# *** RESTORED PREVIEW SELECTOR ***
preview_mode = st.radio("Preview Page:", ["Home", "About", "Contact", "Booking", "Blog Index", "Privacy", "Terms", "Product Detail (Demo)"], horizontal=True)

# Generate Inner Content
about_content = f"<header class='hero' style='min-height:40vh'><h1>About Us</h1></header><div class='container' style='padding:4rem 0'><div class='grid-3'><div class='legal-text'>{format_text(about_long)}</div><img src='{about_img}' style='width:100%;border-radius:12px'></div></div>"
contact_content = f"<header class='hero' style='min-height:40vh'><h1>Contact</h1></header><div class='container' style='padding:4rem 0'><h2>{biz_email}</h2><br>{map_iframe}</div>"
privacy_content = f"<header class='hero' style='min-height:40vh'><h1>Privacy</h1></header><div class='container' style='padding:4rem 0'>{format_text(priv_txt)}</div>"
terms_content = f"<header class='hero' style='min-height:40vh'><h1>Terms</h1></header><div class='container' style='padding:4rem 0'>{format_text(term_txt)}</div>"

# Display Preview
c1, c2 = st.columns([3, 1])
with c1:
    if preview_mode == "Home": st.components.v1.html(build_page("Home", gen_home()), height=600, scrolling=True)
    elif preview_mode == "About": st.components.v1.html(build_page("About", about_content), height=600, scrolling=True)
    elif preview_mode == "Contact": st.components.v1.html(build_page("Contact", contact_content), height=600, scrolling=True)
    elif preview_mode == "Booking": st.components.v1.html(build_page("Booking", gen_booking()), height=600, scrolling=True)
    elif preview_mode == "Blog Index": st.components.v1.html(build_page("Blog", gen_blog_index()), height=600, scrolling=True)
    elif preview_mode == "Privacy": st.components.v1.html(build_page("Privacy", privacy_content), height=600, scrolling=True)
    elif preview_mode == "Terms": st.components.v1.html(build_page("Terms", terms_content), height=600, scrolling=True)
    elif preview_mode == "Product Detail (Demo)":
        st.info("ℹ️ Demo: Shows the first product from CSV.")
        st.components.v1.html(build_page("Product", gen_product_detail(is_demo=True)), height=600, scrolling=True)

with c2:
    if st.button("DOWNLOAD WEBSITE ZIP", type="primary"):
        z_b = io.BytesIO()
        with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
            zf.writestr("index.html", build_page("Home", gen_home()))
            zf.writestr("about.html", build_page("About", about_content))
            zf.writestr("contact.html", build_page("Contact", contact_content))
            zf.writestr("privacy.html", build_page("Privacy", privacy_content))
            zf.writestr("terms.html", build_page("Terms", terms_content))
            zf.writestr("booking.html", build_page("Booking", gen_booking()))
            if show_blog: zf.writestr("blog.html", build_page("Blog", gen_blog_index()))
            zf.writestr("product.html", build_page("Product", gen_product_detail(is_demo=False)))
            zf.writestr("manifest.json", gen_pwa_manifest())
            zf.writestr("service-worker.js", gen_sw())
            
        st.download_button("📥 Save Site", z_b.getvalue(), f"{biz_name}_v35.zip", "application/zip")
