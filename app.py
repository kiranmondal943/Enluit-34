import streamlit as st
import zipfile
import io
import json
import datetime
import re
import requests

# --- 0. STATE MANAGEMENT ---
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
    page_title="Titan v35.1 | Restored Layouts", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED UI SYSTEM ---
st.markdown("""
    <style>
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { 
        background: linear-gradient(90deg, #0f172a, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important; font-size: 1.8rem !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; color: #0f172a !important;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        color: white; font-weight: 800; border: none;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3); text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v35.1 | AI, PWA & Original Layouts")
    st.divider()
    
    # AI GENERATOR
    with st.expander("🤖 Titan AI Generator", expanded=True):
        st.info("Auto-write your website content.")
        groq_key = st.text_input("Groq API Key (Free)", type="password", help="Get at console.groq.com")
        biz_desc = st.text_input("Business Description", placeholder="e.g. Luxury Dental Clinic in Dubai")
        if st.button("✨ Generate Copy"):
            if not groq_key or not biz_desc:
                st.error("Key & Description required.")
            else:
                try:
                    with st.spinner("Titan AI is writing..."):
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                        prompt = f"""
                        Act as a copywriter. Return a JSON object for '{biz_desc}':
                        hero_h (Catchy headline), hero_sub (2 sentences), about_h (Title), about_short (3 sentences),
                        feat_data (4 lines. Format: iconname | Title | Description. Icons: bolt, wallet, shield, star, heart).
                        """
                        data = {"messages": [{"role": "user", "content": prompt}], "model": "llama3-8b-8192", "response_format": {"type": "json_object"}}
                        resp = requests.post(url, headers=headers, json=data)
                        parsed = json.loads(resp.json()['choices'][0]['message']['content'])
                        
                        st.session_state.hero_h = parsed.get('hero_h', st.session_state.hero_h)
                        st.session_state.hero_sub = parsed.get('hero_sub', st.session_state.hero_sub)
                        st.session_state.about_h = parsed.get('about_h', st.session_state.about_h)
                        st.session_state.about_short = parsed.get('about_short', st.session_state.about_short)
                        st.session_state.feat_data = parsed.get('feat_data', st.session_state.feat_data)
                        st.success("Content Generated!")
                except Exception as e:
                    st.error(f"AI Error: {e}")

    # VISUAL DNA
    with st.expander("🎨 Visual DNA", expanded=False):
        theme_mode = st.selectbox("Base Theme", ["Clean Corporate (Light)", "Midnight SaaS (Dark)", "Glassmorphism (Blur)", "Cyberpunk Neon", "Luxury Gold", "Forest Eco", "Ocean Breeze", "Stark Minimalist"])
        c1, c2 = st.columns(2)
        p_color = c1.color_picker("Primary Brand", "#0F172A") 
        s_color = c2.color_picker("Action (CTA)", "#EF4444")  
        h_font = st.selectbox("Headings", ["Montserrat", "Space Grotesk", "Playfair Display", "Oswald", "Clash Display"])
        b_font = st.selectbox("Body Text", ["Inter", "Open Sans", "Roboto", "Satoshi", "Lora"])
        border_rad = st.select_slider("Corner Roundness", ["0px", "4px", "12px", "24px", "40px"], value="12px")
        anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])

    # MODULE MANAGER
    with st.expander("🧩 Section Manager", expanded=False):
        show_hero = st.checkbox("Hero Carousel", True)
        show_stats = st.checkbox("Trust Stats/Logos", True)
        show_features = st.checkbox("Feature Grid", True)
        show_pricing = st.checkbox("Pricing Table", True)
        show_inventory = st.checkbox("Portfolio/Inventory", True)
        show_blog = st.checkbox("Blog Engine", True)
        show_gallery = st.checkbox("About Section", True)
        show_testimonials = st.checkbox("Testimonials", True)
        show_faq = st.checkbox("F.A.Q.", True)
        show_cta = st.checkbox("Call to Action", True)
        show_booking = st.checkbox("Booking Engine (New)", True)

    # TECHNICAL
    with st.expander("⚙️ SEO & Analytics", expanded=False):
        seo_area = st.text_input("Service Area", "Global / Online")
        seo_kw = st.text_area("SEO Keywords", "web design, no monthly fees")
        gsc_tag = st.text_input("Google Verification ID")
        ga_tag = st.text_input("Google Analytics ID")
        og_image = st.text_input("Social Share Image URL")

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ StopWebRent Site Builder v35.1")

tabs = st.tabs(["1. Identity & PWA", "2. Content Blocks", "3. Pricing", "4. Store & Pay", "5. Booking", "6. Blog", "7. Legal"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "StopWebRent.com")
        biz_tagline = st.text_input("Tagline", "Stop Renting. Start Owning.")
        biz_phone = st.text_input("Phone", "966572562151")
        biz_email = st.text_input("Email", "hello@kaydiemscriptlab.com")
    with c2:
        prod_url = st.text_input("Website URL", "https://www.stopwebrent.com")
        biz_addr = st.text_area("Address", "Kaydiem Script Lab\nKanishka’s House, Garia Station Rd\nKolkata, West Bengal 700084, India", height=100)
        map_iframe = st.text_area("Google Map Embed Code", placeholder='<iframe src="..."></iframe>', height=100)
        seo_d = st.text_area("Meta Description", "Stop paying monthly fees...", height=100)
        logo_url = st.text_input("Logo URL")

    st.subheader("📱 PWA Settings")
    pwa_short = st.text_input("App Short Name", biz_name[:12])
    pwa_desc = st.text_input("App Description", "Official App")
    pwa_icon = st.text_input("App Icon (512x512 PNG)", logo_url)

    st.subheader("🌍 Multi-Language")
    lang_sheet = st.text_input("Translation CSV URL (Optional)")
        
    st.subheader("Social Links")
    sc1, sc2, sc3 = st.columns(3)
    fb_link = sc1.text_input("Facebook URL")
    ig_link = sc2.text_input("Instagram URL")
    x_link = sc3.text_input("X (Twitter) URL")
    sc4, sc5, sc6 = st.columns(3)
    li_link = sc4.text_input("LinkedIn URL")
    yt_link = sc5.text_input("YouTube URL")
    wa_num = sc6.text_input("WhatsApp Number (No +)", "966572562151")

with tabs[1]:
    st.subheader("Hero Carousel")
    hero_h = st.text_input("Hero Headline", key="hero_h")
    hero_sub = st.text_input("Hero Subtext", key="hero_sub")
    hc1, hc2, hc3 = st.columns(3)
    hero_img_1 = hc1.text_input("Slide 1", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1600")
    hero_img_2 = hc2.text_input("Slide 2", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1600")
    hero_img_3 = hc3.text_input("Slide 3", "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1600")
    
    st.divider()
    col_s1, col_s2, col_s3 = st.columns(3)
    stat_1 = col_s1.text_input("Stat 1", "0.1s")
    label_1 = col_s1.text_input("Label 1", "Load Speed")
    stat_2 = col_s2.text_input("Stat 2", "$0")
    label_2 = col_s2.text_input("Label 2", "Monthly Fees")
    stat_3 = col_s3.text_input("Stat 3", "100%")
    label_3 = col_s3.text_input("Label 3", "Ownership")

    st.divider()
    f_title = st.text_input("Features Title", "The Titan Value Pillars")
    feat_data_input = st.text_area("Features List", key="feat_data", height=150)
    
    st.subheader("About Content")
    about_h_in = st.text_input("About Title", key="about_h")
    about_img = st.text_input("About Side Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")
    c_a1, c_a2 = st.columns(2)
    about_short_in = c_a1.text_area("Home Page Summary", key="about_short", height=200)
    about_long = c_a2.text_area("Full About Page Content", "**The Digital Landlord Trap**\nMost business owners...", height=200)

with tabs[2]:
    col_p1, col_p2, col_p3 = st.columns(3)
    titan_price = col_p1.text_input("Titan Setup", "$199")
    titan_mo = col_p1.text_input("Titan Monthly", "$0")
    wix_name = col_p2.text_input("Competitor", "Wix")
    wix_mo = col_p2.text_input("Comp. Monthly", "$29/mo")
    save_val = col_p3.text_input("5-Year Savings", "$1,466")

with tabs[3]:
    sheet_url = st.text_input("Google Sheet CSV Link", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    custom_feat = st.text_input("Fallback Image", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800")
    
    st.markdown("### 💳 Payment Gateways")
    col_pay1, col_pay2 = st.columns(2)
    paypal_link = col_pay1.text_input("PayPal.me Link", "https://paypal.me/yourid")
    upi_id = col_pay2.text_input("UPI ID (India)", "yourname@upi")
    st.info("Add a 5th Column to CSV named `StripeLink`. If present, button becomes 'Buy Now'.")

with tabs[4]:
    st.subheader("📅 Booking Engine")
    booking_embed = st.text_area("Paste Embed Code (iframe)", height=150, placeholder='<iframe src="https://calendly.com/yourname" width="100%" height="600"></iframe>')
    booking_title = st.text_input("Booking Title", "Book an Appointment")
    booking_desc = st.text_input("Booking Subtext", "Select a time slot.")

with tabs[5]:
    blog_sheet_url = st.text_input("Blog CSV Link", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    blog_hero_title = st.text_input("Blog Title", "Latest Insights")
    blog_hero_sub = st.text_input("Blog Subtext", "Thoughts on technology.")

with tabs[6]:
    testi_data = st.text_area("Testimonials", "Rajesh Gupta, HVAC Owner | I was paying Wix $35/month... Titan built me a faster site.\nSarah Jenkins, Cafe Owner | Updating my menu is easy now.", height=100)
    faq_data = st.text_area("FAQ Data", "Do I really pay $0? ? Yes.\nIs it secure? ? Safer than WordPress.", height=100)
    l1, l2 = st.columns(2)
    priv_txt = l1.text_area("Privacy Policy", "**1. Introduction**\nWe collect minimum data...", height=200)
    term_txt = l2.text_area("Terms of Service", "**1. Service Agreement**\nBy engaging us...", height=200)

# --- 5. COMPILER ENGINE ---
def format_text(text):
    if not text: return ""
    processed_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    lines = processed_text.split('\n')
    html_out = ""
    in_list = False
    for line in lines:
        clean_line = line.strip()
        if not clean_line: continue
        if clean_line.startswith("* "):
            if not in_list: html_out += '<ul style="margin-bottom:1rem; padding-left:1.5rem;">'; in_list = True
            html_out += f'<li style="margin-bottom:0.5rem; opacity:0.9;">{clean_line[2:]}</li>'
        elif clean_line.startswith("<strong>") and clean_line.endswith("</strong>"):
            if in_list: html_out += "</ul>"; in_list = False
            html_out += f"<h3 style='margin-top:1.5rem; margin-bottom:0.5rem; color:var(--p); font-size:1.25rem;'>{clean_line.replace('<strong>','').replace('</strong>','')}</h3>"
        else:
            if in_list: html_out += "</ul>"; in_list = False
            html_out += f"<p style='margin-bottom:1rem; opacity:0.9;'>{clean_line}</p>"
    if in_list: html_out += "</ul>"
    return html_out

def gen_schema():
    schema = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": biz_name, "image": logo_url or hero_img_1, "telephone": biz_phone, "email": biz_email, "address": {"@type": "PostalAddress", "streetAddress": biz_addr}, "url": prod_url, "description": seo_d}
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def gen_pwa_manifest():
    return json.dumps({"name": biz_name, "short_name": pwa_short, "start_url": "./index.html", "display": "standalone", "background_color": "#ffffff", "theme_color": p_color, "description": pwa_desc, "icons": [{"src": pwa_icon, "sizes": "512x512", "type": "image/png"}]})

def gen_sw():
    return """self.addEventListener('install',(e)=>{e.waitUntil(caches.open('titan-store').then((c)=>c.addAll(['./index.html','./contact.html'])));});self.addEventListener('fetch',(e)=>{e.respondWith(caches.match(e.request).then((r)=>r||fetch(e.request)));});"""

def get_theme_css():
    bg_color, text_color, card_bg, glass_nav = "#ffffff", "#0f172a", "#ffffff", "rgba(255, 255, 255, 0.95)"
    if "Midnight" in theme_mode: bg_color, text_color, card_bg, glass_nav = "#0f172a", "#f8fafc", "#1e293b", "rgba(15, 23, 42, 0.9)"
    elif "Luxury" in theme_mode: bg_color, text_color, card_bg, glass_nav = "#1c1c1c", "#D4AF37", "#2a2a2a", "rgba(28,28,28,0.95)"
    
    anim_css = ".reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; } .reveal.active { opacity: 1; transform: translateY(0); }"
    if anim_type == "Zoom In": anim_css = ".reveal { opacity: 0; transform: scale(0.95); transition: all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); } .reveal.active { opacity: 1; transform: scale(1); }"

    return f"""
    :root {{ --p: {p_color}; --s: {s_color}; --bg: {bg_color}; --txt: {text_color}; --card: {card_bg}; --radius: {border_rad}; --nav: {glass_nav}; --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif; }}
    * {{ box-sizing: border-box; }} html {{ scroll-behavior: smooth; font-size: 16px; }}
    body {{ background-color: var(--bg); color: var(--txt); font-family: var(--b-font); margin: 0; line-height: 1.6; overflow-x: hidden; }}
    h1, h2, h3, h4 {{ font-family: var(--h-font); color: var(--p); line-height: 1.1; margin-bottom: 1rem; }}
    strong {{ color: var(--p); font-weight: 800; }}
    .hero {{ position: relative; min-height: 90vh; overflow: hidden; display: flex; align-items: center; justify-content: center; text-align: center; color: white; padding-top: 80px; background-color: var(--p); }}
    .carousel-slide {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; opacity: 0; transition: opacity 1.5s ease-in-out; z-index: 0; }}
    .carousel-slide.active {{ opacity: 1; }}
    .hero-content {{ z-index: 2; position: relative; animation: slideUp 1s ease-out; width: 100%; padding: 0 20px; }}
    @keyframes slideUp {{ from {{ opacity:0; transform: translateY(30px); }} to {{ opacity:1; transform: translateY(0); }} }}
    .hero h1 {{ color: #ffffff !important; font-size: clamp(2.5rem, 5vw, 4.5rem); text-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
    .hero p {{ color: rgba(255,255,255,0.95) !important; font-size: clamp(1.1rem, 2vw, 1.3rem); max-width: 700px; margin: 0 auto 2rem auto; text-shadow: 0 2px 10px rgba(0,0,0,0.4); }}
    .container {{ max-width: 1280px; margin: 0 auto; padding: 0 20px; }}
    .btn {{ display: inline-block; padding: 1rem 2.5rem; border-radius: var(--radius); font-weight: 700; text-decoration: none; transition: 0.3s; text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; border: none; text-align: center; }}
    .btn-primary {{ background: var(--p); color: white !important; }}
    .btn-accent {{ background: var(--s); color: white !important; box-shadow: 0 10px 25px -5px var(--s); }}
    .btn:hover {{ transform: translateY(-3px); filter: brightness(1.15); }}
    
    /* NAV */
    nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: var(--nav); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(100,100,100,0.1); padding: 1rem 0; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; align-items: center; }}
    .nav-links a {{ margin-left: 2rem; text-decoration: none; font-weight: 600; color: var(--txt); font-size: 0.9rem; opacity: 0.8; transition:0.2s; }}
    .nav-links a:hover {{ opacity: 1; color: var(--s); }}
    .mobile-menu {{ display: none; font-size: 1.5rem; cursor: pointer; }}
    
    /* SECTIONS & GRID */
    section {{ padding: clamp(3rem, 8vw, 5rem) 0; }}
    .section-head {{ text-align: center; margin-bottom: clamp(2rem, 5vw, 4rem); }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }}
    .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }}
    .contact-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 3rem; }}
    .card {{ background: var(--card); padding: 2rem; border-radius: var(--radius); border: 1px solid rgba(100,100,100,0.1); transition: 0.3s; height: 100%; display: flex; flex-direction: column; }}
    .card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1); border-color: var(--s); }}
    .prod-img {{ width: 100%; height: 250px; object-fit: cover; border-radius: calc(var(--radius) - 4px); margin-bottom: 1.5rem; background: #f1f5f9; }}
    
    /* FORMS */
    input, textarea, select {{ width: 100%; padding: 0.8rem; margin-bottom: 1rem; border: 1px solid #ccc; border-radius: 6px; font-family: inherit; }}
    label {{ color: var(--txt); font-weight: bold; margin-bottom: 0.5rem; display: block; }}
    
    /* TABLES & FAQ */
    .pricing-table {{ width: 100%; border-collapse: collapse; min-width: 600px; }}
    .pricing-table th {{ background: var(--p); color: white; padding: 1.5rem; text-align: left; }}
    .pricing-table td {{ padding: 1.5rem; border-bottom: 1px solid rgba(100,100,100,0.1); background: var(--card); }}
    details {{ background: var(--card); border: 1px solid rgba(100,100,100,0.1); border-radius: 8px; margin-bottom: 1rem; padding: 1rem; cursor: pointer; }}
    
    /* FOOTER */
    footer {{ background: var(--p); color: white; padding: 4rem 0; margin-top: auto; }}
    .footer-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 3rem; }}
    footer a {{ color: rgba(255,255,255,0.8) !important; text-decoration: none; display: block; margin-bottom: 0.5rem; }}
    .social-icon {{ width: 24px; height: 24px; fill: rgba(255,255,255,0.7); }}
    
    /* CART */
    #cart-float {{ position: fixed; bottom: 100px; right: 30px; background: var(--p); color: white; padding: 15px 20px; border-radius: 50px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); cursor: pointer; z-index: 998; display: flex; align-items: center; gap: 10px; font-weight: bold; }}
    #cart-modal {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); width: 90%; max-width: 500px; padding: 2rem; border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.3); z-index: 1001; border: 1px solid rgba(128,128,128,0.2); }}
    #cart-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }}
    .cart-item {{ display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0; }}
    
    {anim_css}
    
    @media (max-width: 768px) {{
        .nav-links {{ position: fixed; top: 70px; left: -100%; width: 100%; height: calc(100vh - 70px); background: var(--bg); flex-direction: column; padding: 2rem; transition: 0.3s; align-items: flex-start; justify-content: flex-start; border-top: 1px solid rgba(0,0,0,0.1); overflow-y: auto; gap: 1.5rem; }}
        .nav-links.active {{ left: 0; }}
        .mobile-menu {{ display: block; }}
        .about-grid, .contact-grid {{ grid-template-columns: 1fr !important; gap: 2rem; }}
    }}
    """

def gen_nav():
    logo = f'<img src="{logo_url}" height="40" alt="Logo">' if logo_url else f'<span style="font-weight:900;font-size:1.5rem;color:var(--p)">{biz_name}</span>'
    blog_l = '<a href="blog.html">Blog</a>' if show_blog else ''
    book_l = '<a href="booking.html">Book Now</a>' if show_booking else ''
    lang_btn = f'<a href="#" onclick="toggleLang()" title="Switch Language">🌐 ES</a>' if lang_sheet else ''
    
    return f"""
    <nav><div class="container nav-flex">
        <a href="index.html" style="text-decoration:none">{logo}</a>
        <div class="mobile-menu" onclick="document.querySelector('.nav-links').classList.toggle('active')">☰</div>
        <div class="nav-links">
            <a href="index.html">Home</a>
            {'<a href="index.html#features">Features</a>' if show_features else ''}
            {'<a href="index.html#inventory">Store</a>' if show_inventory else ''}
            {blog_l} {book_l} {lang_btn}
            <a href="contact.html">Contact</a>
            <a href="tel:{biz_phone}" class="btn-accent" style="padding:0.6rem 1.5rem; margin-left:1.5rem; border-radius:50px; color:white!important; width:auto;">Call Now</a>
        </div>
    </div></nav>
    <script>function toggleMenu() {{ document.querySelector('.nav-links').classList.remove('active'); }}</script>
    """

def gen_hero():
    return f"""
    <section class="hero">
        <div class="hero-overlay"></div>
        <div class="carousel-slide active" style="background-image: url('{hero_img_1}')"></div>
        <div class="carousel-slide" style="background-image: url('{hero_img_2}')"></div>
        <div class="carousel-slide" style="background-image: url('{hero_img_3}')"></div>
        <div class="container hero-content">
            <h1>{hero_h}</h1><p>{hero_sub}</p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
                <a href="#inventory" class="btn btn-accent">Explore Now</a>
                <a href="contact.html" class="btn" style="background:rgba(255,255,255,0.2);backdrop-filter:blur(10px);color:white;">Contact Us</a>
            </div>
        </div>
    </section>
    <script>
    let slides=document.querySelectorAll('.carousel-slide');let c=0;
    setInterval(()=>{{slides[c].classList.remove('active');c=(c+1)%slides.length;slides[c].classList.add('active');}},4000);
    </script>
    """

def get_icon(n):
    n=n.lower()
    if "bolt" in n: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M11 21h-1l1-7H7.5c-.58 0-.57-.32-.38-.66.19-.34.05-.08.07-.12C8.48 10.94 10.42 7.54 13 3h1l-1 7h3.5c.49 0 .56.33.47.51l-.07.15C12.96 17.55 11 21 11 21z"/></svg>'
    if "wallet" in n: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>'
    if "shield" in n: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>'
    if "table" in n: return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM5 19V5h14v14H5zm2-2h10v-2H7v2zm0-4h10v-2H7v2zm0-4h10V7H7v2z"/></svg>'
    return '<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>'

def gen_features():
    c = ""
    for l in feat_data_input.split('\n'):
        if "|" in l:
            p = l.split('|')
            if len(p)>=3: c+=f'<div class="card reveal"><div style="color:var(--s);margin-bottom:1rem;">{get_icon(p[0])}</div><h3 style="color:var(--p);font-size:1.2rem;text-transform:uppercase;">{p[1].strip()}</h3><div style="opacity:0.9;">{format_text(p[2].strip())}</div></div>'
    return f'<section id="features"><div class="container"><div class="section-head reveal"><h2>{f_title}</h2></div><div class="grid-3">{c}</div></div></section>'

def gen_stats():
    return f'<div style="background:var(--p);color:white;padding:3rem 0;text-align:center;"><div class="container grid-3"><div class="reveal"><h3>{stat_1}</h3><p>{label_1}</p></div><div class="reveal"><h3>{stat_2}</h3><p>{label_2}</p></div><div class="reveal"><h3>{stat_3}</h3><p>{label_3}</p></div></div></div>'

def gen_cart_system():
    return f"""
    <div id="cart-float" onclick="toggleCart()" style="display:none;"><span>🛒</span> <span id="cart-count">0</span></div>
    <div id="cart-overlay" onclick="toggleCart()"></div>
    <div id="cart-modal"><h3>Your Cart</h3><div id="cart-items" style="max-height:300px;overflow-y:auto;margin:1rem 0;"></div><div style="font-weight:bold;text-align:right;">Total: <span id="cart-total">0.00</span></div><button onclick="checkoutWhatsApp()" class="btn btn-accent" style="width:100%">Checkout via WhatsApp</button></div>
    <script>
    let cart = JSON.parse(localStorage.getItem('titanCart')) || [];
    const waNumber = "{wa_num}"; const payLinks = "UPI: {upi_id} | PayPal: {paypal_link}";
    function renderCart() {{
        const box = document.getElementById('cart-items'); if(!box) return; box.innerHTML = ''; let total = 0;
        cart.forEach((item, i) => {{ total += parseFloat(item.price.replace(/[^0-9.]/g, '')) || 0; box.innerHTML += `<div class="cart-item"><span>${{item.name}}</span><span>${{item.price}} <span onclick="remItem(${{i}})" style="color:red;cursor:pointer;">x</span></span></div>`; }});
        document.getElementById('cart-count').innerText = cart.length; document.getElementById('cart-total').innerText = total.toFixed(2);
        document.getElementById('cart-float').style.display = cart.length > 0 ? 'flex' : 'none'; localStorage.setItem('titanCart', JSON.stringify(cart));
    }}
    function addToCart(name, price) {{ cart.push({{name, price}}); renderCart(); alert(name + " added!"); }}
    function remItem(i) {{ cart.splice(i,1); renderCart(); }}
    function toggleCart() {{ const m=document.getElementById('cart-modal'); m.style.display=m.style.display==='block'?'none':'block'; document.getElementById('cart-overlay').style.display=m.style.display; }}
    function checkoutWhatsApp() {{ let msg="New Order:%0A"; let total=0; cart.forEach(i=>{{msg+=`- ${{i.name}} (${{i.price}})%0A`; total+=parseFloat(i.price.replace(/[^0-9.]/g,''))||0;}}); msg+=`%0ATotal: ${{total.toFixed(2)}}%0A%0A${{payLinks}}`; window.open(`https://wa.me/${{wa_num}}?text=${{msg}}`, '_blank'); cart=[]; renderCart(); toggleCart(); }}
    window.addEventListener('load', renderCart);
    </script>
    """

def gen_lang_script():
    if not lang_sheet: return ""
    return f"""<script>async function toggleLang(){{try{{const r=await fetch('{lang_sheet}');const t=await r.text();const l=t.split(/\\r\\n|\\n/);for(let i=1;i<l.length;i++){{const c=l[i].split(',');if(c.length>1){{const e=document.getElementById(c[0]);if(e)e.innerText=c[1];}}}}alert("Language Switched!");}}catch(e){{console.log(e);}}}}</script>"""

def gen_inner_header(title):
    return f"""<section class="hero" style="min-height: 40vh; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img_1}'); background-size: cover; background-position: center;"><div class="container"><h1>{title}</h1></div></section>"""

def gen_footer():
    icons = ""
    if fb_link: icons += f'<a href="{fb_link}" target="_blank"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>'
    return f"""<footer><div class="container"><div class="footer-grid"><div><h3>{biz_name}</h3><p>{biz_addr}</p><div style="margin-top:1rem;display:flex;gap:1rem;">{icons}</div></div><div><h4>Links</h4><a href="index.html">Home</a><a href="booking.html">Book</a></div><div><h4>Legal</h4><a href="privacy.html">Privacy</a></div></div><div style="margin-top:3rem;text-align:center;opacity:0.6;">&copy; 2026 {biz_name}</div></div></footer>"""

def build_page(title, content, extra=""):
    css = get_theme_css()
    pwa = f'<link rel="manifest" href="manifest.json"><meta name="theme-color" content="{p_color}">'
    sw = "<script>if('serviceWorker' in navigator){navigator.serviceWorker.register('service-worker.js');}</script>"
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title} | {biz_name}</title>{pwa}{gen_schema()}<link href="https://fonts.googleapis.com/css2?family={h_font.replace(' ','+')}:wght@400;700&family={b_font.replace(' ','+')}:wght@300;400;600&display=swap" rel="stylesheet"><style>{css}</style></head><body>{gen_nav()}{content}{gen_footer()}{gen_wa_widget()}{gen_cart_system()}{gen_lang_script()}{sw}{extra}</body></html>"""

# --- RESTORED PAGE CONTENT GENERATORS ---

# 1. RESTORED CONTACT PAGE (Fixed Layout)
contact_content = f"""
{gen_inner_header("Contact Us")}
<section>
    <div class="container">
        <div class="contact-grid">
            <!-- Left: Info -->
            <div>
                <div style="background:var(--card); padding:2rem; border-radius:12px; border:1px solid #eee;">
                    <h3 style="color:var(--p);">Get In Touch</h3>
                    <p style="margin-top:1rem;"><strong>📍 Address:</strong><br>{biz_addr.replace(chr(10),'<br>')}</p>
                    <p style="margin-top:1rem;"><strong>📞 Phone:</strong><br><a href="tel:{biz_phone}" style="color:var(--s);">{biz_phone}</a></p>
                    <p style="margin-top:1rem;"><strong>📧 Email:</strong><br><a href="mailto:{biz_email}">{biz_email}</a></p>
                    <br>
                    <a href="https://wa.me/{wa_num}" target="_blank" class="btn btn-accent" style="width:100%; text-align:center;">Chat on WhatsApp</a>
                </div>
            </div>
            
            <!-- Right: Form -->
            <div class="card">
                <h3 style="margin-bottom:1.5rem;">Send a Message</h3>
                <form action="https://formsubmit.co/{biz_email}" method="POST">
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                        <div><label>Name</label><input type="text" name="name" required placeholder="Your Name"></div>
                        <div><label>Email</label><input type="email" name="email" required placeholder="Your Email"></div>
                    </div>
                    <label>Message</label><textarea name="message" rows="5" required placeholder="How can we help you?"></textarea>
                    <button type="submit" class="btn btn-primary" style="width:100%;">Send Message</button>
                    <input type="hidden" name="_captcha" value="false">
                    <input type="hidden" name="_next" value="{prod_url}/contact.html">
                </form>
            </div>
        </div>
        <br><br>
        <div style="border-radius:12px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.1);">{map_iframe}</div>
    </div>
</section>
"""

# 2. RESTORED ABOUT PAGE
about_full_content = f"""
{gen_inner_header("About Us")}
<section><div class="container">
    <div class="about-grid">
        <div class="legal-text">{format_text(about_long)}</div>
        <img src="{about_img}" style="width:100%; border-radius:var(--radius); box-shadow:0 10px 30px rgba(0,0,0,0.1);">
    </div>
</div></section>
"""

# 3. HOME PAGE
home_content = ""
if show_hero: home_content += gen_hero()
if show_stats: home_content += gen_stats()
if show_features: home_content += gen_features()
if show_pricing: home_content += gen_pricing_table()
if show_inventory: 
    # Store JS
    js_inv = f"""<script>function parseCSVLine(s){{const r=[];let c='';let q=false;for(let i=0;i<s.length;i++){{const x=s[i];if(x==='"'){{if(q&&s[i+1]==='"'){{c+='"';i++}}else{{q=!q}}}}else if(x===','&&!q){{r.push(c.trim());c=''}}else{{c+=x}}}}r.push(c.trim());return r}}async function loadInv(){{const r=await fetch('{sheet_url}');const t=await r.text();const l=t.split(/\\r\\n|\\n/);const b=document.getElementById('inv-grid');b.innerHTML='';for(let i=1;i<l.length;i++){{if(!l[i].trim())continue;const c=parseCSVLine(l[i]);let m=c[3]&&c[3].length>5?c[3]:'{custom_feat}';let s=c.length>4&&c[4].includes('http')?c[4]:'';if(c.length>1){{let x=s?`<a href="${{s}}" class="btn btn-primary">Buy Now</a>`:`<button onclick="addToCart('${{c[0]}}','${{c[1]}}')" class="btn">Add to Cart</button>`;b.innerHTML+=`<div class="card reveal"><img src="${{m}}" class="prod-img"><div><h3>${{c[0]}}</h3><p style="color:var(--s);font-weight:bold;">${{c[1]}}</p><p style="font-size:0.9rem;">${{c[2]}}</p>${{x}}</div></div>`;}}}}}}if(document.getElementById('inv-grid'))window.addEventListener('load',loadInv);</script>"""
    home_content += f'<section id="inventory" style="background:#f9f9f9"><div class="container"><div class="section-head reveal"><h2>Portfolio</h2></div><div id="inv-grid" class="grid-3">Loading...</div></div></section>{js_inv}'
if show_gallery: home_content += gen_about_section()
if show_testimonials: home_content += f'<section style="background:#f8fafc"><div class="container"><div class="section-head"><h2>Stories</h2></div><div class="grid-3">' + "".join([f'<div class="card"><i>"{l.split("|")[1]}"</i><br><b>- {l.split("|")[0]}</b></div>' for l in testi_data.split('\n') if "|" in l]) + '</div></div></section>'
if show_faq: home_content += gen_faq_section()
if show_cta: home_content += f'<section style="background:var(--s);color:white;text-align:center;"><div class="container reveal"><h2>Ready?</h2><a href="contact.html" class="btn" style="background:white;color:var(--s);">Get Started</a></div></section>'

# --- 7. DOWNLOAD & PREVIEW ---
st.divider()
st.subheader("🚀 Launchpad")
preview_mode = st.radio("Preview Page:", ["Home", "About", "Contact", "Booking"], horizontal=True)

c1, c2 = st.columns([3, 1])
with c1:
    if preview_mode == "Home": st.components.v1.html(build_page("Home", home_content), height=600, scrolling=True)
    elif preview_mode == "About": st.components.v1.html(build_page("About", about_full_content), height=600, scrolling=True)
    elif preview_mode == "Contact": st.components.v1.html(build_page("Contact", contact_content), height=600, scrolling=True)
    elif preview_mode == "Booking": st.components.v1.html(build_page("Booking", f"{gen_inner_header(booking_title)}<div class='container' style='padding:2rem 0;text-align:center'>{booking_embed}</div>"), height=600, scrolling=True)

with c2:
    if st.button("DOWNLOAD WEBSITE ZIP", type="primary"):
        z_b = io.BytesIO()
        with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
            zf.writestr("index.html", build_page("Home", home_content))
            zf.writestr("about.html", build_page("About", about_full_content))
            zf.writestr("contact.html", build_page("Contact", contact_content))
            zf.writestr("booking.html", build_page("Booking", f"{gen_inner_header(booking_title)}<div class='container' style='padding:2rem 0;text-align:center'>{booking_embed}</div>"))
            zf.writestr("privacy.html", build_page("Privacy", f"{gen_inner_header('Privacy')}<div class='container'>{format_text(priv_txt)}</div>"))
            zf.writestr("terms.html", build_page("Terms", f"{gen_inner_header('Terms')}<div class='container'>{format_text(term_txt)}</div>"))
            zf.writestr("manifest.json", gen_pwa_manifest())
            zf.writestr("service-worker.js", gen_sw())
        st.download_button("📥 Click to Save", z_b.getvalue(), f"{biz_name}_v35.1.zip", "application/zip")
