/**
 * Krishi Kendra - Comprehensive Multilingual Translation Engine (i18n)
 * Languages supported: English (en), Hindi (hi), Marathi (mr), Tamil (ta), Telugu (te)
 * Features:
 *  - Key-based [data-i18n] replacement
 *  - Bulletproof per-text-node translation with lossless original text caching
 *  - Input/Textarea placeholder translation
 *  - Select option translation
 *  - Dynamic DOM MutationObserver for modals and popups
 *  - Complete dictionary covering Homepage, Farmer Dashboard, Buyer Dashboard,
 *    Cold Storage, Govt Schemes, Marketplace, Orders, Inventory, Logistics & Cards.
 */

// 1. Core Key-Based Translations
const KRISHI_TRANSLATIONS = {
  en: {
    brand_title: "Krishi Kendra",
    brand_tagline: "Direct Farm-to-Buyer Agricultural Trade & Fulfilment",
    nav_home: "Home",
    nav_dashboard: "Dashboard",
    nav_inventory: "My Inventory",
    nav_orders: "Orders & Requests",
    nav_mandi: "Mandi Rates",
    nav_cold_storage: "Cold Storage",
    nav_marketplace: "Farm Supplies",
    nav_schemes: "Govt Schemes",
    nav_card: "Visiting Card",
    nav_requests: "My Requests",
    heading_my_requests: "My Service Requests Hub",
    nav_login: "Login",
    nav_register: "Register",
    nav_logout: "Logout",
    role_farmer: "Farmer",
    role_buyer: "Buyer",
    btn_add_produce: "Add Produce",
    btn_post_req: "Post Requirement",
    btn_compare_offers: "Compare Offers",
    mandi_benchmark: "APMC Mandi Benchmark",
    verified_badge: "Verified",
    total_inventory: "Total Inventory",
    active_orders: "Active Orders",
    total_sales: "Total Sales (Completed)",
    pending_payments: "Pending Payments",

    // Home Page Hero
    hero_sih_badge: "SIH 2026 Problem SIH26033 Solution",
    hero_title: "Better Markets. Direct Connections. Smarter Agricultural Trade.",
    hero_desc: "Eliminating exploitative middlemen across the farm-to-fork chain. Connecting farmers directly with bulk & retail buyers with live APMC Mandi price discovery, smart counter-negotiation, and tracked fulfilment.",
    btn_farmer_dash: "Farmer Dashboard",
    btn_list_crop: "List New Crop",
    btn_buyer_dash: "Buyer Dashboard",
    btn_explore_market: "Explore Marketplace",
    btn_admin_portal: "Admin Portal",
    btn_i_am_farmer: "I am a Farmer (किसान)",
    btn_i_am_buyer: "I am a Buyer (खरीदार)",

    // Real-Time Impact
    impact_title: "Real-Time Platform Impact",
    stat_farmers: "Registered Farmers",
    stat_buyers: "Direct Buyers",
    stat_mandis: "APMC Mandis Linked",
    stat_cold_storages: "Cold Storages",

    // How it works
    how_it_works_title: "How Krishi Kendra Works",
    how_it_works_sub: "A streamlined, transparent 4-step workflow for both Farmers and Buyers",
    for_farmers: "For Farmers",
    step_f1_title: "List Harvest Produce:",
    step_f1_desc: "Enter available crop quantity, expected price, quality grade, and photos.",
    step_f2_title: "Receive Direct Buyer Requests:",
    step_f2_desc: "Get notified instantly when nearby buyers match your crop and quantity range.",
    step_f3_title: "Smart Counter-Offer & Negotiation:",
    step_f3_desc: "Compare buyer offers with live Mandi benchmarks before accepting or countering.",
    step_f4_title: "Logistics & Escrow Payout:",
    step_f4_desc: "Book vehicle transport and receive guaranteed payment directly upon delivery.",

    for_buyers: "For Buyers",
    step_b1_title: "Post Exact Quantity Requirement:",
    step_b1_desc: "Enter the exact kilograms or quintals needed (no bulk/small restrictions).",
    step_b2_title: "Automated Matching Engine:",
    step_b2_desc: "The system identifies and notifies relevant farmers with adequate inventory.",
    step_b3_title: "Side-by-Side Offer Comparison:",
    step_b3_desc: "Compare quotes on price, farmer rating, proximity, and quality grades.",
    step_b4_title: "Live Delivery Tracking:",
    step_b4_desc: "Track the assigned vehicle from farm gate to your warehouse/storefront.",

    // Sections
    fresh_produce_heading: "Fresh Produce Direct from Verified Farmers",
    btn_view_all_produce: "View All Produce",
    btn_find_farmers: "Find Farmers",
    apmc_mandi_heading: "APMC Mandi Rates",
    badge_live_today: "Live Today",
    th_commodity: "Commodity",
    th_market: "Market",
    th_modal_price: "Modal Price",
    btn_view_all_mandi: "View All Mandi Rates",
    schemes_heading: "Government Schemes & Subsidies",
    btn_view_all_schemes: "View All",
    btn_apply_online: "Apply Online",
    cold_storage_heading: "Nearby Cold Storage Network",
    btn_explore_storage: "Explore Facilities",
    cold_storage_desc: "Prevent post-harvest distress selling and perishability losses by storing crops at verified, temperature-controlled facilities with transparent monthly rates.",
    btn_find_storage: "Find & Book Cold Storage"
  },

  hi: {
    brand_title: "कृषि केंद्र",
    brand_tagline: "सीधा किसान-से-व्यापारी कृषि व्यापार और आपूर्ति मंच",
    nav_home: "मुख्य पृष्ठ",
    nav_dashboard: "डैशबोर्ड",
    nav_inventory: "मेरी फसल सूची",
    nav_orders: "ऑर्डर व मांग",
    nav_mandi: "मंडी भाव",
    nav_cold_storage: "कोल्ड स्टोरेज",
    nav_marketplace: "कृषि बाजार",
    nav_schemes: "सरकारी योजनाएं",
    nav_card: "विजिटिंग कार्ड",
    nav_requests: "मेरी मांगें व अनुरोध",
    heading_my_requests: "मेरी सेवा अनुरोध व सहायता केंद्र",
    nav_login: "लॉगिन करें",
    nav_register: "पंजीकरण करें",
    nav_logout: "लॉगआउट",
    role_farmer: "किसान भाई",
    role_buyer: "खरीदार",
    btn_add_produce: "फसल जोड़ें",
    btn_post_req: "मांग पोस्ट करें",
    btn_compare_offers: "ऑफ़र की तुलना करें",
    mandi_benchmark: "मंडी औसत भाव",
    verified_badge: "सत्यापित",
    total_inventory: "कुल उपज भंडार",
    active_orders: "सक्रिय ऑर्डर",
    total_sales: "कुल बिक्री (पूर्ण)",
    pending_payments: "बकाया भुगतान",

    // Home Page Hero
    hero_sih_badge: "SIH 2026 समस्या SIH26033 समाधान",
    hero_title: "बेहतर बाजार। सीधा संपर्क। आधुनिक कृषि व्यापार।",
    hero_desc: "खेत से थाली तक बिचौलियों का उन्मूलन। लाइव APMC मंडी भाव, स्मार्ट बातचीत और डिलीवरी ट्रैकिंग के साथ किसानों को सीधे खरीदारों से जोड़ना।",
    btn_farmer_dash: "किसान डैशबोर्ड",
    btn_list_crop: "नई फसल जोड़ें",
    btn_buyer_dash: "खरीदार डैशबोर्ड",
    btn_explore_market: "मंडी बाजार देखें",
    btn_admin_portal: "प्रशासनिक पोर्टल",
    btn_i_am_farmer: "मैं एक किसान हूँ (Farmer)",
    btn_i_am_buyer: "मैं एक खरीदार हूँ (Buyer)",

    // Real-Time Impact
    impact_title: "प्लेटफ़ॉर्म प्रभाव (लाइव)",
    stat_farmers: "पंजीकृत किसान",
    stat_buyers: "सीधे खरीदार",
    stat_mandis: "जुड़ी हुई APMC मंडियां",
    stat_cold_storages: "सत्यापित कोल्ड स्टोरेज",

    // How it works
    how_it_works_title: "कृषि केंद्र कैसे काम करता है",
    how_it_works_sub: "किसानों और खरीदारों दोनों के लिए 4-चरणीय पारदर्शी प्रक्रिया",
    for_farmers: "किसानों के लिए",
    step_f1_title: "फसल दर्ज करें:",
    step_f1_desc: "उपलब्ध मात्रा, अपेक्षित मूल्य, गुणवत्ता ग्रेड और फोटो जोड़ें।",
    step_f2_title: "सीधे खरीदार मांग प्राप्त करें:",
    step_f2_desc: "निकटतम खरीदार की मांग मिलने पर तुरंत सूचना प्राप्त करें।",
    step_f3_title: "स्मार्ट बातचीत और काउंटर-ऑफ़र:",
    step_f3_desc: "लाइव मंडी बेंचमार्क देखकर खरीदार के ऑफ़र पर निर्णय लें।",
    step_f4_title: "लॉजिस्टिक्स और गारंटीड भुगतान:",
    step_f4_desc: "वाहन बुक करें और डिलीवरी होते ही बैंक खाते में सीधा भुगतान प्राप्त करें।",

    for_buyers: "खरीदारों के लिए",
    step_b1_title: "सटीक मांग दर्ज करें:",
    step_b1_desc: "आवश्यक किलोग्राम या क्विंटल दर्ज करें (कम या अधिक मात्रा की कोई बाधा नहीं)।",
    step_b2_title: "स्वचालित मिलान प्रणाली:",
    step_b2_desc: "उपयुक्त स्टॉक वाले नजदीकी किसानों को स्वचालित रूप से सूचित किया जाता है।",
    step_b3_title: "ऑफ़र की तुलना करें:",
    step_b3_desc: "मूल्य, गुणवत्ता, किसान रेटिंग और दूरी के आधार पर ऑफ़र की तुलना करें।",
    step_b4_title: "लाइव वाहन ट्रैकिंग:",
    step_b4_desc: "खेत से लेकर गोदाम तक वाहन को लाइव ट्रैक करें।",

    // Sections
    fresh_produce_heading: "सत्यापित किसानों से ताज़ा कृषि उपज",
    btn_view_all_produce: "सभी उपज देखें",
    btn_find_farmers: "किसान खोजें",
    apmc_mandi_heading: "APMC लाइव मंडी भाव",
    badge_live_today: "आज का लाइव भाव",
    th_commodity: "फसल / वस्तु",
    th_market: "मंडी",
    th_modal_price: "औसत भाव",
    btn_view_all_mandi: "सभी मंडी भाव देखें",
    schemes_heading: "सरकारी कल्याणकारी योजनाएं व सब्सिडी",
    btn_view_all_schemes: "सभी देखें",
    btn_apply_online: "ऑनलाइन आवेदन करें",
    cold_storage_heading: "नजदीकी कोल्ड स्टोरेज नेटवर्क",
    btn_explore_storage: "सुविधाएं देखें",
    cold_storage_desc: "फसल को सुरक्षित तापमान नियंत्रित कोल्ड स्टोरेज में रखकर उचित मूल्य मिलने तक नुकसान से बचाएं।",
    btn_find_storage: "कोल्ड स्टोरेज खोजें और बुक करें"
  },

  mr: {
    brand_title: "कृषी केंद्र",
    brand_tagline: "थेट शेतकरी ते खरेदीदार कृषी व्यापार आणि पूर्तता मंच",
    nav_home: "मुख्य पान",
    nav_dashboard: "डॅशबोर्ड",
    nav_inventory: "माझी शेतमाल यादी",
    nav_orders: "ऑर्डर्स आणि मागण्या",
    nav_mandi: "बाजार भाव",
    nav_cold_storage: "शीतगृह (कोल्ड स्टोरेज)",
    nav_marketplace: "कृषी बाजार",
    nav_schemes: "शासकीय योजना",
    nav_card: "व्हिजिटिंग कार्ड",
    nav_requests: "माझ्या विनंत्या व अर्ज",
    heading_my_requests: "माझे सेवा विनंती व मदत केंद्र",
    nav_login: "लॉगिन",
    nav_register: "नोंदणी करा",
    nav_logout: "बाहेर पडा",
    role_farmer: "शेतकरी बंधू",
    role_buyer: "खरेदीदार",
    btn_add_produce: "शेतमाल जोडा",
    btn_post_req: "मागणी नोंदवा",
    btn_compare_offers: "दर तुलना करा",
    mandi_benchmark: "बाजार समिती सरासरी दर",
    verified_badge: "प्रमाणित",
    total_inventory: "एकूण साठा",
    active_orders: "सक्रिय ऑर्डर्स",
    total_sales: "एकूण विक्री (पूर्ण)",
    pending_payments: "प्रलंबित पेमेंट",

    hero_sih_badge: "SIH 2026 समस्या SIH26033 उपाय",
    hero_title: "उत्तम बाजारपेठ. थेट जोडणी. आधुनिक कृषी व्यापार.",
    hero_desc: "मध्यस्थांचे उच्चाटन करून शेतकऱ्यांना थेट घाऊक व किरकोळ खरेदीदारांशी जोडणारा पारदर्शक प्लॅटफॉर्म.",
    btn_farmer_dash: "शेतकरी डॅशबोर्ड",
    btn_list_crop: "नवीन शेतमाल जोडा",
    btn_buyer_dash: "खरेदीदार डॅशबोर्ड",
    btn_explore_market: "बाजारपेठ पहा",
    btn_admin_portal: "प्रशासक पोर्टल",
    btn_i_am_farmer: "मी शेतकरी आहे (Farmer)",
    btn_i_am_buyer: "मी खरेदीदार आहे (Buyer)",

    impact_title: "प्लॅटफॉर्म प्रभाव (थेट)",
    stat_farmers: "नोंदणीकृत शेतकरी",
    stat_buyers: "थेट खरेदीदार",
    stat_mandis: "जोडलेल्या बाजार समित्या",
    stat_cold_storages: "शीतगृहे (Cold Storage)",

    how_it_works_title: "कृषी केंद्र कसे कार्य करते",
    how_it_works_sub: "शेतकरी आणि खरेदीदारांसाठी 4 सोप्या पायऱ्या",
    for_farmers: "शेतकऱ्यांसाठी",
    step_f1_title: "शेतमाल नोंदवा:",
    step_f1_desc: "उपलब्ध प्रमाण, अपेक्षित दर आणि गुणवत्ता प्रत नोंदवा.",
    step_f2_title: "थेट खरेदीदार मागणी मिळवा:",
    step_f2_desc: "जवळपासच्या खरेदीदारांची मागणी आल्यास त्वरित संदेश मिळवा.",
    step_f3_title: "स्मार्ट दर वाटाघाटी:",
    step_f3_desc: "थेट बाजार भाव तपासून खरेदीदाराच्या ऑफरवर निर्णय घ्या.",
    step_f4_title: "वाहतूक व खात्रीशीर पेमेंट:",
    step_f4_desc: "माल पोहोचताच थेट बँक खात्यात सुरक्षित पेमेंट मिळवा.",

    for_buyers: "खरेदीदारांसाठी",
    step_b1_title: "आवश्यकता नोंदवा:",
    step_b1_desc: "हवे असलेले अचूक प्रमाण किलो किंवा क्विंटलमध्ये प्रविष्ट करा.",
    step_b2_title: "स्वयंचलित शेतकरी शोध:",
    step_b2_desc: "उपलब्ध माल असलेल्या शेतकऱ्यांना त्वरित सूचित केले जाते.",
    step_b3_title: "दर तुलना:",
    step_b3_desc: "किंमत, शेतकरी रेटिंग आणि अंतरावर आधारित तुलना करा.",
    step_b4_title: "थेट वाहन ट्रॅकिंग:",
    step_b4_desc: "शेतापासून गोदामापर्यंत वाहनाचा थेट मागोवा घ्या.",

    fresh_produce_heading: "प्रमाणित शेतकऱ्यांचा ताजा शेतमाल",
    btn_view_all_produce: "सर्व शेतमाल पहा",
    btn_find_farmers: "शेतकरी शोधा",
    apmc_mandi_heading: "बाजार समिती थेट दर",
    badge_live_today: "आजचे थेट दर",
    th_commodity: "शेतमाल",
    th_market: "बाजार समिती",
    th_modal_price: "सरासरी दर",
    btn_view_all_mandi: "सर्व बाजार भाव पहा",
    schemes_heading: "शासकीय कृषी योजना व सबसिडी",
    btn_view_all_schemes: "सर्व पहा",
    btn_apply_online: "ऑनलाइन अर्ज करा",
    cold_storage_heading: "जवळपासची शीतगृहे (Cold Storage)",
    btn_explore_storage: "सुविधा पहा",
    cold_storage_desc: "शेतमाल खराब होण्यापासून वाचवण्यासाठी शीतगृहात साठवा.",
    btn_find_storage: "शीतगृह शोधा व बुक करा"
  },

  ta: {
    brand_title: "கிருஷி கேந்திரா",
    brand_tagline: "நேரடி உழவர்-வாங்குவோர் விவசாய வர்த்தக தளம்",
    nav_home: "முகப்பு",
    nav_dashboard: "டாஷ்போர்டு",
    nav_inventory: "விளைச்சல்",
    nav_orders: "ஆர்டர்கள்",
    nav_mandi: "மண்டி விலை",
    nav_cold_storage: "குளிர்பதன கிடங்கு",
    nav_marketplace: "விவசாய சந்தை",
    nav_schemes: "அரசு திட்டங்கள்",
    nav_card: "விசிட்டிங் கார்டு",
    nav_requests: "எனது கோரிக்கைகள்",
    heading_my_requests: "எனது சேவை கோரிக்கைகள் மையம்",
    nav_login: "உள்நுழைக",
    nav_register: "பதிவு செய்க",
    nav_logout: "வெளியேறு",
    role_farmer: "விவசாயி",
    role_buyer: "வாங்குபவர்",
    btn_add_produce: "பயிர் சேர்க்க",
    btn_post_req: "தேவையை பதிவிடுக",
    btn_compare_offers: "விலை ஒப்பீடு",
    mandi_benchmark: "சந்தை சராசரி விலை",
    verified_badge: "சரிபார்க்கப்பட்டது",
    total_inventory: "மொத்த இருப்பு",
    active_orders: "செயலில் உள்ள ஆர்டர்கள்",
    total_sales: "மொத்த விற்பனை (முடிந்தது)",
    pending_payments: "நிலுவையில் உள்ள கட்டணம்",

    hero_sih_badge: "SIH 2026 தீர்வு SIH26033",
    hero_title: "சிறந்த சந்தை. நேரடி தொடர்பு. ஸ்மார்ட் விவசாய வர்த்தகம்.",
    hero_desc: "இடைத்தரகர்களை அகற்றி விவசாயிகளையும் வாங்குபவர்களையும் நேரடியாக இணைக்கும் நவீன தளம்.",
    btn_farmer_dash: "விவசாயி டாஷ்போர்டு",
    btn_list_crop: "புதிய பயிர் சேர்க்க",
    btn_buyer_dash: "வாங்குபவர் டாஷ்போர்டு",
    btn_explore_market: "சந்தையை காண்க",
    btn_admin_portal: "நிர்வாக தளம்",
    btn_i_am_farmer: "நான் ஒரு விவசாயி",
    btn_i_am_buyer: "நான் ஒரு வாங்குபவர்",

    impact_title: "தளத்தின் நேரடி தாக்கம்",
    stat_farmers: "பதிவு செய்த விவசாயிகள்",
    stat_buyers: "நேரடி வாங்குபவர்கள்",
    stat_mandis: "இணைக்கப்பட்ட மண்டிகள்",
    stat_cold_storages: "குளிர்பதன கிடங்குகள்",

    how_it_works_title: "கிருஷி கேந்திரா எவ்வாறு செயல்படுகிறது",
    how_it_works_sub: "விவசாயிகள் மற்றும் வாங்குபவர்களுக்கான 4 எளிய வழிமுறைகள்",
    for_farmers: "விவசாயிகளுக்கு",
    step_f1_title: "விளைச்சலை பட்டியலிடுக:",
    step_f1_desc: "அளவு, விலை மற்றும் தரத்தை உள்ளிடவும்.",
    step_f2_title: "வாங்குபவர் கோரிக்கைகளைப் பெறுக:",
    step_f2_desc: "பொருத்தமான வாங்குபவர்களிடமிருந்து உடனடி அறிவிப்பைப் பெறுங்கள்.",
    step_f3_title: "விலை பேச்சுவார்த்தை:",
    step_f3_desc: "நேரடி மண்டி விலையை ஒப்பிட்டு முடிவு செய்யுங்கள்.",
    step_f4_title: "பாதுகாப்பான கட்டணம்:",
    step_f4_desc: "பொருட்கள் விநியோகிக்கப்பட்டவுடன் நேரடியாக வங்கிக் கணக்கில் பணம் பெறவும்.",

    for_buyers: "வாங்குபவர்களுக்கு",
    step_b1_title: "தேவையை பதிவிடவும்:",
    step_b1_desc: "தேவையான சரியான எடையை உள்ளிடவும்.",
    step_b2_title: "விவசாயி பொருத்தம்:",
    step_b2_desc: "பொருத்தமான விவசாயிகளுக்கு தானாகவே தகவல் அனுப்பப்படும்.",
    step_b3_title: "விலை ஒப்பீடு:",
    step_b3_desc: "விலை, தரம் மற்றும் தூரத்தின் அடிப்படையில் ஒப்பிடவும்.",
    step_b4_title: "நேரடி வாகன கண்காணிப்பு:",
    step_b4_desc: "பண்ணையிலிருந்து குடோன் வரை வாகனத்தை கண்காணிக்கவும்.",

    fresh_produce_heading: "விவசாயிகளிடமிருந்து புதிய விளைபொருட்கள்",
    btn_view_all_produce: "அனைத்தையும் காண்க",
    btn_find_farmers: "விவசாயிகளை தேடு",
    apmc_mandi_heading: "நேரடி மண்டி விலை",
    badge_live_today: "இன்றைய நேரலை",
    th_commodity: "பொருள்",
    th_market: "சந்தை",
    th_modal_price: "சராசரி விலை",
    btn_view_all_mandi: "அனைத்து விலைகளையும் காண்க",
    schemes_heading: "அரசு நலத்திட்டங்கள் & மானியங்கள்",
    btn_view_all_schemes: "அனைத்தும்",
    btn_apply_online: "விண்ணப்பிக்கவும்",
    cold_storage_heading: "அருகிலுள்ள குளிர்பதன கிடங்குகள்",
    btn_explore_storage: "கிடங்குகளை காண்க",
    cold_storage_desc: "விளைச்சலை பாதுகாப்பான குளிர்பதன கிடங்கில் சேமிக்கவும்.",
    btn_find_storage: "கிடங்கை பதிவு செய்க"
  },

  te: {
    brand_title: "కృషి కేంద్రం",
    brand_tagline: "రైతు మరియు కొనుగోలుదారు ప్రత్యక్ష వ్యవసాయ వాణిజ్య వేదిక",
    nav_home: "హోమ్",
    nav_dashboard: "డ్యాష్‌బోర్డ్",
    nav_inventory: "నా పంట నిల్వలు",
    nav_orders: "ఆర్డర్లు",
    nav_mandi: "మార్కెట్ ధరలు",
    nav_cold_storage: "కోల్డ్ స్టోరేజ్",
    nav_marketplace: "వ్యవసాయ మార్కెట్",
    nav_schemes: "ప్రభుత్వ పథకాలు",
    nav_card: "విజిటింగ్ కార్డు",
    nav_requests: "నా అభ్యర్థనలు",
    heading_my_requests: "నా సేవా అభ్యర్థనల కేంద్రం",
    nav_login: "లాగిన్",
    nav_register: "నమోదు",
    nav_logout: "లాగ్ అవుట్",
    role_farmer: "రైతు",
    role_buyer: "కొనుగోలుదారు",
    btn_add_produce: "పంటను జోడించండి",
    btn_post_req: "అవసరాన్ని నమోదు చేయండి",
    btn_compare_offers: "ధరల పోలిక",
    mandi_benchmark: "మార్కెట్ సగటు ధర",
    verified_badge: "ధృవీకరించబడింది",
    total_inventory: "మొత్తం నిల్వ",
    active_orders: "యాక్టివ్ ఆర్డర్లు",
    total_sales: "మొత్తం అమ్మకాలు (పూర్తయింది)",
    pending_payments: "బాకీ ఉన్న చెల్లింపులు",

    hero_sih_badge: "SIH 2026 పరిష్కారం SIH26033",
    hero_title: "మెరుగైన మార్కెట్. ప్రత్యక్ష అనుసంధానం. ఆధునిక వ్యవసాయ వాణిజ్యం.",
    hero_desc: "దళారుల రహిత వ్యవసాయ వాణిజ్యం ద్వారా రైతులకు సరసమైన ధరలు మరియు కొనుగోలుదారులకు నాణ్యమైన ఉత్పత్తులు.",
    btn_farmer_dash: "రైతు డ్యాష్‌బోర్డ్",
    btn_list_crop: "కొత్త పంటను జోడించండి",
    btn_buyer_dash: "కొనుగోలుదారు డ్యాష్‌బోర్డ్",
    btn_explore_market: "మార్కెట్ చూడండి",
    btn_admin_portal: "అడ్మిన్ పోర్టల్",
    btn_i_am_farmer: "నేను రైతును",
    btn_i_am_buyer: "నేను కొనుగోలుదారుని",

    impact_title: "ప్లాట్‌ఫారమ్ ప్రత్యక్ష ప్రభావం",
    stat_farmers: "నమోదైన రైతులు",
    stat_buyers: "ప్రత్యక్ష కొనుగోలుదారులు",
    stat_mandis: "అనుసంధానించబడిన మార్కెట్లు",
    stat_cold_storages: "కోల్డ్ స్టోరేజీలు",

    how_it_works_title: "కృషి కేంద్రం ఎలా పనిచేస్తుంది",
    how_it_works_sub: "రైతులు మరియు కొనుగోలుదారుల కోసం 4 సులభమైన దశలు",
    for_farmers: "రైతుల కోసం",
    step_f1_title: "పంట వివరాలు నమోదు చేయండి:",
    step_f1_desc: "పరిమాణం, ఆశించిన ధర మరియు నాణ్యతను నమోదు చేయండి.",
    step_f2_title: "కొనుగోలుదారుల ఆఫర్లు పొందండి:",
    step_f2_desc: "సమీప కొనుగోలుదారుల నుండి తక్షణ నోటిఫికేషన్లు పొందండి.",
    step_f3_title: "ధరల చర్చలు & కౌంటర్ ఆఫర్:",
    step_f3_desc: "లైవ్ మండి ధరలతో పోల్చి సరైన ధరను నిర్ణయించండి.",
    step_f4_title: "రవాణా & సురక్షిత చెల్లింపు:",
    step_f4_desc: "డెలివరీ పూర్తయిన వెంటనే నేరుగా బ్యాంక్ ఖాతాలోకి డబ్బులు జమ అవుతాయి.",

    for_buyers: "కొనుగోలుదారుల కోసం",
    step_b1_title: "మీ అవసరాన్ని పోస్ట్ చేయండి:",
    step_b1_desc: "కావలసిన పరిమాణాన్ని నమోదు చేయండి.",
    step_b2_title: "రైతుల సరిపోలిక:",
    step_b2_desc: "తగిన పంట నిల్వ ఉన్న రైతులకు స్వయంచాలకంగా సమాచారం అందుతుంది.",
    step_b3_title: "ధరల పోలిక:",
    step_b3_desc: "ధర, నాణ్యత మరియు దూరం ఆధారంగా ఉత్తమ ఆఫర్‌ను ఎంచుకోండి.",
    step_b4_title: "లైవ్ వెహికల్ ట్రాకింగ్:",
    step_b4_desc: "పొలం నుండి గిడ్డంగి వరకు వాహనాన్ని ట్రాక్ చేయండి.",

    fresh_produce_heading: "ధృవీకరించబడిన రైతుల నుండి తాజా పంటలు",
    btn_view_all_produce: "అన్ని ఉత్పత్తులను చూడండి",
    btn_find_farmers: "రైతులను కనుగొనండి",
    apmc_mandi_heading: "APMC లైవ్ మార్కెట్ ధరలు",
    badge_live_today: "నేటి ప్రత్యక్ష ధరలు",
    th_commodity: "పంట",
    th_market: "మార్కెట్",
    th_modal_price: "సగటు ధర",
    btn_view_all_mandi: "అన్ని ధరలను చూడండి",
    schemes_heading: "ప్రభుత్వ సంక్షేమ పథకాలు",
    btn_view_all_schemes: "అన్నీ చూడండి",
    btn_apply_online: "దరఖాస్తు చేసుకోండి",
    cold_storage_heading: "సమీప కోల్డ్ స్టోరేజ్ నెట్‌వర్క్",
    btn_explore_storage: "వివరాలు చూడండి",
    cold_storage_desc: "పంటలను కోల్డ్ స్టోరేజీలో భద్రపరుచుకోండి.",
    btn_find_storage: "కోల్డ్ స్టోరేజ్ బుక్ చేయండి"
  }
};

