def classify_intent(message: str) -> str:
    """
    Classify the user's message before retrieval.

    GENERAL messages are handled directly and should NOT go to RAG.
    Clinical messages are routed to the appropriate clinical intent.
    """

    t = message.lower().strip()

    # =========================================================
    # 1. EMPTY / VERY SHORT MESSAGES
    # =========================================================

    if not t:
        return "GENERAL"

    # =========================================================
    # 2. PROMPT INJECTION
    # =========================================================

    prompt_injection_phrases = [
        "ignore previous",
        "ignore all instructions",
        "ignore the previous instructions",
        "system prompt",
        "reveal your prompt",
        "show me your prompt",
        "jailbreak",
        "developer message",
        "hidden instructions",
    ]

    if any(phrase in t for phrase in prompt_injection_phrases):
        return "PROMPT_INJECTION"

    # =========================================================
    # 3. ABUSE
    # =========================================================

    abuse_words = [
        "idiot",
        "stupid",
        "shut up",
        "fuck you",
        "bitch",
        "dumb",
    ]

    if any(word in t for word in abuse_words):
        return "ABUSE"

    # =========================================================
    # 4. GENERAL CONVERSATION
    #    These MUST NOT go to RAG
    # =========================================================

    general_exact = {
        "hello",
        "hi",
        "hey",
        "hello palto",
        "hi palto",
        "hey palto",

        "good morning",
        "good afternoon",
        "good evening",
        "good night",

        "thanks",
        "thank you",
        "thank you palto",
        "thanks palto",

        "ok",
        "okay",
        "sure",
        "great",
        "nice",

        "bye",
        "goodbye",
        "see you",

        # Arabic
        "اهلا",
        "أهلا",
        "اهلاً",
        "أهلاً",

        "اهلا وسهلا",
        "أهلا وسهلا",

        "السلام عليكم",
        "السلام عليكم ورحمة الله وبركاته",

        "صباح الخير",
        "صباح النور",

        "مساء الخير",
        "مساء النور",

        "تصبح على خير",

        "شكرا",
        "شكراً",
        "شكرا ليك",
        "شكراً ليك",
        "متشكر",
        "متشكر جدا",
        "متشكر جدًا",

        "تمام",
        "تمام كده",
        "حلو",
        "جميل",
        "ماشي",
        "اوكي",
        "أوكي",
    }

    if t in general_exact:
        return "GENERAL"

    # =========================================================
    # 5. GENERAL CONVERSATIONAL PHRASES
    # =========================================================

    general_phrases = [
        # English
        "what can you do",
        "who are you",
        "what are you",
        "how are you",
        "nice to meet you",
        "good to see you",

        # Arabic
        "انت مين",
        "إنت مين",
        "أنت مين",

        "انت ايه",
        "إنت ايه",
        "أنت ايه",

        "بتعمل ايه",
        "بتعمل إيه",
        "ماذا يمكنك ان تفعل",
        "ماذا يمكنك أن تفعل",

        "عامل ايه",
        "عامل إيه",

        "ازيك",
        "إزيك",
        "كيف حالك",

        "اهبارك",
        "اخبارك ايه",
        "أخبارك إيه",

        "ممكن تساعدني",
        "ممكن تساعدنى",

        "شكرا يا بالـطو",
        "شكراً يا بالطو",
        "شكرا يا بالطو",
    ]

    if any(phrase in t for phrase in general_phrases):
        return "GENERAL"

    # =========================================================
    # 6. DRUG INTERACTION
    # =========================================================

    if any(word in t for word in [
        "interaction",
        "interact",
        "drug interaction",
        "drug-drug interaction",

        "تداخل دوائي",
        "تداخلات دوائية",
        "تداخل الادوية",
        "تداخل الأدوية",
        "تفاعل دوائي",
        "تفاعلات دوائية",
    ]):
        return "DRUG_INTERACTION"

    # =========================================================
    # 7. CONTRAINDICATION
    # =========================================================

    if any(word in t for word in [
        "contraindication",
        "contraindications",
        "contraindicated",
        "contraindicate",

        "موانع الاستعمال",
        "موانع الاستخدام",
        "ممنوع استخدامه",
        "متى يمنع استخدام",
    ]):
        return "CONTRAINDICATION"

    # =========================================================
    # 8. DOSAGE
    # =========================================================

    if any(word in t for word in [
        "dose",
        "dosage",
        "dosing",
        "how much should i take",
        "how many mg",

        "جرعة",
        "الجرعة",
        "جرعات",
        "الجرعات",
        "كام مجم",
        "كم جرعة",
        "جرعة الدواء",
    ]):
        return "DOSAGE"

    # =========================================================
    # 9. MEDICAL GUIDELINE / RECOMMENDATION
    # =========================================================

    if any(word in t for word in [
        "guideline",
        "guidelines",
        "recommend",
        "recommendation",
        "recommendations",
        "clinical guideline",
        "treatment guideline",

        "إرشادات",
        "ارشادات",
        "توصية",
        "توصيات",
        "التوصيات",
        "إرشادات علاجية",
        "ارشادات علاجية",
    ]):
        return "MEDICAL_GUIDELINE"

    # =========================================================
    # 10. CLINICAL
    # =========================================================

    return "CLINICAL"