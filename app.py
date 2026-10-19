import streamlit as st
from PIL import Image
from datetime import datetime
import urllib.parse

# --- تحميل صورة اللوجو كأيقونة للمتجر (Favicon) ---
try:
    logo_icon = Image.open("logo.jpg")
except:
    logo_icon = "👑"

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="MORA STORE", 
    page_icon=logo_icon, 
    layout="centered"
)

# --- ربط ملف المظهر الخارجي manifest.json ---
st.markdown("""
    <head>
        <link rel="manifest" href="manifest.json">
    </head>
""", unsafe_allow_html=True)

# --- إدارة حالات Session State الشاملة ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""
if 'cart' not in st.session_state:
    st.session_state['cart'] = []
if 'wishlist' not in st.session_state:
    st.session_state['wishlist'] = []
if 'discount' not in st.session_state:
    st.session_state['discount'] = 0.0
if 'all_orders' not in st.session_state:
    st.session_state['all_orders'] = []
if 'reviews' not in st.session_state:
    st.session_state['reviews'] = {}
if 'last_order_wa' not in st.session_state:
    st.session_state['last_order_wa'] = ""

# قائمة المنتجات الأساسية مع صور أو رموز افتراضية
if 'products_list' not in st.session_state:
    st.session_state['products_list'] = [
        {"name": "هودي MORA الأسود", "price": 450, "img": "tshirt.jpg", "category": "ملابس", "has_variants": True, "key": "tshirt"},
        {"name": "شروال MORA الرياضي", "price": 350, "img": "pants.jpg", "category": "ملابس", "has_variants": True, "key": "pants"},
        {"name": "الطقم الكامل MORA", "price": 750, "img": "full_suit.jpg", "category": "ملابس", "has_variants": True, "key": "suit"},
        {"name": "عطر MORA كلاسيك", "price": 500, "img": "perfume.jpg", "category": "عطور", "has_variants": False, "key": "perfume1"},
        {"name": "عطر MORA الملكي", "price": 600, "img": "perfume2.jpg", "category": "عطور", "has_variants": False, "key": "perfume2"},
        {"name": "ساعة MORA الفاخرة", "price": 850, "img": "watch.jpg", "category": "أكسسوارات", "has_variants": False, "key": "watch"},
        {"name": "الحذاء الرياضي العصري", "price": 550, "img": "sneakers.jpg", "category": "أكسسوارات", "has_variants": True, "key": "sneakers"},
        {"name": "الجاكيت الجلد العصري", "price": 950, "img": "jacket.jpg", "category": "ملابس", "has_variants": True, "key": "jacket"},
        {"name": "النظارة الشمسية MORA", "price": 400, "img": "sunglasses.jpg", "category": "أكسسوارات", "has_variants": False, "key": "sunglasses"},
        {"name": "السوار المعدني الفاخر", "price": 250, "img": "bracelet.jpg", "category": "أكسسوارات", "has_variants": False, "key": "bracelet"}
    ]

# إدارة المخزون الافتراضي
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = {
        "tshirt": 15, "pants": 20, "suit": 10, "perfume1": 8, "perfume2": 12,
        "watch": 5, "sneakers": 14, "jacket": 7, "sunglasses": 9, "bracelet": 25
    }