// 2. Comprehensive Phrase Translation Dictionary for Full UI Coverage across all pages
const KRISHI_PHRASES = {
  // Navigation & Core Labels
  "Home": { hi: "मुख्य पृष्ठ", mr: "मुख्य पान", ta: "முகப்பு", te: "హోమ్" },
  "Dashboard": { hi: "डैशबोर्ड", mr: "डॅशबोर्ड", ta: "டாஷ்போர்டு", te: "డ్యాష్‌బోర్డ్" },
  "My Inventory": { hi: "मेरी फसल सूची", mr: "माझी शेतमाल यादी", ta: "விளைச்சல் பட்டியல்", te: "నా పంట నిల్వలు" },
  "Orders": { hi: "ऑर्डर सूची", mr: "ऑर्डर्स", ta: "ஆர்டர்கள்", te: "ఆర్డర్లు" },
  "Orders & Requests": { hi: "ऑर्डर व मांग", mr: "ऑर्डर्स आणि मागण्या", ta: "ஆர்டர்கள் & கோரிக்கைகள்", te: "ఆర్డర్లు & అభ్యర్థనలు" },
  "My Orders": { hi: "मेरे ऑर्डर", mr: "माझे ऑर्डर्स", ta: "எனது ஆர்டர்கள்", te: "నా ఆర్డర్లు" },
  "Cold Storage": { hi: "कोल्ड स्टोरेज", mr: "शीतगृह", ta: "குளிர்பதன கிடங்கு", te: "కోల్డ్ స్టోరేజ్" },
  "Farm Supplies": { hi: "कृषि सामग्री", mr: "शेती साहित्य", ta: "விவசாய பொருட்கள்", te: "వ్యవసాయ సామాగ్రి" },
  "Govt Schemes": { hi: "सरकारी योजनाएं", mr: "शासकीय योजना", ta: "அரசு திட்டங்கள்", te: "ప్రభుత్వ పథకాలు" },
  "Visiting Card": { hi: "विजिटिंग कार्ड", mr: "व्हिजिटिंग कार्ड", ta: "விசிட்டிங் கார்டு", te: "విజిటింగ్ కార్డు" },
  "My Visiting Card": { hi: "मेरा विजिटिंग कार्ड", mr: "माझे व्हिजिटिंग कार्ड", ta: "எனது விசிட்டிங் கார்டு", te: "నా విజిటింగ్ కార్డు" },
  "Profile & Privacy": { hi: "प्रोफाइल व गोपनीयता", mr: "प्रोफाइल व गोपनीयता", ta: "சுயவிவரம் & தனியுரிமை", te: "ప్రొఫైల్ & గోప్యత" },
  "Logout": { hi: "लॉगआउट", mr: "बाहेर पडा", ta: "வெளியேறு", te: "లాగ్ అవుట్" },
  "Login": { hi: "लॉगिन करें", mr: "लॉगिन", ta: "உள்நுழைக", te: "లాగిన్" },
  "Register": { hi: "पंजीकरण करें", mr: "नोंदणी करा", ta: "பதிவு செய்க", te: "నమోదు" },
  "Admin Portal": { hi: "प्रशासनिक पोर्टल", mr: "प्रशासक पोर्टल", ta: "நிர்வாக தளம்", te: "అడ్మిన్ పోర్టల్" },
  "Recent Notifications": { hi: "हाल की सूचनाएं", mr: "अलीकडील सूचना", ta: "சமீபத்திய அறிவிப்புகள்", te: "ఇటీవలి నోటిఫికేషన్లు" },
  "No notifications yet.": { hi: "अभी कोई सूचना नहीं है।", mr: "अद्याप कोणतीही सूचना नाही.", ta: "அறிவிப்புகள் எதுவும் இல்லை.", te: "ఇంకా నోటిఫికేషన్లు లేవు." },

  // User Header & Badges
  "Namaste,": { hi: "नमस्ते,", mr: "नमस्ते,", ta: "வணக்கம்,", te: "నమస్తే," },
  "Welcome,": { hi: "स्वागत है,", mr: "स्वागत आहे,", ta: "வரவேற்பு,", te: "స్వాగతం," },
  "Verified Farmer": { hi: "सत्यापित किसान", mr: "प्रमाणित शेतकरी", ta: "சரிபார்க்கப்பட்ட விவசாயி", te: "ధృవీకరించబడిన రైతు" },
  "Verified Buyer": { hi: "सत्यापित खरीदार", mr: "प्रमाणित खरेदीदार", ta: "சரிபார்க்கப்பட்ட வாங்குபவர்", te: "ధృవీకరించబడిన కొనుగోలుదారు" },
  "Farmer ID:": { hi: "किसान आईडी:", mr: "शेतकरी आयडी:", ta: "விவசாயி எண்:", te: "రైతు ఐడి:" },
  "Buyer ID:": { hi: "खरीदार आईडी:", mr: "खरेदीदार आयडी:", ta: "வாங்குபவர் எண்:", te: "కొనుగోలుదారు ఐడి:" },
  "Location:": { hi: "स्थान:", mr: "ठिकाण:", ta: "இடம்:", te: "ప్రాంతం:" },
  "Organization:": { hi: "संस्था:", mr: "संस्था:", ta: "நிறுவனம்:", te: "సంస్థ:" },
  "Total Inventory": { hi: "कुल उपज भंडार", mr: "एकूण साठा", ta: "மொத்த இருப்பு", te: "మొత్తం నిల్వ" },
  "Active Orders": { hi: "सक्रिय ऑर्डर", mr: "सक्रिय ऑर्डर्स", ta: "செயலில் உள்ள ஆர்டர்கள்", te: "యాక్టివ్ ఆర్డర్లు" },
  "Total Sales (Completed)": { hi: "कुल बिक्री (पूर्ण)", mr: "एकूण विक्री (पूर्ण)", ta: "மொத்த விற்பனை (முடிந்தது)", te: "మొత్తం అమ్మకాలు" },
  "Pending Payments": { hi: "बकाया भुगतान", mr: "प्रलंबित पेमेंट", ta: "நிலுவையில் உள்ள கட்டணம்", te: "బాకీ ఉన్న చెల్లింపులు" },
  "Pending Farmer Offers": { hi: "लंबित किसान ऑफ़र", mr: "प्रलंबित शेतकरी ऑफर्स", ta: "நிலுவையில் உள்ள ஆஃபர்கள்", te: "పెండింగ్ రైతు ఆఫర్లు" },
  "Orders in Transit": { hi: "रास्ते में ऑर्डर", mr: "मार्गावरील ऑर्डर्स", ta: "வழியில் உள்ள ஆர்டர்கள்", te: "రవాణాలో ఉన్న ఆర్డర్లు" },
  "My Posted Requirements": { hi: "मेरी पोस्ट की गई मांगें", mr: "माझ्या नोंदवलेल्या मागण्या", ta: "எனது தேவைகள்", te: "నా అవసరాలు" },

  // Farmer Quick Actions Grid
  "Farmer Quick Actions": { hi: "किसान त्वरित सुविधाएं", mr: "शेतकरी जलद कृती", ta: "விவசாயி விரைவு சேவைகள்", te: "రైతు త్వరిత సేవలు" },
  "Add Produce": { hi: "फसल जोड़ें", mr: "शेतमाल जोडा", ta: "பயிர் சேர்க்க", te: "పంటను జోడించండి" },
  "Buyer Requests": { hi: "खरीदार मांग", mr: "खरेदीदार मागण्या", ta: "வாங்குபவர் கோரிக்கைகள்", te: "కొనుగోలుదారు అభ్యర్థనలు" },
  "Live Mandi Rates": { hi: "लाइव मंडी भाव", mr: "थेट बाजार भाव", ta: "நேரலை மண்டி விலை", te: "లైవ్ మార్కెట్ ధరలు" },
  "Book Transport": { hi: "वाहन बुक करें", mr: "वाहतूक बुक करा", ta: "வாகனம் பதிவு செய்க", te: "రవాణా బుక్ చేయండి" },
  "Cold Storage": { hi: "कोल्ड स्टोरेज", mr: "शीतगृह (Cold Storage)", ta: "குளிர்பதன கிடங்கு", te: "కోల్డ్ స్టోరేజ్" },
  "Seeds & Fertilizers": { hi: "बीज व खाद", mr: "बियाणे व खते", ta: "விதைகள் & உரங்கள்", te: "విత్తనాలు & ఎరువులు" },
  "Govt Schemes": { hi: "सरकारी योजनाएं", mr: "शासकीय योजना", ta: "அரசு திட்டங்கள்", te: "ప్రభుత్వ పథకాలు" },
  "Post Requirement (Qty)": { hi: "मांग पोस्ट करें (मात्रा)", mr: "मागणी नोंदवा (प्रमाण)", ta: "தேவையை பதிவிடுக", te: "అవసరాన్ని పోస్ట్ చేయండి" },

  // Farmer Dashboard Cards & Tables
  "Recent Buyer Offers & Requests": { hi: "हाल के खरीदार ऑफ़र व मांग", mr: "अलीकडील खरेदीदार ऑफर्स व मागण्या", ta: "சமீபத்திய வாங்குபவர் ஆஃபர்கள்", te: "ఇటీవలి కొనుగోలుదారు ఆఫర్లు" },
  "View All Requests": { hi: "सभी मांगें देखें", mr: "सर्व मागण्या पहा", ta: "அனைத்து கோரிக்கைகளையும் காண்க", te: "అన్ని అభ్యర్థనలను చూడండి" },
  "Product": { hi: "उत्पाद", mr: "शेतमाल", ta: "பொருள்", te: "ఉత్పత్తి" },
  "Quantity": { hi: "मात्रा", mr: "प्रमाण", ta: "அளவு", te: "పరిమాణం" },
  "Offered Price": { hi: "प्रस्तावित मूल्य", mr: "प्रस्तावित दर", ta: "வழங்கப்பட்ட விலை", te: "ఆఫర్ చేసిన ధర" },
  "Buyer": { hi: "खरीदार", mr: "खरेदीदार", ta: "வாங்குபவர்", te: "కొనుగోలుదారు" },
  "Status": { hi: "स्थिति", mr: "स्थिती", ta: "நிலை", te: "స్థితి" },
  "Action": { hi: "कार्यवाही", mr: "कृती", ta: "செயல்", te: "చర్య" },
  "Actions": { hi: "कार्यवाही", mr: "कृती", ta: "செயல்கள்", te: "చర్యలు" },
  "Review": { hi: "समीक्षा करें", mr: "तपासा", ta: "மதிப்பாய்வு", te: "పరిశీలించండి" },
  "No buyer requests yet. Add produce to your inventory to start receiving direct purchase orders!": {
    hi: "अभी कोई खरीदार मांग नहीं है। सीधे खरीद ऑर्डर प्राप्त करने के लिए अपनी फसल सूची में उत्पाद जोड़ें!",
    mr: "अद्याप कोणतीही खरेदीदार मागणी नाही. थेट ऑर्डर मिळवण्यासाठी नवीन शेतमाल नोंदवा!",
    ta: "வாங்குபவர் கோரிக்கைகள் எதுவும் இல்லை. உங்கள் விளைச்சலை சேர்த்து நேரடி ஆர்டர்களைப் பெறுங்கள்!",
    te: "ఇంకా కొనుగోలుదారు అభ్యర్థనలు లేవు. ప్రత్యక్ష ఆర్డర్లు పొందడానికి మీ పంటను చేర్చండి!"
  },
  "Add Produce Now": { hi: "अभी फसल जोड़ें", mr: "आत्ताच शेतमाल जोडा", ta: "இப்போதே சேர்க்க", te: "ఇప్పుడే జోడించండి" },
  "Active Produce Stock": { hi: "सक्रिय उपलब्ध स्टॉक", mr: "सक्रिय उपलब्ध साठा", ta: "செயலில் உள்ள இருப்பு", te: "అందుబాటులో ఉన్న నిల్వ" },
  "Manage All": { hi: "सभी प्रबंधित करें", mr: "सर्व व्यवस्थापित करा", ta: "அனைத்தையும் நிர்வகி", te: "అన్నీ నిర్వహించండి" },
  "Stock:": { hi: "स्टॉक:", mr: "साठा:", ta: "இருப்பு:", te: "నిల్వ:" },
  "No produce in inventory.": { hi: "सूची में कोई फसल नहीं है।", mr: "यादीत कोणताही शेतमाल नाही.", ta: "இருப்பில் பயிர் எதுவும் இல்லை.", te: "నిల్వలో పంట లేదు." },
  "Add First Crop": { hi: "पहली फसल जोड़ें", mr: "पहिले पीक जोडा", ta: "முதல் பயிரை சேர்க்க", te: "మొదటి పంటను జోడించండి" },

  // Buyer Dashboard
  "Looking for Specific Produce?": { hi: "क्या आप विशिष्ट कृषि उपज की तलाश में हैं?", mr: "तुम्हाला विशिष्ट शेतमाल हवा आहे का?", ta: "குறிப்பிட்ட விளைபொருள் தேவையா?", te: "నిర్దిష్ట పంట కోసం చూస్తున్నారా?" },
  "Post your required crop and quantity. Our matching engine will notify eligible farmers directly with zero middleman markups.": {
    hi: "अपनी आवश्यक फसल और मात्रा पोस्ट करें। हमारी प्रणाली योग्य किसानों को सीधे बिना किसी बिचौलिये के सूचित करेगी।",
    mr: "तुमची आवश्यक शेतमाल मागणी नोंदवा. आमची यंत्रणा पात्र शेतकऱ्यांना थेट शून्य मध्यस्थांसह सूचित करेल.",
    ta: "உங்கள் தேவையை பதிவு செய்யுங்கள். தகுதியான விவசாயிகளுக்கு நேரடியாக தகவல் அனுப்பப்படும்.",
    te: "మీకు కావలసిన పంట మరియు పరిమాణాన్ని పోస్ట్ చేయండి. అర్హులైన రైతులకు దళారులు లేకుండా నేరుగా సమాచారం అందుతుంది."
  },
  "Post New Requirement": { hi: "नई मांग पोस्ट करें", mr: "नवीन मागणी नोंदवा", ta: "புதிய தேவையை பதிவிடுக", te: "కొత్త అవసరాన్ని పోస్ట్ చేయండి" },
  "Farmer Counter-Offers Awaiting Your Decision:": { hi: "किसान के काउंटर-ऑफ़र आपके निर्णय की प्रतीक्षा में:", mr: "शेतकऱ्यांचे काउंटर-ऑफर्स तुमच्या निर्णयाच्या प्रतीक्षेत:", ta: "விவசாயியின் மாற்று ஆஃபர்கள்:", te: "రైతు కౌంటర్ ఆఫర్లు:" },
  "Review Offer": { hi: "ऑफ़र देखें", mr: "ऑफर पहा", ta: "ஆஃபரை காண்க", te: "ఆఫర్ చూడండి" },
  "Fresh Farm Produce Available for Direct Purchase": { hi: "सीधी खरीद के लिए उपलब्ध ताज़ा कृषि उपज", mr: "थेट खरेदीसाठी उपलब्ध ताजा शेतमाल", ta: "நேரடி கொள்முதலுக்கு கிடைக்கும் புதிய விளைபொருட்கள்", te: "ప్రత్యక్ష కొనుగోలుకు అందుబాటులో ఉన్న తాజా పంటలు" },
  "Browse All": { hi: "सभी देखें", mr: "सर्व पहा", ta: "அனைத்தையும் காண்க", te: "అన్నీ చూడండి" },
  "Farmer:": { hi: "किसान:", mr: "शेतकरी:", ta: "விவசாயி:", te: "రైతు:" },
  "Available Stock:": { hi: "उपलब्ध स्टॉक:", mr: "उपलब्ध साठा:", ta: "கிடைக்கும் இருப்பு:", te: "అందుబాటులో ఉన్న నిల్వ:" },
  "Make Offer / Buy": { hi: "ऑफ़र दें / खरीदें", mr: "ऑफर द्या / खरेदी करा", ta: "ஆஃபர் செய்க / வாங்குக", te: "ఆఫర్ ఇవ్వండి / కొనండి" },
  "No active produce listed currently.": { hi: "वर्तमान में कोई फसल सूचीबद्ध नहीं है।", mr: "सध्या कोणताही शेतमाल नोंदवलेला नाही.", ta: "பயிர்கள் எதுவும் பட்டியலிடப்படவில்லை.", te: "ప్రస్తుతం ఏ పంటలు జాబితా చేయబడలేదు." },
  "My Active Requirements": { hi: "मेरी सक्रिय मांगें", mr: "माझ्या सक्रिय मागण्या", ta: "எனது செயலில் உள்ள தேவைகள்", te: "నా యాక్టివ్ అవసరాలు" },
  "Post New": { hi: "नया जोड़ें", mr: "नवीन जोडा", ta: "புதியது சேர்க்க", te: "కొత్తది చేర్చండి" },
  "Need:": { hi: "आवश्यकता:", mr: "गरज:", ta: "தேவை:", te: "అవసరం:" },
  "Target:": { hi: "लक्षित मूल्य:", mr: "अपेक्षित दर:", ta: "இலக்கு விலை:", te: "లక్ష్య ధర:" },
  "View Farmer Offers": { hi: "किसान ऑफ़र देखें", mr: "शेतकरी ऑफर्स पहा", ta: "விவசாயி ஆஃபர்களை காண்க", te: "రైతు ఆఫర్లు చూడండి" },
  "You haven't posted any requirements yet.": { hi: "आपने अभी तक कोई मांग पोस्ट नहीं की है।", mr: "तुम्ही अद्याप कोणतीही मागणी नोंदवली नाही.", ta: "நீங்கள் இன்னும் எந்த தேவையும் பதிவிடவில்லை.", te: "మీరు ఇంకా ఎలాంటి అవసరాలను పోస్ట్ చేయలేదు." },
  "Post Your First Requirement": { hi: "अपनी पहली मांग पोस्ट करें", mr: "पहिली मागणी नोंदवा", ta: "முதல் தேவையை பதிவிடுக", te: "మీ మొదటి అవసరాన్ని పోస్ట్ చేయండి" },

  // Cold Storage Tab
  "Cold Storage Facilities & Preservation Network": { hi: "कोल्ड स्टोरेज सुविधाएं व संरक्षण नेटवर्क", mr: "शीतगृह (Cold Storage) सुविधा व नेटवर्क", ta: "குளிர்பதன கிடங்கு வசதிகள் & பாதுகாப்பு கட்டமைப்பு", te: "కోల్డ్ స్టోరేజ్ సౌకర్యాలు & పరిరక్షణ నెట్‌వర్క్" },
  "Discover temperature-controlled warehouses to prevent harvest distress sales and preserve perishable produce": {
    hi: "फसल के नुकसान से बचने और उचित मूल्य मिलने तक सुरक्षित रखने के लिए तापमान-नियंत्रित गोदाम खोजें",
    mr: "शेतमालाचे नुकसान टाळण्यासाठी आणि योग्य दर मिळेपर्यंत साठवण्यासाठी शीतगृहे शोधा",
    ta: "விளைச்சலை பாதுகாப்பாக சேமித்து நஷ்டத்தை தவிர்க்க குளிர்பதன கிடங்குகளை கண்டறியுங்கள்",
    te: "పంట నష్టాన్ని నివారించడానికి మరియు సరైన ధర వచ్చేవరకు నిల్వ ఉంచడానికి కోల్డ్ స్టోరేజీలను కనుగొనండి"
  },
  "All Districts": { hi: "सभी ज़िले", mr: "सर्व जिल्हे", ta: "அனைத்து மாவட்டங்கள்", te: "అన్ని జిల్లాలు" },
  "Filter Facilities": { hi: "सुविधाएं खोजें", mr: "सुविधा शोधा", ta: "கிடங்குகளை வடிகட்டு", te: "సౌకర్యాలను ఫిల్టర్ చేయండి" },
  "Available Space:": { hi: "उपलब्ध स्थान:", mr: "उपलब्ध जागा:", ta: "கிடைக்கும் இடம்:", te: "అందుబాటులో ఉన్న స్థలం:" },
  "Storage Fee:": { hi: "भंडारण शुल्क:", mr: "साठवणूक शुल्क:", ta: "சேமிப்பு கட்டணம்:", te: "నిల్వ రుసుము:" },
  "Temperature:": { hi: "तापमान:", mr: "तापमान:", ta: "வெப்பநிலை:", te: "ఉష్ణోగ్రత:" },
  "Supported Produce:": { hi: "समर्थित फसलें:", mr: "साठवणूक योग्य शेतमाल:", ta: "ஏற்றுக்கொள்ளப்படும் பயிர்கள்:", te: "అనుకూలమైన పంటలు:" },
  "Request Storage": { hi: "स्टोरेज का अनुरोध करें", mr: "जागा विनंती करा", ta: "கிடங்கு கோரிக்கை", te: "స్టోరేజ్ అభ్యర్థన" },
  "Call Operator": { hi: "ऑपरेटर को कॉल करें", mr: "ऑपरेटरला कॉल करा", ta: "ஆபரேட்டரை அழைக்கவும்", te: "ఆపరేటర్‌కు కాల్ చేయండి" },
  "My Storage Booking Requests": { hi: "मेरी स्टोरेज बुकिंग मांगें", mr: "माझ्या शीतगृह बुकिंग विनंत्या", ta: "எனது முன்பதிவு கோரிக்கைகள்", te: "నా స్టోరేజ్ బుకింగ్ అభ్యర్థనలు" },
  "Facility": { hi: "सुविधा / केंद्र", mr: "सुविधा केंद्र", ta: "கிடங்கு", te: "సౌకర్యం" },
  "Produce": { hi: "फसल", mr: "शेतमाल", ta: "பயிர்", te: "పంట" },
  "Duration": { hi: "अवधि", mr: "कालावधी", ta: "கால அளவு", te: "వ్యవధి" },
  "Est. Cost": { hi: "अनुमानित लागत", mr: "अंदाजे खर्च", ta: "மதிப்பிடப்பட்ட செலவு", te: "అంచనా వ్యయం" },
  "Book Storage Space": { hi: "कोल्ड स्टोरेज बुक करें", mr: "शीतगृह जागा बुक करा", ta: "கிடங்கு முன்பதிவு செய்க", te: "స్టోరేజ్ బుక్ చేయండి" },
  "Book Cold Storage Space": { hi: "कोल्ड स्टोरेज बुक करें", mr: "शीतगृह जागा बुक करा", ta: "கிடங்கு முன்பதிவு செய்க", te: "కోల్డ్ స్టోరేజ్ బుక్ చేయండి" },

  // Government Schemes Tab
  "Central & State Government Agricultural Schemes": { hi: "केंद्र व राज्य सरकारी कृषि कल्याण योजनाएं", mr: "केंद्र व राज्य शासकीय कृषी कल्याण योजना", ta: "மத்திய & மாநில அரசு விவசாய திட்டங்கள்", te: "కేంద్ర & రాష్ట్ర ప్రభుత్వ వ్యవసాయ పథకాలు" },
  "Official subsidies, PM-KISAN, crop insurance, solar pumps, and direct farmer welfare programs": {
    hi: "आधिकारिक सब्सिडी, पीएम-किसान, फसल बीमा, सोलर पंप और प्रत्यक्ष किसान कल्याणकारी कार्यक्रम",
    mr: "अधिकृत सबसिडी, पीएम-किसान, पीक विमा, सौर कृषी पंप आणि थेट शेतकरी कल्याण योजना",
    ta: "அரசு மானியங்கள், பிஎம்-கிசான், பயிர் காப்பீடு, சோலார் பம்புகள் மற்றும் நலத்திட்டங்கள்",
    te: "ప్రభుత్వ రాయితీలు, పీఎం-కిసాన్, పంటల బీమా, సోలార్ పంపులు మరియు సంక్షేమ పథకాలు"
  },
  "Search Scheme (e.g. PM-KISAN, PMFBY, Solar)": { hi: "योजना खोजें (जैसे पीएम-किसान, फसल बीमा, सोलर पंप)", mr: "योजना शोधा (उदा. पीएम-किसान, पीक विमा, सोलर)", ta: "திட்டங்களை தேடுக (பிஎம்-கிசான், காப்பீடு)", te: "పథకాన్ని శోధించండి (పీఎం-కిసాన్, బీమా, సోలార్)" },
  "All Categories": { hi: "सभी श्रेणियां", mr: "सर्व वर्ग", ta: "அனைத்து வகைகள்", te: "అన్ని వర్గాలు" },
  "Key Benefits:": { hi: "मुख्य लाभ:", mr: "मुख्य फायदे:", ta: "முக்கிய நன்மைகள்:", te: "ముఖ్య ప్రయోజనాలు:" },
  "Eligibility:": { hi: "पात्रता मानदंड:", mr: "पात्रता निकष:", ta: "தகுதி வரம்புகள்:", te: "అర్హత నిబంధనలు:" },
  "Launch Year:": { hi: "शुरुआत वर्ष:", mr: "सुरुवात वर्ष:", ta: "தொடங்கப்பட்ட ஆண்டு:", te: "ప్రారంభించిన సంవత్సరం:" },
  "Official Portal": { hi: "आधिकारिक पोर्टल", mr: "अधिकृत पोर्टल", ta: "அதிகாரப்பூர்வ தளம்", te: "అధికారిక పోర్టల్" },

  // Farm Supplies Marketplace
  "Farm Supplies & Input Marketplace": { hi: "कृषि इनपुट व सामग्री बाजार", mr: "कृषी साहित्य व बियाणे बाजारपेठ", ta: "விவசாய பொருட்கள் & உள்ளீட்டு சந்தை", te: "వ్యవసాయ సామాగ్రి & విత్తనాల మార్కెట్" },
  "High-grade certified seeds, fertilizers, drip irrigation kits, and tools at subsidized direct rates": {
    hi: "उच्च गुणवत्ता वाले प्रमाणित बीज, उर्वरक, ड्रिप सिंचाई किट और उपकरण रियायती दरों पर",
    mr: "उच्च दर्जाची प्रमाणित बियाणे, खते, ठिबक सिंचन संच आणि अवजारे सवलतीच्या दरात",
    ta: "உயர்தர சான்றளிக்கப்பட்ட விதைகள், உரங்கள், சொட்டு நீர் பாசன கருவிகள் மானிய விலையில்",
    te: "అధిక నాణ్యత గల ధృవీకరించబడిన విత్తనాలు, ఎరువులు, బిందు సేద్యం పరికరాలు రాయితీ ధరలలో"
  },
  "Search inputs (e.g. Hybrid Seeds, NPK, Sprayer)": { hi: "सामग्री खोजें (जैसे संकर बीज, एनपीके, स्प्रेयर)", mr: "साहित्य शोधा (उदा. संकरित बियाणे, एनपीके, स्प्रेयर)", ta: "தேடுக (விதைகள், உரங்கள்)", te: "శోధించండి (హైబ్రిడ్ విత్తనాలు, ఎరువులు)" },
  "Price:": { hi: "मूल्य:", mr: "दर:", ta: "விலை:", te: "ధర:" },
  "Order Now": { hi: "अभी ऑर्डर करें", mr: "आत्ताच ऑर्डर करा", ta: "இப்போதே ஆர்டர் செய்", te: "ఇప్పుడే ఆర్డర్ చేయండి" },
  "Purchase Input:": { hi: "सामग्री खरीदें:", mr: "साहित्य खरेदी करा:", ta: "பொருள் வாங்குக:", te: "కొనుగోలు చేయండి:" },
  "Brand:": { hi: "ब्रांड:", mr: "ब्रँड:", ta: "பிராண்ட்:", te: "బ్రాండ్:" },
  "Delivery Farm Address": { hi: "खेत डिलीवरी का पता", mr: "शेत वितरण पत्ता", ta: "பண்ணை டெலிவரி முகவரி", te: "డెలివరీ చిరునామా" },
  "Confirm Purchase": { hi: "खरीद की पुष्टि करें", mr: "खरेदी पुष्टी करा", ta: "கொள்முதலை உறுதிசெய்", te: "కొనుగోలును నిర్ధారించండి" },
  "My Supply Orders History": { hi: "मेरे सामग्री ऑर्डर का इतिहास", mr: "माझ्या साहित्याच्या ऑर्डर्सचा इतिहास", ta: "எனது ஆர்டர் வரலாறு", te: "నా ఆర్డర్ల చరిత్ర" },
  "Order ID": { hi: "ऑर्डर आईडी", mr: "ऑर्डर आयडी", ta: "ஆர்டர் எண்", te: "ఆర్డర్ ఐడి" },
  "Date": { hi: "दिनांक", mr: "तारीख", ta: "தேதி", te: "తేదీ" },

  // Farmer Inventory Page
  "My Produce Inventory": { hi: "मेरी फसल सूची व भंडार", mr: "माझी शेतमाल यादी व साठा", ta: "எனது விளைச்சல் இருப்பு", te: "నా పంట నిల్వలు" },
  "Manage listed crops, available quantities, and quality grading": {
    hi: "सूचीबद्ध फसलों, उपलब्ध मात्रा और गुणवत्ता ग्रेड का प्रबंधन करें",
    mr: "नोंदवलेला शेतमाल, उपलब्ध प्रमाण आणि गुणवत्ता व्यवस्थापित करा",
    ta: "பயிர் பட்டியல், இருப்பு அளவு மற்றும் தரத்தை நிர்வகிக்கவும்",
    te: "జాబితా చేసిన పంటలు, అందుబాటులో ఉన్న పరిమాణం మరియు నాణ్యతను నిర్వహించండి"
  },
  "Add New Produce": { hi: "नई फसल जोड़ें", mr: "नवीन शेतमाल जोडा", ta: "புதிய பயிர் சேர்க்க", te: "కొత్త పంటను చేర్చండి" },
  "Category:": { hi: "श्रेणी:", mr: "वर्ग:", ta: "வகை:", te: "వర్గం:" },
  "Available Quantity": { hi: "उपलब्ध मात्रा", mr: "उपलब्ध प्रमाण", ta: "கிடைக்கும் அளவு", te: "అందుబాటులో ఉన్న పరిమాణం" },
  "Expected Price": { hi: "अपेक्षित मूल्य", mr: "अपेक्षित दर", ta: "எதிர்பார்க்கும் விலை", te: "ఆశించిన ధర" },
  "Quality Grade": { hi: "गुणवत्ता ग्रेड", mr: "गुणवत्ता प्रत", ta: "தர நிலை", te: "నాణ్యత గ్రేడ్" },
  "Harvest Date": { hi: "कटाई की तारीख", mr: "कापणी तारीख", ta: "அறுவடை தேதி", te: "కోత తేదీ" },
  "Recent": { hi: "हालिया", mr: "अलीकडील", ta: "சமீபத்திய", te: "ఇటీవలి" },
  "Edit": { hi: "संपादित करें", mr: "बदला", ta: "திருத்து", te: "సవరించు" },
  "Delete": { hi: "हटाएं", mr: "हटवा", ta: "நீக்கு", te: "తొలगించు" },
  "No Produce in Inventory Yet": { hi: "सूची में अभी कोई फसल नहीं है", mr: "यादीत अद्याप कोणताही शेतमाल नाही", ta: "இருப்பில் பயிர் எதுவும் இல்லை", te: "ఇంకా నిల్వలో పంట లేదు" },
  "Start adding your available crops so direct buyers can discover and place orders.": {
    hi: "अपनी उपलब्ध फसलों को जोड़ना शुरू करें ताकि खरीदार सीधे देख सकें और ऑर्डर दे सकें।",
    mr: "तुमचा उपलब्ध शेतमाल नोंदवणे सुरू करा जेणेकरून खरेदीदार थेट ऑर्डर देऊ शकतील.",
    ta: "நேரடி வாங்குபவர்கள் கண்டறிந்து ஆர்டர் செய்ய உங்கள் பயிர்களை சேர்க்கத் தொடங்குங்கள்.",
    te: "కొనుగోలుదారులు నేరుగా చూసి ఆర్డర్లు ఇవ్వడానికి మీ పంటలను చేర్చడం ప్రారంభించండి."
  },
  "Add Your First Crop": { hi: "अपनी पहली फसल जोड़ें", mr: "पहिले पीक जोडा", ta: "முதல் பயிரை சேர்க்க", te: "మొదటి పంటను జోడించండి" },

  // Orders & Negotiation Pages
  "Buyer Orders & Negotiation Requests": { hi: "खरीदार ऑर्डर व बातचीत अनुरोध", mr: "खरेदीदार ऑर्डर्स व वाटाघाटी विनंत्या", ta: "வாங்குபவர் ஆர்டர்கள் & பேச்சுவார்த்தை", te: "కొనుగోలుదారు ఆర్డర్లు & సంప్రదింపులు" },
  "Evaluate buyer offers against live Mandi prices, send counter-offers, or confirm orders.": {
    hi: "लाइव मंडी भाव के मुकाबले खरीदार के ऑफ़र का मूल्यांकन करें, काउंटर-ऑफ़र भेजें या ऑर्डर पक्का करें।",
    mr: "थेट बाजार भावाशी तुलना करून खरेदीदाराच्या ऑफर तपासा, पर्यायी दर पाठवा किंवा ऑर्डर निश्चित करा.",
    ta: "நேரடி மண்டி விலையுடன் ஒப்பிட்டு முடிவெடுங்கள் அல்லது மாற்று ஆஃபர் அனுப்புங்கள்.",
    te: "లైవ్ మండి ధరలతో సరిపోల్చి ఆర్డర్‌ను ఖరారు చేయండి లేదా కౌంటర్ ఆఫర్ పంపండి."
  },
  "Incoming Buyer Offers": { hi: "प्राप्त खरीदार ऑफ़र", mr: "आलेले खरेदीदार ऑफर्स", ta: "வந்த வாங்குபவர் ஆஃபர்கள்", te: "వచ్చిన కొనుగోలుదారు ఆఫర్లు" },
  "Confirmed & Active Orders": { hi: "पुष्टीकृत व सक्रिय ऑर्डर", mr: "निश्चित व सक्रिय ऑर्डर्स", ta: "உறுதிசெய்யப்பட்ட ஆர்டர்கள்", te: "ధృవీకరించబడిన & యాక్టివ్ ఆర్డర్లు" },
  "Requested Quantity": { hi: "मांगी गई मात्रा", mr: "मागितलेले प्रमाण", ta: "கோரப்பட்ட அளவு", te: "కోరిన పరిమాణం" },
  "Total Order Value:": { hi: "कुल ऑर्डर मूल्य:", mr: "एकूण ऑर्डर मूल्य:", ta: "மொத்த ஆர்டர் மதிப்பு:", te: "మొత్తం ఆర్డర్ విలువ:" },
  "Accept Deal": { hi: "सौदा स्वीकार करें", mr: "सौदा स्वीकारा", ta: "ஒப்பந்தத்தை ஏற்றுக்கொள்", te: "డీల్ అంగీకరించండి" },
  "Make Counter-Offer": { hi: "काउंटर ऑफ़र दें", mr: "पर्यायी ऑफर द्या", ta: "மாற்று ஆஃபர் செய்க", te: "కౌంటర్ ఆఫర్ ఇవ్వండి" },
  "Reject Offer": { hi: "ऑफ़र अस्वीकार करें", mr: "ऑफर नाकारा", ta: "நிராகரி", te: "తిరస్కరించండి" },
  "Fulfilment & Delivery Progress": { hi: "आपूर्ति व डिलीवरी प्रगति", mr: "वितरण व डिलिव्हरी प्रगती", ta: "விநியோக முன்னேற்றம்", te: "డెలివరీ పురోగతి" },
  "1. Confirmed": { hi: "1. पक्का हुआ", mr: "1. निश्चित", ta: "1. உறுதிசெய்யப்பட்டது", te: "1. నిర్ధారించబడింది" },
  "2. Packing": { hi: "2. पैकिंग", mr: "2. पॅकिंग", ta: "2. பேக்கிங்", te: "2. ప్యాకింగ్" },
  "3. Vehicle Assigned": { hi: "3. वाहन आवंटित", mr: "3. वाहन नियुक्त", ta: "3. வாகனம் ஒதுக்கப்பட்டது", te: "3. వాహనం కేటాయించబడింది" },
  "4. In Transit": { hi: "4. रास्ते में", mr: "4. मार्गावर", ta: "4. வழியில் உள்ளது", te: "4. రవాణాలో ఉంది" },
  "5. Delivered": { hi: "5. डिलीवर हुआ", mr: "5. पोहोचले", ta: "5. விநியோகிக்கப்பட்டது", te: "5. డెలివరీ చేయబడింది" },
  "Trade Specifications": { hi: "व्यापार विवरण", mr: "व्यापार तपशील", ta: "வர்த்தக விவரங்கள்", te: "వాణిజ్య వివరాలు" },
  "View Tax Invoice": { hi: "टैक्स इनवॉइस देखें", mr: "टॅक्स इनव्हॉइस पहा", ta: "வரி விலைப்பட்டியல் காண்க", te: "పన్ను ఇన్‌వాయిస్ చూడండి" },
  "Print Invoice": { hi: "इनवॉइस प्रिंट करें", mr: "इनव्हॉइस प्रिंट करा", ta: "அச்சிடுக", te: "ప్రింట్ చేయండి" },
  "File Dispute": { hi: "शिकायत दर्ज करें", mr: "तक्रार नोंदवा", ta: "புகார் பதிவு செய்க", te: "ఫిర్యాదు చేయండి" },

  // Common Statuses & Words
  "Pending": { hi: "लंबित", mr: "प्रलंबित", ta: "நிலுவையில்", te: "పెండింగ్" },
  "Accepted": { hi: "स्वीकृत", mr: "स्वीकृत", ta: "ஏற்றுக்கொள்ளப்பட்டது", te: "ఆమోదించబడింది" },
  "Rejected": { hi: "अस्वीकृत", mr: "नाकारले", ta: "நிராகரிக்கப்பட்டது", te: "తిరస్కరించబడింది" },
  "Countered": { hi: "काउंटर ऑफ़र", mr: "पर्यायी दर", ta: "மாற்று ஆஃபர்", te: "కౌంటర్ ఆఫర్" },
  "In Transit": { hi: "रास्ते में (ट्रांजिट)", mr: "मार्गावर", ta: "வழியில் உள்ளது", te: "రవాణాలో ఉంది" },
  "Delivered": { hi: "डिलीवर हो गया", mr: "पोहोचले", ta: "விநியோகிக்கப்பட்டது", te: "చేరింది" },
  "Completed": { hi: "पूर्ण हुआ", mr: "पूर्ण झाले", ta: "முடிந்தது", te: "పూర్తయింది" },
  "Available": { hi: "उपलब्ध", mr: "उपलब्ध", ta: "இருப்பில் உள்ளது", te: "అందుబాటులో ఉంది" },
  "Low Stock": { hi: "कम स्टॉक", mr: "कमी साठा", ta: "குறைந்த இருப்பு", te: "తక్కువ నిల్వ" },
  "Sold Out": { hi: "बिक चुका है", mr: "विक्री झाली", ta: "விற்றுத் தீர்ந்தது", te: "అయిపోయింది" },
  "Verified": { hi: "सत्यापित", mr: "प्रमाणित", ta: "சரிபார்க்கப்பட்டது", te: "ధృవీకరించబడింది" },
  "Search": { hi: "खोजें", mr: "शोधा", ta: "தேடுக", te: "శోధించండి" },
  "Filter": { hi: "फ़िल्टर", mr: "फिल्टर", ta: "வடிகட்டு", te: "ఫిల్టర్" },
  "Save Changes": { hi: "बदलाव सहेजें", mr: "बदल जतन करा", ta: "சேமிக்கவும்", te: "మార్పులను సేవ్ చేయండి" },
  "Submit": { hi: "जमा करें", mr: "सबमिट करा", ta: "சமர்ப்பிக்கவும்", te: "సమర్పించండి" },
  "Cancel": { hi: "रद्द करें", mr: "रद्द करा", ta: "ரத்து செய்", te: "రద్దు చేయండి" },
  "Back": { hi: "वापस जाएं", mr: "मागे जा", ta: "பின்செல்", te: "వెనుకకు" },
  "Close": { hi: "बंद करें", mr: "बंद करा", ta: "மூடு", te: "మూసివేయి" },
  "Kisan Saarthi": { hi: "किसान सारथी", mr: "किसान सारथी", ta: "கிசான் சாரதி", te: "కిసాన్ సారథి" },

  // Service Requests Hub & Sub-sections
  "My Service Requests Hub": { hi: "मेरी सेवा अनुरोध केंद्र", mr: "माझे सेवा विनंती केंद्र", ta: "எனது சேவை கோரிக்கைகள் மையம்", te: "నా సేవా అభ్యర్థనల కేంద్రం" },
  "My Service Requests": { hi: "मेरी सेवा अनुरोध सूची", mr: "माझ्या सेवा विनंत्या", ta: "எனது சேவை கோரிக்கைகள்", te: "నా సేవా అభ్యర్థనలు" },
  "Cold Storage Requests": { hi: "कोल्ड स्टोरेज अनुरोध", mr: "शीतगृह विनंत्या", ta: "குளிர்பதன கோரிக்கைகள்", te: "కోల్డ్ స్టోరేజ్ అభ్యర్థనలు" },
  "Cold Storage Space Requests": { hi: "कोल्ड स्टोरेज स्थान अनुरोध", mr: "शीतगृह जागा विनंत्या", ta: "குளிர்பதன இடக் கோரிக்கைகள்", te: "కోల్డ్ స్టోరేజ్ స్థల అభ్యర్థనలు" },
  "Transport / Logistics": { hi: "परिवहन व वाहन बुकिंग", mr: "वाहतूक व वाहन बुकिंग", ta: "போக்குவரத்து & வாகனம்", te: "రవాణా & వాహనం" },
  "Transport & Logistics": { hi: "परिवहन व लॉजिस्टिक्स", mr: "वाहतूक आणि लॉजिस्टिक्स", ta: "போக்குவரத்து & விநியோகம்", te: "రవాణా మరియు లాజిస్టిక్స్" },
  "Vehicle Transport Bookings": { hi: "वाहन परिवहन बुकिंग", mr: "वाहन वाहतूक बुकिंग", ta: "வாகன போக்குவரத்து முன்பதிவுகள்", te: "వాహన రవాణా బుకింగ్‌లు" },
  "Admin Support Tickets": { hi: "प्रशासनिक सहायता टिकट", mr: "प्रशासकीय मदत अर्ज", ta: "நிர்வாக உதவி கோரிக்கைகள்", te: "అడ్మిన్ సహాయం టిక్కెట్లు" },
  "Admin Support & Grievances": { hi: "प्रशासनिक सहायता व शिकायतें", mr: "प्रशासकीय मदत व तक्रारी", ta: "நிர்வாக உதவி & புகார்கள்", te: "అడ్మిన్ మద్దతు & ఫిర్యాదులు" },
  "Platform Admin Requests & Grievance Tickets": { hi: "प्लेटफ़ॉर्म प्रशासनिक अनुरोध व शिकायत टिकट", mr: "प्लॅटफॉर्म प्रशासकीय विनंत्या व तक्रार अर्ज", ta: "நிர்வாக கோரிக்கைகள் & புகார்கள்", te: "ప్లాట్‌ఫారమ్ అడ్మిన్ అభ్యర్థనలు & ఫిర్యాదులు" },
  "Contact Admin / Support": { hi: "प्रशासन / सहायता से संपर्क करें", mr: "प्रशासक / मदतीशी संपर्क साधा", ta: "நிர்வாக தொடர்பு", te: "అడ్మిన్ సహాయం కోరండి" },
  "Book Transport": { hi: "वाहन बुक करें", mr: "वाहतूक बुक करा", ta: "வாகனம் பதிவு செய்", te: "రవాణా బుక్ చేయండి" },
  "Book Transport Vehicle": { hi: "परिवहन वाहन बुक करें", mr: "वाहतूक वाहन बुक करा", ta: "போக்குவரத்து வாகனம் பதிவு செய்க", te: "రవాణా వాహనాన్ని బుక్ చేయండి" },
  "Find Cold Storage": { hi: "कोल्ड स्टोरेज खोजें", mr: "शीतगृह शोधा", ta: "குளிர்பதன கிடங்கை தேடு", te: "కోల్డ్ స్టోరేజ్ కనుగొనండి" },
  "Raise New Ticket": { hi: "नया टिकट दर्ज करें", mr: "नवीन अर्ज नोंदवा", ta: "புதிய கோரிக்கை", te: "కొత్త టిక్కెట్ నమోదు చేయండి" },
  "Raise Admin Support Ticket": { hi: "प्रशासनिक सहायता टिकट दर्ज करें", mr: "प्रशासकीय मदत अर्ज नोंदवा", ta: "நிர்வாக உதவி பதிவு செய்க", te: "అడ్మిన్ సపోర్ట్ టిక్కెట్ నమోదు చేయండి" },
  "Book Cold Storage": { hi: "कोल्ड स्टोरेज बुक करें", mr: "शीतगृह बुक करा", ta: "கிடங்கு பதிவு செய்க", te: "కోల్డ్ స్టోరేజ్ బుక్ చేయండి" },
  "Cold Storage Facility": { hi: "कोल्ड स्टोरेज केंद्र", mr: "शीतगृह सुविधा", ta: "குளிர்பதன மையம்", te: "కోల్డ్ స్టోరేజ్ కేంద్రం" },
  "Booking ID": { hi: "बुकिंग आईडी", mr: "बुकिंग आयडी", ta: "முன்பதிவு எண்", te: "బుకింగ్ ఐడి" },
  "Space Allocated": { hi: "स्थान आवंटित", mr: "जागा वाटप झाली", ta: "இடம் ஒதுக்கப்பட்டது", te: "స్థలం కేటాయించబడింది" },
  "In Storage": { hi: "भंडारण में सुरक्षित", mr: "शीतगृहात साठवले", ta: "சேமிப்பில் உள்ளது", te: "నిల్వలో ఉంది" },
  "Driver Assigned": { hi: "ड्राइवर आवंटित", mr: "चालक नियुक्त", ta: "ஓட்டுநர் நியமிக்கப்பட்டார்", te: "డ్రైవర్ కేటాయించబడ్డాడు" },
  "En Route": { hi: "रास्ते में", mr: "मार्गावर", ta: "வழியில் உள்ளது", te: "రవాణాలో ఉంది" },
  "Call Driver": { hi: "ड्राइवर को कॉल करें", mr: "चालकाला कॉल करा", ta: "ஓட்டுநரை அழைக்கவும்", te: "డ్రైవర్‌కు కాల్ చేయండి" },
  "Call Operator": { hi: "ऑपरेटर को कॉल करें", mr: "ऑपरेटरला कॉल करा", ta: "ஆபरेட்டரை அழைக்கவும்", te: "ఆపరేటర్‌కు కాల్ చేయండి" },
  "Close Ticket": { hi: "टिकट बंद करें", mr: "अर्ज बंद करा", ta: "கோரிக்கையை மூடு", te: "టిక్కెట్‌ను మూసివేయండి" },
  "Request Category": { hi: "अनुरोध श्रेणी", mr: "विनंती वर्ग", ta: "கோரிக்கை வகை", te: "అభ్యర్థన వర్గం" },
  "Pickup Location": { hi: "पिकअप स्थान", mr: "पिकअप ठिकाण", ta: "ஏற்றுமதி இடம்", te: "పికప్ స్థలం" },
  "Freight Cost:": { hi: "भाड़ा लागत:", mr: "वाहतूक खर्च:", ta: "போக்குவரத்து செலவு:", te: "రవాణా ఖర్చు:" },
  "Truck No:": { hi: "ट्रक नंबर:", mr: "ट्रक क्रमांक:", ta: "வாகன எண்:", te: "ట్రక్ నంబర్:" },
  "Pickup Time:": { hi: "पिकअप समय:", mr: "पिकअप वेळ:", ta: "நேரம்:", te: "పికప్ సమయం:" },

  // Commodities
  "Wheat": { hi: "गेहूं", mr: "गहू", ta: "கோதுமை", te: "గోధుమలు" },
  "Onion": { hi: "प्याज", mr: "कांदा", ta: "வெங்காயம்", te: "ఉల్లిపాయలు" },
  "Tomato": { hi: "टमाटर", mr: "टोमॅटो", ta: "தக்காளி", te: "టమాటాలు" },
  "Potato": { hi: "आलू", mr: "बटाटा", ta: "உருளைக்கிழங்கு", te: "బంగాళాదుంపలు" },
  "Rice": { hi: "चावल (धान)", mr: "तांदूळ / भात", ta: "அரிசி", te: "వరి / బియ్యం" },
  "Soybean": { hi: "सोयाबीन", mr: "सोयाबीन", ta: "சோயாபீன்", te: "సోయాబీన్" },
  "Cotton": { hi: "कपास", mr: "कापूस", ta: "பருத்தி", te: "పత్తి" },
  "Garlic": { hi: "लहसुन", mr: "लसूण", ta: "பூண்டு", te: "వెల్లుల్లి" },
  "Mustard": { hi: "सरसों", mr: "मोहरी", ta: "கடுகு", te: "ఆవాలు" },
  "Maize": { hi: "मक्का", mr: "मका", ta: "மக்காச்சோளம்", te: "మొక్కజొన్న" },
  "Gram": { hi: "चना", mr: "हरभरा", ta: "கடலை", te: "శనగలు" }
};

