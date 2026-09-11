/**
 * Krishi Kendra - Comprehensive Multilingual Translation Engine (i18n)
 * Languages supported: English (en), Hindi (hi), Marathi (mr), Tamil (ta), Telugu (te)
 * Features Key-based translation + Whole-DOM Phrase Translation + Safe String Preservation
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
    total_sales: "Total Sales",
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
    total_sales: "कुल बिक्री",
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
    total_sales: "एकूण विक्री",
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
    total_sales: "மொத்த விற்பனை",
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
    total_sales: "మొత్తం అమ్మకాలు",
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
  "My Visiting Card": { hi: "मेरा विजिटिंग कार्ड", mr: "माझे व्हिजिटिंग कार्ड", ta: "எனது விசிட்டிங் கார்டு", te: "నా విజిటింగ్ కార్డు" },
  "Profile & Privacy": { hi: "प्रोफाइल व गोपनीयता", mr: "प्रोफाइल व गोपनीयता", ta: "சுயவிவரம் & தனியுரிமை", te: "ప్రొఫైల్ & గోప్యత" },
  "Logout": { hi: "लॉगआउट", mr: "बाहेर पडा", ta: "வெளியேறு", te: "లాగ్ అవుట్" },
  "Login": { hi: "लॉगिन करें", mr: "लॉगिन", ta: "உள்நுழைக", te: "లాగిన్" },
  "Register": { hi: "पंजीकरण करें", mr: "नोंदणी करा", ta: "பதிவு செய்க", te: "నమోదు" },
  "Admin Portal": { hi: "प्रशासनिक पोर्टल", mr: "प्रशासक पोर्टल", ta: "நிர்வாக தளம்", te: "అడ్మిన్ పోర్టల్" },
  "Recent Notifications": { hi: "हाल की सूचनाएं", mr: "अलीकडील सूचना", ta: "சமீபத்திய அறிவிப்புகள்", te: "ఇటీవలి నోటిఫికేషన్లు" },
  "No notifications yet.": { hi: "अभी कोई सूचना नहीं है।", mr: "अद्याप कोणतीही सूचना नाही.", ta: "அறிவிப்புகள் எதுவும் இல்லை.", te: "ఇంకా నోటిఫికేషన్లు లేవు." },

  // Farmer Dashboard & Inventory
  "Farmer Dashboard": { hi: "किसान डैशबोर्ड", mr: "शेतकरी डॅशबोर्ड", ta: "விவசாயி டாஷ்போர்டு", te: "రైతు డ్యాష్‌బోర్డ్" },
  "Buyer Dashboard": { hi: "खरीदार डैशबोर्ड", mr: "खरेदीदार डॅशबोर्ड", ta: "வாங்குபவர் டாஷ்போர்டு", te: "కొనుగోలుదారు డ్యాష్‌బోర్డ్" },
  "Add Produce": { hi: "नई फसल जोड़ें", mr: "नवीन शेतमाल जोडा", ta: "பயிர் சேர்க்க", te: "పంటను జోడించండి" },
  "List New Crop": { hi: "नई फसल दर्ज करें", mr: "नवीन पीक नोंदवा", ta: "புதிய பயிர் சேர்க்க", te: "కొత్త పంటను చేర్చండి" },
  "Post Requirement": { hi: "मांग पोस्ट करें", mr: "मागणी नोंदवा", ta: "தேவையை பதிவிடுக", te: "అవసరాన్ని పోస్ట్ చేయండి" },
  "Browse Produce": { hi: "फसलें खोजें", mr: "शेतमाल शोधा", ta: "பயிர்களை காண்க", te: "పంటలను చూడండి" },
  "Quick Actions": { hi: "त्वरित क्रियाएं", mr: "जलद कृती", ta: "விரைவு செயல்கள்", te: "త్వరిత చర్యలు" },
  "Total Produce Listed": { hi: "कुल सूचीबद्ध फसल", mr: "एकूण नोंदवलेला शेतमाल", ta: "பட்டியலிடப்பட்ட பயிர்கள்", te: "మొత్తం లిస్ట్ చేసిన పంట" },
  "Active Deals & Negotiations": { hi: "सक्रिय सौदे व बातचीत", mr: "सक्रिय सौदे व चर्चा", ta: "செயலில் உள்ள வர்த்தகம்", te: "యాక్టివ్ డీల్స్" },
  "Total Earnings": { hi: "कुल कमाई", mr: "एकूण उत्पन्न", ta: "மொத்த வருவாய்", te: "మొత్తం ఆదాయం" },
  "Cold Storage Bookings": { hi: "कोल्ड स्टोरेज बुकिंग", mr: "शीतगृह बुकींग", ta: "குளிர்பதன முன்பதிவு", te: "కోల్డ్ స్టోరేజ్ బుకింగ్స్" },
  "Crop Inventory": { hi: "फसल भंडार", mr: "शेतमाल साठा", ta: "பயிர் இருப்பு", te: "పంట నిల్వ" },
  "Available Quantity": { hi: "उपलब्ध मात्रा", mr: "उपलब्ध प्रमाण", ta: "கிடைக்கும் அளவு", te: "అందుబాటులో ఉన్న పరిమాణం" },
  "Expected Price": { hi: "अपेक्षित मूल्य", mr: "अपेक्षित दर", ta: "எதிர்பார்க்கும் விலை", te: "ఆశించిన ధర" },
  "Quality Grade": { hi: "गुणवत्ता ग्रेड", mr: "गुणवत्ता प्रत", ta: "தர நிலை", te: "నాణ్యత గ్రేడ్" },
  "Harvest Date": { hi: "कटाई की तारीख", mr: "कापणी तारीख", ta: "அறுவடை தேதி", te: "కోత తేదీ" },
  "Location": { hi: "स्थान", mr: "ठिकाण", ta: "இடம்", te: "ప్రాంతం" },
  "Status": { hi: "स्थिति", mr: "स्थिती", ta: "நிலை", te: "స్థితి" },
  "Action": { hi: "कार्यवाही", mr: "कृती", ta: "செயல்", te: "చర్య" },
  "Actions": { hi: "कार्यवाही", mr: "कृती", ta: "செயல்கள்", te: "చర్యలు" },
  "Edit": { hi: "संपादित करें", mr: "बदला", ta: "திருத்து", te: "సవరించు" },
  "Delete": { hi: "हटाएं", mr: "हटवा", ta: "நீக்கு", te: "తొలగించు" },
  "View Details": { hi: "विवरण देखें", mr: "तपशील पहा", ta: "விவரங்களை காண்க", te: "వివరాలు చూడండి" },
  "Available": { hi: "उपलब्ध", mr: "उपलब्ध", ta: "இருப்பில் உள்ளது", te: "అందుబాటులో ఉంది" },
  "Low Stock": { hi: "कम स्टॉक", mr: "कमी साठा", ta: "குறைந்த இருப்பு", te: "తక్కువ నిల్వ" },
  "Sold Out": { hi: "बिक चुका है", mr: "विक्री झाली", ta: "விற்றுத் தீர்ந்தது", te: "అయిపోయింది" },

  // Orders & Deals
  "Pending": { hi: "लंबित", mr: "प्रलंबित", ta: "நிலுவையில்", te: "పెండింగ్" },
  "Accepted": { hi: "स्वीकृत", mr: "स्वीकृत", ta: "ஏற்றுக்கொள்ளப்பட்டது", te: "ఆమోదించబడింది" },
  "Rejected": { hi: "अस्वीकृत", mr: "नाकारले", ta: "நிராகரிக்கப்பட்டது", te: "తిరస్కరించబడింది" },
  "Countered": { hi: "काउंटर ऑफ़र", mr: "पर्यायी दर", ta: "மாற்று ஆஃபர்", te: "కౌంటర్ ఆఫర్" },
  "In Transit": { hi: "रास्ते में (ट्रांजिट)", mr: "मार्गावर", ta: "வழியில் உள்ளது", te: "రవాణాలో ఉంది" },
  "Delivered": { hi: "डिलीवर हो गया", mr: "पोहोचले", ta: "விநியோகிக்கப்பட்டது", te: "చేరింది" },
  "Completed": { hi: "पूर्ण हुआ", mr: "पूर्ण झाले", ta: "முடிந்தது", te: "పూర్తయింది" },
  "View Tax Invoice": { hi: "टैक्स इनवॉइस देखें", mr: "टॅक्स इनव्हॉइस पहा", ta: "வரி விலைப்பட்டியல்", te: "పన్ను ఇన్‌వాయిస్" },
  "Print Invoice": { hi: "इनवॉइस प्रिंट करें", mr: "इनव्हॉइस प्रिंट करा", ta: "அச்சிடுக", te: "ప్రింట్ చేయండి" },
  "Total Amount": { hi: "कुल राशि", mr: "एकूण रक्कम", ta: "மொத்த தொகை", te: "మొత్తం మొత్తం" },
  "Agreed Price": { hi: "सहमति मूल्य", mr: "ठरलेला दर", ta: "ஒப்புக்கொண்ட விலை", te: "ఒప్పుకున్న ధర" },
  "Delivery Address": { hi: "डिलीवरी का पता", mr: "वितरण पत्ता", ta: "டெலிவரி முகவரி", te: "డెలివరీ చిరునామా" },
  "Accept Offer": { hi: "ऑफ़र स्वीकार करें", mr: "ऑफर स्वीकारा", ta: "ஏற்றுக்கொள்", te: "ఆమోదించండి" },
  "Make Counter-Offer": { hi: "काउंटर ऑफ़र दें", mr: "पर्यायी ऑफर द्या", ta: "மாற்று ஆஃபர்", te: "కౌంటర్ ఆఫర్ ఇవ్వండి" },

  // Cold Storage & Schemes
  "Nearby Cold Storage Network": { hi: "नजदीकी कोल्ड स्टोरेज नेटवर्क", mr: "जवळपासची शीतगृहे", ta: "அருகிலுள்ள குளிர்பதன கிடங்குகள்", te: "సమీప కోల్డ్ స్టోరేజ్ నెట్‌వర్క్" },
  "Accredited Cold Storages": { hi: "प्रमाणित कोल्ड स्टोरेज", mr: "प्रमाणित शीतगृहे", ta: "அங்கீகரிக்கப்பட்ட கிடங்குகள்", te: "ధృవీకరించబడిన కోల్డ్ స్టోరేజీలు" },
  "Total Capacity": { hi: "कुल क्षमता", mr: "एकूण क्षमता", ta: "மொத்த கொள்ளளவு", te: "మొత్తం సామర్థ్యం" },
  "Available Space": { hi: "उपलब्ध स्थान", mr: "उपलब्ध जागा", ta: "கிடைக்கும் இடம்", te: "అందుబాటులో ఉన్న స్థలం" },
  "Daily Rental Rate": { hi: "दैनिक किराया दर", mr: "दैनिक भाडे दर", ta: "தினசரி வாடகை", te: "రోజువారీ అద్దె ధర" },
  "Book Storage Space": { hi: "स्टोरेज बुक करें", mr: "जागा बुक करा", ta: "முன்பதிவு செய்க", te: "బుక్ చేయండి" },
  "Government Schemes & Subsidies": { hi: "सरकारी कल्याणकारी योजनाएं व सब्सिडी", mr: "शासकीय योजना व सबसिडी", ta: "அரசு திட்டங்கள் & மானியங்கள்", te: "ప్రభుత్వ పథకాలు & రాయితీలు" },
  "Apply Online": { hi: "ऑनलाइन आवेदन करें", mr: "ऑनलाइन अर्ज करा", ta: "விண்ணப்பிக்கவும்", te: "దరఖాస్తు చేసుకోండి" },
  "Eligibility": { hi: "पात्रता", mr: "पात्रता", ta: "தகுதி", te: "అర్హత" },
  "Benefits": { hi: "लाभ", mr: "फायदे", ta: "நன்மைகள்", te: "ప్రయోజనాలు" },

  // Mandi & Crops
  "APMC Mandi Rates": { hi: "APMC मंडी भाव", mr: "बाजार समिती थेट दर", ta: "நேரடி மंडी விலை", te: "APMC మార్కెట్ ధరలు" },
  "Commodity": { hi: "फसल / वस्तु", mr: "शेतमाल", ta: "பயிர்", te: "పంట" },
  "Market": { hi: "मंडी", mr: "बाजार समिती", ta: "சந்தை", te: "మార్కెట్" },
  "Modal Price": { hi: "औसत भाव", mr: "सरासरी दर", ta: "சராசரி விலை", te: "సగటు ధర" },
  "Live Mandi Rates": { hi: "लाइव मंडी भाव", mr: "थेट बाजार भाव", ta: "நேரலை மண்டி விலை", te: "లైవ్ మార్కెట్ ధరలు" },
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
  "Gram": { hi: "चना", mr: "हरभरा", ta: "கடலை", te: "శనగలు" },

  // General Buttons & Filters
  "Search": { hi: "खोजें", mr: "शोधा", ta: "தேடுக", te: "శోధించండి" },
  "Filter": { hi: "फ़िल्टर", mr: "फिल्टर", ta: "வடிகட்டு", te: "ఫిల్టర్" },
  "Save Changes": { hi: "बदलाव सहेजें", mr: "बदल जतन करा", ta: "சேமிக்கவும்", te: "మార్పులను సేవ్ చేయండి" },
  "Submit": { hi: "जमा करें", mr: "सबमिट करा", ta: "சமர்ப்பிக்கவும்", te: "సమర్పించండి" },
  "Cancel": { hi: "रद्द करें", mr: "रद्द करा", ta: "ரத்து செய்", te: "రద్దు చేయండి" },
  "Back": { hi: "वापस जाएं", mr: "मागे जा", ta: "பின்செல்", te: "వెనుకకు" },
  "Close": { hi: "बंद करें", mr: "बंद करा", ta: "மூடு", te: "మూసివేయి" },
  "Verified": { hi: "सत्यापित", mr: "प्रमाणित", ta: "சரிபார்க்கப்பட்டது", te: "ధృవీకరించబడింది" },
  "State": { hi: "राज्य", mr: "राज्य", ta: "மாநிலம்", te: "రాష్ట్రం" },
  "District": { hi: "ज़िला", mr: "जिल्हा", ta: "மாவட்டம்", te: "జిల్లా" },
  "Price": { hi: "मूल्य", mr: "दर", ta: "விலை", te: "ధర" },
  "Quantity": { hi: "मात्रा", mr: "प्रमाण", ta: "அளவு", te: "పరిమాణం" },
  "Kisan Saarthi": { hi: "किसान सारथी", mr: "किसान सारथी", ta: "கிசான் சாரதி", te: "కిసాన్ సారథి" }
};

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

  // Step B: Translate [data-i18n-placeholder] and [placeholder]
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (dict[key]) {
      el.setAttribute('placeholder', dict[key]);
    }
  });

  // Step C: If non-English selected, perform recursive phrase matching on text nodes
  if (lang !== 'en') {
    translateDOMTextNodes(document.body, lang);
  } else {
    restoreOriginalEnglish(document.body);
  }

  // Save selected language in localStorage and html tag
  localStorage.setItem('krishi_selected_lang', lang);
  document.documentElement.lang = lang;
}

// Helper: Recursively walk and translate all text nodes while preserving original strings
function translateDOMTextNodes(node, lang) {
  if (!node) return;
  // Skip script, style, textarea, input, and pre tags
  const skipTags = ['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT', 'CODE', 'PRE', 'SVG', 'PATH'];
  if (node.nodeType === Node.ELEMENT_NODE && skipTags.includes(node.tagName)) {
    return;
  }

  if (node.nodeType === Node.TEXT_NODE) {
    const rawText = node.textContent.trim();
    if (rawText.length > 0) {
      // Store original English text if not already stored
      const parent = node.parentElement;
      if (parent && !parent.hasAttribute('data-i18n') && !parent.classList.contains('font-monospace')) {
        let original = parent.getAttribute('data-original-text');
        if (!original) {
          parent.setAttribute('data-original-text', node.textContent);
          original = node.textContent;
        }

        const trimmedOrig = original.trim();
        if (KRISHI_PHRASES[trimmedOrig] && KRISHI_PHRASES[trimmedOrig][lang]) {
          node.textContent = original.replace(trimmedOrig, KRISHI_PHRASES[trimmedOrig][lang]);
        }
      }
    }
    return;
  }

  // Walk child nodes
  for (let child of node.childNodes) {
    translateDOMTextNodes(child, lang);
  }
}

// Helper: Restore original English text
function restoreOriginalEnglish(node) {
  if (!node) return;
  if (node.nodeType === Node.ELEMENT_NODE) {
    const original = node.getAttribute('data-original-text');
    if (original && node.childNodes.length === 1 && node.childNodes[0].nodeType === Node.TEXT_NODE) {
      node.childNodes[0].textContent = original;
    }
  }
  for (let child of node.childNodes) {
    restoreOriginalEnglish(child);
  }
}

// 4. Initialization & Event Handlers
document.addEventListener('DOMContentLoaded', () => {
  // Read saved language from server session or localStorage
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
});