# --- تصميم الألوان والطباعة الاحترافية (CSS) ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1f4068 0%, #162447 50%, #1b1b2f 100%);
            color: #ffffff;
        }
        
        h1, h2, h3 {
            color: #e4e4e4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        }

        div.stButton > button {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            border-radius: 25px;
            border: none;
            padding: 10px 20px;
            font-size: 15px;
            font-weight: bold;
            width: 100%;
            box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
            transition: all 0.3s ease;
        }
        
        div.stButton > button:hover {
            background: linear-gradient(45deg, #ff4b2b, #ff416c);
            box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
            transform: translateY(-2px);
        }
        
        div.stTextInput > div > div > input, div.stSelectbox > div > div, div.stRadio > div, div.stTextArea > div > div > textarea {
            border-radius: 12px;
            border: 2px solid #00adb5;
            background-color: #0f172a;
            color: white;
        }

        @media print {
            header, footer, .stButton, div[data-testid="stToolbar"], .no-print {
                display: none !important;
            }
            .stApp {
                background: white !important;
                color: black !important;
            }
            .invoice-box {
                color: black !important;
                border: 2px solid #000 !important;
                padding: 20px !important;
                background-color: #fff !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- صفحة تسجيل الدخول ---
def show_login_page():
    col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
    with col_l2:
        try:
            st.image("logo.jpg", use_column_width=True)
        except:
            st.write("👑")
            
    st.markdown("<h1>MORA STORE</h1>", unsafe_allow_html=True)
    st.markdown("<h3>مرحباً بك، يرجى تسجيل الدخول للبدء</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("---")
        username = st.text_input("اسم المستخدم", placeholder="ادخل اسمك هنا...")
        password = st.text_input("كلمة المرور", type="password", placeholder="••••••••")
        
        login_button = st.button("تسجيل الدخول")
        
        if login_button:
            if username.strip() == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.session_state['is_admin'] = True
                st.session_state['user_name'] = "الأدمن (عمر)"
                st.success("تم تسجيل الدخول كأدمن بنجاح!")
                st.rerun()
            elif username.strip() != "" and password == "12345":
                st.session_state['logged_in'] = True
                st.session_state['is_admin'] = False
                st.session_state['user_name'] = username.strip()
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            elif username == "" or password == "":
                st.warning("الرجاء إدخال اسم المستخدم وكلمة المرور.")
            else:
                st.error("كلمة المرور غير صحيحة، يرجى المحاولة مرة أخرى.")

    st.write("\n\n")
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 14px;'>© 2026 MORA STORE. All Rights Reserved.</p>", unsafe_allow_html=True)

# --- لوحة تحكم الأدمن ---
def show_admin_page():
    st.markdown("<h1>🛠️ لوحة تحكم الإدارة - MORA STORE</h1>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### 📊 إحصائيات المبيعات العامة")
    total_revenue = sum(order['total'] for order in st.session_state['all_orders'])
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("عدد الطلبات المؤكدة", len(st.session_state['all_orders']))
    with col_s2:
        st.metric("إجمالي المبيعات", f"{total_revenue:.1f} جنيه")

    st.write("---")
    st.markdown("### ➕ إضافة منتج جديد (مع إمكانية رفع صورة حية)")
    with st.form("add_product_form"):
        new_name = st.text_input("اسم المنتج الجديد")
        new_price = st.number_input("سعر المنتج (بالجنيه)", min_value=1, value=100)
        new_category = st.selectbox("القسم", ["ملابس", "عطور", "أكسسوارات"])
        new_key = st.text_input("مفتاح فريد بالإنجليزية (مثال: jacket2)")
        new_stock = st.number_input("الكمية المتاحة في المخزون", min_value=1, value=10)
        uploaded_img = st.file_uploader("ارفع صورة المنتج (JPG/PNG)", type=["jpg", "jpeg", "png"])
        
        submit_product = st.form_submit_button("إضافة المنتج للمتجر")
        if submit_product:
            if new_name.strip() and new_key.strip():
                img_path = "logo.jpg"
                if uploaded_img is not None:
                    img_path = uploaded_img.name
                    with open(img_path, "wb") as f:
                        f.write(uploaded_img.getbuffer())

                st.session_state['products_list'].append({
                    "name": new_name.strip(),
                    "price": new_price,
                    "img": img_path,
                    "category": new_category,
                    "has_variants": True if new_category == "ملابس" else False,
                    "key": new_key.strip()
                })
                st.session_state['inventory'][new_key.strip()] = new_stock
                st.success(f"تم إضافة المنتج '{new_name}' بنجاح! 🎉")
                st.rerun()
            else:
                st.warning("الرجاء إدخال اسم المنتج والمفتاح الإنجليزي.")

    st.write("---")
    st.markdown("### 📦 إدارة وتحديث المخزون الحالي")
    for prod in st.session_state['products_list']:
        pkey = prod['key']
        current_qty = st.session_state['inventory'].get(pkey, 10)
        
        c_p1, c_p2 = st.columns([2, 1])
        with c_p1:
            st.write(f"🔹 **{prod['name']}** ({prod['category']}) - السعر: {prod['price']} جنيه")
        with c_p2:
            updated_qty = st.number_input(f"الكمية لـ {pkey}", value=current_qty, key=f"inv_qty_{pkey}", label_visibility="collapsed")
            st.session_state['inventory'][pkey] = updated_qty

    st.write("---")
    st.markdown("### 🧾 سجل الطلبات الأخيرة")
    if not st.session_state['all_orders']:
        st.write("لا توجد طلبات مسجلة حتى الآن.")
    else:
        for ord_idx, o in enumerate(reversed(st.session_state['all_orders']), 1):
            st.markdown(f"**طلب #{ord_idx}** - العميل: `{o['user']}` | الهاتف: `{o.get('phone', 'غير متوفر')}` | العنوان: `{o.get('address', 'غير متوفر')}` | الإجمالي: `{o['total']:.1f} جنيه` | الوقت: `{o['time']}`")

    st.write("\n")
    col_bt1, col_bt2, col_bt3 = st.columns([1, 2, 1])
    with col_bt2:
        if st.button("🚪 تسجيل الخروج", key="logout_admin"):
            st.session_state['logged_in'] = False
            st.session_state['is_admin'] = False
            st.session_state['user_name'] = ""
            st.rerun()

# --- صفحة المفضلة (Wishlist) ---
def show_wishlist_page():
    st.markdown("<h1>❤️ قائمة المفضلة - MORA STORE</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if not st.session_state['wishlist']:
        st.info("قائمة المفضلة فارغة حالياً. أضف منتجاتك المفضلة لتظهر هنا!")
    else:
        for w_item in st.session_state['wishlist']:
            col_w1, col_w2, col_w3 = st.columns([2, 1, 1])
            with col_w1:
                st.subheader(w_item['name'])
                st.markdown(f"**السعر:** {w_item['price']} جنيه")
            with col_w2:
                if st.button("نقل للعربة 🛒", key=f"mov_{w_item['key']}"):
                    st.session_state['cart'].append({
                        "item_key": w_item['key'],
                        "name": w_item['name'],
                        "price": w_item['price']
                    })
                    st.success("تم النقل إلى الفاتورة!")
            with col_w3:
                if st.button("إزالة ❌", key=f"rem_w_{w_item['key']}"):
                    st.session_state['wishlist'] = [i for i in st.session_state['wishlist'] if i['key'] != w_item['key']]
                    st.rerun()
            st.write("---")

    if st.button("العودة إلى المتجر"):
        st.session_state['show_wishlist'] = False
        st.rerun()

# --- صفحة المنتجات والتسوق ---
def show_products_page():
    user = st.session_state['user_name']
    
    c_top1, c_top2, c_top3, c_top4 = st.columns([2, 1, 1, 1])
    with c_top1:
        st.markdown(f"<h2>Hello, {user}! 👋</h2>", unsafe_allow_html=True)
    with c_top2:
        if st.button(f"❤️ المفضلة ({len(st.session_state['wishlist'])})"):
            st.session_state['show_wishlist'] = True
            st.session_state['show_cart'] = False
            st.rerun()
    with c_top3:
        cart_count = len(st.session_state['cart'])
        if st.button(f"🛒 الفاتورة ({cart_count})"):
            st.session_state['show_cart'] = True
            st.session_state['show_wishlist'] = False
            st.rerun()
    with c_top4:
        if st.button("🚪 خروج"):
            st.session_state['logged_in'] = False
            st.session_state['user_name'] = ""
            st.session_state['cart'] = []
            st.session_state['wishlist'] = []
            st.rerun()

    if st.session_state.get('show_wishlist', False):
        show_wishlist_page()
        return

    col_img1, col_img2, col_img3 = st.columns([1, 1, 1])
    with col_img2:
        try:
            st.image("logo.jpg", width=120)
        except:
            pass

    st.markdown("<p style='text-align: center; color: #00adb5; font-size: 18px;'>استمتع بأحدث تشكيلة من منتجات وعطور وأكسسوارات MORA CLOTHING الفخمة</p>", unsafe_allow_html=True)
    st.write("---")
    
    products = st.session_state['products_list']

    c_search, c_cat = st.columns([2, 1])
    with c_search:
        search_query = st.text_input("🔍 بحث عن منتج...", placeholder="اكتب اسم المنتج هنا...")
    with c_cat:
        selected_cat = st.selectbox("الأقسام", ["الكل", "ملابس", "عطور", "أكسسوارات"])

    filtered_products = [
        p for p in products 
        if (selected_cat == "الكل" or p["category"] == selected_cat)
        and (search_query.strip().lower() in p["name"].lower())
    ]

    st.write("---")

    if not filtered_products:
        st.warning("لم يتم العثور على منتجات تطابق بحثك.")
    
    for i in range(0, len(filtered_products), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            p1 = filtered_products[i]
            st.subheader(p1["name"])
            try:
                st.image(p1["img"], use_column_width=True)
            except:
                st.write("👑")
            st.markdown(f"**السعر:** {p1['price']} جنيه")
            
            stock1 = st.session_state['inventory'].get(p1['key'], 0)
            st.caption(f"المخزون المتاح: {stock1} قطعة")

            size_selected, color_selected = "", ""
            if p1["has_variants"]:
                if p1["key"] == "sneakers":
                    size_selected = st.selectbox("المقاس", ["40", "41", "42", "43", "44", "45"], key=f"sz_{p1['key']}")
                else:
                    size_selected = st.selectbox("المقاس", ["S", "M", "L", "XL", "XXL"], key=f"sz_{p1['key']}")
                    color_selected = st.selectbox("اللون", ["أسود", "أبيض", "كحلي"], key=f"cl_{p1['key']}")

            c_b1, c_b2 = st.columns(2)
            with c_b1:
                if stock1 > 0:
                    if st.button("إضافة للعربة", key=f"btn_{p1['key']}"):
                        variant_info = f" ({size_selected} - {color_selected})" if p1["has_variants"] and color_selected else (f" (مقاس: {size_selected})" if size_selected else "")
                        st.session_state['cart'].append({
                            "item_key": p1["key"],
                            "name": p1["name"] + variant_info, 
                            "price": p1["price"]
                        })
                        st.success("تمت الإضافة للفاتورة!")
                else:
                    st.error("نفذت الكمية!")
            with c_b2:
                if st.button("❤️ مفضلة", key=f"wish_{p1['key']}"):
                    if not any(item['key'] == p1['key'] for item in st.session_state['wishlist']):
                        st.session_state['wishlist'].append(p1)
                        st.success("أضيف للمفضلة!")
                    else:
                        st.info("المنتج موجود مسبقاً بالمفضلة.")

            with st.expander("⭐ تقييمات المنتج وآراء العملاء"):
                prod_reviews = st.session_state['reviews'].get(p1['key'], [])
                if not prod_reviews:
                    st.write("لا توجد تقييمات بعد. كن أول من يقييم!")
                else:
                    for rev in prod_reviews:
                        st.markdown(f"⭐ **{rev['rating']}/5** - {rev['user']}: {rev['comment']}")
                
                with st.form(key=f"rev_form_{p1['key']}"):
                    r_score = st.slider("التقييم بالنجوم", 1, 5, 5, key=f"r_sc_{p1['key']}")
                    r_comment = st.text_area("أكتب رأيك...", key=f"r_cm_{p1['key']}")
                    r_submit = st.form_submit_button("إرسال التقييم")
                    if r_submit:
                        if p1['key'] not in st.session_state['reviews']:
                            st.session_state['reviews'][p1['key']] = []
                        st.session_state['reviews'][p1['key']].append({
                            "user": user,
                            "rating": r_score,
                            "comment": r_comment
                        })
                        st.success("شكراً لتقييمك!")
                        st.rerun()

        if i + 1 < len(filtered_products):
            with col2:
                p2 = filtered_products[i + 1]
                st.subheader(p2["name"])
                try:
                    st.image(p2["img"], use_column_width=True)
                except:
                    st.write("👑")
                st.markdown(f"**السعر:** {p2['price']} جنيه")
                
                stock2 = st.session_state['inventory'].get(p2['key'], 0)
                st.caption(f"المخزون المتاح: {stock2} قطعة")

                size_selected2, color_selected2 = "", ""
                if p2["has_variants"]:
                    if p2["key"] == "sneakers":
                        size_selected2 = st.selectbox("المقاس", ["40", "41", "42", "43", "44", "45"], key=f"sz_{p2['key']}")
                    else:
                        size_selected2 = st.selectbox("المقاس", ["S", "M", "L", "XL", "XXL"], key=f"sz_{p2['key']}")
                        color_selected2 = st.selectbox("اللون", ["أسود", "أبيض", "كحلي"], key=f"cl_{p2['key']}")

                c_bb1, c_bb2 = st.columns(2)
                with c_bb1:
                    if stock2 > 0:
                        if st.button("إضافة للعربة", key=f"btn_{p2['key']}"):
                            variant_info2 = f" ({size_selected2} - {color_selected2})" if p2["has_variants"] and color_selected2 else (f" (مقاس: {size_selected2})" if size_selected2 else "")
                            st.session_state['cart'].append({
                                "item_key": p2["key"],
                                "name": p2["name"] + variant_info2, 
                                "price": p2["price"]
                            })
                            st.success("تمت الإضافة للفاتورة!")
                    else:
                        st.error("نفذت الكمية!")
                with c_bb2:
                    if st.button("❤️ مفضلة", key=f"wish_{p2['key']}"):
                        if not any(item['key'] == p2['key'] for item in st.session_state['wishlist']):
                            st.session_state['wishlist'].append(p2)
                            st.success("أضيف للمفضلة!")
                        else:
                            st.info("المنتج موجود مسبقاً بالمفضلة.")

                with st.expander("⭐ تقييمات المنتج وآراء العملاء"):
                    prod_reviews2 = st.session_state['reviews'].get(p2['key'], [])
                    if not prod_reviews2:
                        st.write("لا توجد تقييمات بعد. كن أول من يقييم!")
                    else:
                        for rev in prod_reviews2:
                            st.markdown(f"⭐ **{rev['rating']}/5** - {rev['user']}: {rev['comment']}")
                    
                    with st.form(key=f"rev_form_{p2['key']}"):
                        r_score2 = st.slider("التقييم بالنجوم", 1, 5, 5, key=f"r_sc_{p2['key']}")
                        r_comment2 = st.text_area("أكتب رأيك...", key=f"r_cm_{p2['key']}")
                        r_submit2 = st.form_submit_button("إرسال التقييم")
                        if r_submit2:
                            if p2['key'] not in st.session_state['reviews']:
                                st.session_state['reviews'][p2['key']] = []
                            st.session_state['reviews'][p2['key']].append({
                                "user": user,
                                "rating": r_score2,
                                "comment": r_comment2
                            })
                            st.success("شكراً لتقييمك!")
                            st.rerun()
        
        st.write("---")

    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 14px;'>© 2026 MORA STORE. All Rights Reserved.</p>", unsafe_allow_html=True)

# --- صفحة الفاتورة والدفع وتفاصيل الشحن ---
def show_cart_page():
    user = st.session_state['user_name']
    now_str = datetime.now().strftime("%d/%m/%Y - %I:%M %p")
    
    st.markdown(f"<h1>🧾 فاتورة المشتريات وعنوان الشحن - MORA STORE</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if len(st.session_state['cart']) == 0:
        st.info("عربة التسوق فارغة حالياً. لم تقم بإضافة أي منتجات بعد.")
    else:
        raw_total = sum(item['price'] for item in st.session_state['cart'])
        discount_amount = raw_total * st.session_state['discount']
        final_total = raw_total - discount_amount

        st.markdown("### 📍 تفاصيل وعنوان الشحن للعميل:")
        c_ph1, c_ph2 = st.columns(2)
        with c_ph1:
            customer_phone = st.text_input("رقم الهاتف للتواصل:", placeholder="مثال: 01012345678")
        with c_ph2:
            customer_city = st.selectbox("المحافظة:", ["القاهرة", "الجيزة", "الإسكندرية", "الدقهلية", "الغربية", "الشرقية", "أسيوط", "أخرى"])
        
        customer_address = st.text_input("العنوان بالتفصيل (الشارع، المنطقة، رقم الحضانة/المنزل):")

        st.write("---")
        st.markdown("### 💳 اختر طريقة الدفع:")
        payment_method = st.radio("طريقة الدفع:", ["الدفع عند الاستلام (Cash on Delivery)", "فودافون كاش (Vodafone Cash)"])
        
        if "فودافون كاش" in payment_method:
            st.warning("📱 **رقم تحويل فودافون كاش الخاص بالمتجر:** `01558478544` \n\n يرجى تحويل قيمة الفاتورة وإرسال صورة التحويل عبر الواتساب لتأكيد الشحن.")

        st.write("---")
        c_code1, c_code2 = st.columns([2, 1])
        with c_code1:
            promo_input = st.text_input("هل لديك كود خصم؟", placeholder="مثال: MORA10")
        with c_code2:
            st.write("\n")
            if st.button("تطبيق الخصم"):
                if promo_input.strip().upper() == "MORA10":
                    st.session_state['discount'] = 0.10
                    st.success("تم تطبيق خصم 10% بنجاح! 🎉")
                    st.rerun()
                else:
                    st.error("كود غير صحيح!")

        items_html = ""
        items_text_wa = ""
        for idx, item in enumerate(st.session_state['cart'], 1):
            items_html += f"<div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #334155;'><span><b>{idx}. {item['name']}</b></span><span><b>{item['price']} جنيه</b></span></div>"
            items_text_wa += f"{idx}. {item['name']} - {item['price']} EGP\n"

        invoice_template = f"""
        <div class="invoice-box" style="background-color: #0f172a; padding: 25px; border-radius: 15px; border: 1px solid #00adb5; margin-bottom: 20px;">
            <div style="text-align: center; margin-bottom: 15px;">
                <h2 style="margin:0; color: #00adb5;">👑 MORA STORE</h2>
                <p style="margin:5px 0; font-size:14px; color:#cbd5e1;">عميلنا العزيز: <b>{user}</b> | الهاتف: <b>{customer_phone}</b></p>
                <p style="margin:5px 0; font-size:14px; color:#cbd5e1;">📍 المحافظة: <b>{customer_city}</b> - العنوان: <b>{customer_address}</b></p>
                <p style="margin:5px 0; font-size:13px; color:#00adb5;">📅 <b>تاريخ ووقت الطلب: {now_str}</b></p>
                <p style="margin:5px 0; font-size:13px; color:#ff416c;">💳 <b>طريقة الدفع: {payment_method}</b></p>
                <hr style="border-color:#334155;">
            </div>
            {items_html}
            <div style="margin-top:15px; text-align:right;">
                <p style="margin:3px 0; font-size:14px;">الإجمالي قبل الخصم: {raw_total} جنيه</p>
                <p style="margin:3px 0; font-size:14px; color:#00adb5;">الخصم: {discount_amount:.1f} جنيه</p>
            </div>
            <div style="display:flex; justify-content:space-between; padding-top:10px; font-size:20px; font-weight:bold; color:#ff416c; border-top:1px dashed #00adb5;">
                <span>الإجمالي الكلي:</span>
                <span>{final_total:.1f} جنيه</span>
            </div>
        </div>
        """
        st.markdown(invoice_template, unsafe_allow_html=True)

        st.components.v1.html("""
            <button onclick="window.parent.print()" style="
                background: linear-gradient(45deg, #00adb5, #0077b6);
                color: white; border: none; padding: 12px 24px;
                font-size: 16px; font-weight: bold; border-radius: 25px;
                cursor: pointer; width: 100%; box-shadow: 0 4px 15px rgba(0, 173, 181, 0.4);
            ">🖨️ اضغط هنا لطباعة الفاتورة الآن</button>
        """, height=60)

        wa_admin_message = f"🚨 تنبيه طلب جديد لمتاجر MORA STORE!\n\nاسم العميل: {user}\nالهاتف: {customer_phone}\nالمحافظة: {customer_city}\nالعنوان: {customer_address}\nالتاريخ: {now_str}\nطريقة الدفع: {payment_method}\n\nالمنتجات المطلوبة:\n{items_text_wa}\nالإجمالي الكلي: {final_total:.1f} جنيه"
        encoded_wa_admin = urllib.parse.quote(wa_admin_message)
        wa_admin_url = f"https://wa.me/201558478544?text={encoded_wa_admin}"

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("إتمام الشراء وتأكيد الطلب"):
                if not customer_phone.strip() or not customer_address.strip():
                    st.error("الرجاء إدخال رقم الهاتف وعنوان الشحن بدقة لتأكيد الطلب!")
                else:
                    for cart_item in st.session_state['cart']:
                        key = cart_item.get('item_key')
                        if key in st.session_state['inventory'] and st.session_state['inventory'][key] > 0:
                            st.session_state['inventory'][key] -= 1
                    
                    st.session_state['all_orders'].append({
                        "user": user,
                        "phone": customer_phone,
                        "address": f"{customer_city} - {customer_address}",
                        "total": final_total,
                        "payment": payment_method,
                        "time": now_str
                    })
                    
                    st.session_state['last_order_wa'] = wa_admin_url
                    st.success("🎉 تم تأكيد طلبك بنجاح! شكراً لتسوقك في MORA STORE.")
                    st.session_state['cart'] = []
                    st.session_state['discount'] = 0.0
        with col_btn2:
            if st.button("تفريغ الفاتورة"):
                st.session_state['cart'] = []
                st.session_state['discount'] = 0.0
                st.rerun()

        if st.session_state.get('last_order_wa'):
            st.write("\n")
            st.markdown(f"""
                <a href="{st.session_state['last_order_wa']}" target="_blank" style="text-decoration:none;">
                    <div style="background-color:#25D366; color:white; text-align:center; padding:15px; border-radius:25px; font-weight:bold; font-size:18px; box-shadow:0 4px 15px rgba(37, 211, 102, 0.4);">
                        📲 اضغط هنا لإرسال تفاصيل الفاتورة والطلب إلى واتساب الأدمن (أنت)
                    </div>
                </a>
            """, unsafe_allow_html=True)

    st.write("---")
    if st.button("العودة إلى المتجر"):
        st.session_state['show_cart'] = False
        st.rerun()

    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 14px;'>© 2026 MORA STORE. All Rights Reserved.</p>", unsafe_allow_html=True)

# --- التحكم في التنقل الرئيسي ---
if not st.session_state['logged_in']:
    show_login_page()
else:
    if st.session_state['is_admin']:
        show_admin_page()
    else:
        if 'show_cart' not in st.session_state:
            st.session_state['show_cart'] = False
        
        if st.session_state['show_cart']:
            show_cart_page()
        else:
            show_products_page()