// Sorted array of phrase keys by descending string length for greedy matching
let SORTED_PHRASE_KEYS = Object.keys(KRISHI_PHRASES).sort((a, b) => b.length - a.length);

// 3. Smart Full-DOM Translation Execution Engine
function applyTranslations(lang) {
  if (!lang) lang = 'en';
  const dict = KRISHI_TRANSLATIONS[lang] || KRISHI_TRANSLATIONS.en;

  // Step A: Translate all elements with explicit [data-i18n]
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  // Step B: Translate [data-i18n-placeholder] and plain [placeholder]
  document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(el => {
    const explicitKey = el.getAttribute('data-i18n-placeholder');
    if (explicitKey && dict[explicitKey]) {
      el.setAttribute('placeholder', dict[explicitKey]);
      return;
    }

    if (el._krishi_orig_placeholder === undefined) {
      el._krishi_orig_placeholder = el.getAttribute('placeholder') || '';
    }

    if (lang === 'en') {
      el.setAttribute('placeholder', el._krishi_orig_placeholder);
    } else {
      let orig = el._krishi_orig_placeholder.trim();
      if (KRISHI_PHRASES[orig] && KRISHI_PHRASES[orig][lang]) {
        el.setAttribute('placeholder', KRISHI_PHRASES[orig][lang]);
      } else {
        // Partial placeholder replacement
        let modified = el._krishi_orig_placeholder;
        for (let phrase of SORTED_PHRASE_KEYS) {
          if (modified.includes(phrase) && KRISHI_PHRASES[phrase][lang]) {
            modified = modified.split(phrase).join(KRISHI_PHRASES[phrase][lang]);
          }
        }
        el.setAttribute('placeholder', modified);
      }
    }
  });

  // Step C: Translate <option> texts in dropdowns
  document.querySelectorAll('option').forEach(opt => {
    if (opt._krishi_orig_text === undefined) {
      opt._krishi_orig_text = opt.textContent;
    }
    if (lang === 'en') {
      opt.textContent = opt._krishi_orig_text;
    } else {
      let origTrim = opt._krishi_orig_text.trim();
      if (KRISHI_PHRASES[origTrim] && KRISHI_PHRASES[origTrim][lang]) {
        opt.textContent = KRISHI_PHRASES[origTrim][lang];
      }
    }
  });

  // Step D: Recursively walk text nodes with lossless original text caching
  if (lang !== 'en') {
    translateDOMTextNodes(document.body, lang);
  } else {
    restoreOriginalEnglish(document.body);
  }

  // Save selected language in localStorage and html tag
  localStorage.setItem('krishi_selected_lang', lang);
  document.documentElement.lang = lang;
}

// Helper: Recursively walk and translate all text nodes without breaking HTML or numbers
function translateDOMTextNodes(node, lang) {
  if (!node) return;
  const skipTags = ['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT', 'CODE', 'PRE', 'SVG', 'PATH'];
  if (node.nodeType === Node.ELEMENT_NODE && skipTags.includes(node.tagName)) {
    return;
  }

  if (node.nodeType === Node.TEXT_NODE) {
    if (node._krishi_orig === undefined) {
      node._krishi_orig = node.nodeValue;
    }

    const orig = node._krishi_orig;
    const trimmed = orig.trim();
    if (trimmed.length === 0) return;

    // Check exact match first
    if (KRISHI_PHRASES[trimmed] && KRISHI_PHRASES[trimmed][lang]) {
      node.nodeValue = orig.replace(trimmed, KRISHI_PHRASES[trimmed][lang]);
      return;
    }

    // Check greedy multi-phrase match
    let updated = orig;
    let modified = false;
    for (let phrase of SORTED_PHRASE_KEYS) {
      if (updated.includes(phrase) && KRISHI_PHRASES[phrase][lang]) {
        updated = updated.split(phrase).join(KRISHI_PHRASES[phrase][lang]);
        modified = true;
      }
    }

    if (modified) {
      node.nodeValue = updated;
    }
    return;
  }

  // Walk child nodes
  for (let child of node.childNodes) {
    translateDOMTextNodes(child, lang);
  }
}

// Helper: Restore original English text cleanly
function restoreOriginalEnglish(node) {
  if (!node) return;
  if (node.nodeType === Node.TEXT_NODE) {
    if (node._krishi_orig !== undefined) {
      node.nodeValue = node._krishi_orig;
    }
    return;
  }

  const skipTags = ['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT', 'CODE', 'PRE', 'SVG', 'PATH'];
  if (node.nodeType === Node.ELEMENT_NODE && skipTags.includes(node.tagName)) {
    return;
  }

  for (let child of node.childNodes) {
    restoreOriginalEnglish(child);
  }
}

// 4. Initialization & Event Handlers
document.addEventListener('DOMContentLoaded', () => {
  const serverLang = document.documentElement.lang;
  const savedLang = localStorage.getItem('krishi_selected_lang') || serverLang || 'en';
  
  applyTranslations(savedLang);

  // Hook all language dropdown items for instant real-time live translation
  document.querySelectorAll('.lang-select-item').forEach(item => {
    item.addEventListener('click', (e) => {
      const selectedLang = item.getAttribute('data-lang');
      if (selectedLang) {
        applyTranslations(selectedLang);
      }
    });
  });

  // Re-translate dynamically opened Bootstrap modals and popups
  document.addEventListener('shown.bs.modal', () => {
    const currentLang = localStorage.getItem('krishi_selected_lang') || 'en';
    if (currentLang !== 'en') {
      applyTranslations(currentLang);
    }
  });
});
