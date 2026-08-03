import socket

from flask import Flask, abort, render_template


app = Flask(__name__)
app.config["FREEZER_DESTINATION"] = "build"

BASE_URL = "https://mistfallhunterclasses.blog"
SUPPORT_EMAIL = "support@mistfallhunterclasses.blog"
OFFICIAL_STEAM_URL = "https://store.steampowered.com/app/3282300/Mistfall_Hunter/"
OFFICIAL_STEAM_DELUXE_URL = "https://store.steampowered.com/app/4572310/Mistfall_Hunter__Upgrade_to_Deluxe_Edition/"
STEAMDB_EMBED_URL = "https://steamdb.info/embed/?appid=3282300"
STEAMDB_CHARTS_URL = "https://steamdb.info/app/3282300/charts/"
CURRENT_YEAR = "2026"
LAST_UPDATED = "2026-07-30"
PAGE_LASTMOD = {"price": "2026-08-01", "player-count": "2026-08-01", "review": "2026-08-03"}

LOCALE_ORDER = ["en", "es", "ja", "fr", "de", "pt", "ko", "it"]
LOCALES = {
    "en": {"name": "English", "market": "US", "html_lang": "en"},
    "es": {"name": "Español", "market": "US / Latin America", "html_lang": "es"},
    "ja": {"name": "日本語", "market": "Japan", "html_lang": "ja"},
    "fr": {"name": "Français", "market": "France", "html_lang": "fr"},
    "de": {"name": "Deutsch", "market": "Germany", "html_lang": "de"},
    "pt": {"name": "Português", "market": "Brazil", "html_lang": "pt"},
    "ko": {"name": "한국어", "market": "Korea", "html_lang": "ko"},
    "it": {"name": "Italiano", "market": "Italy", "html_lang": "it"},
}

PAGE_ORDER = [
    "home",
    "classes",
    "build-planner",
    "price",
    "player-count",
    "steam",
    "review",
    "about",
    "contact",
    "privacy-policy",
    "terms-of-service",
]

PAGE_SLUGS = {
    "home": "",
    "classes": "classes",
    "build-planner": "build-planner",
    "price": "price",
    "player-count": "player-count",
    "steam": "steam",
    "review": "review",
    "about": "about",
    "contact": "contact",
    "privacy-policy": "privacy-policy",
    "terms-of-service": "terms-of-service",
}

CLASS_STATS = [
    {"id": "mercenary", "name": "Mercenary", "solo": 86, "squad": 78, "burst": 60, "control": 54, "frontline": 92, "risk": "low"},
    {"id": "blackarrow", "name": "Blackarrow", "solo": 74, "squad": 84, "burst": 78, "control": 64, "frontline": 58, "risk": "medium"},
    {"id": "shadowstrix", "name": "Shadowstrix", "solo": 82, "squad": 70, "burst": 90, "control": 58, "frontline": 62, "risk": "high"},
    {"id": "sorcerer", "name": "Sorcerer", "solo": 66, "squad": 88, "burst": 92, "control": 82, "frontline": 40, "risk": "high"},
    {"id": "seer", "name": "Seer", "solo": 58, "squad": 92, "burst": 42, "control": 86, "frontline": 38, "risk": "medium"},
    {"id": "withered-knight", "name": "Withered Knight", "solo": 78, "squad": 86, "burst": 64, "control": 76, "frontline": 88, "risk": "medium"},
]

KEYWORD_MAP = {
    "en": {"market": "US", "primary": "Mistfall Hunter classes", "related": ["Mistfall Hunter build planner", "Mistfall Hunter class guide", "Mistfall Hunter best class", "Mistfall Hunter Steam"], "rejected": ["Mistfall Hunter codes as a priority keyword"], "evidence": "English SERP intent favors class guide, build planner, Steam facts, and early best-class comparison.", "confidence": "medium"},
    "es": {"market": "US / Latin America", "primary": "clases de Mistfall Hunter", "related": ["guia de clases Mistfall Hunter", "mejor clase Mistfall Hunter", "planificador de builds Mistfall Hunter", "Mistfall Hunter Steam"], "rejected": ["codigos Mistfall Hunter as high priority"], "evidence": "Spanish game queries commonly keep the game name and localize guide, classes, best class, and builds.", "confidence": "medium"},
    "ja": {"market": "Japan", "primary": "Mistfall Hunter クラス", "related": ["Mistfall Hunter ビルド", "Mistfall Hunter クラスガイド", "Mistfall Hunter おすすめクラス", "Mistfall Hunter Steam"], "rejected": ["Mistfall Hunter コード as primary intent"], "evidence": "Japanese game searches commonly keep the title and use クラス, ビルド, ガイド, and おすすめ.", "confidence": "medium"},
    "fr": {"market": "France", "primary": "classes Mistfall Hunter", "related": ["guide des classes Mistfall Hunter", "meilleure classe Mistfall Hunter", "build Mistfall Hunter", "Mistfall Hunter Steam"], "rejected": ["codes Mistfall Hunter as current homepage priority"], "evidence": "French SERP wording for games keeps the title and uses guide, classes, meilleure classe, and build.", "confidence": "medium"},
    "de": {"market": "Germany", "primary": "Mistfall Hunter Klassen", "related": ["Mistfall Hunter Klassen Guide", "beste Klasse Mistfall Hunter", "Mistfall Hunter Build Planner", "Mistfall Hunter Steam"], "rejected": ["Mistfall Hunter Codes as high-priority page"], "evidence": "German game searches commonly retain the title and localize class intent as Klassen and beste Klasse.", "confidence": "medium"},
    "pt": {"market": "Brazil", "primary": "classes de Mistfall Hunter", "related": ["guia de classes Mistfall Hunter", "melhor classe Mistfall Hunter", "planejador de build Mistfall Hunter", "Mistfall Hunter Steam"], "rejected": ["codigos Mistfall Hunter as priority"], "evidence": "Brazilian Portuguese game queries usually keep the title and localize classes, guide, best class, and build.", "confidence": "medium"},
    "ko": {"market": "Korea", "primary": "Mistfall Hunter 클래스", "related": ["Mistfall Hunter 빌드", "Mistfall Hunter 클래스 가이드", "Mistfall Hunter 추천 클래스", "Mistfall Hunter Steam"], "rejected": ["Mistfall Hunter 코드 as primary page"], "evidence": "Korean game searches commonly keep the title and use 클래스, 빌드, 가이드, and 추천.", "confidence": "medium"},
    "it": {"market": "Italy", "primary": "classi Mistfall Hunter", "related": ["guida classi Mistfall Hunter", "migliore classe Mistfall Hunter", "build Mistfall Hunter", "Mistfall Hunter Steam"], "rejected": ["codici Mistfall Hunter as homepage priority"], "evidence": "Italian game search wording commonly keeps the title and uses classi, guida, migliore classe, and build.", "confidence": "medium"},
}

REVIEW_KEYWORD_MAP = {
    "en": {"market": "US", "primary": "Mistfall Hunter review", "related": ["is Mistfall Hunter worth it", "Mistfall Hunter price", "Mistfall Hunter player count", "Mistfall Hunter classes"], "rejected": ["Mistfall Hunter character creation as a standalone page; fold into the review because its global window volume was 400."], "evidence": "Similarweb global phrase match: window volume 11,420, difficulty 19, informational intent, 2026-08-03; question tab returned no rows.", "confidence": "medium"},
    "es": {"market": "US / Latin America", "primary": "reseña de Mistfall Hunter", "related": ["vale la pena Mistfall Hunter", "precio de Mistfall Hunter", "clases de Mistfall Hunter", "jugadores de Mistfall Hunter"], "rejected": ["Mistfall Hunter Test as a literal German-only candidate"], "evidence": "Similarweb localized query returned no rows in all three tabs; wording follows neutral Latin-American game-search usage and the validated global English review intent.", "confidence": "low"},
    "ja": {"market": "Japan", "primary": "Mistfall Hunter 評価", "related": ["Mistfall Hunter レビュー", "Mistfall Hunter 感想", "Mistfall Hunter 価格", "Mistfall Hunter クラス"], "rejected": ["Mistfall Hunter レビュー as primary because the phrase tab had 0 window volume; it remains a supporting variant."], "evidence": "Similarweb related tab returned Mistfall Hunter 評価 with window volume 100 and difficulty 17; the phrase tab for レビュー had 0 window volume and average volume 82.", "confidence": "medium"},
    "fr": {"market": "France", "primary": "avis Mistfall Hunter", "related": ["Mistfall Hunter vaut-il le coup", "prix Mistfall Hunter", "classes Mistfall Hunter", "joueurs Mistfall Hunter"], "rejected": ["review Mistfall Hunter as the only French wording"], "evidence": "Similarweb localized query returned no rows in all three tabs; avis is the natural French review intent and is bounded by the validated global English review cluster.", "confidence": "low"},
    "de": {"market": "Germany", "primary": "Mistfall Hunter Review", "related": ["lohnt sich Mistfall Hunter", "Mistfall Hunter Preis", "Mistfall Hunter Klassen", "Mistfall Hunter Spielerzahl"], "rejected": ["Mistfall Hunter Test as an isolated primary; Similarweb returned playtest-related phrases rather than a clean review cluster."], "evidence": "Similarweb German Test query was polluted by playtest terms; the global review phrase remains the cleanest validated intent, while Review is retained as common German gaming usage.", "confidence": "low"},
    "pt": {"market": "Brazil", "primary": "análise de Mistfall Hunter", "related": ["Mistfall Hunter vale a pena", "preço de Mistfall Hunter", "classes de Mistfall Hunter", "jogadores de Mistfall Hunter"], "rejected": ["review Mistfall Hunter as the only localized wording"], "evidence": "Similarweb localized query returned no rows in all three tabs; análise de is the natural Brazilian Portuguese review intent and is bounded by the global cluster.", "confidence": "low"},
    "ko": {"market": "Korea", "primary": "Mistfall Hunter 리뷰", "related": ["Mistfall Hunter 할 만한가", "Mistfall Hunter 가격", "Mistfall Hunter 클래스", "Mistfall Hunter 플레이어 수"], "rejected": ["Mistfall Hunter 평가 as the primary because local Similarweb coverage was empty"], "evidence": "Similarweb Korean query returned no rows in all three tabs; 리뷰 is the established Korean game-review wording and is bounded by the validated global review intent.", "confidence": "low"},
    "it": {"market": "Italy", "primary": "recensione Mistfall Hunter", "related": ["Mistfall Hunter vale la pena", "prezzo Mistfall Hunter", "classi Mistfall Hunter", "giocatori Mistfall Hunter"], "rejected": ["review Mistfall Hunter as the only Italian wording"], "evidence": "Similarweb localized query returned no rows in all three tabs; recensione is the natural Italian review intent and is bounded by the validated global review cluster.", "confidence": "low"},
}

TEXT = {
    "en": {
        "site_name": "Mistfall Hunter Classes",
        "brand": "Mistfall Classes",
        "nav_aria": "Primary navigation",
        "footer_aria": "Footer navigation",
        "language_aria": "Choose language",
        "steam_cta": "Steam",
        "nav": {"home": "Planner", "classes": "Classes", "build-planner": "Build Planner", "player-count": "Player Count", "steam": "Steam Info", "contact": "Contact"},
        "footer": {"about": "About", "contact": "Contact", "privacy-policy": "Privacy", "terms-of-service": "Terms", "sitemap": "Sitemap", "disclaimer": "Fan-made Mistfall Hunter class guide and build planner. Not affiliated with Bellring Games, Skystone Games, Steam, or Valve."},
        "pages": {
            "home": {"title": "Mistfall Hunter Classes & Build Planner", "description": "Compare Mistfall Hunter classes, plan solo or squad builds, and check role recommendations with a fan-made class planner.", "h1": "Mistfall Hunter Classes & Build Planner", "kicker": "Updated July 2026 - Steam / PC - fan-made tool"},
            "classes": {"title": "Mistfall Hunter Classes Guide", "description": "A practical Mistfall Hunter classes guide covering roles, strengths, risk level, and beginner picks.", "h1": "Mistfall Hunter Classes Guide", "kicker": "Mistfall Hunter Classes"},
            "build-planner": {"title": "Mistfall Hunter Build Planner", "description": "Use the Mistfall Hunter build planner to match classes with solo, duo, and squad play styles.", "h1": "Mistfall Hunter Build Planner", "kicker": "Mistfall Hunter Classes"},
            "steam": {"title": "Mistfall Hunter Steam Info", "description": "Mistfall Hunter Steam info for availability, platform facts, release date, developer, publisher, and official source links.", "h1": "Mistfall Hunter Steam Info", "kicker": "Mistfall Hunter Classes"},
            "about": {"title": "About Mistfall Hunter Classes", "description": "Learn how Mistfall Hunter Classes reviews public sources and keeps class guide recommendations transparent.", "h1": "About Mistfall Hunter Classes", "kicker": "Mistfall Hunter Classes"},
            "contact": {"title": "Contact Mistfall Hunter Classes", "description": "Send corrections, source notes, class data updates, and site feedback to Mistfall Hunter Classes.", "h1": "Contact Mistfall Hunter Classes", "kicker": "Mistfall Hunter Classes"},
            "privacy-policy": {"title": "Privacy Policy", "description": "Privacy policy for Mistfall Hunter Classes, a fan-made guide and build planner site.", "h1": "Privacy Policy", "kicker": "Mistfall Hunter Classes"},
            "terms-of-service": {"title": "Terms of Service", "description": "Terms of service and fan-site disclaimer for Mistfall Hunter Classes.", "h1": "Terms of Service", "kicker": "Mistfall Hunter Classes"},
        },
        "classes": {
            "risk": {"low": "Low risk", "medium": "Medium risk", "high": "High risk"},
            "metrics": {"solo": "Solo", "squad": "Squad", "burst": "Burst", "control": "Control"},
            "roles": {
                "mercenary": ["Frontline brawler", "Players who want forgiving melee pressure and steady extractions."],
                "blackarrow": ["Ranged pressure", "Careful players who prefer scouting, poking, and choosing fights."],
                "shadowstrix": ["Assassin skirmisher", "High-mobility players who like ambushes, flanks, and fast disengage."],
                "sorcerer": ["Area damage caster", "Players who want spell burst, zone pressure, and group fight impact."],
                "seer": ["Support and information", "Squads that value tracking, utility, and safer extraction decisions."],
                "withered-knight": ["Durable initiator", "Players who like holding space, surviving trades, and protecting allies."],
            },
        },
        "planner": {
            "kicker": "Interactive class picker",
            "title": "Mistfall Hunter class planner",
            "description": "Answer four questions and the tool ranks classes for your run. The output is a recommendation model, not an official tier list, so use it as a starting point and recheck after balance patches.",
            "labels": {"format": "Run format", "style": "Preferred combat rhythm", "risk": "Risk tolerance", "experience": "Experience level"},
            "options": {
                "format": {"solo": "Solo extraction", "duo": "Duo skirmish", "squad": "Squad play"},
                "style": {"balanced": "Balanced survival", "burst": "Burst damage", "control": "Control and utility", "frontline": "Frontline pressure"},
                "risk": {"low": "Low risk", "medium": "Medium risk", "high": "High risk"},
                "experience": {"new": "New player", "returning": "Returning ARPG player", "advanced": "Advanced extraction player"},
            },
            "submit": "Find my class",
            "reset": "Reset",
            "empty": "Your recommendation will appear here. Try the default solo setup first if you are unsure.",
            "short_empty": "Pick your settings to generate a build direction.",
            "calculating": "Calculating class fit...",
            "recommended": "Recommended class",
            "fit": "{name} fits your {format} run because the scoring model balances class role, selected combat rhythm, risk tolerance, and experience level.",
            "score_label": "{score} out of 100",
            "score_text": "{score}/100 - {role}",
            "note": "Model note: this is a fan-made recommendation and should be rechecked when verified Mistfall Hunter class balance data changes.",
        },
        "home": {
            "lede": "Choose a class for solo runs, duo pressure, or squad extraction before you spend hours learning the wrong rhythm. The planner below compares Mistfall Hunter classes by play style, risk tolerance, damage needs, control, and team utility.",
            "actions": ["Use the planner", "Read class guide"],
            "facts": [["Game type", "PvPvE extraction ARPG"], ["Release", "29 Jul, 2026"], ["Developer", "Bellring Games"], ["Platform", "Windows on Steam"]],
            "media_alt": "Official Steam hero art for Mistfall Hunter dark fantasy extraction ARPG",
            "media_caption": "Official Steam store media, processed for this fan guide.",
            "classes_kicker": "Role overview",
            "classes_title": "Mistfall Hunter classes at a glance",
            "classes_desc": "These profiles keep the class choice practical: who should play it, what the role contributes, and where the risk sits.",
            "steps_kicker": "How to use the result",
            "steps_title": "Turn a recommendation into a playable build",
            "steps": ["Pick the class role first. Mistfall Hunter rewards extraction decisions, so survivability and information can matter as much as raw damage.", "Match gear to the job. Frontline classes need staying power, burst classes need clean engage windows, and support classes need safe positioning.", "Recheck after patches. This site records source dates because class balance, skill values, and gear availability can change quickly."],
            "source_title": "Source policy",
            "source_text": "Official Steam facts are used for platform and release details. Class recommendations are a transparent fan scoring model and should be corrected when stronger patch or gameplay evidence appears.",
            "source_link": "Open official Steam page",
            "method_kicker": "Planner method",
            "method_title": "Why the Mistfall Hunter class planner weights roles this way",
            "method_paragraphs": ["The class planner starts with the practical question players ask before a run: will this class help me survive the next extraction, win a fight, or support the squad decision? Solo scoring favors classes that can recover from mistakes and finish a route without constant help. Squad scoring gives more credit to information, control, and space creation because those traits turn into safer team decisions.", "Combat rhythm changes the second layer of scoring. Burst damage favors Shadowstrix and Sorcerer because they fit short engage windows. Control and utility lift Seer, Sorcerer, and Withered Knight because they help shape fights before the final trade. Frontline pressure favors Mercenary and Withered Knight because they are easier to understand when a fight becomes messy.", "Risk tolerance matters because a strong class can still be wrong for the player using it. New players get a penalty on high-risk picks, while advanced extraction players get more room to choose fragile burst tools. This keeps the result practical rather than pretending one universal tier list fits every run."],
            "method_card_title": "Inputs used by the tool",
            "method_items": ["Run format: solo, duo, or squad.", "Combat rhythm: balanced, burst, control, or frontline.", "Risk tolerance: low, medium, or high.", "Experience level: new, returning, or advanced."],
            "output_title": "Output you get",
            "output_text": "A top recommended class, a role explanation, and the next four ranked alternatives with score bars. The result is designed to help you pick a direction quickly, then read the class guide before committing to gear and talent choices.",
            "comparison_kicker": "Decision table",
            "comparison_title": "Best class by player need",
            "comparison_headers": ["Need", "Best starting pick", "Why it fits"],
            "comparison_rows": [["First solo extraction", "Mercenary", "Forgiving frontline profile and lower planning load."], ["Squad utility", "Seer", "Information and control help the whole team choose safer fights."], ["High burst plays", "Shadowstrix or Sorcerer", "Both reward timing, but punish bad positioning."], ["Anchor role", "Withered Knight", "Durability and space control suit coordinated groups."]],
            "examples_kicker": "Examples",
            "examples_title": "Example Mistfall Hunter class choices",
            "examples": ["New solo player: choose solo extraction, balanced survival, low risk, and new player. The planner should lean toward Mercenary because it reduces decision overload and gives a clearer frontline pattern for early learning.", "Coordinated three-player squad: choose squad play, control and utility, medium risk, and returning ARPG player. Seer and Withered Knight usually rise because information, control, and anchoring help teammates make cleaner extraction calls.", "Aggressive PvP hunter: choose duo skirmish, burst damage, high risk, and advanced extraction player. Shadowstrix or Sorcerer can appear near the top because the model assumes you can handle positioning mistakes and timing windows."],
            "caution_title": "When not to trust the result blindly",
            "caution": ["Do not treat the planner as final if a new patch changes class skills, talent values, gear scaling, or extraction rewards. If your party already has a support or frontline role, pick the class that fills the missing job instead of stacking the highest score.", "The safest workflow is planner first, class guide second, then in-game testing with your current gear.", "If two classes score close together, treat the result as a tie and choose the role your party lacks. A ten-point gap usually means the recommended class fits the selected run shape more clearly."],
            "update_title": "Update policy",
            "update_text": "Because Mistfall Hunter launched recently, early class advice can shift as players find stronger routes and the developer adjusts balance. This planner should be reviewed whenever official patch notes, verified class values, or repeated community gameplay evidence contradict the current scoring assumptions.",
            "faq_title": "Mistfall Hunter classes FAQ",
            "faq": [["What is the best Mistfall Hunter class for beginners?", "Mercenary is the safest default for new players because its role is easier to understand during stressful extraction fights. Withered Knight is also a strong beginner option for players joining squads."], ["Is Shadowstrix good for solo play?", "Shadowstrix can be strong for solo players who already understand ambush timing and disengage windows. It is less forgiving than Mercenary because mistakes are punished faster."], ["Should squads always bring Seer?", "No class should be mandatory in every squad. Seer is valuable when your team needs information, utility, and safer extraction calls, but a damage-heavy squad may prefer Sorcerer or Blackarrow."], ["How accurate is the Mistfall Hunter build planner?", "The planner is a practical scoring model based on role fit. It is useful for choosing a starting direction, but it is not official and should be updated when verified skill values or patch notes change."], ["Does Mistfall Hunter have codes?", "This site focuses on classes and builds because the current opportunity is a decision-support guide, not a short-lived codes page. If official redeem codes become meaningful, they should be handled on a separate page."]],
        },
    },
}

LOCALE_OVERRIDES = {
    "es": {
        "site_name": "Clases de Mistfall Hunter", "brand": "Mistfall Clases", "nav_aria": "Navegacion principal", "footer_aria": "Navegacion del pie", "language_aria": "Elegir idioma", "steam_cta": "Steam",
        "nav": {"home": "Planificador", "classes": "Clases", "build-planner": "Builds", "player-count": "Jugadores", "steam": "Steam", "contact": "Contacto"},
        "footer": {"about": "Acerca de", "contact": "Contacto", "privacy-policy": "Privacidad", "terms-of-service": "Terminos", "sitemap": "Mapa del sitio", "disclaimer": "Guia y planificador fan-made de Mistfall Hunter. No esta afiliado con Bellring Games, Skystone Games, Steam ni Valve."},
        "pages": {
            "home": {"title": "Clases de Mistfall Hunter y Builds", "description": "Compara clases de Mistfall Hunter, planea builds solo o en escuadron y revisa recomendaciones con una herramienta fan-made.", "h1": "Clases de Mistfall Hunter y Builds", "kicker": "Actualizado en julio de 2026 - Steam / PC - herramienta fan-made"},
            "classes": {"title": "Guia de Clases de Mistfall Hunter", "description": "Guia practica de clases de Mistfall Hunter con roles, fortalezas, riesgo y elecciones para principiantes.", "h1": "Guia de Clases de Mistfall Hunter", "kicker": "Clases de Mistfall Hunter"},
            "build-planner": {"title": "Planificador de Builds Mistfall Hunter", "description": "Usa el planificador de builds Mistfall Hunter para unir clases con juego solo, duo o escuadron.", "h1": "Planificador de Builds Mistfall Hunter", "kicker": "Clases de Mistfall Hunter"},
            "steam": {"title": "Mistfall Hunter en Steam", "description": "Datos de Mistfall Hunter en Steam: disponibilidad, plataforma, fecha, desarrollador, editor y enlaces oficiales.", "h1": "Mistfall Hunter en Steam", "kicker": "Clases de Mistfall Hunter"},
            "about": {"title": "Acerca de Clases de Mistfall Hunter", "description": "Como revisamos fuentes publicas y mantenemos recomendaciones transparentes para Mistfall Hunter.", "h1": "Acerca de Clases de Mistfall Hunter", "kicker": "Clases de Mistfall Hunter"},
            "contact": {"title": "Contacto de Clases de Mistfall Hunter", "description": "Envia correcciones, notas de fuente, datos de clases y comentarios sobre el sitio.", "h1": "Contacto", "kicker": "Clases de Mistfall Hunter"},
            "privacy-policy": {"title": "Politica de Privacidad", "description": "Politica de privacidad de Clases de Mistfall Hunter, una guia fan-made y planificador de builds.", "h1": "Politica de Privacidad", "kicker": "Clases de Mistfall Hunter"},
            "terms-of-service": {"title": "Terminos de Servicio", "description": "Terminos de servicio y aviso de sitio fan-made para Clases de Mistfall Hunter.", "h1": "Terminos de Servicio", "kicker": "Clases de Mistfall Hunter"},
        },
        "home": {"lede": "Elige una clase para rutas en solo, presion en duo o extraccion de escuadron antes de invertir horas en un ritmo que no encaja. El planificador compara clases de Mistfall Hunter por estilo, riesgo, dano, control y utilidad.", "actions": ["Usar planificador", "Leer guia de clases"], "facts": [["Tipo de juego", "ARPG de extraccion PvPvE"], ["Lanzamiento", "29 de julio de 2026"], ["Desarrollador", "Bellring Games"], ["Plataforma", "Windows en Steam"]], "classes_kicker": "Resumen de roles", "classes_title": "Clases de Mistfall Hunter de un vistazo", "classes_desc": "Cada perfil explica quien deberia usar la clase, que aporta al grupo y donde esta el riesgo.", "method_title": "Como pondera roles el planificador de clases Mistfall Hunter", "faq_title": "Preguntas sobre clases de Mistfall Hunter"},
    },
    "ja": {
        "site_name": "Mistfall Hunter クラス", "brand": "Mistfall クラス", "nav_aria": "主要ナビゲーション", "footer_aria": "フッターナビゲーション", "language_aria": "言語を選択", "steam_cta": "Steam",
        "nav": {"home": "プランナー", "classes": "クラス", "build-planner": "ビルド", "player-count": "プレイヤー数", "steam": "Steam情報", "contact": "連絡先"},
        "footer": {"about": "このサイトについて", "contact": "連絡先", "privacy-policy": "プライバシー", "terms-of-service": "利用規約", "sitemap": "サイトマップ", "disclaimer": "Mistfall Hunter のファン作成クラスガイド兼ビルドプランナーです。Bellring Games、Skystone Games、Steam、Valve とは提携していません。"},
        "pages": {
            "home": {"title": "Mistfall Hunter クラスとビルド", "description": "Mistfall Hunter クラスを比較し、ソロや分隊向けのビルドを考えるファン作成プランナーです。", "h1": "Mistfall Hunter クラスとビルド", "kicker": "2026年7月更新 - Steam / PC - ファン作成ツール"},
            "classes": {"title": "Mistfall Hunter クラスガイド", "description": "Mistfall Hunter クラスの役割、強み、リスク、初心者向け候補を整理した実用ガイドです。", "h1": "Mistfall Hunter クラスガイド", "kicker": "Mistfall Hunter クラス"},
            "build-planner": {"title": "Mistfall Hunter ビルドプランナー", "description": "Mistfall Hunter ビルドプランナーで、ソロ、デュオ、分隊の遊び方に合うクラスを探せます。", "h1": "Mistfall Hunter ビルドプランナー", "kicker": "Mistfall Hunter クラス"},
            "steam": {"title": "Mistfall Hunter Steam情報", "description": "Mistfall Hunter のSteam掲載情報、対応環境、発売日、開発元、発売元、公式リンクを確認できます。", "h1": "Mistfall Hunter Steam情報", "kicker": "Mistfall Hunter クラス"},
            "about": {"title": "Mistfall Hunter クラスについて", "description": "公開情報を確認し、クラスおすすめを透明に管理する方針を説明します。", "h1": "Mistfall Hunter クラスについて", "kicker": "Mistfall Hunter クラス"},
            "contact": {"title": "Mistfall Hunter クラス連絡先", "description": "修正、情報源、クラスデータ、サイト改善案を送るための連絡ページです。", "h1": "連絡先", "kicker": "Mistfall Hunter クラス"},
            "privacy-policy": {"title": "プライバシーポリシー", "description": "ファン作成ガイド Mistfall Hunter クラスのプライバシーポリシーです。", "h1": "プライバシーポリシー", "kicker": "Mistfall Hunter クラス"},
            "terms-of-service": {"title": "利用規約", "description": "Mistfall Hunter クラスの利用規約とファンサイト免責事項です。", "h1": "利用規約", "kicker": "Mistfall Hunter クラス"},
        },
        "home": {"lede": "ソロ探索、デュオでの圧力、分隊での脱出判断に合うクラスを、長時間試す前に整理できます。このプランナーは Mistfall Hunter クラスをプレイスタイル、リスク、火力、制御、チーム支援で比較します。", "actions": ["プランナーを使う", "クラスガイドを読む"], "facts": [["ゲーム種別", "PvPvE脱出ARPG"], ["発売日", "2026年7月29日"], ["開発元", "Bellring Games"], ["プラットフォーム", "Steam版Windows"]], "classes_kicker": "役割概要", "classes_title": "Mistfall Hunter クラス早見表", "classes_desc": "各プロフィールは、誰に向くか、どの役割を担うか、どこにリスクがあるかを実戦向けにまとめます。", "method_title": "Mistfall Hunter クラスプランナーの重み付け", "faq_title": "Mistfall Hunter クラスFAQ"},
    },
    "fr": {
        "site_name": "Classes Mistfall Hunter", "brand": "Mistfall Classes", "nav_aria": "Navigation principale", "footer_aria": "Navigation du pied", "language_aria": "Choisir la langue", "steam_cta": "Steam",
        "nav": {"home": "Planificateur", "classes": "Classes", "build-planner": "Builds", "player-count": "Joueurs", "steam": "Steam", "contact": "Contact"},
        "footer": {"about": "A propos", "contact": "Contact", "privacy-policy": "Confidentialite", "terms-of-service": "Conditions", "sitemap": "Plan du site", "disclaimer": "Guide et planificateur fan-made pour Mistfall Hunter. Non affilie a Bellring Games, Skystone Games, Steam ou Valve."},
        "pages": {
            "home": {"title": "Classes Mistfall Hunter et Builds", "description": "Comparez les classes Mistfall Hunter, preparez vos builds solo ou escouade et utilisez un planificateur fan-made.", "h1": "Classes Mistfall Hunter et Builds", "kicker": "Mis a jour en juillet 2026 - Steam / PC - outil fan-made"},
            "classes": {"title": "Guide des Classes Mistfall Hunter", "description": "Guide pratique des classes Mistfall Hunter avec roles, forces, risque et choix pour debutants.", "h1": "Guide des Classes Mistfall Hunter", "kicker": "Classes Mistfall Hunter"},
            "build-planner": {"title": "Planificateur de Build Mistfall Hunter", "description": "Utilisez le planificateur de build Mistfall Hunter pour relier classes, jeu solo, duo et escouade.", "h1": "Planificateur de Build Mistfall Hunter", "kicker": "Classes Mistfall Hunter"},
            "steam": {"title": "Informations Steam Mistfall Hunter", "description": "Informations Steam de Mistfall Hunter: disponibilite, plateforme, date, developpeur, editeur et liens officiels.", "h1": "Informations Steam Mistfall Hunter", "kicker": "Classes Mistfall Hunter"},
            "about": {"title": "A propos de Classes Mistfall Hunter", "description": "Decouvrez comment ce site verifie les sources publiques et garde les recommandations transparentes.", "h1": "A propos", "kicker": "Classes Mistfall Hunter"},
            "contact": {"title": "Contact Classes Mistfall Hunter", "description": "Envoyez corrections, sources, donnees de classes et retours sur le site.", "h1": "Contact", "kicker": "Classes Mistfall Hunter"},
            "privacy-policy": {"title": "Politique de Confidentialite", "description": "Politique de confidentialite de Classes Mistfall Hunter, guide fan-made et planificateur de builds.", "h1": "Politique de Confidentialite", "kicker": "Classes Mistfall Hunter"},
            "terms-of-service": {"title": "Conditions d Utilisation", "description": "Conditions d utilisation et avertissement fan-site pour Classes Mistfall Hunter.", "h1": "Conditions d Utilisation", "kicker": "Classes Mistfall Hunter"},
        },
        "home": {"lede": "Choisissez une classe pour le solo, la pression en duo ou l extraction en escouade avant de passer des heures sur un rythme mal adapte. Le planificateur compare les classes Mistfall Hunter par style, risque, degats, controle et utilite.", "actions": ["Utiliser le planificateur", "Lire le guide"], "facts": [["Type de jeu", "ARPG d extraction PvPvE"], ["Sortie", "29 juillet 2026"], ["Developpeur", "Bellring Games"], ["Plateforme", "Windows sur Steam"]], "classes_kicker": "Apercu des roles", "classes_title": "Classes Mistfall Hunter en bref", "classes_desc": "Chaque profil indique a qui la classe convient, ce qu elle apporte et ou se situe le risque.", "method_title": "Pourquoi le planificateur de classes Mistfall Hunter pondere les roles", "faq_title": "FAQ classes Mistfall Hunter"},
    },
    "de": {
        "site_name": "Mistfall Hunter Klassen", "brand": "Mistfall Klassen", "nav_aria": "Hauptnavigation", "footer_aria": "Footer-Navigation", "language_aria": "Sprache waehlen", "steam_cta": "Steam",
        "nav": {"home": "Planer", "classes": "Klassen", "build-planner": "Build-Planer", "player-count": "Spielerzahl", "steam": "Steam-Info", "contact": "Kontakt"},
        "footer": {"about": "Uber uns", "contact": "Kontakt", "privacy-policy": "Datenschutz", "terms-of-service": "Nutzungsbedingungen", "sitemap": "Sitemap", "disclaimer": "Fan-erstellter Mistfall Hunter Klassen Guide und Build-Planer. Nicht mit Bellring Games, Skystone Games, Steam oder Valve verbunden."},
        "pages": {
            "home": {"title": "Mistfall Hunter Klassen & Build-Planer", "description": "Vergleiche Mistfall Hunter Klassen, plane Solo- oder Gruppen-Builds und nutze einen fan-erstellten Klassenplaner.", "h1": "Mistfall Hunter Klassen & Build-Planer", "kicker": "Aktualisiert im Juli 2026 - Steam / PC - Fan-Tool"},
            "classes": {"title": "Mistfall Hunter Klassen Guide", "description": "Praktischer Mistfall Hunter Klassen Guide mit Rollen, Staerken, Risiko und Einsteiger-Tipps.", "h1": "Mistfall Hunter Klassen Guide", "kicker": "Mistfall Hunter Klassen"},
            "build-planner": {"title": "Mistfall Hunter Build-Planer", "description": "Nutze den Mistfall Hunter Build-Planer, um Klassen mit Solo-, Duo- und Gruppenstil abzugleichen.", "h1": "Mistfall Hunter Build-Planer", "kicker": "Mistfall Hunter Klassen"},
            "steam": {"title": "Mistfall Hunter Steam Info", "description": "Steam-Infos zu Mistfall Hunter: Verfuegbarkeit, Plattform, Release, Entwickler, Publisher und offizielle Links.", "h1": "Mistfall Hunter Steam Info", "kicker": "Mistfall Hunter Klassen"},
            "about": {"title": "Uber Mistfall Hunter Klassen", "description": "Wie diese Seite oeffentliche Quellen prueft und Klassenempfehlungen transparent haelt.", "h1": "Uber Mistfall Hunter Klassen", "kicker": "Mistfall Hunter Klassen"},
            "contact": {"title": "Kontakt zu Mistfall Hunter Klassen", "description": "Sende Korrekturen, Quellen, Klassendaten und Feedback zur Website.", "h1": "Kontakt", "kicker": "Mistfall Hunter Klassen"},
            "privacy-policy": {"title": "Datenschutzerklaerung", "description": "Datenschutzerklaerung fuer Mistfall Hunter Klassen, einen fan-erstellten Guide und Build-Planer.", "h1": "Datenschutzerklaerung", "kicker": "Mistfall Hunter Klassen"},
            "terms-of-service": {"title": "Nutzungsbedingungen", "description": "Nutzungsbedingungen und Fan-Site-Hinweis fuer Mistfall Hunter Klassen.", "h1": "Nutzungsbedingungen", "kicker": "Mistfall Hunter Klassen"},
        },
        "home": {"lede": "Waehle eine Klasse fuer Solo-Routen, Duo-Druck oder Gruppen-Extraktion, bevor du Stunden in einen falschen Spielrhythmus steckst. Der Planer vergleicht Mistfall Hunter Klassen nach Stil, Risiko, Schaden, Kontrolle und Teamnutzen.", "actions": ["Planer nutzen", "Klassenguide lesen"], "facts": [["Spieltyp", "PvPvE Extraction ARPG"], ["Release", "29. Juli 2026"], ["Entwickler", "Bellring Games"], ["Plattform", "Windows auf Steam"]], "classes_kicker": "Rollenueberblick", "classes_title": "Mistfall Hunter Klassen auf einen Blick", "classes_desc": "Die Profile zeigen, fuer wen eine Klasse passt, welchen Beitrag sie leistet und wie hoch das Risiko ist.", "method_title": "Warum der Mistfall Hunter Klassenplaner Rollen so gewichtet", "faq_title": "Mistfall Hunter Klassen FAQ"},
    },
    "pt": {
        "site_name": "Classes de Mistfall Hunter", "brand": "Mistfall Classes", "nav_aria": "Navegacao principal", "footer_aria": "Navegacao do rodape", "language_aria": "Escolher idioma", "steam_cta": "Steam",
        "nav": {"home": "Planejador", "classes": "Classes", "build-planner": "Builds", "player-count": "Jogadores", "steam": "Steam", "contact": "Contato"},
        "footer": {"about": "Sobre", "contact": "Contato", "privacy-policy": "Privacidade", "terms-of-service": "Termos", "sitemap": "Mapa do site", "disclaimer": "Guia e planejador fan-made de Mistfall Hunter. Nao afiliado a Bellring Games, Skystone Games, Steam ou Valve."},
        "pages": {
            "home": {"title": "Classes de Mistfall Hunter e Builds", "description": "Compare classes de Mistfall Hunter, planeje builds solo ou em grupo e use um planejador fan-made.", "h1": "Classes de Mistfall Hunter e Builds", "kicker": "Atualizado em julho de 2026 - Steam / PC - ferramenta fan-made"},
            "classes": {"title": "Guia de Classes Mistfall Hunter", "description": "Guia pratico de classes Mistfall Hunter com papeis, pontos fortes, risco e escolhas para iniciantes.", "h1": "Guia de Classes Mistfall Hunter", "kicker": "Classes de Mistfall Hunter"},
            "build-planner": {"title": "Planejador de Build Mistfall Hunter", "description": "Use o planejador de build Mistfall Hunter para combinar classes com jogo solo, duo e esquadrao.", "h1": "Planejador de Build Mistfall Hunter", "kicker": "Classes de Mistfall Hunter"},
            "steam": {"title": "Mistfall Hunter no Steam", "description": "Informacoes do Mistfall Hunter no Steam: disponibilidade, plataforma, data, desenvolvedor, publicadora e links oficiais.", "h1": "Mistfall Hunter no Steam", "kicker": "Classes de Mistfall Hunter"},
            "about": {"title": "Sobre Classes de Mistfall Hunter", "description": "Como revisamos fontes publicas e mantemos recomendacoes de classes transparentes.", "h1": "Sobre Classes de Mistfall Hunter", "kicker": "Classes de Mistfall Hunter"},
            "contact": {"title": "Contato Classes de Mistfall Hunter", "description": "Envie correcoes, fontes, dados de classes e feedback do site.", "h1": "Contato", "kicker": "Classes de Mistfall Hunter"},
            "privacy-policy": {"title": "Politica de Privacidade", "description": "Politica de privacidade de Classes de Mistfall Hunter, guia fan-made e planejador de builds.", "h1": "Politica de Privacidade", "kicker": "Classes de Mistfall Hunter"},
            "terms-of-service": {"title": "Termos de Servico", "description": "Termos de servico e aviso de fan-site para Classes de Mistfall Hunter.", "h1": "Termos de Servico", "kicker": "Classes de Mistfall Hunter"},
        },
        "home": {"lede": "Escolha uma classe para rotas solo, pressao em duo ou extracao em esquadrao antes de gastar horas no ritmo errado. O planejador compara classes de Mistfall Hunter por estilo, risco, dano, controle e utilidade de equipe.", "actions": ["Usar planejador", "Ler guia de classes"], "facts": [["Tipo de jogo", "ARPG de extracao PvPvE"], ["Lancamento", "29 de julho de 2026"], ["Desenvolvedor", "Bellring Games"], ["Plataforma", "Windows no Steam"]], "classes_kicker": "Resumo de papeis", "classes_title": "Classes de Mistfall Hunter em resumo", "classes_desc": "Os perfis mostram quem deve jogar, o que a classe entrega e onde fica o risco.", "method_title": "Por que o planejador de classes Mistfall Hunter pesa esses papeis", "faq_title": "FAQ de classes Mistfall Hunter"},
    },
    "ko": {
        "site_name": "Mistfall Hunter 클래스", "brand": "Mistfall 클래스", "nav_aria": "기본 탐색", "footer_aria": "바닥글 탐색", "language_aria": "언어 선택", "steam_cta": "Steam",
        "nav": {"home": "플래너", "classes": "클래스", "build-planner": "빌드", "player-count": "플레이어 수", "steam": "Steam 정보", "contact": "문의"},
        "footer": {"about": "소개", "contact": "문의", "privacy-policy": "개인정보", "terms-of-service": "이용 약관", "sitemap": "사이트맵", "disclaimer": "Mistfall Hunter 팬 제작 클래스 가이드와 빌드 플래너입니다. Bellring Games, Skystone Games, Steam, Valve와 제휴하지 않습니다."},
        "pages": {
            "home": {"title": "Mistfall Hunter 클래스와 빌드", "description": "Mistfall Hunter 클래스를 비교하고 솔로와 파티 빌드를 계획하는 팬 제작 클래스 플래너입니다.", "h1": "Mistfall Hunter 클래스와 빌드", "kicker": "2026년 7월 업데이트 - Steam / PC - 팬 제작 도구"},
            "classes": {"title": "Mistfall Hunter 클래스 가이드", "description": "Mistfall Hunter 클래스의 역할, 강점, 위험도, 초보자 선택을 정리한 실전 가이드입니다.", "h1": "Mistfall Hunter 클래스 가이드", "kicker": "Mistfall Hunter 클래스"},
            "build-planner": {"title": "Mistfall Hunter 빌드 플래너", "description": "Mistfall Hunter 빌드 플래너로 솔로, 듀오, 파티 플레이 스타일에 맞는 클래스를 찾으세요.", "h1": "Mistfall Hunter 빌드 플래너", "kicker": "Mistfall Hunter 클래스"},
            "steam": {"title": "Mistfall Hunter Steam 정보", "description": "Mistfall Hunter Steam 출시 정보, 플랫폼, 출시일, 개발사, 배급사, 공식 링크를 확인합니다.", "h1": "Mistfall Hunter Steam 정보", "kicker": "Mistfall Hunter 클래스"},
            "about": {"title": "Mistfall Hunter 클래스 소개", "description": "공개 자료를 검토하고 클래스 추천을 투명하게 관리하는 방식을 설명합니다.", "h1": "Mistfall Hunter 클래스 소개", "kicker": "Mistfall Hunter 클래스"},
            "contact": {"title": "Mistfall Hunter 클래스 문의", "description": "수정 제안, 출처, 클래스 데이터, 사이트 의견을 보내는 페이지입니다.", "h1": "문의", "kicker": "Mistfall Hunter 클래스"},
            "privacy-policy": {"title": "개인정보 처리방침", "description": "팬 제작 Mistfall Hunter 클래스 가이드와 빌드 플래너의 개인정보 처리방침입니다.", "h1": "개인정보 처리방침", "kicker": "Mistfall Hunter 클래스"},
            "terms-of-service": {"title": "이용 약관", "description": "Mistfall Hunter 클래스의 이용 약관과 팬 사이트 면책 안내입니다.", "h1": "이용 약관", "kicker": "Mistfall Hunter 클래스"},
        },
        "home": {"lede": "솔로 루트, 듀오 압박, 파티 탈출에 맞는 클래스를 오래 시행착오하기 전에 정리하세요. 이 플래너는 Mistfall Hunter 클래스를 플레이 스타일, 위험도, 피해, 제어, 팀 유틸리티로 비교합니다.", "actions": ["플래너 사용", "클래스 가이드 읽기"], "facts": [["게임 유형", "PvPvE 탈출 ARPG"], ["출시일", "2026년 7월 29일"], ["개발사", "Bellring Games"], ["플랫폼", "Steam Windows"]], "classes_kicker": "역할 개요", "classes_title": "Mistfall Hunter 클래스 한눈에 보기", "classes_desc": "각 프로필은 누구에게 맞는지, 어떤 역할을 하는지, 위험이 어디에 있는지 실전 중심으로 정리합니다.", "method_title": "Mistfall Hunter 클래스 플래너의 역할 가중치", "faq_title": "Mistfall Hunter 클래스 FAQ"},
    },
    "it": {
        "site_name": "Classi Mistfall Hunter", "brand": "Mistfall Classi", "nav_aria": "Navigazione principale", "footer_aria": "Navigazione footer", "language_aria": "Scegli lingua", "steam_cta": "Steam",
        "nav": {"home": "Planner", "classes": "Classi", "build-planner": "Build", "player-count": "Giocatori", "steam": "Steam", "contact": "Contatto"},
        "footer": {"about": "Chi siamo", "contact": "Contatto", "privacy-policy": "Privacy", "terms-of-service": "Termini", "sitemap": "Mappa del sito", "disclaimer": "Guida e planner fan-made di Mistfall Hunter. Non affiliato a Bellring Games, Skystone Games, Steam o Valve."},
        "pages": {
            "home": {"title": "Classi Mistfall Hunter e Build", "description": "Confronta le classi Mistfall Hunter, pianifica build solo o squadra e usa un planner fan-made.", "h1": "Classi Mistfall Hunter e Build", "kicker": "Aggiornato a luglio 2026 - Steam / PC - strumento fan-made"},
            "classes": {"title": "Guida Classi Mistfall Hunter", "description": "Guida pratica alle classi Mistfall Hunter con ruoli, punti forti, rischio e scelte per principianti.", "h1": "Guida Classi Mistfall Hunter", "kicker": "Classi Mistfall Hunter"},
            "build-planner": {"title": "Planner Build Mistfall Hunter", "description": "Usa il planner build Mistfall Hunter per abbinare classi a gioco solo, duo e squadra.", "h1": "Planner Build Mistfall Hunter", "kicker": "Classi Mistfall Hunter"},
            "steam": {"title": "Informazioni Steam Mistfall Hunter", "description": "Informazioni Steam su Mistfall Hunter: disponibilita, piattaforma, data, sviluppatore, editore e link ufficiali.", "h1": "Informazioni Steam Mistfall Hunter", "kicker": "Classi Mistfall Hunter"},
            "about": {"title": "Informazioni su Classi Mistfall Hunter", "description": "Come il sito controlla fonti pubbliche e mantiene trasparenti le raccomandazioni.", "h1": "Informazioni su Classi Mistfall Hunter", "kicker": "Classi Mistfall Hunter"},
            "contact": {"title": "Contatto Classi Mistfall Hunter", "description": "Invia correzioni, fonti, dati sulle classi e feedback sul sito.", "h1": "Contatto", "kicker": "Classi Mistfall Hunter"},
            "privacy-policy": {"title": "Informativa Privacy", "description": "Informativa privacy di Classi Mistfall Hunter, guida fan-made e planner build.", "h1": "Informativa Privacy", "kicker": "Classi Mistfall Hunter"},
            "terms-of-service": {"title": "Termini di Servizio", "description": "Termini di servizio e avviso fan-site per Classi Mistfall Hunter.", "h1": "Termini di Servizio", "kicker": "Classi Mistfall Hunter"},
        },
        "home": {"lede": "Scegli una classe per run solo, pressione in duo o estrazione di squadra prima di perdere ore con un ritmo sbagliato. Il planner confronta le classi Mistfall Hunter per stile, rischio, danno, controllo e utilita di gruppo.", "actions": ["Usa il planner", "Leggi la guida"], "facts": [["Tipo di gioco", "ARPG extraction PvPvE"], ["Uscita", "29 luglio 2026"], ["Sviluppatore", "Bellring Games"], ["Piattaforma", "Windows su Steam"]], "classes_kicker": "Panoramica ruoli", "classes_title": "Classi Mistfall Hunter in sintesi", "classes_desc": "I profili spiegano chi dovrebbe usare la classe, cosa offre al gruppo e dove si trova il rischio.", "method_title": "Perche il planner classi Mistfall Hunter pesa cosi i ruoli", "faq_title": "FAQ classi Mistfall Hunter"},
    },
}


def deep_merge(base, override):
    """
    递归合并两组语言数据。

    :param base: 基础语言数据字典
    :param override: 需要覆盖或补充的语言数据字典
    :return: dict，合并后的新语言数据
    """
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


for locale, override in LOCALE_OVERRIDES.items():
    TEXT[locale] = deep_merge(TEXT["en"], override)

LOCALIZED_BLOCKS = {
    "es": {
        "classes": {
            "risk": {"low": "Riesgo bajo", "medium": "Riesgo medio", "high": "Riesgo alto"},
            "metrics": {"solo": "Solo", "squad": "Escuadrón", "burst": "Ráfaga", "control": "Control"},
            "roles": {
                "mercenary": ["Luchador de primera línea", "Jugadores que quieren presión cuerpo a cuerpo clara y extracciones estables."],
                "blackarrow": ["Presión a distancia", "Jugadores pacientes que prefieren explorar, desgastar y elegir peleas."],
                "shadowstrix": ["Asesino móvil", "Jugadores de alta movilidad que buscan emboscadas, flancos y salidas rápidas."],
                "sorcerer": ["Mago de daño en área", "Jugadores que quieren ráfaga mágica, presión de zona e impacto grupal."],
                "seer": ["Apoyo e información", "Escuadrones que valoran rastreo, utilidad y decisiones de extracción más seguras."],
                "withered-knight": ["Iniciador resistente", "Jugadores que quieren ocupar espacio, aguantar intercambios y proteger aliados."],
            },
        },
        "planner": {
            "kicker": "Selector interactivo de clases", "title": "Planificador de clases Mistfall Hunter", "description": "Responde cuatro preguntas y la herramienta ordena las clases para tu partida. Es un modelo fan-made, no una tier list oficial.",
            "labels": {"format": "Formato de partida", "style": "Ritmo de combate", "risk": "Tolerancia al riesgo", "experience": "Experiencia"},
            "options": {"format": {"solo": "Extracción solo", "duo": "Escaramuza en dúo", "squad": "Juego en escuadrón"}, "style": {"balanced": "Supervivencia equilibrada", "burst": "Daño de ráfaga", "control": "Control y utilidad", "frontline": "Presión frontal"}, "risk": {"low": "Riesgo bajo", "medium": "Riesgo medio", "high": "Riesgo alto"}, "experience": {"new": "Jugador nuevo", "returning": "Jugador ARPG con experiencia", "advanced": "Jugador avanzado de extracción"}},
            "submit": "Encontrar mi clase", "reset": "Restablecer", "empty": "Tu recomendación aparecerá aquí. Prueba primero la configuración solo por defecto si tienes dudas.", "short_empty": "Elige ajustes para generar una dirección de build.", "calculating": "Calculando ajuste de clase...", "recommended": "Clase recomendada", "fit": "{name} encaja con tu ruta {format} porque el modelo equilibra rol, ritmo de combate, riesgo y experiencia.", "score_label": "{score} de 100", "score_text": "{score}/100 - {role}", "note": "Nota del modelo: es una recomendación fan-made y debe revisarse cuando cambie el balance verificado."},
        "home": {"media_alt": "Arte oficial de Steam de Mistfall Hunter, ARPG oscuro de extracción", "media_caption": "Medio oficial de Steam procesado para esta guía fan-made.", "steps_kicker": "Cómo usar el resultado", "steps_title": "Convierte una recomendación en una build jugable", "steps": ["Elige primero el rol de clase; sobrevivir y leer información importa tanto como el daño.", "Ajusta el equipo al trabajo: frente necesita aguante, ráfaga necesita ventanas limpias y apoyo necesita posición segura.", "Revisa después de parches porque valores, talentos y equipo pueden cambiar rápido."], "source_title": "Política de fuentes", "source_text": "Los datos de plataforma y lanzamiento vienen de Steam oficial. Las recomendaciones de clase son un modelo editorial fan-made.", "source_link": "Abrir página oficial de Steam", "method_kicker": "Método del planificador", "method_paragraphs": ["El planificador empieza con una pregunta práctica: qué clase ayuda a sobrevivir, ganar una pelea o apoyar la extracción.", "El ritmo de combate cambia la puntuación. Ráfaga favorece a Shadowstrix y Sorcerer; control sube a Seer, Sorcerer y Withered Knight.", "La tolerancia al riesgo evita recomendar clases frágiles a jugadores que piden una ruta segura."], "method_card_title": "Entradas usadas", "method_items": ["Formato: solo, dúo o escuadrón.", "Ritmo: equilibrio, ráfaga, control o frente.", "Riesgo: bajo, medio o alto.", "Experiencia: nuevo, recurrente o avanzado."], "output_title": "Salida de la herramienta", "output_text": "Recibes una clase principal, explicación de rol y alternativas con barras de puntuación.", "comparison_kicker": "Tabla de decisión", "comparison_title": "Mejor clase por necesidad", "comparison_headers": ["Necesidad", "Mejor inicio", "Por qué encaja"], "comparison_rows": [["Primera extracción solo", "Mercenary", "Perfil frontal permisivo y baja carga de planificación."], ["Utilidad de escuadrón", "Seer", "Información y control ayudan a elegir peleas seguras."], ["Jugadas de ráfaga", "Shadowstrix o Sorcerer", "Premian el tiempo correcto, pero castigan mala posición."], ["Rol ancla", "Withered Knight", "Durabilidad y control de espacio para grupos coordinados."]], "examples_kicker": "Ejemplos", "examples_title": "Ejemplos de elección de clase", "examples": ["Jugador nuevo solo: solo, equilibrado, riesgo bajo y nuevo suele orientar a Mercenary.", "Escuadrón coordinado: escuadrón, control, riesgo medio y experiencia ARPG sube a Seer o Withered Knight.", "Dúo agresivo PvP: dúo, ráfaga, riesgo alto y avanzado puede favorecer Shadowstrix o Sorcerer."], "caution_title": "Cuándo no seguir el resultado a ciegas", "caution": ["No lo trates como definitivo si un parche cambia habilidades o escalado.", "Usa el planner, lee la guía y prueba en juego con tu equipo.", "Si dos clases quedan cerca, elige el rol que falta en tu grupo."], "update_title": "Política de actualización", "update_text": "Como Mistfall Hunter es reciente, la guía debe revisarse cuando notas oficiales o evidencias repetidas contradigan el modelo.", "faq": [["¿Cuál es la mejor clase para principiantes?", "Mercenary es el punto de partida más seguro; Withered Knight también ayuda en escuadrones."], ["¿Shadowstrix sirve para solo?", "Sí, si entiendes ventanas de emboscada y retirada; es menos permisiva que Mercenary."], ["¿Un escuadrón siempre necesita Seer?", "No siempre, pero Seer aporta información cuando el grupo necesita decisiones más seguras."], ["¿Qué tan preciso es el planner?", "Es un modelo práctico fan-made y debe actualizarse con datos verificados."], ["¿Mistfall Hunter tiene códigos?", "Esta página prioriza clases y builds; si hay códigos oficiales útiles, conviene crear una página separada."]]},
        "simple": {"classes_title": "Cómo comparar clases de Mistfall Hunter", "classes_paragraphs": ["Las clases de Mistfall Hunter se comparan mejor por trabajo de la partida, no por una lista universal.", "Mercenary y Withered Knight son rutas seguras; Blackarrow aporta rango; Shadowstrix y Sorcerer premian timing; Seer brilla en grupo."], "build_paragraphs": ["El planificador convierte formato, ritmo, riesgo y experiencia en una dirección de build.", "Si dos resultados están cerca, úsalo como empate y cubre el rol que falta en tu equipo."], "steam_paragraphs": ["Usa Steam oficial para precio, instalación, requisitos, reseñas y anuncios actuales.", "Esta web no ofrece descargas, keys ni mirrors no oficiales."], "about": ["Este sitio fan-made ayuda a comparar clases antes de comprometer una build.", "Separamos datos oficiales de Steam de recomendaciones editoriales y aceptamos correcciones con fuentes."], "contact": [f"Envía correcciones a {SUPPORT_EMAIL}.", "Incluye URL, idioma y fuente para revisar el cambio."], "privacy": ["El planner funciona en tu navegador y no requiere cuenta.", "Si se agregan analíticas o anuncios, deben usarse con configuración real y transparente."], "terms": ["Este sitio no está afiliado con los propietarios de Mistfall Hunter, Steam o Valve.", "Las recomendaciones son orientación editorial y pueden quedar desactualizadas tras cambios de balance."]},
    },
    "ja": {
        "classes": {"risk": {"low": "低リスク", "medium": "中リスク", "high": "高リスク"}, "metrics": {"solo": "ソロ", "squad": "分隊", "burst": "瞬間火力", "control": "制御"}, "roles": {"mercenary": ["前線の近接役", "安定した近接圧力と安全な脱出を重視するプレイヤー向け。"], "blackarrow": ["遠距離圧力", "偵察、牽制、有利な戦闘選択を好む慎重なプレイヤー向け。"], "shadowstrix": ["奇襲型スカーミッシャー", "待ち伏せ、側面攻撃、素早い離脱を好む高機動プレイヤー向け。"], "sorcerer": ["範囲火力キャスター", "魔法の瞬間火力、ゾーン支配、集団戦の影響力を求める人向け。"], "seer": ["支援と情報", "追跡、補助、安全な脱出判断を重視する分隊向け。"], "withered-knight": ["耐久型イニシエーター", "場所を押さえ、取引に耐え、味方を守りたい人向け。"]}},
        "planner": {"kicker": "インタラクティブなクラス選択", "title": "Mistfall Hunter クラスプランナー", "description": "4つの質問に答えると、プレイ方針に合うクラスを順位付けします。公式ティアリストではなく、出発点として使うファン作成モデルです。", "labels": {"format": "ラン形式", "style": "戦闘テンポ", "risk": "リスク許容度", "experience": "経験"}, "options": {"format": {"solo": "ソロ脱出", "duo": "デュオ戦闘", "squad": "分隊プレイ"}, "style": {"balanced": "安定重視", "burst": "瞬間火力", "control": "制御と補助", "frontline": "前線圧力"}, "risk": {"low": "低リスク", "medium": "中リスク", "high": "高リスク"}, "experience": {"new": "新規プレイヤー", "returning": "ARPG経験者", "advanced": "上級脱出プレイヤー"}}, "submit": "おすすめを出す", "reset": "リセット", "empty": "ここにおすすめが表示されます。迷う場合は標準のソロ設定から試してください。", "short_empty": "設定を選ぶとビルド方針が表示されます。", "calculating": "相性を計算中...", "recommended": "おすすめクラス", "fit": "{name} は {format} に合います。モデルは役割、戦闘テンポ、リスク、経験を合わせて評価します。", "score_label": "{score} / 100", "score_text": "{score}/100 - {role}", "note": "注: ファン作成の推薦です。バランス変更や検証済みデータが出たら見直してください。"},
        "home": {"media_alt": "Mistfall Hunter のSteam公式ヒーローアート", "media_caption": "Steam公式ストア素材をこのファンガイド向けに処理しました。", "steps_kicker": "結果の使い方", "steps_title": "おすすめを実戦ビルドに変える", "steps": ["まずクラスの役割を決めます。脱出判断では生存力と情報も火力と同じくらい重要です。", "装備を役割に合わせます。前線は耐久、瞬間火力はきれいな開始、支援は安全な位置取りが必要です。", "パッチ後に見直します。スキル値、才能、装備環境は早く変わる可能性があります。"], "source_title": "情報源ポリシー", "source_text": "プラットフォームと発売情報はSteam公式に基づきます。クラス推薦は透明なファン編集モデルです。", "source_link": "Steam公式ページを開く", "method_kicker": "計算方法", "method_paragraphs": ["プランナーは、このクラスが生存、戦闘、分隊判断を助けるかという実用的な質問から始めます。", "瞬間火力は Shadowstrix と Sorcerer を押し上げ、制御は Seer、Sorcerer、Withered Knight を高くします。", "リスク許容度は、初心者に扱いづらい高リスククラスを出しすぎないための補正です。"], "method_card_title": "使用する入力", "method_items": ["ラン形式: ソロ、デュオ、分隊。", "戦闘テンポ: 安定、瞬間火力、制御、前線。", "リスク: 低、中、高。", "経験: 新規、復帰、上級。"], "output_title": "表示される結果", "output_text": "最上位のおすすめ、役割説明、スコアバー付きの代替候補を表示します。", "comparison_kicker": "判断表", "comparison_title": "目的別おすすめクラス", "comparison_headers": ["目的", "最初の候補", "合う理由"], "comparison_rows": [["初めてのソロ脱出", "Mercenary", "前線役として扱いやすく、判断負荷が低い。"], ["分隊の補助", "Seer", "情報と制御で安全な戦闘選択を助ける。"], ["高い瞬間火力", "Shadowstrix または Sorcerer", "タイミングを要求するが爆発力がある。"], ["アンカー役", "Withered Knight", "耐久と空間制御で味方を支える。"]], "examples_kicker": "例", "examples_title": "クラス選択の例", "examples": ["新規ソロなら、ソロ、安定、低リスク、新規を選ぶと Mercenary が上がりやすいです。", "連携分隊なら、分隊、制御、中リスク、ARPG経験者で Seer や Withered Knight が上がります。", "攻撃的なデュオなら、デュオ、瞬間火力、高リスク、上級で Shadowstrix や Sorcerer が候補になります。"], "caution_title": "結果を盲信しない場面", "caution": ["パッチでスキルや装備倍率が変わった場合は最終判断にしないでください。", "プランナー、クラスガイド、ゲーム内テストの順で確認するのが安全です。", "差が小さい場合は同点として、分隊に足りない役割を選びます。"], "update_title": "更新方針", "update_text": "Mistfall Hunter は新しいため、公式パッチや繰り返し確認できるプレイ証拠が出たら見直します。", "faq": [["初心者におすすめのクラスは？", "Mercenary が最も安全な初期候補です。分隊なら Withered Knight も扱いやすいです。"], ["Shadowstrix はソロ向きですか？", "奇襲と離脱を理解していれば強いですが、Mercenary より失敗の許容度は低いです。"], ["分隊に Seer は必須ですか？", "必須ではありませんが、情報と補助が必要な分隊では大きな価値があります。"], ["プランナーはどれくらい正確ですか？", "役割適性のファン作成モデルです。検証済みデータやパッチで更新してください。"], ["Mistfall Hunter にコードはありますか？", "このサイトはクラスとビルドを優先します。公式コード需要が強ければ別ページで扱うべきです。"]]},
        "simple": {"classes_title": "Mistfall Hunter クラスの比較方法", "classes_paragraphs": ["Mistfall Hunter クラスは万能ランキングではなく、ランで必要な役割ごとに比較するのが実用的です。", "Mercenary と Withered Knight は安全、Blackarrow は距離、Shadowstrix と Sorcerer はタイミング、Seer は分隊支援に向きます。"], "build_paragraphs": ["ビルドプランナーは形式、テンポ、リスク、経験を使って方向性を出します。", "結果が近い場合は同点として、分隊に不足している役割を選んでください。"], "steam_paragraphs": ["価格、インストール、必要環境、レビュー、告知はSteam公式で確認してください。", "このサイトはダウンロード、キー販売、非公式ミラーを提供しません。"], "about": ["このファンサイトは、ビルドを決める前にクラスを比較するためのものです。", "Steam公式情報と編集上のおすすめを分け、出典つきの修正を歓迎します。"], "contact": [f"修正提案は {SUPPORT_EMAIL} に送ってください。", "URL、言語、確認したい出典を含めてください。"], "privacy": ["プランナーはブラウザ内で動作し、アカウントは不要です。", "将来分析や広告を入れる場合は、実際の設定と透明な説明が必要です。"], "terms": ["このサイトは Mistfall Hunter、Steam、Valve の権利者と提携していません。", "おすすめは編集上のガイドであり、バランス変更後は古くなる可能性があります。"]},
    },
    "fr": {
        "classes": {"risk": {"low": "Risque faible", "medium": "Risque moyen", "high": "Risque élevé"}, "metrics": {"solo": "Solo", "squad": "Escouade", "burst": "Burst", "control": "Contrôle"}, "roles": {"mercenary": ["Combattant de première ligne", "Pour jouer une pression melee lisible et des extractions plus stables."], "blackarrow": ["Pression à distance", "Pour scout, poke et choisir les combats avec prudence."], "shadowstrix": ["Assassin mobile", "Pour embuscades, flancs et désengagements rapides."], "sorcerer": ["Lanceur de dégâts de zone", "Pour burst magique, pression de zone et impact en combat groupé."], "seer": ["Soutien et information", "Pour équipes qui valorisent suivi, utilité et appels d extraction sûrs."], "withered-knight": ["Initiateur durable", "Pour tenir l espace, survivre aux échanges et protéger les alliés."]}},
        "planner": {"kicker": "Sélecteur interactif", "title": "Planificateur de classes Mistfall Hunter", "description": "Répondez à quatre questions et l outil classe les options pour votre run. C est un modèle fan-made, pas une tier list officielle.", "labels": {"format": "Format du run", "style": "Rythme de combat", "risk": "Tolérance au risque", "experience": "Expérience"}, "options": {"format": {"solo": "Extraction solo", "duo": "Duel en duo", "squad": "Jeu en escouade"}, "style": {"balanced": "Survie équilibrée", "burst": "Dégâts burst", "control": "Contrôle et utilité", "frontline": "Pression de front"}, "risk": {"low": "Risque faible", "medium": "Risque moyen", "high": "Risque élevé"}, "experience": {"new": "Nouveau joueur", "returning": "Joueur ARPG habitué", "advanced": "Joueur extraction avancé"}}, "submit": "Trouver ma classe", "reset": "Réinitialiser", "empty": "Votre recommandation apparaîtra ici. Essayez le profil solo par défaut si vous hésitez.", "short_empty": "Choisissez vos réglages pour générer une direction de build.", "calculating": "Calcul de l adéquation...", "recommended": "Classe recommandée", "fit": "{name} correspond à votre run {format} car le modèle combine rôle, rythme, risque et expérience.", "score_label": "{score} sur 100", "score_text": "{score}/100 - {role}", "note": "Note: recommandation fan-made à revoir quand des données de balance vérifiées changent."},
        "home": {"media_alt": "Illustration Steam officielle de Mistfall Hunter", "media_caption": "Média officiel Steam traité pour ce guide fan-made.", "steps_kicker": "Utiliser le résultat", "steps_title": "Transformer la recommandation en build jouable", "steps": ["Choisissez d abord le rôle: survie et information comptent autant que les dégâts.", "Adaptez l équipement: front pour l endurance, burst pour les fenêtres propres, soutien pour le placement.", "Revérifiez après les patchs, car compétences, talents et équipement peuvent changer."], "source_title": "Politique des sources", "source_text": "Les faits de plateforme viennent de Steam officiel. Les recommandations sont un modèle éditorial transparent.", "source_link": "Ouvrir la page Steam officielle", "method_kicker": "Méthode", "method_paragraphs": ["Le planificateur part de la question pratique: survivre, gagner un échange ou soutenir l extraction.", "Le burst favorise Shadowstrix et Sorcerer; le contrôle met en avant Seer, Sorcerer et Withered Knight.", "La tolérance au risque évite de pousser une classe fragile à un joueur cherchant une route sûre."], "method_card_title": "Entrées utilisées", "method_items": ["Format: solo, duo ou escouade.", "Rythme: équilibre, burst, contrôle ou front.", "Risque: faible, moyen ou élevé.", "Expérience: nouveau, habitué ou avancé."], "output_title": "Résultat obtenu", "output_text": "Une classe principale, une explication de rôle et des alternatives avec barres de score.", "comparison_kicker": "Table de décision", "comparison_title": "Meilleure classe selon le besoin", "comparison_headers": ["Besoin", "Premier choix", "Pourquoi"], "comparison_rows": [["Première extraction solo", "Mercenary", "Profil frontal permissif et charge de décision faible."], ["Utilité d escouade", "Seer", "Information et contrôle rendent les combats plus sûrs."], ["Jeu burst", "Shadowstrix ou Sorcerer", "Récompense le timing mais punit le mauvais placement."], ["Rôle d ancre", "Withered Knight", "Durabilité et contrôle d espace pour groupes coordonnés."]], "examples_kicker": "Exemples", "examples_title": "Exemples de choix", "examples": ["Nouveau solo: solo, équilibré, risque faible et nouveau mène souvent à Mercenary.", "Escouade coordonnée: escouade, contrôle, risque moyen et habitué fait monter Seer ou Withered Knight.", "Duo agressif: duo, burst, risque élevé et avancé peut favoriser Shadowstrix ou Sorcerer."], "caution_title": "Quand ne pas suivre aveuglément", "caution": ["Ne l utilisez pas comme vérité finale après un patch majeur.", "Planificateur, guide, puis test en jeu reste le flux le plus sûr.", "Si deux scores sont proches, choisissez le rôle manquant."], "update_title": "Politique de mise à jour", "update_text": "Le guide doit évoluer quand des notes officielles ou preuves de gameplay répétées contredisent le modèle.", "faq": [["Quelle classe pour débuter?", "Mercenary est le choix le plus sûr; Withered Knight convient aussi en escouade."], ["Shadowstrix est-elle bonne en solo?", "Oui avec de bons timings d embuscade et de fuite, mais elle pardonne moins."], ["Faut-il toujours un Seer?", "Non, mais Seer apporte beaucoup quand l équipe manque d information."], ["Le planificateur est-il précis?", "C est un modèle fan-made pratique qui doit suivre les données vérifiées."], ["Y a-t-il des codes Mistfall Hunter?", "Cette page traite les classes et builds; des codes officiels utiles mériteraient une page séparée."]]},
        "simple": {"classes_title": "Comparer les classes Mistfall Hunter", "classes_paragraphs": ["Comparez les classes par rôle de run plutôt que par classement universel.", "Mercenary et Withered Knight sont sûrs; Blackarrow apporte la portée; Shadowstrix et Sorcerer demandent du timing; Seer sert l escouade."], "build_paragraphs": ["Le planificateur transforme format, rythme, risque et expérience en direction de build.", "Si les scores sont proches, traitez le résultat comme une égalité et couvrez le rôle manquant."], "steam_paragraphs": ["Vérifiez prix, installation, exigences et annonces sur Steam officiel.", "Ce site ne fournit ni téléchargement, ni clé, ni miroir non officiel."], "about": ["Ce site fan-made aide à comparer les classes avant de choisir un build.", "Nous séparons faits Steam et recommandations éditoriales, avec corrections sourcées."], "contact": [f"Envoyez les corrections à {SUPPORT_EMAIL}.", "Ajoutez URL, langue et source à vérifier."], "privacy": ["Le planner fonctionne dans votre navigateur sans compte.", "Toute future analyse ou publicité devra utiliser une configuration réelle et transparente."], "terms": ["Ce site n est pas affilié aux ayants droit de Mistfall Hunter, Steam ou Valve.", "Les recommandations sont éditoriales et peuvent changer après équilibrage."]},
    },
}

for locale, block in LOCALIZED_BLOCKS.items():
    TEXT[locale] = deep_merge(TEXT[locale], block)

COMPACT_LOCALE_BLOCKS = {
    "de": {
        "classes": {"risk": {"low": "Niedriges Risiko", "medium": "Mittleres Risiko", "high": "Hohes Risiko"}, "metrics": {"solo": "Solo", "squad": "Gruppe", "burst": "Burst", "control": "Kontrolle"}, "roles": {"mercenary": ["Frontkämpfer", "Für Spieler, die verlässlichen Nahkampfdruck und stabile Extraktionen wollen."], "blackarrow": ["Fernkampfdruck", "Für vorsichtige Spieler, die scouten, poken und Kämpfe auswählen."], "shadowstrix": ["Mobiler Assassine", "Für Hinterhalte, Flanken und schnelle Rückzüge."], "sorcerer": ["Flächenschaden-Zauberer", "Für Zauber-Burst, Zonendruck und Wirkung in Gruppenkämpfen."], "seer": ["Unterstützung und Information", "Für Gruppen, die Tracking, Nutzen und sichere Extraktionsentscheidungen brauchen."], "withered-knight": ["Robuster Initiator", "Für Spieler, die Raum halten, Trades überleben und Verbündete schützen."]}},
        "planner": {"kicker": "Interaktiver Klassenwähler", "title": "Mistfall Hunter Klassenplaner", "description": "Beantworte vier Fragen und der Planer sortiert Klassen für deinen Run. Das ist ein Fan-Modell, keine offizielle Tier List.", "labels": {"format": "Run-Format", "style": "Kampfrhythmus", "risk": "Risikotoleranz", "experience": "Erfahrung"}, "options": {"format": {"solo": "Solo-Extraktion", "duo": "Duo-Gefecht", "squad": "Gruppenspiel"}, "style": {"balanced": "Ausgewogen überleben", "burst": "Burst-Schaden", "control": "Kontrolle und Nutzen", "frontline": "Frontdruck"}, "risk": {"low": "Niedrig", "medium": "Mittel", "high": "Hoch"}, "experience": {"new": "Neuer Spieler", "returning": "ARPG-Erfahrung", "advanced": "Fortgeschrittener Extraction-Spieler"}}, "submit": "Klasse finden", "reset": "Zurücksetzen", "empty": "Deine Empfehlung erscheint hier. Nutze bei Unsicherheit zuerst das Solo-Standardprofil.", "short_empty": "Wähle Werte, um eine Build-Richtung zu erhalten.", "calculating": "Klassenpassung wird berechnet...", "recommended": "Empfohlene Klasse", "fit": "{name} passt zu deinem {format}-Run, weil Rolle, Rhythmus, Risiko und Erfahrung zusammen bewertet werden.", "score_label": "{score} von 100", "score_text": "{score}/100 - {role}", "note": "Hinweis: Fan-Empfehlung, die bei verifizierten Balanceänderungen geprüft werden sollte."},
        "home": {"media_alt": "Offizielle Steam-Grafik zu Mistfall Hunter", "media_caption": "Offizielles Steam-Material, für diesen Fan-Guide verarbeitet.", "steps_kicker": "Ergebnis nutzen", "steps_title": "Aus der Empfehlung einen spielbaren Build machen", "steps": ["Wähle zuerst die Rolle; Überleben und Information zählen so viel wie Schaden.", "Passe Ausrüstung an: Front braucht Standfestigkeit, Burst braucht klare Fenster, Support braucht sichere Position.", "Prüfe nach Patches erneut, weil Werte, Talente und Ausrüstung wechseln können."], "source_title": "Quellenpolitik", "source_text": "Plattform- und Release-Fakten stammen von Steam. Klassentipps sind ein transparentes Fan-Modell.", "source_link": "Offizielle Steam-Seite öffnen", "method_kicker": "Planer-Methode", "method_paragraphs": ["Der Planer fragt, ob eine Klasse Überleben, Kampfgewinn oder Gruppenentscheidung verbessert.", "Burst hebt Shadowstrix und Sorcerer; Kontrolle hebt Seer, Sorcerer und Withered Knight.", "Risikotoleranz verhindert, dass fragile Klassen Spielern mit sicherem Profil empfohlen werden."], "method_card_title": "Genutzte Eingaben", "method_items": ["Format: Solo, Duo oder Gruppe.", "Rhythmus: ausgewogen, Burst, Kontrolle oder Front.", "Risiko: niedrig, mittel oder hoch.", "Erfahrung: neu, erfahren oder fortgeschritten."], "output_title": "Ausgabe", "output_text": "Du erhältst eine Top-Klasse, Rollenbegründung und Alternativen mit Balken.", "comparison_kicker": "Entscheidungstabelle", "comparison_title": "Beste Klasse nach Bedarf", "comparison_headers": ["Bedarf", "Startwahl", "Warum"], "comparison_rows": [["Erste Solo-Extraktion", "Mercenary", "Verzeihender Frontstil mit weniger Planungsdruck."], ["Gruppennutzen", "Seer", "Information und Kontrolle machen Kämpfe sicherer."], ["Burst-Spiel", "Shadowstrix oder Sorcerer", "Belohnt Timing, bestraft aber schlechte Position."], ["Ankerrolle", "Withered Knight", "Hält Raum und schützt koordinierte Gruppen."]], "examples_kicker": "Beispiele", "examples_title": "Beispielhafte Klassenwahl", "examples": ["Neuer Solo-Spieler: Solo, ausgewogen, niedriges Risiko und neu führt oft zu Mercenary.", "Koordinierte Gruppe: Gruppe, Kontrolle, mittleres Risiko und ARPG-Erfahrung hebt Seer oder Withered Knight.", "Aggressives Duo: Duo, Burst, hohes Risiko und fortgeschritten kann Shadowstrix oder Sorcerer bevorzugen."], "caution_title": "Wann das Ergebnis nicht blind gilt", "caution": ["Nach großen Patches nicht als endgültig behandeln.", "Planer, Guide und Ingame-Test bleiben der sichere Ablauf.", "Bei engen Scores zählt die fehlende Gruppenrolle."], "update_title": "Update-Regel", "update_text": "Der Guide wird angepasst, wenn offizielle Notizen oder wiederholte Gameplay-Belege das Modell widerlegen.", "faq": [["Welche Klasse ist gut für Anfänger?", "Mercenary ist der sicherste Start; Withered Knight passt gut in Gruppen."], ["Ist Shadowstrix solo gut?", "Ja, wenn Hinterhalt und Rückzug sitzen, aber Fehler werden stärker bestraft."], ["Braucht jede Gruppe Seer?", "Nein, aber Seer ist stark, wenn Information fehlt."], ["Wie genau ist der Planer?", "Es ist ein praktisches Fan-Modell und muss mit Daten aktualisiert werden."], ["Gibt es Mistfall Hunter Codes?", "Diese Seite priorisiert Klassen und Builds; sinnvolle offizielle Codes gehören auf eine eigene Seite."]]},
        "simple": {"classes_title": "Mistfall Hunter Klassen vergleichen", "classes_paragraphs": ["Vergleiche Klassen nach Run-Aufgabe statt nach universeller Rangliste.", "Mercenary und Withered Knight sind sicher; Blackarrow liefert Reichweite; Shadowstrix und Sorcerer brauchen Timing; Seer hilft Gruppen."], "build_paragraphs": ["Der Planer macht aus Format, Rhythmus, Risiko und Erfahrung eine Build-Richtung.", "Bei engen Ergebnissen zählt die Rolle, die deiner Gruppe fehlt."], "steam_paragraphs": ["Preis, Installation, Anforderungen und Ankündigungen bitte auf Steam prüfen.", "Diese Seite bietet keine Downloads, Keys oder inoffiziellen Mirrors."], "about": ["Diese Fan-Seite hilft beim Klassenvergleich vor dem Build.", "Steam-Fakten und redaktionelle Empfehlungen werden getrennt."], "contact": [f"Korrekturen an {SUPPORT_EMAIL} senden.", "Bitte URL, Sprache und Quelle angeben."], "privacy": ["Der Planer läuft im Browser und braucht kein Konto.", "Analyse oder Werbung muss später transparent konfiguriert werden."], "terms": ["Diese Seite ist nicht mit Mistfall Hunter, Steam oder Valve verbunden.", "Empfehlungen sind redaktionell und können nach Balanceänderungen veralten."]},
    },
    "pt": {
        "classes": {"risk": {"low": "Risco baixo", "medium": "Risco médio", "high": "Risco alto"}, "metrics": {"solo": "Solo", "squad": "Esquadrão", "burst": "Explosão", "control": "Controle"}, "roles": {"mercenary": ["Lutador de linha de frente", "Para quem quer pressão corpo a corpo perdoável e extrações estáveis."], "blackarrow": ["Pressão à distância", "Para jogadores cuidadosos que preferem observar, cutucar e escolher lutas."], "shadowstrix": ["Assassino móvel", "Para emboscadas, flancos e recuos rápidos."], "sorcerer": ["Conjurador de área", "Para explosão mágica, pressão de zona e impacto em grupo."], "seer": ["Suporte e informação", "Para esquadrões que valorizam rastreio, utilidade e decisões seguras."], "withered-knight": ["Iniciador resistente", "Para segurar espaço, sobreviver trocas e proteger aliados."]}},
        "planner": {"kicker": "Seletor interativo", "title": "Planejador de classes Mistfall Hunter", "description": "Responda quatro perguntas e a ferramenta ordena as classes para sua run. É um modelo fan-made, não uma tier list oficial.", "labels": {"format": "Formato da run", "style": "Ritmo de combate", "risk": "Tolerância a risco", "experience": "Experiência"}, "options": {"format": {"solo": "Extração solo", "duo": "Escaramuça em dupla", "squad": "Jogo em esquadrão"}, "style": {"balanced": "Sobrevivência equilibrada", "burst": "Dano explosivo", "control": "Controle e utilidade", "frontline": "Pressão frontal"}, "risk": {"low": "Risco baixo", "medium": "Risco médio", "high": "Risco alto"}, "experience": {"new": "Jogador novo", "returning": "Jogador de ARPG", "advanced": "Jogador avançado de extração"}}, "submit": "Encontrar classe", "reset": "Redefinir", "empty": "Sua recomendação aparecerá aqui. Se estiver em dúvida, teste o solo padrão.", "short_empty": "Escolha ajustes para gerar uma direção de build.", "calculating": "Calculando encaixe...", "recommended": "Classe recomendada", "fit": "{name} combina com sua run {format} porque o modelo equilibra papel, ritmo, risco e experiência.", "score_label": "{score} de 100", "score_text": "{score}/100 - {role}", "note": "Nota: recomendação fan-made que deve ser revisada quando o balanceamento mudar."},
        "home": {"media_alt": "Arte oficial de Steam de Mistfall Hunter", "media_caption": "Mídia oficial do Steam processada para este guia fan-made.", "steps_kicker": "Como usar o resultado", "steps_title": "Transforme a recomendação em build jogável", "steps": ["Escolha primeiro o papel; sobrevivência e informação importam tanto quanto dano.", "Ajuste equipamentos: frente precisa aguentar, burst precisa janela limpa e suporte precisa posição segura.", "Revise depois de patches, pois valores e equipamentos mudam rápido."], "source_title": "Política de fontes", "source_text": "Fatos de plataforma vêm do Steam oficial. Recomendações são um modelo editorial transparente.", "source_link": "Abrir página oficial no Steam", "method_kicker": "Método", "method_paragraphs": ["O planejador pergunta se a classe ajuda a sobreviver, vencer troca ou apoiar extração.", "Burst favorece Shadowstrix e Sorcerer; controle favorece Seer, Sorcerer e Withered Knight.", "Tolerância a risco evita indicar classes frágeis para perfis que pedem segurança."], "method_card_title": "Entradas usadas", "method_items": ["Formato: solo, dupla ou esquadrão.", "Ritmo: equilibrado, explosão, controle ou frente.", "Risco: baixo, médio ou alto.", "Experiência: novo, retornando ou avançado."], "output_title": "Resultado", "output_text": "Uma classe principal, explicação de papel e alternativas com barras de pontuação.", "comparison_kicker": "Tabela de decisão", "comparison_title": "Melhor classe por necessidade", "comparison_headers": ["Necessidade", "Melhor início", "Por quê"], "comparison_rows": [["Primeira extração solo", "Mercenary", "Perfil frontal permissivo e baixa carga de planejamento."], ["Utilidade em esquadrão", "Seer", "Informação e controle ajudam decisões seguras."], ["Jogadas explosivas", "Shadowstrix ou Sorcerer", "Premiam tempo certo, mas punem posição ruim."], ["Papel âncora", "Withered Knight", "Durabilidade e controle para grupos coordenados."]], "examples_kicker": "Exemplos", "examples_title": "Exemplos de escolha", "examples": ["Novo solo: solo, equilibrado, risco baixo e novo tende a Mercenary.", "Esquadrão coordenado: esquadrão, controle, risco médio e experiência sobe Seer ou Withered Knight.", "Dupla agressiva: dupla, burst, risco alto e avançado pode favorecer Shadowstrix ou Sorcerer."], "caution_title": "Quando não confiar cegamente", "caution": ["Após patch grande, não trate como definitivo.", "Use planejador, guia e teste no jogo.", "Se os pontos forem próximos, escolha o papel que falta."], "update_title": "Política de atualização", "update_text": "O guia deve mudar quando notas oficiais ou evidência repetida contradizem o modelo.", "faq": [["Qual classe é melhor para iniciantes?", "Mercenary é o começo mais seguro; Withered Knight também ajuda em grupo."], ["Shadowstrix é boa solo?", "Sim, com timing de emboscada e recuo, mas pune mais erros."], ["Todo grupo precisa de Seer?", "Não, mas Seer vale muito quando falta informação."], ["O planejador é preciso?", "É um modelo fan-made útil e deve seguir dados verificados."], ["Há códigos Mistfall Hunter?", "Esta página prioriza classes e builds; códigos oficiais úteis merecem página separada."]]},
        "simple": {"classes_title": "Comparar classes Mistfall Hunter", "classes_paragraphs": ["Compare por papel de run, não por ranking universal.", "Mercenary e Withered Knight são seguros; Blackarrow traz alcance; Shadowstrix e Sorcerer exigem timing; Seer ajuda esquadrões."], "build_paragraphs": ["O planejador transforma formato, ritmo, risco e experiência em direção de build.", "Se os resultados forem próximos, cubra o papel que falta no grupo."], "steam_paragraphs": ["Confira preço, instalação, requisitos e anúncios no Steam oficial.", "Este site não oferece downloads, keys ou mirrors não oficiais."], "about": ["Este site fan-made ajuda a comparar classes antes da build.", "Fatos do Steam e recomendações editoriais ficam separados."], "contact": [f"Envie correções para {SUPPORT_EMAIL}.", "Inclua URL, idioma e fonte."], "privacy": ["O planner roda no navegador e não exige conta.", "Análises ou anúncios futuros devem ser configurados com transparência."], "terms": ["Este site não é afiliado a Mistfall Hunter, Steam ou Valve.", "Recomendações são editoriais e podem ficar desatualizadas."]},
    },
    "ko": {
        "classes": {"risk": {"low": "낮은 위험", "medium": "중간 위험", "high": "높은 위험"}, "metrics": {"solo": "솔로", "squad": "파티", "burst": "폭딜", "control": "제어"}, "roles": {"mercenary": ["전방 전투원", "안정적인 근접 압박과 탈출을 원하는 플레이어에게 맞습니다."], "blackarrow": ["원거리 압박", "정찰하고 견제하며 싸움을 고르는 신중한 플레이어에게 맞습니다."], "shadowstrix": ["기습형 암살자", "매복, 측면 공격, 빠른 이탈을 좋아하는 고기동 플레이어용입니다."], "sorcerer": ["광역 피해 시전자", "마법 폭딜, 지역 압박, 단체전 영향력을 원하는 플레이어용입니다."], "seer": ["지원과 정보", "추적, 유틸리티, 안전한 탈출 판단을 중시하는 파티에 좋습니다."], "withered-knight": ["튼튼한 개시자", "공간을 잡고 교전을 버티며 아군을 보호하고 싶은 플레이어용입니다."]}},
        "planner": {"kicker": "대화형 클래스 선택기", "title": "Mistfall Hunter 클래스 플래너", "description": "네 가지 질문에 답하면 현재 플레이에 맞는 클래스를 정렬합니다. 공식 티어표가 아니라 팬 제작 추천 모델입니다.", "labels": {"format": "플레이 형식", "style": "전투 리듬", "risk": "위험 허용도", "experience": "경험 수준"}, "options": {"format": {"solo": "솔로 탈출", "duo": "듀오 교전", "squad": "파티 플레이"}, "style": {"balanced": "균형 생존", "burst": "폭딜", "control": "제어와 유틸", "frontline": "전방 압박"}, "risk": {"low": "낮은 위험", "medium": "중간 위험", "high": "높은 위험"}, "experience": {"new": "신규 플레이어", "returning": "ARPG 경험자", "advanced": "상급 탈출 플레이어"}}, "submit": "클래스 찾기", "reset": "초기화", "empty": "추천 결과가 여기에 표시됩니다. 모르겠다면 기본 솔로 설정부터 시도하세요.", "short_empty": "설정을 선택하면 빌드 방향이 표시됩니다.", "calculating": "클래스 적합도 계산 중...", "recommended": "추천 클래스", "fit": "{name}은 {format} 플레이에 맞습니다. 모델은 역할, 리듬, 위험, 경험을 함께 평가합니다.", "score_label": "{score}점 / 100점", "score_text": "{score}/100 - {role}", "note": "참고: 팬 제작 추천이며 검증된 밸런스 변화가 있으면 다시 확인해야 합니다."},
        "home": {"media_alt": "Mistfall Hunter Steam 공식 아트", "media_caption": "이 팬 가이드를 위해 처리한 Steam 공식 미디어입니다.", "steps_kicker": "결과 사용법", "steps_title": "추천을 실제 빌드로 바꾸기", "steps": ["먼저 역할을 고르세요. 탈출 판단에서는 생존과 정보도 피해만큼 중요합니다.", "장비를 역할에 맞추세요. 전방은 버티기, 폭딜은 진입 타이밍, 지원은 안전한 위치가 필요합니다.", "패치 후에는 다시 확인하세요. 스킬, 재능, 장비 값이 빠르게 바뀔 수 있습니다."], "source_title": "출처 정책", "source_text": "플랫폼과 출시 정보는 Steam 공식 자료를 사용합니다. 추천은 투명한 팬 편집 모델입니다.", "source_link": "Steam 공식 페이지 열기", "method_kicker": "계산 방식", "method_paragraphs": ["플래너는 생존, 교전 승리, 파티 판단 지원이라는 실전 질문에서 시작합니다.", "폭딜은 Shadowstrix와 Sorcerer를 올리고, 제어는 Seer, Sorcerer, Withered Knight를 올립니다.", "위험 허용도는 안전한 플레이를 원하는 초보자에게 고위험 클래스를 과하게 추천하지 않게 합니다."], "method_card_title": "사용 입력", "method_items": ["형식: 솔로, 듀오, 파티.", "리듬: 균형, 폭딜, 제어, 전방.", "위험: 낮음, 중간, 높음.", "경험: 신규, 복귀, 상급."], "output_title": "결과", "output_text": "최상위 클래스, 역할 설명, 점수 막대가 있는 대체 후보를 제공합니다.", "comparison_kicker": "판단 표", "comparison_title": "상황별 추천 클래스", "comparison_headers": ["필요", "시작 후보", "이유"], "comparison_rows": [["첫 솔로 탈출", "Mercenary", "전방 역할이 이해하기 쉽고 판단 부담이 낮습니다."], ["파티 유틸", "Seer", "정보와 제어가 안전한 교전을 돕습니다."], ["높은 폭딜", "Shadowstrix 또는 Sorcerer", "타이밍을 보상하지만 위치 실수를 벌합니다."], ["앵커 역할", "Withered Knight", "내구와 공간 제어로 팀을 지탱합니다."]], "examples_kicker": "예시", "examples_title": "클래스 선택 예시", "examples": ["신규 솔로: 솔로, 균형, 낮은 위험, 신규는 Mercenary로 기울기 쉽습니다.", "조율된 파티: 파티, 제어, 중간 위험, ARPG 경험은 Seer나 Withered Knight를 올립니다.", "공격적 듀오: 듀오, 폭딜, 높은 위험, 상급은 Shadowstrix나 Sorcerer가 후보입니다."], "caution_title": "맹신하면 안 되는 경우", "caution": ["큰 패치 후에는 최종 답으로 보지 마세요.", "플래너, 가이드, 게임 내 테스트 순서가 안전합니다.", "점수가 비슷하면 파티에 부족한 역할을 고르세요."], "update_title": "업데이트 정책", "update_text": "공식 패치나 반복 검증된 플레이 증거가 모델과 다르면 가이드를 업데이트합니다.", "faq": [["초보자에게 좋은 클래스는?", "Mercenary가 가장 안전한 시작입니다. 파티라면 Withered Knight도 좋습니다."], ["Shadowstrix는 솔로에 좋나요?", "매복과 이탈 타이밍을 안다면 강하지만 실수 허용도가 낮습니다."], ["파티에 Seer가 꼭 필요한가요?", "필수는 아니지만 정보가 부족한 파티에는 매우 유용합니다."], ["플래너는 정확한가요?", "팬 제작 실용 모델이며 검증된 데이터에 맞춰 갱신해야 합니다."], ["Mistfall Hunter 코드가 있나요?", "이 페이지는 클래스와 빌드를 우선합니다. 공식 코드 수요가 있으면 별도 페이지가 적합합니다."]]},
        "simple": {"classes_title": "Mistfall Hunter 클래스 비교법", "classes_paragraphs": ["보편 순위보다 런에서 필요한 역할로 비교하는 편이 실용적입니다.", "Mercenary와 Withered Knight는 안전하고, Blackarrow는 거리, Shadowstrix와 Sorcerer는 타이밍, Seer는 파티 지원에 강합니다."], "build_paragraphs": ["플래너는 형식, 리듬, 위험, 경험을 빌드 방향으로 바꿉니다.", "결과가 비슷하면 파티에 없는 역할을 선택하세요."], "steam_paragraphs": ["가격, 설치, 요구 사양, 공지는 Steam 공식 페이지에서 확인하세요.", "이 사이트는 다운로드, 키 판매, 비공식 미러를 제공하지 않습니다."], "about": ["이 팬 사이트는 빌드를 정하기 전에 클래스를 비교하도록 돕습니다.", "Steam 공식 사실과 편집 추천을 분리합니다."], "contact": [f"수정 제안은 {SUPPORT_EMAIL} 으로 보내주세요.", "URL, 언어, 출처를 함께 적어주세요."], "privacy": ["플래너는 브라우저에서 실행되며 계정이 필요 없습니다.", "향후 분석이나 광고는 투명하게 설정되어야 합니다."], "terms": ["이 사이트는 Mistfall Hunter, Steam, Valve와 제휴하지 않습니다.", "추천은 편집 의견이며 밸런스 변경 후 오래될 수 있습니다."]},
    },
    "it": {
        "classes": {"risk": {"low": "Rischio basso", "medium": "Rischio medio", "high": "Rischio alto"}, "metrics": {"solo": "Solo", "squad": "Squadra", "burst": "Burst", "control": "Controllo"}, "roles": {"mercenary": ["Combattente di prima linea", "Per chi vuole pressione melee leggibile ed estrazioni stabili."], "blackarrow": ["Pressione a distanza", "Per giocatori cauti che preferiscono scout, poke e scelta degli scontri."], "shadowstrix": ["Assassino mobile", "Per imboscate, fianchi e disimpegni rapidi."], "sorcerer": ["Caster ad area", "Per burst magico, pressione di zona e impatto nei fight di gruppo."], "seer": ["Supporto e informazioni", "Per squadre che vogliono tracking, utilità e chiamate di estrazione sicure."], "withered-knight": ["Iniziatore resistente", "Per tenere spazio, sopravvivere agli scambi e proteggere alleati."]}},
        "planner": {"kicker": "Selettore interattivo", "title": "Planner classi Mistfall Hunter", "description": "Rispondi a quattro domande e lo strumento ordina le classi per la tua run. È un modello fan-made, non una tier list ufficiale.", "labels": {"format": "Formato run", "style": "Ritmo di combattimento", "risk": "Tolleranza al rischio", "experience": "Esperienza"}, "options": {"format": {"solo": "Estrazione solo", "duo": "Schermaglia duo", "squad": "Gioco di squadra"}, "style": {"balanced": "Sopravvivenza bilanciata", "burst": "Danno burst", "control": "Controllo e utilità", "frontline": "Pressione frontale"}, "risk": {"low": "Rischio basso", "medium": "Rischio medio", "high": "Rischio alto"}, "experience": {"new": "Nuovo giocatore", "returning": "Giocatore ARPG", "advanced": "Giocatore extraction avanzato"}}, "submit": "Trova classe", "reset": "Reimposta", "empty": "La raccomandazione apparirà qui. Se hai dubbi, prova prima il profilo solo standard.", "short_empty": "Scegli impostazioni per generare una direzione build.", "calculating": "Calcolo compatibilità...", "recommended": "Classe consigliata", "fit": "{name} si adatta alla run {format} perché il modello combina ruolo, ritmo, rischio ed esperienza.", "score_label": "{score} su 100", "score_text": "{score}/100 - {role}", "note": "Nota: raccomandazione fan-made da rivedere quando cambia il bilanciamento verificato."},
        "home": {"media_alt": "Arte ufficiale Steam di Mistfall Hunter", "media_caption": "Media ufficiale Steam elaborato per questa guida fan-made.", "steps_kicker": "Come usare il risultato", "steps_title": "Trasforma il consiglio in build giocabile", "steps": ["Scegli prima il ruolo: sopravvivenza e informazione contano quanto il danno.", "Adatta l equipaggiamento: frontline regge, burst cerca finestre pulite, supporto resta sicuro.", "Ricontrolla dopo patch perché valori, talenti ed equipaggiamento cambiano."], "source_title": "Politica fonti", "source_text": "I fatti di piattaforma vengono da Steam ufficiale. Le raccomandazioni sono un modello editoriale trasparente.", "source_link": "Apri pagina Steam ufficiale", "method_kicker": "Metodo", "method_paragraphs": ["Il planner chiede se una classe aiuta sopravvivenza, scambio o decisione di squadra.", "Burst favorisce Shadowstrix e Sorcerer; controllo favorisce Seer, Sorcerer e Withered Knight.", "La tolleranza al rischio evita di spingere classi fragili a chi cerca sicurezza."], "method_card_title": "Input usati", "method_items": ["Formato: solo, duo o squadra.", "Ritmo: bilanciato, burst, controllo o frontline.", "Rischio: basso, medio o alto.", "Esperienza: nuovo, abituale o avanzato."], "output_title": "Output", "output_text": "Classe principale, spiegazione del ruolo e alternative con barre punteggio.", "comparison_kicker": "Tabella decisione", "comparison_title": "Migliore classe per bisogno", "comparison_headers": ["Bisogno", "Scelta iniziale", "Perché"], "comparison_rows": [["Prima estrazione solo", "Mercenary", "Profilo frontline permissivo e semplice."], ["Utilità squadra", "Seer", "Informazioni e controllo rendono sicuri gli scontri."], ["Giocate burst", "Shadowstrix o Sorcerer", "Premiano il timing ma puniscono il posizionamento."], ["Ruolo ancora", "Withered Knight", "Durabilità e controllo spazio per gruppi coordinati."]], "examples_kicker": "Esempi", "examples_title": "Esempi di scelta classe", "examples": ["Nuovo solo: solo, bilanciato, rischio basso e nuovo porta spesso a Mercenary.", "Squadra coordinata: squadra, controllo, rischio medio ed esperienza ARPG alza Seer o Withered Knight.", "Duo aggressivo: duo, burst, rischio alto e avanzato può favorire Shadowstrix o Sorcerer."], "caution_title": "Quando non fidarsi alla cieca", "caution": ["Dopo una patch grande non usarlo come risposta finale.", "Planner, guida e test in gioco restano il flusso sicuro.", "Se i punteggi sono vicini, scegli il ruolo mancante."], "update_title": "Politica aggiornamento", "update_text": "La guida va aggiornata quando note ufficiali o prove ripetute contraddicono il modello.", "faq": [["Quale classe per principianti?", "Mercenary è il punto di partenza più sicuro; Withered Knight aiuta in squadra."], ["Shadowstrix è buona solo?", "Sì se gestisci imboscate e fuga, ma perdona meno errori."], ["Serve sempre Seer?", "No, ma Seer vale molto quando manca informazione."], ["Il planner è preciso?", "È un modello fan-made pratico da aggiornare con dati verificati."], ["Ci sono codici Mistfall Hunter?", "Questa pagina priorizza classi e build; codici ufficiali utili meritano una pagina separata."]]},
        "simple": {"classes_title": "Confrontare le classi Mistfall Hunter", "classes_paragraphs": ["Confronta per ruolo nella run, non per classifica universale.", "Mercenary e Withered Knight sono sicuri; Blackarrow dà distanza; Shadowstrix e Sorcerer richiedono timing; Seer aiuta la squadra."], "build_paragraphs": ["Il planner trasforma formato, ritmo, rischio ed esperienza in direzione build.", "Se i risultati sono vicini, copri il ruolo che manca al gruppo."], "steam_paragraphs": ["Prezzo, installazione, requisiti e annunci vanno verificati su Steam ufficiale.", "Questo sito non offre download, key o mirror non ufficiali."], "about": ["Questo sito fan-made aiuta a confrontare classi prima della build.", "Fatti Steam e raccomandazioni editoriali restano separati."], "contact": [f"Invia correzioni a {SUPPORT_EMAIL}.", "Includi URL, lingua e fonte."], "privacy": ["Il planner funziona nel browser e non richiede account.", "Analisi o pubblicità future devono essere configurate con trasparenza."], "terms": ["Questo sito non è affiliato a Mistfall Hunter, Steam o Valve.", "Le raccomandazioni sono editoriali e possono diventare obsolete."]},
    },
}

for locale, block in COMPACT_LOCALE_BLOCKS.items():
    TEXT[locale] = deep_merge(TEXT[locale], block)

FINAL_TEXT_FIXES = {
    "es": {"home": {"faq_title": "Preguntas frecuentes sobre clases Mistfall Hunter"}, "simple": {"steam_paragraphs": ["Usa Steam oficial para precio, instalación, requisitos, reseñas y anuncios actuales.", "Esta web no ofrece descargas, claves ni espejos no oficiales."]}},
    "fr": {"footer": {"disclaimer": "Aide et planificateur fan-made pour Mistfall Hunter. Non affilié à Bellring Games, Skystone Games, Steam ou Valve."}, "pages": {"classes": {"title": "Manuel des Classes Mistfall Hunter", "description": "Manuel pratique des classes Mistfall Hunter avec rôles, forces, risque et choix pour débutants.", "h1": "Manuel des Classes Mistfall Hunter"}, "privacy-policy": {"description": "Politique de confidentialité de Classes Mistfall Hunter, aide fan-made et planificateur de builds."}}, "home": {"actions": ["Utiliser le planificateur", "Lire le manuel"], "media_caption": "Média officiel Steam traité pour cette aide fan-made.", "method_items": ["Mode: solo, duo ou escouade.", "Rythme: équilibre, burst, contrôle ou front.", "Risque: faible, moyen ou élevé.", "Expérience: nouveau, habitué ou avancé."], "caution": ["Ne l utilisez pas comme vérité finale après un patch majeur.", "Planificateur, manuel, puis test en jeu reste le flux le plus sûr.", "Si deux scores sont proches, choisissez le rôle manquant."], "update_text": "Cette aide doit évoluer quand des notes officielles ou preuves de gameplay répétées contredisent le modèle.", "faq_title": "Questions fréquentes sur les classes Mistfall Hunter"}, "planner": {"labels": {"format": "Mode du run"}}, "simple": {"build_paragraphs": ["Le planificateur transforme mode, rythme, risque et expérience en direction de build.", "Si les scores sont proches, traitez le résultat comme une égalité et couvrez le rôle manquant."]}},
    "de": {"footer": {"disclaimer": "Fan-erstellter Mistfall Hunter Klassenleitfaden und Build-Planer. Nicht mit Bellring Games, Skystone Games, Steam oder Valve verbunden."}, "pages": {"classes": {"title": "Mistfall Hunter Klassenleitfaden", "description": "Praktischer Mistfall Hunter Klassenleitfaden mit Rollen, Stärken, Risiko und Einsteiger-Tipps.", "h1": "Mistfall Hunter Klassenleitfaden"}, "privacy-policy": {"description": "Datenschutzerklaerung fuer Mistfall Hunter Klassen, einen fan-erstellten Klassenleitfaden und Build-Planer."}}, "home": {"media_caption": "Offizielles Steam-Material, für diesen Fan-Leitfaden verarbeitet.", "method_items": ["Run-Art: Solo, Duo oder Gruppe.", "Rhythmus: ausgewogen, Burst, Kontrolle oder Front.", "Risiko: niedrig, mittel oder hoch.", "Erfahrung: neu, erfahren oder fortgeschritten."], "caution": ["Nach großen Patches nicht als endgültig behandeln.", "Planer, Leitfaden und Ingame-Test bleiben der sichere Ablauf.", "Bei engen Scores zählt die fehlende Gruppenrolle."], "update_text": "Der Leitfaden wird angepasst, wenn offizielle Notizen oder wiederholte Gameplay-Belege das Modell widerlegen.", "faq_title": "Häufige Fragen zu Mistfall Hunter Klassen"}, "planner": {"labels": {"format": "Run-Art"}}, "simple": {"build_paragraphs": ["Der Planer macht aus Run-Art, Rhythmus, Risiko und Erfahrung eine Build-Richtung.", "Bei engen Ergebnissen zählt die Rolle, die deiner Gruppe fehlt."]}},
    "pt": {"home": {"faq_title": "Perguntas frequentes sobre classes Mistfall Hunter"}, "simple": {"steam_paragraphs": ["Confira preço, instalação, requisitos e anúncios no Steam oficial.", "Este site não oferece baixas, chaves ou espelhos não oficiais."]}},
    "ja": {"home": {"faq_title": "Mistfall Hunter クラス よくある質問"}, "simple": {"steam_paragraphs": ["価格、インストール、必要環境、レビュー、告知はSteam公式で確認してください。", "このサイトはファイル取得、キー販売、非公式ミラーを提供しません。"]}},
    "ko": {"home": {"faq_title": "Mistfall Hunter 클래스 자주 묻는 질문"}, "simple": {"steam_paragraphs": ["가격, 설치, 요구 사양, 공지는 Steam 공식 페이지에서 확인하세요.", "이 사이트는 파일 제공, 키 판매, 비공식 미러를 제공하지 않습니다."]}},
    "it": {"home": {"faq_title": "Domande frequenti sulle classi Mistfall Hunter"}, "simple": {"steam_paragraphs": ["Prezzo, installazione, requisiti e annunci vanno verificati su Steam ufficiale.", "Questo sito non offre scaricamenti, chiavi o mirror non ufficiali."]}},
}

for locale, block in FINAL_TEXT_FIXES.items():
    TEXT[locale] = deep_merge(TEXT[locale], block)

PRICE_PAGE_DATA = {
    "en": {
        "page": {"title": "Mistfall Hunter Price: 5 Checks Before Buying on Steam", "description": "Check the current Mistfall Hunter price, launch discount, edition facts, refund window, and where to verify updates before buying on Steam.", "h1": "Mistfall Hunter Price: 5 Checks Before Buying on Steam", "kicker": "Price guide"},
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-price-check.webp", "alt": "Fan-made Mistfall Hunter price check illustration with Steam purchase cues", "caption": "Fan-made price-check graphic for comparing the Steam listing, discount state, and buy-now timing."},
            {"type": "rich", "title": "Quick answer: what Mistfall Hunter costs right now", "paragraphs": ["As of 2026-08-01, the official Steam appdetails feed for Mistfall Hunter shows a United States list price of $24.99 and a current price of $22.49, which means a 10% launch discount is active. Treat that number as a checked snapshot, not a permanent promise: Steam prices can vary by region, taxes, bundles, sales, and publisher updates.", "The safest way to use this guide is simple. First, open the official Steam page from this site, confirm the price in your own currency, then decide whether the game fits your extraction ARPG appetite. This page does not sell keys, mirror downloads, or claim a universal cheapest price. It explains what to verify before you buy.", "Mistfall Hunter is a paid Steam game, not a free-to-play download. The official store data also lists Bellring Games as developer, Skystone Games as publisher, and Jul 29, 2026 as the release date. Those facts matter because price pages written before launch may still mention expected pricing, wishlists, or demo access rather than the live purchase state."]},
            {"type": "table", "title": "Current Steam price snapshot", "headers": ["Item", "Checked value", "How to use it"], "rows": [["Standard game", "$24.99 list / $22.49 current in US Steam data", "Use this as a directional US snapshot, then verify your regional store before checkout."], ["Discount", "10% launch discount visible in official Steam API", "If the store page no longer shows the discount, trust the live Steam checkout over this article."], ["Release status", "Released on Jul 29, 2026", "Older preview articles may be outdated if they discuss only wishlist or playtest access."], ["Platform", "Windows on Steam", "Do not buy from unofficial key pages unless you accept the account and refund risk."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Official Steam hero art used to identify the Mistfall Hunter store listing", "caption": "Official Steam media helps identify the correct game page before comparing prices."},
            {"type": "rich", "title": "What to check before paying", "paragraphs": ["Price is only one part of the decision. Mistfall Hunter is a PvPvE extraction ARPG, so the value depends on whether you enjoy repeated runs, gear-risk tension, class mastery, and group decision making. If you only want a short single-player campaign, the price may feel different than it does for a squad planning dozens of extraction attempts.", "Check the edition name and package carefully. Steam also lists Mistfall Hunter - Upgrade to Deluxe Edition, which requires the base game and adds cosmetic bonuses plus Fate Coins. The store page states the DLC is non-refundable due to platform policy, so compare the live package contents before you choose standard, upgrade, or deluxe bundle.", "Also check the refund window before you experiment. Steam's standard refund policy is generally tied to purchase age and playtime, but eligibility can depend on region, payment method, abuse review, and special cases. Read the policy at checkout instead of relying on a short summary from any fan site.", "Finally, avoid unofficial mirrors. This site links to Steam because the official store is the reliable source for price, release status, platform support, and updates. A third-party key reseller can be cheaper, but it may also add refund, region-lock, activation, or account-support problems that do not show up in a headline price."]},
            {"type": "table", "title": "Buyer fit: pay now or wait?", "headers": ["Player situation", "Better move", "Reason"], "rows": [["You already want extraction PvPvE", "Buy during a verified Steam discount", "The genre rewards repeated runs, so early learning time has value."], ["You mainly want the best class first", "Read the classes guide before buying", "Class rhythm matters; avoid paying before knowing whether the roles fit you."], ["You need controller, language, or hardware certainty", "Check Steam requirements and recent reviews first", "Support details can change after launch and differ by setup."], ["You dislike early balance shifts", "Wait for patch notes and community consensus", "Class values, loot tuning, and matchmaking feel can move quickly after release."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Official Mistfall Hunter Steam header image for confirming the store page", "caption": "Use official store media and publisher names to avoid confusing Mistfall Hunter with unrelated Mistfall titles."},
            {"type": "rich", "title": "How this price guide stays current", "paragraphs": ["The page separates checked facts from editorial advice. The current USD price, discount percentage, release date, developer, publisher, and package id were checked from official Steam endpoints on 2026-08-01. The buying advice is editorial and should be rechecked when Steam changes the store page, when a major sale starts, or when the publisher adds editions.", "If you found this page through a search result that says Mistfall Hunter price, use the first table as the answer and the second table as the decision filter. If you searched for Mistfall Hunter release date or Steam availability, the dedicated Steam info page is still the better source because it keeps platform and official-link facts together.", "A practical workflow is: verify the live Steam price, read the class guide, try the build planner, then decide whether the game fits your solo or squad plan. That order avoids buying purely on discount pressure and gives you a better sense of the kind of runs you are paying to repeat."]},
            {"type": "faq", "title": "Mistfall Hunter price FAQ", "items": [["How much is Mistfall Hunter on Steam?", "On 2026-08-01, official US Steam appdetails data showed $24.99 list price and $22.49 current price with a 10% discount. Always verify the live store page in your region before buying."], ["Is Mistfall Hunter free to play?", "No. The official Steam data marks Mistfall Hunter as a paid game, not a free-to-play title."], ["Should I wait for a bigger Mistfall Hunter sale?", "Wait if you are unsure about extraction PvPvE, hardware fit, or post-launch balance. Buy during a verified discount if you already want the genre and plan to play repeated runs."], ["Where should I buy Mistfall Hunter?", "The safest source is the official Steam page. This fan site does not provide downloads, keys, or unofficial mirrors."], ["Does the price include Deluxe content?", "The standard package is separate from Mistfall Hunter - Upgrade to Deluxe Edition. Steam says the upgrade requires the base game and is non-refundable due to platform policy, so verify the live bundle contents before buying."]]},
            {"type": "links", "title": "Verification sources", "items": [["Official Steam page", OFFICIAL_STEAM_URL, "Current store price, platform, publisher, and purchase state."], ["Steam refund policy", "https://store.steampowered.com/steam_refunds/", "Refund eligibility should be checked against Steam's current policy before purchase."]]},
        ],
    },
    "es": {
        "page": {"title": "Precio de Mistfall Hunter: 5 revisiones antes de comprar", "description": "Consulta precio actual de Mistfall Hunter, descuento de lanzamiento, version de Steam, reembolso y fuentes oficiales antes de comprar.", "h1": "Precio de Mistfall Hunter: 5 revisiones antes de comprar", "kicker": "Guia de precio"},
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-price-check.webp", "alt": "Ilustracion fan-made para revisar precio de Mistfall Hunter en Steam", "caption": "Grafico fan-made para ordenar precio, descuento y momento de compra."},
            {"type": "rich", "title": "Respuesta rapida sobre el precio", "paragraphs": ["El 2026-08-01, los datos oficiales de Steam para Estados Unidos mostraban Mistfall Hunter con precio base de $24.99 y precio actual de $22.49, con 10% de descuento. Es una captura verificada, no una promesa permanente, porque Steam cambia moneda, impuestos, ofertas y paquetes segun region.", "Antes de pagar, abre la pagina oficial de Steam, confirma el precio en tu moneda y revisa si el juego encaja con lo que buscas: extraccion PvPvE, progreso por runs, riesgo de equipo y aprendizaje de clases. Esta web no vende claves ni ofrece descargas.", "Tambien conviene separar precio de valor. Si planeas jugar con escuadron y repetir rutas, el descuento puede tener sentido. Si solo quieres probar por curiosidad, revisa reseñas recientes, requisitos y la politica de reembolso."]},
            {"type": "table", "title": "Resumen de precio en Steam", "headers": ["Dato", "Valor revisado", "Uso practico"], "rows": [["Juego base", "$24.99 / $22.49 en datos US de Steam", "Verifica tu tienda regional antes de pagar."], ["Descuento", "10% visible en la API oficial", "Si la tienda ya no lo muestra, manda la pagina en vivo."], ["Lanzamiento", "29 de julio de 2026", "Evita guias antiguas que hablan solo de wishlist o demo."], ["Plataforma", "Windows en Steam", "Prioriza Steam sobre mirrors o claves dudosas."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Arte oficial de Steam para identificar la pagina de Mistfall Hunter", "caption": "Usa medios oficiales para confirmar que estas en la ficha correcta del juego."},
            {"type": "rich", "title": "Que revisar antes de comprar", "paragraphs": ["Mira el nombre del paquete. Steam tambien lista Mistfall Hunter - Upgrade to Deluxe Edition, que requiere el juego base y agrega cosmeticos y Fate Coins. La ficha indica que ese DLC no es reembolsable por politica de la plataforma, asi que compara el contenido visible antes de elegir estandar, upgrade o bundle.", "Lee la politica de reembolso desde Steam en el momento de pago. Las reglas suelen depender de tiempo desde la compra y horas jugadas, pero tambien pueden variar por region, metodo de pago y revision de abuso.", "Evita comprar solo por urgencia de descuento. Primero revisa clases, estilo de combate, soporte de idioma y requisitos. Un precio bajo no ayuda si el bucle de extraccion no es lo que quieres jugar."]},
            {"type": "table", "title": "Comprar ahora o esperar", "headers": ["Situacion", "Decision", "Motivo"], "rows": [["Te gusta PvPvE de extraccion", "Comprar con descuento verificado", "El aprendizaje temprano aporta valor."], ["No sabes que clase usar", "Leer la guia de clases", "La eleccion de rol cambia la experiencia."], ["Necesitas certeza tecnica", "Revisar requisitos y reseñas", "El soporte puede cambiar tras el lanzamiento."], ["Te molestan ajustes de balance", "Esperar parches", "Clases y botin pueden moverse rapido."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Cabecera oficial de Mistfall Hunter en Steam", "caption": "La cabecera oficial ayuda a no confundir este juego con otros titulos parecidos."},
            {"type": "faq", "title": "Preguntas frecuentes sobre precio de Mistfall Hunter", "items": [["Cuanto cuesta Mistfall Hunter?", "El 2026-08-01, Steam US mostraba $24.99 de precio base y $22.49 actual. Confirma siempre tu region."], ["Mistfall Hunter es gratis?", "No. La ficha oficial lo marca como juego de pago."], ["Conviene esperar otra oferta?", "Si dudas del genero o de los requisitos, espera. Si ya quieres PvPvE, un descuento oficial puede valer."], ["Donde comprarlo?", "La fuente mas segura es Steam oficial; este sitio no ofrece descargas ni claves."], ["El precio incluye Deluxe?", "El paquete estandar es distinto del Upgrade to Deluxe Edition. Steam indica que el upgrade requiere el juego base y no es reembolsable por politica de la plataforma."]]},
            {"type": "links", "title": "Fuentes", "items": [["Steam oficial", OFFICIAL_STEAM_URL, "Precio, plataforma y estado de compra."], ["Politica de reembolso de Steam", "https://store.steampowered.com/steam_refunds/", "Reglas actuales antes de pagar."]]},
        ],
    },
    "fr": {
        "page": {"title": "Prix de Mistfall Hunter : 5 controles avant achat", "description": "Verifiez le prix Mistfall Hunter, la remise Steam, le contenu du paquet, le remboursement et les sources officielles avant d acheter.", "h1": "Prix de Mistfall Hunter : 5 controles avant achat", "kicker": "Aide prix"},
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-price-check.webp", "alt": "Illustration fan-made de verification du prix Mistfall Hunter sur Steam", "caption": "Visuel fan-made pour comparer prix, remise et moment d achat."},
            {"type": "rich", "title": "Reponse courte sur le prix", "paragraphs": ["Le 2026-08-01, les donnees officielles Steam aux Etats-Unis indiquaient Mistfall Hunter a $24.99 en prix de base et $22.49 en prix actuel, avec 10% de remise. C est un instantane verifie, pas une garantie durable, car Steam adapte devise, taxes, promotions et paquets par region.", "Avant d acheter, ouvrez la page Steam officielle, confirmez votre prix local, puis jugez si le jeu correspond a votre envie d ARPG d extraction PvPvE. Ce site ne vend pas de cles et ne propose aucun miroir de telechargement.", "Le bon critere n est pas seulement le prix. La valeur vient des runs repetes, du risque d equipement, de la maitrise de classe et du jeu de groupe. Si ces boucles vous attirent, la remise pese plus que pour une simple curiosite."]},
            {"type": "table", "title": "Instantane du prix Steam", "headers": ["Element", "Valeur verifiee", "Conseil"], "rows": [["Jeu standard", "$24.99 / $22.49 dans les donnees Steam US", "Verifiez votre boutique regionale avant paiement."], ["Remise", "10% visible dans l API officielle", "La page Steam en direct reste prioritaire."], ["Sortie", "29 juillet 2026", "Mefiez-vous des anciens articles pre-lancement."], ["Plateforme", "Windows sur Steam", "Evitez les pages de cles non officielles si vous voulez un remboursement simple."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Image officielle Steam pour identifier Mistfall Hunter", "caption": "Les medias Steam officiels aident a confirmer la bonne fiche du jeu."},
            {"type": "rich", "title": "Controles utiles avant paiement", "paragraphs": ["Controlez le nom du paquet. Steam liste aussi Mistfall Hunter - Upgrade to Deluxe Edition, qui exige le jeu de base et ajoute des cosmetiques ainsi que des Fate Coins. La fiche indique que ce DLC n est pas remboursable selon la politique de la plateforme; comparez donc le contenu visible avant de choisir.", "Lisez la politique de remboursement Steam au moment d achat. Elle depend souvent de l anciennete de l achat et du temps de jeu, avec des cas particuliers selon region, paiement ou abus.", "Ne laissez pas une remise decider seule. Consultez aussi le manuel des classes, les exigences PC et les avis recents pour savoir si le rythme d extraction vous convient."]},
            {"type": "table", "title": "Acheter maintenant ou attendre", "headers": ["Situation", "Choix", "Pourquoi"], "rows": [["Vous aimez le PvPvE d extraction", "Acheter avec remise verifiee", "Le temps d apprentissage precoce a de la valeur."], ["Vous cherchez surtout la meilleure classe", "Lire le manuel des classes", "Le role choisi change beaucoup l experience."], ["Vous avez un doute technique", "Verifier exigences et avis", "Le confort depend du PC et des mises a jour."], ["Vous craignez l equilibrage", "Attendre des patchs", "Classes, butin et matchmaking peuvent changer."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Banniere officielle Mistfall Hunter sur Steam", "caption": "La banniere officielle evite la confusion avec d autres jeux Mistfall."},
            {"type": "faq", "title": "Questions frequentes sur le prix Mistfall Hunter", "items": [["Combien coute Mistfall Hunter?", "Le 2026-08-01, Steam US indiquait $24.99 de prix de base et $22.49 en prix actuel. Verifiez toujours votre region."], ["Mistfall Hunter est-il gratuit?", "Non, les donnees Steam le classent comme jeu payant."], ["Faut-il attendre une meilleure remise?", "Attendez si le genre ou le support PC vous semble incertain. Achetez seulement si la boucle d extraction vous interesse vraiment."], ["Ou l acheter?", "La source la plus sure reste Steam officiel; ce site ne fournit ni cle ni telechargement."], ["Le prix inclut-il le contenu Deluxe?", "Le paquet standard est separe de l Upgrade to Deluxe Edition. Steam indique que l upgrade exige le jeu de base et n est pas remboursable selon la politique de la plateforme."]]},
            {"type": "links", "title": "Sources", "items": [["Steam officiel", OFFICIAL_STEAM_URL, "Prix, plateforme et etat d achat."], ["Remboursements Steam", "https://store.steampowered.com/steam_refunds/", "Regles de remboursement a verifier avant paiement."]]},
        ],
    },
    "de": {
        "page": {"title": "Mistfall Hunter Preis: 5 Checks vor dem Kauf", "description": "Pruefe Mistfall Hunter Preis, Steam-Rabatt, Paketinhalt, Rueckerstattung und offizielle Quellen, bevor du kaufst.", "h1": "Mistfall Hunter Preis: 5 Checks vor dem Kauf", "kicker": "Preisleitfaden"},
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-price-check.webp", "alt": "Fan-Grafik zur Mistfall Hunter Preispruefung auf Steam", "caption": "Fan-made Grafik fuer Preis, Rabatt und Kaufzeitpunkt."},
            {"type": "rich", "title": "Kurze Antwort zum aktuellen Preis", "paragraphs": ["Am 2026-08-01 zeigte der offizielle Steam-Appdetails-Datensatz fuer die USA einen Listenpreis von $24.99 und einen aktuellen Preis von $22.49, also 10% Rabatt. Das ist eine gepruefte Momentaufnahme, keine dauerhafte Zusage, weil Steam Preise, Steuern, Aktionen und Pakete regional aendern kann.", "Oeffne vor dem Kauf die offizielle Steam-Seite, bestaetige deinen regionalen Preis und entscheide dann, ob ein PvPvE-Extraction-ARPG zu dir passt. Diese Fan-Seite verkauft keine Keys und bietet keine Downloads an.", "Der Wert haengt stark vom Spielstil ab. Wer wiederholte Runs, Ausruestungsrisiko, Klassenlernen und Gruppenentscheidungen mag, bewertet den Preis anders als jemand, der nur kurz reinschauen will."]},
            {"type": "table", "title": "Steam-Preisuebersicht", "headers": ["Punkt", "Gepruefter Wert", "Nutzen"], "rows": [["Standardspiel", "$24.99 / $22.49 in US-Steam-Daten", "Vor dem Bezahlen die regionale Shopseite pruefen."], ["Rabatt", "10% in der offiziellen API sichtbar", "Wenn Steam live etwas anderes zeigt, gilt die Shopseite."], ["Release", "29. Juli 2026", "Aeltere Vorschauartikel koennen ueberholt sein."], ["Plattform", "Windows auf Steam", "Offizielle Seite vermeidet Key- und Refund-Risiken."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Offizielles Steam-Artwork zur Identifikation von Mistfall Hunter", "caption": "Offizielle Steam-Medien helfen, die richtige Store-Seite zu erkennen."},
            {"type": "rich", "title": "Was vor dem Kauf wichtig ist", "paragraphs": ["Pruefe den Paketnamen. Steam listet auch Mistfall Hunter - Upgrade to Deluxe Edition; es benoetigt das Basisspiel und enthaelt kosmetische Inhalte sowie Fate Coins. Die Store-Seite nennt das DLC wegen Plattformrichtlinie als nicht erstattbar, also vergleiche Standard, Upgrade und Bundle live auf Steam.", "Lies die Steam-Rueckerstattungsregeln direkt beim Kauf. Sie haengen oft von Kaufalter und Spielzeit ab, koennen aber je nach Region, Zahlungsart oder Einzelfall anders bewertet werden.", "Kaufe nicht nur wegen Rabattdruck. Lies Klassenleitfaden, Anforderungen und aktuelle Bewertungen, damit du weisst, ob der Extraction-Rhythmus zu deinem Spielplan passt."]},
            {"type": "table", "title": "Jetzt kaufen oder warten", "headers": ["Situation", "Entscheidung", "Grund"], "rows": [["Du willst PvPvE-Extraction", "Bei bestaetigtem Rabatt kaufen", "Fruehes Lernen bringt Nutzen."], ["Du suchst zuerst die beste Klasse", "Klassenleitfaden lesen", "Die Rolle praegt den Spielspass."], ["Du brauchst technische Sicherheit", "Anforderungen und Reviews pruefen", "Performance kann setupabhaengig sein."], ["Du magst keine Balance-Schwankungen", "Patchnotes abwarten", "Klassen und Loot koennen sich schnell aendern."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Offizieller Steam-Header von Mistfall Hunter", "caption": "Der offizielle Header reduziert Verwechslungen mit anderen Mistfall-Titeln."},
            {"type": "faq", "title": "Haeufige Fragen zum Mistfall Hunter Preis", "items": [["Was kostet Mistfall Hunter?", "Am 2026-08-01 zeigte Steam US $24.99 Listenpreis und $22.49 aktuellen Preis. Pruefe immer deine Region."], ["Ist Mistfall Hunter kostenlos?", "Nein, die offizielle Steam-Datenquelle markiert es als kostenpflichtiges Spiel."], ["Sollte ich auf einen groesseren Sale warten?", "Warte, wenn Genre, PC-Support oder Balance unklar sind. Kaufe nur, wenn du den Extraction-Loop wirklich willst."], ["Wo sollte ich kaufen?", "Am sichersten ist die offizielle Steam-Seite; diese Website bietet keine Keys oder Downloads."], ["Ist Deluxe im Preis enthalten?", "Das Standardpaket ist getrennt vom Upgrade to Deluxe Edition. Steam nennt fuer das Upgrade Basisspiel-Pflicht und keine Erstattung gemaess Plattformrichtlinie."]]},
            {"type": "links", "title": "Quellen", "items": [["Offizielle Steam-Seite", OFFICIAL_STEAM_URL, "Preis, Plattform und Kaufstatus."], ["Steam-Rueckerstattung", "https://store.steampowered.com/steam_refunds/", "Aktuelle Refund-Regeln."]]},
        ],
    },
    "pt": {
        "page": {"title": "Preco de Mistfall Hunter: 5 checagens antes de comprar", "description": "Veja preco de Mistfall Hunter, desconto no Steam, pacote, reembolso e fontes oficiais antes de comprar.", "h1": "Preco de Mistfall Hunter: 5 checagens antes de comprar", "kicker": "Guia de preco"},
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-price-check.webp", "alt": "Ilustracao fan-made para conferir preco de Mistfall Hunter no Steam", "caption": "Grafico fan-made para comparar preco, desconto e momento de compra."},
            {"type": "rich", "title": "Resposta rapida sobre o preco", "paragraphs": ["Em 2026-08-01, os dados oficiais do Steam para os EUA mostravam Mistfall Hunter com preco base de $24.99 e preco atual de $22.49, com 10% de desconto. Use isso como captura verificada, nao como promessa permanente, pois moeda, impostos, promocoes e pacotes variam por regiao.", "Antes de pagar, abra a pagina oficial do Steam, confirme o preco local e avalie se voce quer um ARPG de extracao PvPvE com runs repetidas, risco de equipamento e aprendizado de classes. Este site nao vende chaves nem oferece arquivos para baixar.", "Se voce joga com amigos e pretende repetir rotas, o valor pode ser maior. Se so quer testar por curiosidade, confira requisitos, avaliacoes recentes e regras de reembolso antes de decidir."]},
            {"type": "table", "title": "Resumo do preco no Steam", "headers": ["Item", "Valor conferido", "Como usar"], "rows": [["Jogo padrao", "$24.99 / $22.49 nos dados US do Steam", "Confira sua loja regional antes de pagar."], ["Desconto", "10% visivel na API oficial", "Se a pagina ao vivo mudou, confie no checkout."], ["Lancamento", "29 de julho de 2026", "Evite artigos antigos de pre-lancamento."], ["Plataforma", "Windows no Steam", "Prefira a fonte oficial a mirrors ou keys duvidosas."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Arte oficial do Steam para identificar Mistfall Hunter", "caption": "A midia oficial ajuda a confirmar a pagina correta do jogo."},
            {"type": "rich", "title": "O que conferir antes da compra", "paragraphs": ["Veja o nome do pacote. O Steam tambem lista Mistfall Hunter - Upgrade to Deluxe Edition, que exige o jogo base e inclui cosmeticos e Fate Coins. A pagina informa que esse DLC nao e reembolsavel pela politica da plataforma, entao compare o conteudo ao vivo antes de escolher.", "Leia a politica de reembolso no momento da compra. Ela costuma envolver tempo desde a compra e horas jogadas, mas pode ter excecoes por regiao, pagamento e analise de abuso.", "Nao compre apenas pela pressa do desconto. Leia o guia de classes, requisitos e avaliacoes recentes para saber se o ritmo de extracao combina com voce."]},
            {"type": "table", "title": "Comprar agora ou esperar", "headers": ["Situacao", "Melhor decisao", "Motivo"], "rows": [["Voce gosta de PvPvE de extracao", "Comprar com desconto verificado", "Aprender cedo pode valer a pena."], ["Quer saber a melhor classe", "Ler o guia de classes", "A escolha de papel muda a experiencia."], ["Tem duvida tecnica", "Checar requisitos e reviews", "Suporte pode variar por PC."], ["Nao gosta de balanceamento instavel", "Esperar patches", "Classes e loot podem mudar rapido."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Cabecalho oficial de Mistfall Hunter no Steam", "caption": "O cabecalho oficial evita confusao com outros jogos Mistfall."},
            {"type": "faq", "title": "Perguntas frequentes sobre preco de Mistfall Hunter", "items": [["Quanto custa Mistfall Hunter?", "Em 2026-08-01, Steam US mostrava $24.99 de preco base e $22.49 atual. Verifique sua regiao."], ["Mistfall Hunter e gratis?", "Nao, o Steam oficial marca o jogo como pago."], ["Vale esperar promocao maior?", "Espere se genero, requisitos ou balanceamento ainda geram duvida. Compre se voce ja quer o loop de extracao."], ["Onde comprar?", "A fonte mais segura e o Steam oficial; este site nao fornece keys ou arquivos para baixar."], ["O preco inclui Deluxe?", "O pacote padrao e separado do Upgrade to Deluxe Edition. O Steam informa que o upgrade exige o jogo base e nao e reembolsavel pela politica da plataforma."]]},
            {"type": "links", "title": "Fontes", "items": [["Steam oficial", OFFICIAL_STEAM_URL, "Preco, plataforma e estado de compra."], ["Reembolsos Steam", "https://store.steampowered.com/steam_refunds/", "Regras atuais antes de pagar."]]},
        ],
    },
    "it": {
        "page": {"title": "Prezzo Mistfall Hunter: 5 controlli prima di comprarlo", "description": "Controlla prezzo Mistfall Hunter, sconto Steam, pacchetto, rimborso e fonti ufficiali prima dell acquisto.", "h1": "Prezzo Mistfall Hunter: 5 controlli prima di comprarlo", "kicker": "Guida prezzo"},
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-price-check.webp", "alt": "Illustrazione fan-made per controllare il prezzo di Mistfall Hunter su Steam", "caption": "Grafica fan-made per confrontare prezzo, sconto e momento di acquisto."},
            {"type": "rich", "title": "Risposta rapida sul prezzo", "paragraphs": ["Il 2026-08-01 i dati ufficiali Steam per gli Stati Uniti mostravano Mistfall Hunter a $24.99 di listino e $22.49 come prezzo attuale, con sconto del 10%. E una fotografia verificata, non una promessa permanente, perche Steam puo cambiare valuta, tasse, offerte e pacchetti per regione.", "Prima di pagare, apri la pagina Steam ufficiale, conferma il prezzo locale e valuta se vuoi davvero un ARPG extraction PvPvE basato su run ripetute, rischio equipaggiamento e apprendimento delle classi. Questo sito non vende key e non offre scaricamenti.", "Il valore dipende dal tuo uso. Se giochi in squadra e ripeti molte estrazioni, il prezzo pesa diversamente rispetto a un acquisto solo per curiosita."]},
            {"type": "table", "title": "Riepilogo prezzo Steam", "headers": ["Elemento", "Valore controllato", "Uso"], "rows": [["Gioco standard", "$24.99 / $22.49 nei dati Steam US", "Verifica la tua regione prima del checkout."], ["Sconto", "10% visibile nell API ufficiale", "Se Steam live mostra altro, vale il checkout."], ["Uscita", "29 luglio 2026", "Evita vecchi articoli pre-lancio."], ["Piattaforma", "Windows su Steam", "Meglio Steam rispetto a mirror o key dubbie."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Arte ufficiale Steam per identificare Mistfall Hunter", "caption": "I media ufficiali aiutano a riconoscere la scheda corretta del gioco."},
            {"type": "rich", "title": "Controlli prima dell acquisto", "paragraphs": ["Controlla il pacchetto. Steam elenca anche Mistfall Hunter - Upgrade to Deluxe Edition, che richiede il gioco base e aggiunge cosmetici e Fate Coins. La pagina indica che il DLC non e rimborsabile per politica della piattaforma, quindi confronta standard, upgrade e bundle dal vivo.", "Leggi le regole di rimborso al momento dell acquisto. Di solito dipendono da eta dell acquisto e ore giocate, ma possono avere eccezioni per regione, pagamento e casi specifici.", "Non comprare solo per paura di perdere lo sconto. Leggi la guida classi, requisiti e recensioni recenti per capire se il ritmo extraction e adatto a te."]},
            {"type": "table", "title": "Comprare ora o aspettare", "headers": ["Situazione", "Scelta", "Motivo"], "rows": [["Ti piace il PvPvE extraction", "Compra con sconto verificato", "Imparare presto ha valore."], ["Vuoi prima la classe migliore", "Leggi la guida classi", "Il ruolo cambia il feeling."], ["Hai dubbi tecnici", "Controlla requisiti e review", "Il supporto dipende dal setup."], ["Temi cambi di bilanciamento", "Aspetta patch", "Classi e loot possono cambiare."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Header ufficiale Steam di Mistfall Hunter", "caption": "L header ufficiale evita confusione con altri titoli Mistfall."},
            {"type": "faq", "title": "Domande frequenti sul prezzo Mistfall Hunter", "items": [["Quanto costa Mistfall Hunter?", "Il 2026-08-01 Steam US mostrava $24.99 di listino e $22.49 attuale. Verifica sempre la tua regione."], ["Mistfall Hunter e gratis?", "No, Steam lo indica come gioco a pagamento."], ["Conviene aspettare un saldo maggiore?", "Aspetta se hai dubbi su genere, requisiti o bilanciamento. Compra se vuoi gia il loop extraction."], ["Dove comprarlo?", "La fonte piu sicura e Steam ufficiale; questo sito non offre key o scaricamenti."], ["Il prezzo include Deluxe?", "Il pacchetto standard e separato dall Upgrade to Deluxe Edition. Steam indica che l upgrade richiede il gioco base e non e rimborsabile per politica della piattaforma."]]},
            {"type": "links", "title": "Fonti", "items": [["Steam ufficiale", OFFICIAL_STEAM_URL, "Prezzo, piattaforma e acquisto."], ["Rimborsi Steam", "https://store.steampowered.com/steam_refunds/", "Regole di rimborso attuali."]]},
        ],
    },
    "ja": {
        "page": {"title": "Mistfall Hunter 価格: 購入前に確認したい5項目", "description": "Mistfall Hunterの価格、Steam割引、パッケージ内容、返金条件、公式確認先を購入前に整理します。", "h1": "Mistfall Hunter 価格: 購入前に確認したい5項目", "kicker": "価格ガイド"},
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-price-check.webp", "alt": "SteamでMistfall Hunterの価格を確認するファン作成の説明図", "caption": "価格、割引、購入タイミングを整理するファン作成の説明図です。"},
            {"type": "rich", "title": "現在価格の要点", "paragraphs": ["2026-08-01時点で、公式Steam appdetailsの米国データではMistfall Hunterの通常価格は$24.99、現在価格は$22.49、割引率は10%でした。これは確認済みの時点情報であり、地域、税、セール、パッケージ変更によって表示価格は変わります。", "購入前には必ず公式Steamページを開き、自分の地域の価格を確認してください。このサイトはキー販売、ファイル配布、非公式ミラーを提供しません。価格だけでなく、PvPvE抽出ARPGの繰り返しプレイ、装備リスク、クラス習熟が自分に合うかも判断材料です。", "発売日はSteam公式データでJul 29, 2026です。発売前の記事や予想価格の記事は、現在の購入状態を反映していない場合があります。"]},
            {"type": "table", "title": "Steam価格スナップショット", "headers": ["項目", "確認値", "使い方"], "rows": [["標準版", "米国Steamデータで$24.99 / $22.49", "購入前に地域ストアで再確認する。"], ["割引", "公式APIで10%表示", "ライブページが変わっていればSteamを優先する。"], ["発売日", "2026年7月29日", "古いプレビュー記事と区別する。"], ["平台", "Steam版Windows", "非公式キーやミラーは返金リスクを確認する。"]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Mistfall Hunterの公式Steamヒーロー画像", "caption": "公式Steam素材で正しいストアページか確認できます。"},
            {"type": "rich", "title": "支払う前の確認ポイント", "paragraphs": ["まずパッケージ名を確認します。SteamにはMistfall Hunter - Upgrade to Deluxe Editionも掲載されており、基本ゲームが必要で、コスメティック要素とFate Coinsが含まれます。ストアではプラットフォーム方針により返金不可と案内されているため、標準版、アップグレード、バンドルの内容を購入前に比較してください。", "返金条件もSteam上で確認します。一般に購入からの期間とプレイ時間が重要ですが、地域、支払い方法、個別判断で変わる場合があります。短い要約だけで判断しない方が安全です。", "割引だけで急いで買う必要はありません。クラスガイド、ビルドプランナー、必要環境、最近のレビューを確認してから、自分のソロや分隊の遊び方に合うか判断してください。"]},
            {"type": "table", "title": "今買うか待つか", "headers": ["状況", "おすすめ", "理由"], "rows": [["抽出PvPvEが好き", "公式割引中なら購入候補", "早く慣れるほど判断が楽になります。"], ["最適クラスが気になる", "先にクラスガイドを読む", "役割選びで体験が大きく変わります。"], ["PC環境が不安", "要件とレビューを確認", "快適さは環境と更新で変わります。"], ["バランス調整が不安", "パッチを待つ", "クラス性能や報酬は変化しやすいです。"]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Mistfall Hunterの公式Steamヘッダー画像", "caption": "公式ヘッダーは似た名前の別作品との混同防止に役立ちます。"},
            {"type": "faq", "title": "Mistfall Hunter 価格 よくある質問", "items": [["Mistfall Hunterはいくらですか?", "2026-08-01時点の米国Steamデータでは通常$24.99、現在$22.49でした。購入前に地域価格を確認してください。"], ["無料で遊べますか?", "いいえ。公式Steamデータでは有料ゲームとして扱われています。"], ["もっと大きなセールを待つべきですか?", "ジャンルや動作環境に迷いがあるなら待つ価値があります。抽出PvPvEを遊びたいなら公式割引中に検討できます。"], ["どこで買うのが安全ですか?", "公式Steamページが最も安全です。このサイトはキーやダウンロードを提供しません。"], ["Deluxe内容は価格に含まれますか?", "標準パッケージとUpgrade to Deluxe Editionは別です。Steamではアップグレードに基本ゲームが必要で、プラットフォーム方針により返金不可と案内されています。"]]},
            {"type": "links", "title": "確認元", "items": [["Steam公式ページ", OFFICIAL_STEAM_URL, "価格、平台、購入状態を確認。"], ["Steam返金ポリシー", "https://store.steampowered.com/steam_refunds/", "購入前に返金条件を確認。"]]},
        ],
    },
    "ko": {
        "page": {"title": "Mistfall Hunter 가격: 구매 전 확인할 5가지", "description": "Mistfall Hunter 가격, Steam 할인, 패키지, 환불 조건, 공식 확인 출처를 구매 전 정리합니다.", "h1": "Mistfall Hunter 가격: 구매 전 확인할 5가지", "kicker": "가격 가이드"},
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-price-check.webp", "alt": "Steam에서 Mistfall Hunter 가격을 확인하는 팬 제작 설명 이미지", "caption": "가격, 할인, 구매 시점을 정리한 팬 제작 설명 이미지입니다."},
            {"type": "rich", "title": "현재 가격 요약", "paragraphs": ["2026-08-01 기준 공식 Steam appdetails의 미국 데이터는 Mistfall Hunter 정가 $24.99, 현재가 $22.49, 할인 10%로 표시했습니다. 이 값은 확인된 시점 자료이며 지역, 세금, 세일, 패키지 변경에 따라 달라질 수 있습니다.", "구매 전에는 공식 Steam 페이지에서 본인 지역 가격을 직접 확인하세요. 이 사이트는 키 판매, 파일 제공, 비공식 미러를 하지 않습니다. 가격뿐 아니라 PvPvE 추출 ARPG의 반복 플레이, 장비 위험, 클래스 숙련이 본인 취향에 맞는지도 봐야 합니다.", "공식 데이터의 출시일은 Jul 29, 2026입니다. 출시 전 예상 가격이나 위시리스트 안내 글은 현재 구매 상태와 다를 수 있습니다."]},
            {"type": "table", "title": "Steam 가격 스냅샷", "headers": ["항목", "확인 값", "활용"], "rows": [["기본 게임", "미국 Steam 데이터 $24.99 / $22.49", "결제 전 지역 상점에서 다시 확인합니다."], ["할인", "공식 API에서 10% 표시", "실시간 Steam 페이지가 우선입니다."], ["출시", "2026년 7월 29일", "오래된 출시 전 글과 구분합니다."], ["플랫폼", "Windows on Steam", "비공식 키와 미러는 환불 위험을 확인합니다."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Mistfall Hunter 공식 Steam 히어로 이미지", "caption": "공식 Steam 이미지는 올바른 게임 페이지 확인에 도움이 됩니다."},
            {"type": "rich", "title": "결제 전 체크포인트", "paragraphs": ["먼저 패키지 이름을 확인하세요. Steam에는 Mistfall Hunter - Upgrade to Deluxe Edition도 등록되어 있으며 기본 게임이 필요하고 꾸미기 보상과 Fate Coins가 포함됩니다. 상점은 플랫폼 정책상 해당 DLC가 환불 불가라고 안내하므로 표준판, 업그레이드, 번들 내용을 결제 전 비교하세요.", "환불 조건도 구매 시점에 Steam에서 확인하세요. 보통 구매 후 기간과 플레이 시간이 중요하지만 지역, 결제 방식, 개별 검토에 따라 달라질 수 있습니다.", "할인 압박만으로 구매하지 마세요. 클래스 가이드, 빌드 플래너, 요구 사양, 최근 리뷰를 확인한 뒤 솔로 또는 분대 플레이에 맞는지 판단하는 편이 안전합니다."]},
            {"type": "table", "title": "지금 구매할까 기다릴까", "headers": ["상황", "선택", "이유"], "rows": [["추출 PvPvE를 원함", "공식 할인 중 구매 검토", "초반 학습 시간이 가치가 있습니다."], ["최적 클래스가 궁금함", "클래스 가이드 먼저 읽기", "역할 선택이 경험을 바꿉니다."], ["PC 환경이 걱정됨", "요구 사양과 리뷰 확인", "성능은 환경에 따라 다릅니다."], ["밸런스 변동이 싫음", "패치 후 기다리기", "클래스와 보상이 빠르게 바뀔 수 있습니다."]]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Mistfall Hunter 공식 Steam 헤더 이미지", "caption": "공식 헤더는 비슷한 이름의 다른 게임과 혼동을 줄입니다."},
            {"type": "faq", "title": "Mistfall Hunter 가격 자주 묻는 질문", "items": [["Mistfall Hunter 가격은 얼마인가요?", "2026-08-01 기준 미국 Steam 데이터는 정가 $24.99, 현재가 $22.49였습니다. 지역 가격은 직접 확인하세요."], ["무료 게임인가요?", "아닙니다. 공식 Steam 데이터는 유료 게임으로 표시합니다."], ["더 큰 할인을 기다려야 하나요?", "장르나 사양이 불확실하면 기다리세요. 추출 PvPvE를 원한다면 공식 할인 중 검토할 수 있습니다."], ["어디서 사는 게 안전한가요?", "공식 Steam 페이지가 가장 안전합니다. 이 사이트는 키나 다운로드를 제공하지 않습니다."], ["가격에 Deluxe가 포함되나요?", "기본 패키지와 Upgrade to Deluxe Edition은 별도입니다. Steam은 업그레이드에 기본 게임이 필요하며 플랫폼 정책상 환불 불가라고 안내합니다."]]},
            {"type": "links", "title": "확인 출처", "items": [["공식 Steam 페이지", OFFICIAL_STEAM_URL, "가격, 플랫폼, 구매 상태 확인."], ["Steam 환불 정책", "https://store.steampowered.com/steam_refunds/", "구매 전 환불 조건 확인."]]},
        ],
    },
}

DELUXE_SOURCE_COPY = {
    "en": ["Official Deluxe Upgrade page", "Required base-game and non-refundable DLC details."],
    "es": ["Pagina oficial Deluxe Upgrade", "Detalles de juego base requerido y DLC no reembolsable."],
    "fr": ["Page officielle Deluxe Upgrade", "Details sur jeu de base requis et DLC non remboursable."],
    "de": ["Offizielle Deluxe-Upgrade-Seite", "Details zu Basisspiel-Pflicht und nicht erstattbarem DLC."],
    "pt": ["Pagina oficial Deluxe Upgrade", "Detalhes de jogo base exigido e DLC nao reembolsavel."],
    "it": ["Pagina ufficiale Deluxe Upgrade", "Dettagli su gioco base richiesto e DLC non rimborsabile."],
    "ja": ["Deluxe Upgrade公式ページ", "基本ゲーム必須と返金不可DLCの確認。"],
    "ko": ["Deluxe Upgrade 공식 페이지", "기본 게임 필요와 환불 불가 DLC 확인."],
}

for locale, data in PRICE_PAGE_DATA.items():
    TEXT[locale]["pages"]["price"] = data["page"]
    for section in data["sections"]:
        if section["type"] == "links":
            label, description = DELUXE_SOURCE_COPY[locale]
            section["items"].insert(1, [label, OFFICIAL_STEAM_DELUXE_URL, description])

PLAYER_COUNT_PAGE_DATA = {
    "en": {
        "page": {"title": "Mistfall Hunter Player Count: Steam Charts, Peaks, and Queue Timing", "description": "Check how to read Mistfall Hunter player count, Steam Charts and SteamDB peaks, with queue-timing tips for solo and squad runs.", "h1": "Mistfall Hunter Player Count: Steam Charts, Peaks, and Queue Timing", "kicker": "Player count guide"},
        "sections": [
            {"type": "embed", "title": "Live SteamDB chart", "src": STEAMDB_EMBED_URL, "link_href": STEAMDB_CHARTS_URL, "caption": "SteamDB embed for Mistfall Hunter app 3282300. SteamDB is a third-party tracking site; use it as a directional live chart, not an official publisher statement.", "link_label": "Open live SteamDB chart"},
            {"type": "rich", "title": "Quick answer: where to check the live player count", "paragraphs": ["The most useful Mistfall Hunter player count source is a live Steam chart, because the number changes by hour, region, sale timing, patch timing, and weekend activity. This page does not freeze a permanent player-count claim. Instead, it shows where to verify the current number and how to decide whether the chart is healthy enough for your next solo, duo, or squad session.", "Use SteamDB or Steam chart pages for the live count, then compare three signals: current players, 24-hour peak, and all-time peak. Current players tell you how busy the game is right now. The 24-hour peak tells you whether the day still has a reliable activity window. The all-time peak is historical context and should not be treated as today queue quality.", "For Mistfall Hunter specifically, player count matters because it is a PvPvE extraction ARPG. A thin activity window can affect matchmaking, market feel, squad availability, and how often you meet hostile players. A strong peak does not guarantee perfect queues in every region, but it is a better signal than review count alone." ]},
            {"type": "table", "title": "How to read Mistfall Hunter Steam Charts", "headers": ["Signal", "What it means", "Decision use"], "rows": [["Current players", "People currently in-game on Steam", "Best for deciding whether to queue now."], ["24-hour peak", "The busiest recent daily window", "Best for planning play time if current count is low."], ["All-time peak", "Highest tracked Steam peak", "Useful for launch history, weak for today queue quality."], ["Patch or sale spike", "Temporary activity lift after news or discount", "Check whether the spike lasts beyond one day."]]},
            {"type": "rich", "title": "What player count can and cannot tell you", "paragraphs": ["Player count is useful, but it is not a complete quality score. A game can have a modest player count and still feel good if matchmaking is regional, peak hours are predictable, and squads coordinate through Discord or friends. A large all-time peak can also be misleading if the launch surge faded or if a free demo created a temporary spike.", "For solo players, the practical question is whether the current window gives enough encounters without turning every route into a crowded brawl. For squads, the question is different: can your group find consistent sessions at your usual hour, and are enough players online to keep extraction decisions unpredictable? That is why this guide separates current count, daily peak, and trend direction instead of giving one simple verdict.", "If you are deciding whether to buy, combine player count with the price guide, official Steam page, recent reviews, and the class planner. A discount plus an active weekend peak is a stronger signal than a discount alone. If you already own the game, use the 24-hour peak to find better run windows before changing your class or build because of one quiet queue." ]},
            {"type": "table", "title": "Queue-timing checklist", "headers": ["Situation", "What to do", "Why"], "rows": [["Current count is low but daily peak is higher", "Play near the recent peak hour", "The community may be active in a different timezone."], ["Daily peak is falling for several days", "Wait for patch notes, sale news, or weekend activity", "One quiet hour is noise; several quiet days are a stronger trend."], ["You play with a fixed squad", "Check the chart at your normal session time", "Global peaks matter less than your own play window."], ["You are buying mainly for PvP", "Read recent reviews and watch activity after launch updates", "Population affects encounter density more than class choice does."]]},
            {"type": "faq", "title": "Mistfall Hunter player count FAQ", "items": [["What is the best Mistfall Hunter player count source?", "Use a live Steam chart such as SteamDB for the current count, 24-hour peak, and historical peak. This fan page explains how to interpret those numbers rather than claiming they stay fixed."], ["Is Mistfall Hunter dead if the current player count is low?", "Not necessarily. Check the 24-hour peak, weekend pattern, patch timing, and your region. Extraction games can feel different by timezone and squad habits."], ["Should I buy Mistfall Hunter based on player count?", "Use player count as one signal. Also check Steam price, recent reviews, system fit, refund policy, and whether the classes match your play style."], ["Do Steam charts include console players?", "Mistfall Hunter is tracked here as a Steam/Windows game. Steam chart data should not be treated as a full cross-platform audience count unless the publisher confirms other platforms and tracking sources."], ["Why does the all-time peak matter less than current players?", "All-time peak shows launch or event history. Current players and 24-hour peak are more useful for deciding whether queues are active now."]]},
            {"type": "links", "title": "Verification sources", "items": [["SteamDB Mistfall Hunter charts", STEAMDB_CHARTS_URL, "Live current players, 24-hour peak, and historical Steam chart context.", "nofollow noopener"], ["Official Steam page", OFFICIAL_STEAM_URL, "Official app page for platform, release, publisher, and store facts."]]},
            {"type": "related", "title": "Related Mistfall Hunter guides", "items": [["Mistfall Hunter Steam info", "/steam/", "Verify the official store and platform facts."], ["Mistfall Hunter classes guide", "/classes/", "Pick a role after checking activity windows."], ["Mistfall Hunter build planner", "/build-planner/", "Match a class direction to your solo or squad plan."], ["Mistfall Hunter price guide", "/price/", "Use player-count trends together with price and refund checks before buying."]]},
        ],
    }
}

PLAYER_COUNT_LOCALE_COPY = {
    "es": {"title": "Jugadores de Mistfall Hunter: Steam Charts, picos y mejor hora", "description": "Aprende a leer jugadores de Mistfall Hunter, Steam Charts y picos de SteamDB antes de entrar solo o con escuadron.", "h1": "Jugadores de Mistfall Hunter: Steam Charts, picos y mejor hora", "kicker": "Guia de jugadores", "keyword": "jugadores de Mistfall Hunter", "source": "grafico de SteamDB", "related_title": "Guias relacionadas de Mistfall Hunter", "faq_title": "Preguntas frecuentes sobre jugadores de Mistfall Hunter"},
    "ja": {"title": "Mistfall Hunter player count: Steam Chartsとピークの読み方", "description": "Mistfall Hunterのplayer count、Steam Charts、SteamDBのピークを確認し、ソロや分隊で遊ぶ時間を判断するガイド。", "h1": "Mistfall Hunter player count: Steam Chartsとピークの読み方", "kicker": "プレイヤー数ガイド", "keyword": "Mistfall Hunter player count", "source": "SteamDBチャート", "related_title": "関連するMistfall Hunterガイド", "faq_title": "Mistfall Hunter player count FAQ"},
    "fr": {"title": "Nombre de joueurs Mistfall Hunter : Steam Charts, pics et horaires", "description": "Lisez le nombre de joueurs Mistfall Hunter, Steam Charts et les pics SteamDB avant de lancer une session solo ou en escouade.", "h1": "Nombre de joueurs Mistfall Hunter : Steam Charts, pics et horaires", "kicker": "Guide joueurs", "keyword": "nombre de joueurs Mistfall Hunter", "source": "graphique SteamDB", "related_title": "Ressources Mistfall Hunter liees", "faq_title": "Questions sur le nombre de joueurs Mistfall Hunter"},
    "de": {"title": "Mistfall Hunter Spielerzahl: Steam Charts, Peaks und Queue-Zeiten", "description": "So liest du Mistfall Hunter Spielerzahl, Steam Charts und SteamDB-Peaks fuer Solo- und Gruppenruns.", "h1": "Mistfall Hunter Spielerzahl: Steam Charts, Peaks und Queue-Zeiten", "kicker": "Spielerzahl-Guide", "keyword": "Mistfall Hunter Spielerzahl", "source": "SteamDB-Chart", "related_title": "Verwandte Mistfall Hunter Guides", "faq_title": "Haeufige Fragen zur Mistfall Hunter Spielerzahl"},
    "pt": {"title": "Jogadores de Mistfall Hunter: Steam Charts, picos e horarios", "description": "Veja como ler jogadores de Mistfall Hunter, Steam Charts e picos no SteamDB antes de jogar solo ou em equipe.", "h1": "Jogadores de Mistfall Hunter: Steam Charts, picos e horarios", "kicker": "Guia de jogadores", "keyword": "jogadores de Mistfall Hunter", "source": "grafico do SteamDB", "related_title": "Guias relacionados de Mistfall Hunter", "faq_title": "Perguntas sobre jogadores de Mistfall Hunter"},
    "ko": {"title": "Mistfall Hunter player count: Steam Charts와 피크 읽는 법", "description": "Mistfall Hunter player count, Steam Charts, SteamDB 피크를 확인하고 솔로 또는 스쿼드 플레이 시간을 판단하세요.", "h1": "Mistfall Hunter player count: Steam Charts와 피크 읽는 법", "kicker": "플레이어 수 가이드", "keyword": "Mistfall Hunter player count", "source": "SteamDB 차트", "related_title": "관련 Mistfall Hunter 가이드", "faq_title": "Mistfall Hunter player count FAQ"},
    "it": {"title": "Giocatori Mistfall Hunter: Steam Charts, picchi e orari migliori", "description": "Come leggere giocatori Mistfall Hunter, Steam Charts e picchi SteamDB prima di giocare solo o in squadra.", "h1": "Giocatori Mistfall Hunter: Steam Charts, picchi e orari migliori", "kicker": "Guida giocatori", "keyword": "giocatori Mistfall Hunter", "source": "grafico SteamDB", "related_title": "Risorse Mistfall Hunter correlate", "faq_title": "FAQ giocatori Mistfall Hunter"},
}

PLAYER_COUNT_DETAIL_COPY = {
    "es": {
        "image_caption": "Ilustracion editorial generada para leer tendencias de jugadores; no es una captura en vivo de Steam.",
        "quick_title": "Respuesta rapida: donde comprobar los jugadores en vivo",
        "quick": ["La forma mas fiable de usar los jugadores de Mistfall Hunter es revisar un grafico de Steam antes de entrar, porque el numero cambia por hora, zona horaria, fin de semana, rebajas, parches y ventana regional de emparejamiento.", "Empieza por el grafico de SteamDB y compara jugadores actuales, pico de 24 horas y pico historico. Los jugadores actuales sirven para decidir si conviene hacer cola ahora; el pico diario ayuda a escoger mejor hora.", "Como Mistfall Hunter es un ARPG de extraccion PvPvE, la poblacion afecta encuentros, sensacion de mercado, disponibilidad de escuadron y ritmo de rutas."],
        "signals_title": "Como leer Steam Charts", "signal_headers": ["Senal", "Que significa", "Uso"], "signal_rows": [["Jugadores actuales", "Usuarios dentro del juego en Steam ahora", "Mejor senal para entrar ya."], ["Pico de 24 horas", "Momento mas activo del dia reciente", "Sirve para planear horario."], ["Pico historico", "Mayor pico registrado en Steam", "Contexto de lanzamiento, no cola actual."], ["Subida por parche o rebaja", "Actividad temporal por noticia o descuento", "Comprueba si dura mas de un dia."]],
        "media_caption": "El arte oficial de Steam ayuda a confirmar que el grafico corresponde al juego correcto.",
        "limits_title": "Lo que el numero no puede demostrar",
        "limits": ["Un conteo bajo en este momento no significa automaticamente que el juego este muerto. Mira el pico diario, patron de fin de semana, fecha de parche y tu propio horario antes de decidir.", "Para solitario importa si la ventana actual ofrece encuentros suficientes sin convertir cada ruta en caos. Para escuadrones importa si el grupo encuentra sesiones estables en su horario normal.", "Si todavia vas a comprar, combina actividad con precio, pagina oficial de Steam, resenas recientes y guia de clases. La actividad mas el encaje de juego pesa mas que un pico aislado."],
        "queue_title": "Lista para elegir horario", "queue_headers": ["Situacion", "Accion", "Motivo"], "queue_rows": [["Actual bajo pero pico diario mayor", "Juega cerca del pico reciente", "La comunidad puede estar en otra zona horaria."], ["Pico diario baja varios dias", "Espera parche, rebaja o fin de semana", "Varios dias flojos pesan mas que una hora."], ["Juegas con escuadron fijo", "Mira tu horario habitual", "Tu ventana importa mas que el pico global."], ["Compras por PvP", "Lee resenas y actividad tras updates", "La poblacion cambia la densidad de encuentros."]],
        "hero_caption": "El arte oficial de Steam es medio real del juego; la grafica generada es solo explicativa.",
        "faq": [["Donde comprobar jugadores de Mistfall Hunter?", "Usa un grafico en vivo como SteamDB para jugadores actuales, pico de 24 horas y pico historico."], ["Un conteo bajo significa que esta muerto?", "No por si solo. Revisa pico diario, fin de semana, parche, region y habitos de escuadron."], ["Debo comprar solo por jugadores?", "No. Combinalo con precio, resenas, reembolso, requisitos y clases."], ["Steam Charts incluye consolas?", "No para esta lectura. Tratalo como dato Steam/Windows salvo confirmacion del editor."], ["Por que importa menos el pico historico?", "Muestra interes de lanzamiento o evento; jugadores actuales y pico diario sirven mas para la cola de hoy."]],
    },
    "fr": {
        "image_caption": "Illustration editoriale generee pour lire une tendance de joueurs; ce n'est pas une capture Steam en direct.",
        "quick_title": "Reponse rapide : ou verifier les joueurs en direct",
        "quick": ["La meilleure maniere d'utiliser le nombre de joueurs Mistfall Hunter est de consulter un graphique Steam en direct avant de lancer une session, car le chiffre varie selon l'heure, le fuseau, le week-end, les soldes, les patchs et la region.", "Commencez par le graphique SteamDB, puis comparez joueurs actuels, pic sur 24 heures et pic historique. Le chiffre actuel aide a decider si vous lancez maintenant; le pic quotidien aide a trouver une meilleure fenetre.", "Mistfall Hunter etant un ARPG d'extraction PvPvE, la population influence la densite des rencontres, les escouades disponibles et le rythme des routes."],
        "signals_title": "Comment lire Steam Charts", "signal_headers": ["Signal", "Signification", "Utilisation"], "signal_rows": [["Joueurs actuels", "Joueurs en jeu sur Steam maintenant", "Meilleur signal pour lancer tout de suite."], ["Pic 24 h", "Fenetre la plus active recente", "Planifier une meilleure heure."], ["Pic historique", "Plus haut pic suivi sur Steam", "Contexte, pas qualite de file actuelle."], ["Pic patch ou solde", "Hausse temporaire apres une annonce", "Verifier si elle dure plus d'un jour."]],
        "media_caption": "Le media officiel Steam confirme que le graphique appartient bien a l'app Mistfall Hunter.",
        "limits_title": "Ce que le nombre ne prouve pas",
        "limits": ["Un faible nombre actuel ne veut pas dire automatiquement que le jeu est mort. Regardez le pic quotidien, le week-end, les patchs et votre horaire local.", "En solo, la question est d'avoir assez de rencontres sans transformer chaque route en bagarre permanente. En escouade, il faut surtout savoir si votre groupe trouve des sessions stables.", "Avant achat, combinez activite, prix Steam, avis recents et guide des classes. L'activite plus l'adequation de style vaut mieux qu'un seul pic."],
        "queue_title": "Checklist pour choisir l'horaire", "queue_headers": ["Situation", "Action", "Raison"], "queue_rows": [["Actuel bas, pic quotidien plus haut", "Jouer pres du pic recent", "La communaute peut etre active ailleurs."], ["Pic quotidien en baisse plusieurs jours", "Attendre patch, solde ou week-end", "Plusieurs jours faibles sont un vrai signal."], ["Escouade fixe", "Verifier votre heure habituelle", "Votre fenetre compte plus que le pic global."], ["Achat surtout pour PvP", "Lire avis et activite apres update", "La population change la densite d'affrontements."]],
        "hero_caption": "L'art officiel Steam est un vrai media du jeu; le visuel de graphique reste explicatif.",
        "faq": [["Ou verifier le nombre de joueurs?", "Utilisez un graphique live comme SteamDB pour actuel, pic 24 h et historique."], ["Un chiffre bas signifie jeu mort?", "Pas seul. Verifiez pic quotidien, week-end, patch, region et habitudes d'escouade."], ["Acheter seulement avec ce chiffre?", "Non. Croisez avec prix, avis, remboursement, configuration et classes."], ["Steam Charts inclut les consoles?", "Non pour cette lecture; traitez-le comme donnees Steam/Windows."], ["Pourquoi le pic historique compte moins?", "Il montre le lancement ou un evenement; actuel et pic quotidien servent mieux la file d'aujourd'hui."]],
    },
    "de": {
        "image_caption": "Generierte redaktionelle Grafik zum Lesen von Spielertrends; kein Live-Steam-Screenshot.",
        "quick_title": "Kurzantwort: Wo du die Live-Spielerzahl pruefst",
        "quick": ["Die Mistfall Hunter Spielerzahl solltest du vor dem Spielen in einem Live-Steam-Chart pruefen, weil sie sich nach Uhrzeit, Zeitzone, Wochenende, Sale, Patch und Region veraendert.", "Starte mit dem SteamDB-Chart und vergleiche aktuelle Spieler, 24-Stunden-Peak und Allzeit-Peak. Aktuelle Spieler helfen fuer die Queue jetzt; der Tagespeak hilft bei der Zeitplanung.", "Da Mistfall Hunter ein PvPvE-Extraction-ARPG ist, beeinflusst Population Begegnungsdichte, Squad-Verfuegbarkeit und wie unberechenbar eine Route wirkt."],
        "signals_title": "Steam Charts richtig lesen", "signal_headers": ["Signal", "Bedeutung", "Nutzen"], "signal_rows": [["Aktuelle Spieler", "Jetzt auf Steam im Spiel", "Bestes Signal fuer sofortige Queue."], ["24h-Peak", "Aktivstes aktuelles Tagesfenster", "Bessere Spielzeit finden."], ["Allzeit-Peak", "Hoechster Steam-Peak", "Historie, nicht heutige Queue."], ["Patch- oder Sale-Spike", "Kurzfristige Aktivitaet", "Pruefen, ob sie laenger als einen Tag haelt."]],
        "media_caption": "Offizielles Steam-Material hilft, das richtige Spiel und die App-ID zu bestaetigen.",
        "limits_title": "Was die Zahl nicht beweist",
        "limits": ["Eine niedrige aktuelle Zahl bedeutet nicht automatisch, dass das Spiel tot ist. Tagespeak, Wochenende, Patch-Zeitpunkt und dein eigenes Zeitfenster zaehlen.", "Solo-Spieler brauchen genug Begegnungen ohne Dauerchaos. Gruppen muessen wissen, ob ihr normales Zeitfenster stabile Sessions bietet.", "Beim Kaufentscheid zaehlen Spielertrend, Preis, Steam-Seite, aktuelle Reviews und Klassenpassung zusammen. Ein einzelner Peak reicht nicht."],
        "queue_title": "Queue-Zeit-Checkliste", "queue_headers": ["Situation", "Aktion", "Grund"], "queue_rows": [["Aktuell niedrig, Tagespeak hoeher", "Nahe am Peak spielen", "Die Community kann in anderer Zeitzone aktiv sein."], ["Tagespeak sinkt mehrere Tage", "Patch, Sale oder Wochenende abwarten", "Mehrere ruhige Tage sind staerker als eine Stunde."], ["Feste Gruppe", "Normale Sessionzeit pruefen", "Eigenes Fenster zaehlt mehr als globaler Peak."], ["Kauf wegen PvP", "Reviews und Post-Update-Aktivitaet lesen", "Population aendert Begegnungsdichte."]],
        "hero_caption": "Offizielle Steam-Grafik ist echtes Spielmaterial; die Chart-Grafik ist nur erklaerend.",
        "faq": [["Wo pruefe ich die Spielerzahl?", "Nutze ein Live-Chart wie SteamDB fuer aktuelle Spieler, 24h-Peak und Historie."], ["Ist das Spiel tot, wenn die Zahl niedrig ist?", "Nicht automatisch. Pruefe Tagespeak, Wochenende, Patch, Region und Squad-Gewohnheiten."], ["Soll ich nur danach kaufen?", "Nein. Kombiniere mit Preis, Reviews, Rueckerstattung, Systemfit und Klassen."], ["Enthaelt Steam Charts Konsolen?", "Nein, hier ist es Steam/Windows-Datenkontext."], ["Warum ist Allzeit-Peak weniger wichtig?", "Er zeigt Historie; aktuell und Tagespeak sind fuer heutige Queues nuetzlicher."]],
    },
    "pt": {
        "image_caption": "Ilustracao editorial gerada para ler tendencias de jogadores; nao e captura ao vivo do Steam.",
        "quick_title": "Resposta rapida: onde ver jogadores ao vivo",
        "quick": ["A melhor forma de usar jogadores de Mistfall Hunter e consultar um grafico Steam ao vivo antes de jogar, porque o numero muda por hora, fuso, fim de semana, promocao, patch e regiao.", "Comece pelo grafico do SteamDB e compare jogadores atuais, pico de 24 horas e pico historico. O numero atual ajuda a entrar agora; o pico diario ajuda a escolher horario.", "Como Mistfall Hunter e um ARPG de extracao PvPvE, populacao afeta encontros, disponibilidade de grupo e imprevisibilidade das rotas."],
        "signals_title": "Como ler Steam Charts", "signal_headers": ["Sinal", "Significado", "Uso"], "signal_rows": [["Jogadores atuais", "Pessoas no jogo agora no Steam", "Melhor sinal para fila imediata."], ["Pico 24 h", "Janela recente mais ativa", "Planejar melhor horario."], ["Pico historico", "Maior pico rastreado", "Contexto, nao fila de hoje."], ["Pico por patch ou promocao", "Alta temporaria apos noticia", "Ver se dura mais de um dia."]],
        "media_caption": "Midia oficial do Steam ajuda a confirmar a pagina correta do jogo.",
        "limits_title": "O que o numero nao prova",
        "limits": ["Contagem baixa agora nao significa jogo morto automaticamente. Veja pico diario, fim de semana, patch e seu horario.", "Solo precisa de encontros suficientes sem caos constante; equipe precisa de sessoes consistentes no horario combinado.", "Antes de comprar, junte tendencia de jogadores, preco, pagina Steam, avaliacoes recentes e guia de classes. Atividade com encaixe vale mais que um pico isolado."],
        "queue_title": "Checklist de horario", "queue_headers": ["Situacao", "Acao", "Motivo"], "queue_rows": [["Atual baixo, pico diario maior", "Jogar perto do pico recente", "A comunidade pode estar em outro fuso."], ["Pico diario cai por dias", "Esperar patch, promocao ou fim de semana", "Dias fracos pesam mais que uma hora."], ["Equipe fixa", "Conferir seu horario normal", "Sua janela importa mais que o pico global."], ["Compra focada em PvP", "Ler avaliacoes e atividade pos-update", "Populacao muda densidade de encontros."]],
        "hero_caption": "Arte oficial do Steam e midia real do jogo; a grafica gerada e explicativa.",
        "faq": [["Onde conferir jogadores?", "Use grafico ao vivo como SteamDB para atual, pico 24 h e historico."], ["Contagem baixa significa jogo morto?", "Nao sozinha. Veja pico diario, fim de semana, patch, regiao e habitos de grupo."], ["Comprar so por player count?", "Nao. Combine com preco, avaliacoes, reembolso, requisitos e classes."], ["Steam Charts inclui consoles?", "Nao nesta leitura; trate como dados Steam/Windows."], ["Por que pico historico importa menos?", "Mostra lancamento ou evento; atual e pico diario ajudam mais a fila de hoje."]],
    },
    "ja": {
        "image_caption": "プレイヤー推移の読み方を示す生成イラストです。Steamのライブ画面ではありません。",
        "quick_title": "結論：ライブのplayer countを確認する場所",
        "quick": ["Mistfall Hunter player countは、プレイ前にライブのSteamチャートで確認するのが安全です。人数は時間帯、地域、週末、セール、パッチ、マッチング地域で変わります。", "まずSteamDBチャートを見て、現在のプレイヤー数、24時間ピーク、過去最高ピークを分けて確認します。現在数は今キューに入る判断、24時間ピークは遊ぶ時間帯の判断に向いています。", "Mistfall HunterはPvPvE抽出ARPGなので、人口は遭遇密度、分隊の集まりやすさ、ルートの緊張感に影響します。"],
        "signals_title": "Steam Chartsの読み方", "signal_headers": ["指標", "意味", "使い方"], "signal_rows": [["現在のプレイヤー数", "Steamで今プレイ中の人数", "今キューに入る判断。"], ["24時間ピーク", "直近1日の最大活動時間", "遊ぶ時間帯を選ぶ。"], ["過去最高ピーク", "記録上の最大ピーク", "履歴確認。今日のキュー判断には弱い。"], ["パッチ・セールの急増", "告知後の一時的な増加", "1日以上続くか確認。"]],
        "media_caption": "公式Steamメディアは、チャートが正しいゲームに対応しているか確認する助けになります。",
        "limits_title": "人数だけでは判断できないこと",
        "limits": ["現在数が低くても、すぐに過疎と決めるべきではありません。24時間ピーク、週末傾向、パッチ時期、自分のプレイ時間を合わせて見ます。", "ソロでは遭遇が少なすぎないか、分隊では普段の時間に安定して遊べるかが重要です。単なるランキング数字ではなく、実際のプレイ時間で判断します。", "購入前なら、player countだけでなく価格、Steam公式ページ、最近のレビュー、クラス適性も合わせて確認します。"],
        "queue_title": "キュー時間チェック", "queue_headers": ["状況", "行動", "理由"], "queue_rows": [["現在数は低いが日次ピークは高い", "ピーク付近で遊ぶ", "活動時間が別の時間帯に偏っている可能性。"], ["日次ピークが数日下落", "パッチ、セール、週末を待つ", "1時間の静けさより数日の傾向が重要。"], ["固定分隊で遊ぶ", "普段の集合時間で確認", "世界ピークより自分の時間帯が大切。"], ["PvP目的で買う", "最近のレビューと更新後の活動を見る", "人口は遭遇密度に直結します。"]],
        "hero_caption": "公式Steamアートは実際のゲームメディアです。チャート画像は説明用です。",
        "faq": [["どこでplayer countを確認できますか？", "SteamDBのようなライブチャートで現在数、24時間ピーク、過去ピークを確認します。"], ["現在数が低いと過疎ですか？", "それだけでは判断できません。日次ピーク、週末、パッチ、地域、分隊の習慣を見ます。"], ["購入判断に使えますか？", "一つの材料です。価格、レビュー、返金条件、動作環境、クラス適性も確認してください。"], ["Steam Chartsは全プラットフォームですか？", "この文脈ではSteam/Windowsデータとして扱います。"], ["過去最高ピークはなぜ弱いですか？", "発売時やイベントの履歴であり、今日のキュー状況は現在数と日次ピークの方が近いからです。"]],
    },
    "ko": {
        "image_caption": "플레이어 추이를 읽기 위한 생성 설명 그림입니다. Steam 실시간 화면이 아닙니다.",
        "quick_title": "빠른 답: 실시간 player count를 확인할 곳",
        "quick": ["Mistfall Hunter player count는 플레이 전에 실시간 Steam 차트로 확인하는 것이 가장 안전합니다. 수치는 시간대, 주말, 세일, 패치, 지역 매칭 상황에 따라 계속 바뀝니다.", "먼저 SteamDB 차트에서 현재 플레이어, 24시간 피크, 역대 피크를 나눠 봅니다. 현재 수치는 지금 큐에 들어갈지, 24시간 피크는 언제 플레이할지 판단하는 데 유용합니다.", "Mistfall Hunter는 PvPvE 추출 ARPG이므로 인구는 교전 밀도, 스쿼드 구인, 루트의 긴장감에 영향을 줍니다."],
        "signals_title": "Steam Charts 읽는 법", "signal_headers": ["신호", "의미", "사용법"], "signal_rows": [["현재 플레이어", "지금 Steam에서 플레이 중인 인원", "즉시 큐 판단에 가장 유용."], ["24시간 피크", "최근 하루 중 가장 활발한 시간", "플레이 시간대를 고를 때 사용."], ["역대 피크", "Steam에서 기록된 최고 피크", "역사 정보, 오늘 큐 판단은 약함."], ["패치/세일 급등", "소식 이후의 일시적 증가", "하루 이상 유지되는지 확인."]],
        "media_caption": "공식 Steam 이미지는 차트가 올바른 게임에 해당하는지 확인하는 데 도움이 됩니다.",
        "limits_title": "숫자만으로 알 수 없는 것",
        "limits": ["현재 수치가 낮다고 곧바로 죽은 게임이라고 볼 수는 없습니다. 일일 피크, 주말 패턴, 패치 시점, 본인의 플레이 시간을 함께 봐야 합니다.", "솔로는 충분한 교전이 있는지, 스쿼드는 평소 시간대에 안정적으로 세션을 잡을 수 있는지가 중요합니다.", "구매 전이라면 player count와 함께 가격, 공식 Steam 페이지, 최근 리뷰, 클래스 적합성을 같이 확인하세요."],
        "queue_title": "큐 시간 체크리스트", "queue_headers": ["상황", "행동", "이유"], "queue_rows": [["현재 수치는 낮고 일일 피크는 높음", "최근 피크 시간대에 플레이", "커뮤니티 활동 시간이 다를 수 있습니다."], ["일일 피크가 며칠 하락", "패치, 세일, 주말을 기다림", "한 시간보다 며칠 추세가 강한 신호입니다."], ["고정 스쿼드", "평소 세션 시간에 확인", "전 세계 피크보다 본인 시간대가 중요합니다."], ["PvP 목적으로 구매", "최근 리뷰와 업데이트 후 활동 확인", "인구는 교전 밀도에 영향을 줍니다."]],
        "hero_caption": "공식 Steam 아트는 실제 게임 미디어이며, 차트 일러스트는 설명용입니다.",
        "faq": [["어디에서 player count를 확인하나요?", "SteamDB 같은 실시간 차트에서 현재 플레이어, 24시간 피크, 역대 피크를 확인합니다."], ["현재 수치가 낮으면 죽은 게임인가요?", "그 자체로는 아닙니다. 일일 피크, 주말, 패치, 지역, 스쿼드 습관을 함께 보세요."], ["구매 판단에 써도 되나요?", "하나의 신호입니다. 가격, 리뷰, 환불 정책, 사양, 클래스 취향도 확인하세요."], ["Steam Charts는 콘솔도 포함하나요?", "이 문맥에서는 Steam/Windows 데이터로 보아야 합니다."], ["역대 피크가 덜 중요한 이유는?", "출시나 이벤트 이력이고, 오늘 큐 판단은 현재 수치와 일일 피크가 더 가깝기 때문입니다."]],
    },
    "it": {
        "image_caption": "Illustrazione editoriale generata per leggere trend giocatori; non e uno screenshot Steam live.",
        "quick_title": "Risposta rapida: dove controllare i giocatori live",
        "quick": ["Il modo piu utile per leggere i giocatori Mistfall Hunter e controllare un grafico Steam live prima di giocare, perche il numero cambia con ora, fuso, weekend, sconti, patch e regione.", "Parti dal grafico SteamDB e confronta giocatori attuali, picco 24 ore e picco storico. Il numero attuale serve per entrare ora; il picco giornaliero aiuta a scegliere orario.", "Essendo un ARPG extraction PvPvE, la popolazione influenza incontri, disponibilita squadra e ritmo delle rotte."],
        "signals_title": "Come leggere Steam Charts", "signal_headers": ["Segnale", "Significato", "Uso"], "signal_rows": [["Giocatori attuali", "Utenti in gioco ora su Steam", "Miglior segnale per fare queue."], ["Picco 24 h", "Finestra recente piu attiva", "Serve a pianificare l'orario."], ["Picco storico", "Massimo registrato su Steam", "Contesto, non qualita della queue di oggi."], ["Spike patch o sconto", "Aumento temporaneo dopo novita", "Verifica se dura oltre un giorno."]],
        "media_caption": "Il media ufficiale Steam aiuta a confermare che il grafico riguarda la pagina corretta.",
        "limits_title": "Cosa il numero non dimostra",
        "limits": ["Un numero attuale basso non significa automaticamente gioco morto. Guarda picco giornaliero, weekend, patch e il tuo orario.", "In solo conta avere abbastanza incontri senza caos continuo. In squadra conta trovare sessioni stabili nell'orario abituale.", "Prima di comprare, unisci trend giocatori, prezzo, pagina Steam, recensioni recenti e guida classi. Attivita piu fit conta piu di un picco isolato."],
        "queue_title": "Checklist orario queue", "queue_headers": ["Situazione", "Azione", "Motivo"], "queue_rows": [["Attuale basso, picco giornaliero alto", "Gioca vicino al picco", "La community puo essere in altro fuso."], ["Picco giornaliero cala per giorni", "Aspetta patch, sconto o weekend", "Piu giorni pesano piu di un'ora."], ["Squadra fissa", "Controlla il tuo orario", "La tua finestra conta piu del picco globale."], ["Compri per PvP", "Leggi recensioni e attivita post-update", "La popolazione cambia la densita incontri."]],
        "hero_caption": "L'arte ufficiale Steam e media reale del gioco; il grafico generato e solo esplicativo.",
        "faq": [["Dove controllare i giocatori?", "Usa un grafico live come SteamDB per attuali, picco 24 h e storico."], ["Numero basso significa gioco morto?", "Non da solo. Guarda picco giornaliero, weekend, patch, regione e abitudini squadra."], ["Comprare solo su player count?", "No. Combina prezzo, recensioni, rimborso, requisiti e classi."], ["Steam Charts include console?", "No in questa lettura; trattalo come dato Steam/Windows."], ["Perche il picco storico conta meno?", "Mostra storia di lancio o evento; attuali e picco giornaliero aiutano la queue di oggi."]],
    },
}

def localized_player_count_data(locale):
    """
    生成玩家数量指南页的本地化内容。

    :param locale: 语言代码
    :return: dict，包含页面元信息和正文区块
    """
    if locale == "en":
        return PLAYER_COUNT_PAGE_DATA["en"]
    copy = PLAYER_COUNT_LOCALE_COPY[locale]
    detail = PLAYER_COUNT_DETAIL_COPY[locale]
    common = {
        "es": {"embed_title": "Grafico SteamDB en vivo", "embed_caption": "Insercion de SteamDB para Mistfall Hunter app 3282300. Usalo como grafico direccional de terceros, no como declaracion oficial.", "open_chart": "Abrir el grafico en vivo de SteamDB", "sources": "Fuentes de verificacion", "steamdb_desc": "Jugadores actuales, pico diario y contexto historico en Steam.", "steam_desc": "Pagina oficial para plataforma, lanzamiento, editor y tienda.", "steam_info": "Informacion Steam de Mistfall Hunter", "steam_info_desc": "Verifica plataforma y datos oficiales.", "classes": "Guia de clases Mistfall Hunter", "classes_desc": "Elige rol despues de revisar horarios activos.", "planner": "Planificador de builds Mistfall Hunter", "planner_desc": "Relaciona clase con plan solo o escuadron.", "price": "Precio de Mistfall Hunter", "price_desc": "Combina actividad con precio y reembolso."},
        "ja": {"embed_title": "SteamDBライブチャート", "embed_caption": "Mistfall Hunter app 3282300のSteamDB埋め込みです。公式発表ではなく、第三者の参考チャートとして扱ってください。", "open_chart": "SteamDBのライブチャートを開く", "sources": "確認ソース", "steamdb_desc": "現在数、日次ピーク、Steam上の履歴を確認できます。", "steam_desc": "プラットフォーム、発売日、販売元、ストア情報の公式ページです。", "steam_info": "Mistfall Hunter Steam情報", "steam_info_desc": "公式プラットフォーム情報を確認します。", "classes": "Mistfall Hunterクラスガイド", "classes_desc": "活動時間を見たあとに役割を選びます。", "planner": "Mistfall Hunterビルドプランナー", "planner_desc": "ソロや分隊の方針に合うクラスを探します。", "price": "Mistfall Hunter価格ガイド", "price_desc": "プレイヤー数と価格、返金条件を合わせて確認します。"},
        "fr": {"embed_title": "Graphique SteamDB en direct", "embed_caption": "Integration SteamDB pour Mistfall Hunter app 3282300. A utiliser comme graphique tiers indicatif, pas comme declaration officielle.", "open_chart": "Ouvrir le graphique SteamDB en direct", "sources": "Sources de verification", "steamdb_desc": "Joueurs actuels, pic quotidien et contexte historique Steam.", "steam_desc": "Page officielle pour plateforme, sortie, editeur et boutique.", "steam_info": "Infos Steam Mistfall Hunter", "steam_info_desc": "Verifier les faits officiels de plateforme.", "classes": "Guide des classes Mistfall Hunter", "classes_desc": "Choisir un role apres les horaires actifs.", "planner": "Planificateur de build Mistfall Hunter", "planner_desc": "Associer une classe au plan solo ou escouade.", "price": "Prix de Mistfall Hunter", "price_desc": "Croiser activite, prix et conditions de remboursement."},
        "de": {"embed_title": "Live-SteamDB-Chart", "embed_caption": "SteamDB-Einbettung fuer Mistfall Hunter App 3282300. Als Drittanbieter-Chart lesen, nicht als offizielle Aussage.", "open_chart": "Live-SteamDB-Chart offnen", "sources": "Pruefquellen", "steamdb_desc": "Aktuelle Spieler, Tagespeak und Steam-Historie.", "steam_desc": "Offizielle Seite fuer Plattform, Release, Publisher und Store.", "steam_info": "Mistfall Hunter Steam-Info", "steam_info_desc": "Offizielle Plattformdaten pruefen.", "classes": "Mistfall Hunter Klassenleitfaden", "classes_desc": "Rolle nach Aktivitaetsfenster waehlen.", "planner": "Mistfall Hunter Build-Planer", "planner_desc": "Klasse auf Solo- oder Gruppenplan abstimmen.", "price": "Mistfall Hunter Preis", "price_desc": "Aktivitaet mit Preis und Rueckerstattung abgleichen."},
        "pt": {"embed_title": "Grafico SteamDB ao vivo", "embed_caption": "Embed do SteamDB para Mistfall Hunter app 3282300. Use como grafico direcional de terceiros, nao como comunicado oficial.", "open_chart": "Abrir o grafico ao vivo do SteamDB", "sources": "Fontes de verificacao", "steamdb_desc": "Jogadores atuais, pico diario e historico Steam.", "steam_desc": "Pagina oficial de plataforma, lancamento, publicadora e loja.", "steam_info": "Mistfall Hunter no Steam", "steam_info_desc": "Verifique dados oficiais de plataforma.", "classes": "Guia de classes Mistfall Hunter", "classes_desc": "Escolha papel depois de ver horarios ativos.", "planner": "Planejador de build Mistfall Hunter", "planner_desc": "Combine classe com plano solo ou equipe.", "price": "Preco de Mistfall Hunter", "price_desc": "Cruze atividade, preco e reembolso."},
        "ko": {"embed_title": "실시간 SteamDB 차트", "embed_caption": "Mistfall Hunter app 3282300용 SteamDB 임베드입니다. 공식 발표가 아닌 제3자 참고 차트로 보세요.", "open_chart": "실시간 SteamDB 차트 열기", "sources": "확인 출처", "steamdb_desc": "현재 플레이어, 일일 피크, Steam 기록 맥락.", "steam_desc": "플랫폼, 출시, 퍼블리셔, 스토어 공식 페이지.", "steam_info": "Mistfall Hunter Steam 정보", "steam_info_desc": "공식 플랫폼 정보를 확인합니다.", "classes": "Mistfall Hunter 클래스 가이드", "classes_desc": "활동 시간 확인 후 역할을 고릅니다.", "planner": "Mistfall Hunter 빌드 플래너", "planner_desc": "솔로 또는 스쿼드 계획에 맞는 클래스를 찾습니다.", "price": "Mistfall Hunter 가격 가이드", "price_desc": "활동 추이와 가격, 환불 조건을 함께 확인합니다."},
        "it": {"embed_title": "Grafico SteamDB live", "embed_caption": "Embed SteamDB per Mistfall Hunter app 3282300. Usalo come grafico terzo indicativo, non come dichiarazione ufficiale.", "open_chart": "Apri il grafico SteamDB live", "sources": "Fonti di verifica", "steamdb_desc": "Giocatori attuali, picco giornaliero e storico Steam.", "steam_desc": "Pagina ufficiale per piattaforma, uscita, editore e store.", "steam_info": "Info Steam Mistfall Hunter", "steam_info_desc": "Verifica dati ufficiali di piattaforma.", "classes": "Guida classi Mistfall Hunter", "classes_desc": "Scegli ruolo dopo gli orari attivi.", "planner": "Planner build Mistfall Hunter", "planner_desc": "Abbina classe a piano solo o squadra.", "price": "Prezzo Mistfall Hunter", "price_desc": "Unisci attivita, prezzo e rimborso."},
    }[locale]
    sections = [
        {"type": "embed", "title": common["embed_title"], "src": STEAMDB_EMBED_URL, "link_href": STEAMDB_CHARTS_URL, "caption": common["embed_caption"], "link_label": common["open_chart"]},
        {"type": "rich", "title": detail["quick_title"], "paragraphs": detail["quick"]},
        {"type": "table", "title": detail["signals_title"], "headers": detail["signal_headers"], "rows": detail["signal_rows"]},
        {"type": "rich", "title": detail["limits_title"], "paragraphs": detail["limits"]},
        {"type": "table", "title": detail["queue_title"], "headers": detail["queue_headers"], "rows": detail["queue_rows"]},
        {"type": "faq", "title": copy["faq_title"], "items": detail["faq"]},
        {"type": "links", "title": common["sources"], "items": [["SteamDB Mistfall Hunter charts", STEAMDB_CHARTS_URL, common["steamdb_desc"], "nofollow noopener"], ["Official Steam page", OFFICIAL_STEAM_URL, common["steam_desc"]]]},
        {"type": "related", "title": copy["related_title"], "items": [[common["steam_info"], get_page_path("steam", locale), common["steam_info_desc"]], [common["classes"], get_page_path("classes", locale), common["classes_desc"]], [common["planner"], get_page_path("build-planner", locale), common["planner_desc"]], [common["price"], get_page_path("price", locale), common["price_desc"]]]},
    ]
    return {"page": {"title": copy["title"], "description": copy["description"], "h1": copy["h1"], "kicker": copy["kicker"]}, "sections": sections}

PRICE_RELATED_COPY = {
    "en": {"title": "Related Mistfall Hunter guides", "price_label": "Mistfall Hunter price guide", "price_desc": "Check the current Steam price, discount, and buyer cautions.", "steam_label": "Mistfall Hunter Steam info", "steam_desc": "Verify official platform, developer, publisher, and store facts.", "classes_label": "Mistfall Hunter classes guide", "classes_desc": "Compare roles before deciding whether the game fits your play style.", "planner_label": "Mistfall Hunter build planner", "planner_desc": "Match a class direction to solo, duo, or squad runs."},
    "es": {"title": "Guias relacionadas de Mistfall Hunter", "price_label": "Precio de Mistfall Hunter", "price_desc": "Revisa precio, descuento y cautelas de compra.", "steam_label": "Mistfall Hunter en Steam", "steam_desc": "Verifica plataforma y datos oficiales.", "classes_label": "Guia de clases", "classes_desc": "Compara roles antes de comprar.", "planner_label": "Planificador de builds", "planner_desc": "Elige direccion para solo, duo o escuadron."},
    "fr": {"title": "Ressources Mistfall Hunter liees", "price_label": "Prix de Mistfall Hunter", "price_desc": "Verifiez prix, remise et precautions d achat.", "steam_label": "Infos Steam Mistfall Hunter", "steam_desc": "Confirmez plateforme et sources officielles.", "classes_label": "Manuel des classes", "classes_desc": "Comparez les roles avant achat.", "planner_label": "Planificateur de build", "planner_desc": "Trouvez une direction solo, duo ou escouade."},
    "de": {"title": "Verwandte Mistfall Hunter Guides", "price_label": "Mistfall Hunter Preis", "price_desc": "Pruefe Preis, Rabatt und Kaufhinweise.", "steam_label": "Mistfall Hunter Steam-Info", "steam_desc": "Offizielle Plattform- und Store-Fakten.", "classes_label": "Klassenleitfaden", "classes_desc": "Vergleiche Rollen vor dem Kauf.", "planner_label": "Build-Planer", "planner_desc": "Finde eine Richtung fuer Solo, Duo oder Gruppe."},
    "pt": {"title": "Guias relacionados de Mistfall Hunter", "price_label": "Preco de Mistfall Hunter", "price_desc": "Confira preco, desconto e cuidados de compra.", "steam_label": "Mistfall Hunter no Steam", "steam_desc": "Verifique plataforma e dados oficiais.", "classes_label": "Guia de classes", "classes_desc": "Compare papeis antes de comprar.", "planner_label": "Planejador de build", "planner_desc": "Escolha direcao para solo, duo ou equipe."},
    "it": {"title": "Risorse Mistfall Hunter correlate", "price_label": "Prezzo Mistfall Hunter", "price_desc": "Controlla prezzo, sconto e note d acquisto.", "steam_label": "Info Steam Mistfall Hunter", "steam_desc": "Verifica piattaforma e fonti ufficiali.", "classes_label": "Guida classi", "classes_desc": "Confronta ruoli prima dell acquisto.", "planner_label": "Planner build", "planner_desc": "Scegli una direzione per solo, duo o squadra."},
    "ja": {"title": "関連するMistfall Hunterガイド", "price_label": "Mistfall Hunter 価格ガイド", "price_desc": "価格、割引、購入前の注意を確認します。", "steam_label": "Mistfall Hunter Steam情報", "steam_desc": "公式平台とストア情報を確認します。", "classes_label": "クラスガイド", "classes_desc": "購入前に役割を比較します。", "planner_label": "ビルドプランナー", "planner_desc": "ソロ、デュオ、分隊の方向性を選びます。"},
    "ko": {"title": "관련 Mistfall Hunter 가이드", "price_label": "Mistfall Hunter 가격 가이드", "price_desc": "가격, 할인, 구매 주의점을 확인합니다.", "steam_label": "Mistfall Hunter Steam 정보", "steam_desc": "공식 플랫폼과 상점 정보를 확인합니다.", "classes_label": "클래스 가이드", "classes_desc": "구매 전 역할을 비교합니다.", "planner_label": "빌드 플래너", "planner_desc": "솔로, 듀오, 분대 방향을 고릅니다."},
}

SIMPLE_LABELS = {
    "en": {"class_table": "Class role comparison", "class_headers": ["Class", "Best role", "When to pick it"], "planner_table": "Example planner inputs", "planner_headers": ["Situation", "Inputs", "Likely direction"], "steam_faq": "Mistfall Hunter Steam FAQ", "planner_faq": "Mistfall Hunter build planner FAQ", "game": "Game", "developer": "Developer", "publisher": "Publisher", "release": "Release", "platform": "Platform"},
    "es": {"class_table": "Comparación de roles", "class_headers": ["Clase", "Mejor rol", "Cuándo elegirla"], "planner_table": "Ejemplos del planificador", "planner_headers": ["Situación", "Opciones", "Dirección probable"], "steam_faq": "Preguntas frecuentes de Steam", "planner_faq": "Preguntas frecuentes del planificador", "game": "Juego", "developer": "Desarrollador", "publisher": "Editor", "release": "Lanzamiento", "platform": "Plataforma"},
    "ja": {"class_table": "クラス役割比較", "class_headers": ["クラス", "主な役割", "選ぶ場面"], "planner_table": "プランナー入力例", "planner_headers": ["状況", "入力", "方向性"], "steam_faq": "Steam情報 よくある質問", "planner_faq": "ビルドプランナー よくある質問", "game": "ゲーム", "developer": "開発元", "publisher": "発売元", "release": "発売日", "platform": "プラットフォーム"},
    "fr": {"class_table": "Comparaison des rôles", "class_headers": ["Classe", "Meilleur rôle", "Quand la choisir"], "planner_table": "Exemples du planificateur", "planner_headers": ["Situation", "Réglages", "Direction probable"], "steam_faq": "Questions fréquentes Steam", "planner_faq": "Questions fréquentes du planificateur", "game": "Jeu", "developer": "Développeur", "publisher": "Éditeur", "release": "Sortie", "platform": "Plateforme"},
    "de": {"class_table": "Klassenrollen im Vergleich", "class_headers": ["Klasse", "Beste Rolle", "Wann wählen"], "planner_table": "Beispiel-Eingaben", "planner_headers": ["Situation", "Eingaben", "Wahrscheinliche Richtung"], "steam_faq": "Häufige Fragen zu Steam", "planner_faq": "Häufige Fragen zum Build-Planer", "game": "Spiel", "developer": "Entwickler", "publisher": "Publisher", "release": "Veröffentlichung", "platform": "Plattform"},
    "pt": {"class_table": "Comparação de papéis", "class_headers": ["Classe", "Melhor papel", "Quando escolher"], "planner_table": "Exemplos do planejador", "planner_headers": ["Situação", "Entradas", "Direção provável"], "steam_faq": "Perguntas frequentes do Steam", "planner_faq": "Perguntas frequentes do planejador", "game": "Jogo", "developer": "Desenvolvedor", "publisher": "Publicadora", "release": "Lançamento", "platform": "Plataforma"},
    "ko": {"class_table": "클래스 역할 비교", "class_headers": ["클래스", "주요 역할", "선택 시점"], "planner_table": "플래너 입력 예시", "planner_headers": ["상황", "입력", "예상 방향"], "steam_faq": "Steam 정보 자주 묻는 질문", "planner_faq": "빌드 플래너 자주 묻는 질문", "game": "게임", "developer": "개발사", "publisher": "배급사", "release": "출시일", "platform": "플랫폼"},
    "it": {"class_table": "Confronto ruoli classe", "class_headers": ["Classe", "Ruolo migliore", "Quando sceglierla"], "planner_table": "Esempi del planner", "planner_headers": ["Situazione", "Input", "Direzione probabile"], "steam_faq": "Domande frequenti Steam", "planner_faq": "Domande frequenti del planner", "game": "Gioco", "developer": "Sviluppatore", "publisher": "Editore", "release": "Uscita", "platform": "Piattaforma"},
}


def get_locale_text(locale):
    """
    获取指定语言的站点文案。

    :param locale: 语言代码
    :return: dict，指定语言的完整文案数据
    """
    return TEXT[locale]


def get_page_path(page_key, locale="en"):
    """
    根据页面和语言生成规范化站内路径。

    :param page_key: 页面标识
    :param locale: 语言代码
    :return: str，带尾斜杠的站内路径
    """
    slug = PAGE_SLUGS[page_key]
    if locale == "en":
        return "/" if not slug else f"/{slug}/"
    return f"/{locale}/" if not slug else f"/{locale}/{slug}/"


REVIEW_PAGE_DATA = {
    "en": {
        "page": {
            "title": "Mistfall Hunter Review: Is It Worth Buying on Steam?",
            "description": "This practical Mistfall Hunter review weighs the extraction loop, class learning curve, Steam price, player activity, and who should buy.",
            "h1": "Mistfall Hunter Review: Is It Worth Buying on Steam?",
            "kicker": "Mistfall Hunter review | Updated August 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-review-verdict.webp", "alt": "Editorial illustration of a Mistfall Hunter reviewing an extraction route", "caption": "Editorial illustration generated for this fan-made review; it is not an official gameplay screenshot."},
            {"type": "rich", "title": "Quick verdict: a promising extraction ARPG for the right player", "paragraphs": [
                "Our Mistfall Hunter review verdict is conditional: the game is worth considering if you enjoy extraction PvPvE, repeated runs, risky gear decisions, and learning a role through play. It is not an easy recommendation for someone looking for a short single-player campaign or a fixed, low-stress progression path. The useful question is not whether the game is universally good. It is whether its loop gives you a reason to return after a successful extraction and a reason to try again after losing a kit.",
                "Mistfall Hunter has a strong starting point for players who like making decisions under pressure. You choose a route, read danger, decide when to fight, and weigh the value of staying longer against the value of leaving with what you have. That structure makes class choice matter, because a forgiving frontline role changes the kinds of mistakes you can survive while a burst or control role asks for cleaner timing.",
                "The main caution is freshness. Early advice can change as players discover routes, balance shifts, and the Steam community forms a clearer view of matchmaking and performance. Treat this as an independent decision guide, not an official tier list or a promise of a permanent meta. Check the live Steam page, recent reviews, and your own PC compatibility before paying."
            ]},
            {"type": "table", "title": "Mistfall Hunter review at a glance", "headers": ["Question", "Review answer", "Why it matters"], "rows": [
                ["What kind of game is it?", "Extraction PvPvE ARPG", "Runs combine combat, route choices, loot risk, and an extraction decision."],
                ["Who is the best fit?", "Players who enjoy repeatable high-stakes runs", "The core appeal comes from decisions and learning, not a one-time story finish."],
                ["Is it beginner-friendly?", "Yes with the right class, but not frictionless", "Mercenary or Withered Knight can reduce early punishment while you learn the loop."],
                ["Should you buy immediately?", "Only after checking live Steam facts", "Price, reviews, requirements, and activity can change after launch."],
                ["What is this site's stance?", "Independent fan guidance", "Class recommendations are editorial and separate from official Steam facts."]
            ]},
            {"type": "rich", "title": "What the Mistfall Hunter game loop asks of you", "paragraphs": [
                "An extraction game asks you to manage an incomplete plan. You enter with a goal, but the route, enemies, loot, and other players can force a new decision. The most valuable skill is often knowing when a small gain is enough. Staying for one more chest or fight may improve the run, but it can also turn a safe exit into a lost loadout. That tension gives the game its identity and also explains why the first hours may feel less comfortable than a conventional action RPG.",
                "The loop rewards information as much as mechanical execution. You need to recognize when a fight is favorable, when your class has its strongest window, and when your squad has already spent the resources needed to continue. A good build therefore is not only a damage list. It is a plan for positioning, recovery, disengagement, and the kind of risk your group can communicate clearly.",
                "Solo and squad play can feel like different products. Solo runs place more weight on self-recovery, information, and mistakes you can correct alone. A coordinated squad can turn control, anchoring, and scouting into shared safety, but it also creates a communication burden. Before judging the game, play enough sessions in the format you actually intend to use. A class or mode that feels awkward in a random group may feel excellent with friends."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Official Steam artwork showing Mistfall Hunter characters in a snowy battle", "caption": "Official Steam artwork used to identify the game and set the review's visual context; it is not a performance benchmark."},
            {"type": "rich", "title": "Classes and the learning curve", "paragraphs": [
                "The class system is one of the site's strongest reasons to review Mistfall Hunter through player fit rather than a single winner. Mercenary offers a clearer frontline pattern and is a sensible first stop for players who need room to make mistakes. Withered Knight adds durability and space control for players who want to anchor a group. These choices may not produce the biggest highlight moments, but they make the game's decision language easier to read.",
                "Blackarrow, Shadowstrix, and Sorcerer ask for more deliberate timing. Blackarrow rewards range, scouting, and choosing when to apply pressure. Shadowstrix can create strong ambush and disengage moments, but its mistakes are exposed quickly. Sorcerer offers burst and area control while asking the player to understand positioning and cooldown windows. Seer sits on the utility side of the spectrum: its value rises when information, control, and safer squad calls matter more than personal damage.",
                "For a first session, use the class guide and build planner as a starting map, not a command. Pick one job you can describe in a sentence, then test whether the class actually helps you survive and communicate. If two recommendations are close, treat them as a tie and choose the role your squad lacks. That approach remains useful even when a future patch changes individual values."
            ]},
            {"type": "table", "title": "Who should start with which class?", "headers": ["Player need", "Good starting direction", "Tradeoff to understand"], "rows": [
                ["First solo sessions", "Mercenary", "Safer mistakes, but less burst spectacle."],
                ["Squad anchor", "Withered Knight", "You trade some damage for space and durability."],
                ["Range and scouting", "Blackarrow", "Positioning and patience matter more than face-tanking."],
                ["Aggressive flanks", "Shadowstrix", "High payoff comes with a sharper punishment curve."],
                ["Area pressure or utility", "Sorcerer or Seer", "Choose between burst control and team information."]
            ]},
            {"type": "rich", "title": "Strengths, tradeoffs, and what to verify", "paragraphs": [
                "The strongest part of Mistfall Hunter is the decision density. Even a short run can ask you to compare time, noise, equipment value, enemy pressure, and the needs of the next fight. That makes a successful extraction feel earned rather than automatic. The class planner supports this strength because it frames a role around solo, duo, or squad conditions instead of pretending that one score fits every player.",
                "The tradeoff is that the game can feel demanding before its habits become familiar. If you dislike losing progress, cautious exits, or repeating a route to improve your read of it, the central loop may feel like friction. If you enjoy studying patterns and turning a failed run into a better plan, the same friction becomes the reason to return. Neither response is a skill issue; it is a fit question.",
                "Before buying, verify four live details: the current Steam price in your region, recent user-review direction, PC requirements and performance reports, and the player activity during your normal play time. The existing price and player-count guides cover those checks in more detail. The review should help you decide what to inspect, not replace the official store page or current community evidence."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Official Mistfall Hunter Steam header in a dark forest", "caption": "Official Steam header used as a second identification reference; the review does not treat store art as gameplay evidence."},
            {"type": "rich", "title": "How to use this review before buying", "paragraphs": [
                "Start with the format you will actually play. If you will mostly queue solo, read the solo sections of the class guide and use a forgiving recommendation as your baseline. If you will play with friends, compare the jobs your group already has and use the build planner to test a missing role. This avoids buying for an imagined meta while ignoring the way your own group communicates.",
                "Next, separate stable facts from changing signals. Developer, publisher, platform, and store identity belong to the official Steam listing. Price, reviews, queue feel, and class strength are time-sensitive. A review can explain how to interpret those signals, but it should date its assumptions and avoid turning one early impression into a permanent verdict.",
                "The short conclusion is simple: buy when the extraction loop itself sounds appealing, your system is supported, and the live Steam evidence matches your expectations. Wait when you are only reacting to launch momentum, a discount countdown, or a claimed best class. That decision rule is more durable than a numeric rating and leaves room for the game to improve or change."
            ]},
            {"type": "table", "title": "Buy now, wait, or skip?", "headers": ["Your situation", "Practical choice", "Reason"], "rows": [
                ["You already enjoy extraction PvPvE", "Consider buying after live checks", "The core loop is likely aligned with your taste."],
                ["You want a relaxed campaign", "Wait or skip", "Loss risk and repeated runs may feel like the wrong structure."],
                ["You have a fixed squad", "Check class coverage first", "Role fit can turn the same game into a better group experience."],
                ["Your PC or region is uncertain", "Wait", "Confirm requirements, regional price, and current reviews."],
                ["You are chasing a temporary meta", "Do not rush", "Early class advice can move with patches and new evidence."]
            ]},
            {"type": "faq", "title": "Mistfall Hunter review FAQ", "items": [
                ["Is Mistfall Hunter worth buying?", "It is worth considering when you enjoy extraction PvPvE, repeatable runs, and making risk decisions under pressure. Check the live Steam price, requirements, recent reviews, and player activity before buying."],
                ["Is Mistfall Hunter good for solo players?", "It can be, but solo places more weight on self-recovery, information, and forgiving class choices. Mercenary is a practical starting point; test the class before treating the recommendation as final."],
                ["What is the best class for a new player?", "Mercenary is the clearest low-risk starting direction in this site's model. Withered Knight is another sensible option for players who prefer a durable squad role."],
                ["Does this review give an official score?", "No. It is an independent fan review and decision guide. A fixed score would hide how much the answer depends on mode, class preference, PC setup, and current balance."],
                ["Where should I check current price and player count?", "Use the official Steam listing for the regional price and product facts, then use a live SteamDB chart as a third-party activity signal. The site's price and player-count guides explain what to compare."],
                ["Will this review stay accurate after patches?", "The decision framework should remain useful, but class strength, performance, queue timing, and value can change. Recheck official patch information and recent player evidence before relying on old details."]
            ]},
            {"type": "links", "title": "Review sources and verification", "items": [
                ["Official Mistfall Hunter Steam page", OFFICIAL_STEAM_URL, "Product identity, platform, price, requirements, reviews, and current store state.", "noopener"],
                ["SteamDB Mistfall Hunter charts", STEAMDB_CHARTS_URL, "Third-party current-player and peak context; interpret as directional activity data.", "nofollow noopener"],
                ["Steam refund policy", "https://store.steampowered.com/steam_refunds/", "Check the current platform rules before paying.", "nofollow noopener"]
            ]},
            {"type": "related", "title": "Continue with related Mistfall Hunter guides", "items": [
                ["Mistfall Hunter classes guide", get_page_path("classes", "en"), "Compare role fit, risk, and beginner directions."],
                ["Mistfall Hunter build planner", get_page_path("build-planner", "en"), "Match a class direction to solo, duo, or squad play."],
                ["Mistfall Hunter player count guide", get_page_path("player-count", "en"), "Read SteamDB signals and queue timing without overclaiming."],
                ["Mistfall Hunter price guide", get_page_path("price", "en"), "Check price snapshots, discounts, and buyer cautions."],
                ["Mistfall Hunter Steam info", get_page_path("steam", "en"), "Verify official platform and release facts."]
            ]}
        ]
    }
}


REVIEW_PAGE_DATA.update({
    "es": {
        "page": {
            "title": "Reseña de Mistfall Hunter: ¿vale la pena comprarlo?",
            "description": "Reseña práctica de Mistfall Hunter sobre el bucle de extracción, clases, precio de Steam, actividad y quién debería comprar.",
            "h1": "Reseña de Mistfall Hunter: ¿vale la pena comprarlo?",
            "kicker": "Reseña de Mistfall Hunter | Actualizada en agosto de 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-review-verdict.webp", "alt": "Ilustración editorial de una ruta de extracción de Mistfall Hunter", "caption": "Ilustración editorial generada para esta reseña hecha por fans; no es una captura oficial del juego."},
            {"type": "rich", "title": "Veredicto rápido: buen juego de extracción para el jugador adecuado", "paragraphs": [
                "Nuestra reseña de Mistfall Hunter llega a un veredicto condicionado: merece consideración si te gustan el PvPvE de extracción, las partidas repetibles, el riesgo de perder equipo y aprender un rol jugando. No es una recomendación automática para quien busca una campaña corta y relajada o una progresión sin retrocesos. La pregunta útil no es si es bueno para todo el mundo, sino si sus decisiones de ruta, combate y extracción te dan motivos para volver.",
                "El juego funciona mejor cuando disfrutas decidir bajo presión. Entras con un plan, lees el peligro, eliges cuándo pelear y comparas el valor de seguir explorando con el valor de salir con lo que ya tienes. Por eso las clases importan: un rol frontal puede perdonar un fallo que un personaje de ráfaga no perdona, mientras que apoyo y control exigen comunicación más limpia.",
                "La principal cautela es que se trata de un juego reciente. Las rutas, el equilibrio, el rendimiento y la sensación de encontrar partida pueden cambiar mientras la comunidad aprende. Usa esta página como guía independiente, no como tier list oficial. Antes de pagar, revisa la página de Steam, las reseñas recientes, los requisitos de tu PC y la actividad en tu horario normal."
            ]},
            {"type": "table", "title": "Mistfall Hunter: resumen de la reseña", "headers": ["Pregunta", "Respuesta", "Por qué importa"], "rows": [
                ["¿Qué tipo de juego es?", "ARPG PvPvE de extracción", "Cada partida mezcla combate, decisiones de ruta, botín y una salida con riesgo."],
                ["¿Para quién encaja?", "Para quien disfruta partidas tensas y repetibles", "La gracia está en aprender y decidir, no solo en terminar una historia."],
                ["¿Es fácil para empezar?", "Sí con una clase adecuada, pero no sin fricción", "Mercenary o Withered Knight dan más margen mientras aprendes."],
                ["¿Comprar ya?", "Solo después de revisar Steam en directo", "Precio, reseñas, requisitos y actividad pueden cambiar."],
                ["¿Qué postura tiene esta web?", "Guía independiente hecha por fans", "Las recomendaciones son editoriales y no datos oficiales."]
            ]},
            {"type": "rich", "title": "Qué te pide el bucle de juego", "paragraphs": [
                "Un juego de extracción empieza con un plan incompleto. La ruta, los enemigos, el botín y otros jugadores obligan a cambiarlo. A menudo la habilidad más importante es reconocer cuándo una ganancia pequeña ya es suficiente. Quedarte por otro cofre puede mejorar la partida, pero también convertir una salida segura en una pérdida de equipo. Esa tensión explica tanto el atractivo como la incomodidad de las primeras horas.",
                "El bucle premia la información además de la ejecución. Debes reconocer qué pelea conviene, cuándo tu clase tiene su mejor ventana y cuándo el grupo ya gastó recursos para continuar. Una build, por tanto, no es solo daño: también es posición, recuperación, retirada y un nivel de riesgo que el equipo pueda comunicar.",
                "Solo y escuadrón pueden sentirse como experiencias distintas. En solo pesan la recuperación y la información que puedes conseguir por tu cuenta. En grupo, el control, la exploración y un ancla resistente crean seguridad compartida, pero exigen coordinación. Juega varias sesiones en el formato que realmente usarás antes de decidir si el juego te encaja."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Arte oficial de Steam de Mistfall Hunter durante una batalla nevada", "caption": "Arte oficial de Steam para identificar el juego y contextualizar la reseña; no demuestra rendimiento."},
            {"type": "rich", "title": "Clases y curva de aprendizaje", "paragraphs": [
                "La forma más útil de valorar las clases de Mistfall Hunter es pensar en el jugador y la partida, no en un ganador universal. Mercenary ofrece una línea frontal fácil de leer y es un buen primer paso si necesitas margen para equivocarte. Withered Knight añade resistencia y control de espacio para quien quiere anclar al equipo. Quizá no producen los momentos más llamativos, pero hacen más comprensible el lenguaje del juego.",
                "Blackarrow, Shadowstrix y Sorcerer piden un timing más deliberado. Blackarrow premia distancia, exploración y presión paciente. Shadowstrix puede crear emboscadas fuertes, pero castiga pronto un mal cálculo. Sorcerer aporta ráfaga y control de área mientras exige entender posición y enfriamientos. Seer se acerca al lado de utilidad: sube de valor cuando la información y las decisiones seguras del escuadrón importan más que el daño individual.",
                "Para tu primera sesión, usa la guía de clases y el planificador como mapa, no como orden. Elige un trabajo que puedas explicar en una frase y comprueba si realmente te ayuda a sobrevivir y comunicarte. Si dos resultados quedan cerca, trátalos como empate y cubre el rol que falta. Así la recomendación sigue siendo útil aunque un parche cambie valores concretos."
            ]},
            {"type": "table", "title": "Dirección inicial según tu necesidad", "headers": ["Necesidad", "Dirección", "Coste o riesgo"], "rows": [
                ["Primeras partidas en solo", "Mercenary", "Perdona más fallos, pero tiene menos ráfaga."],
                ["Ancla del escuadrón", "Withered Knight", "Cambia parte del daño por espacio y resistencia."],
                ["Distancia y exploración", "Blackarrow", "La posición y la paciencia son esenciales."],
                ["Flancos agresivos", "Shadowstrix", "Mayor recompensa con curva de castigo más dura."],
                ["Área o utilidad", "Sorcerer o Seer", "Elige entre control explosivo e información para el grupo."]
            ]},
            {"type": "rich", "title": "Puntos fuertes, límites y comprobaciones", "paragraphs": [
                "La mayor fortaleza de Mistfall Hunter es la densidad de decisiones. Una partida corta puede pedirte comparar tiempo, ruido, valor del equipo, presión enemiga y necesidades de la siguiente pelea. Una extracción exitosa se siente ganada porque no todo está automatizado. El planificador de clases refuerza esa idea al separar solo, dúo y escuadrón en vez de imponer una puntuación universal.",
                "El coste es que el juego puede sentirse exigente antes de que sus hábitos sean familiares. Si no te gustan perder progreso, salir con poco o repetir una ruta para leerla mejor, el bucle puede parecer fricción. Si disfrutas convertir una partida fallida en un plan mejor, la misma fricción se convierte en motivo para volver. Es una cuestión de encaje, no de habilidad.",
                "Antes de comprar, comprueba cuatro datos que cambian: precio local en Steam, dirección de las reseñas recientes, requisitos y rendimiento en tu PC, y actividad en tu horario. Las guías de precio y jugadores de esta web explican esos controles. Esta reseña te dice qué mirar, pero no sustituye la tienda oficial ni la evidencia actual de jugadores."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Cabecera oficial de Mistfall Hunter en Steam", "caption": "Cabecera oficial usada como segunda referencia de identidad; no se presenta como prueba de jugabilidad."},
            {"type": "rich", "title": "Cómo usar esta reseña antes de comprar", "paragraphs": [
                "Empieza por el formato que jugarás de verdad. Si vas a jugar solo, lee las partes de solo de la guía de clases y toma una recomendación permisiva como base. Si jugarás con amigos, revisa qué roles ya tiene el grupo y prueba el hueco con el planificador. Así no compras persiguiendo una meta imaginaria que no coincide con la forma en que jugáis.",
                "Después separa hechos estables de señales cambiantes. El nombre del producto, la plataforma, el desarrollador y la tienda pertenecen a Steam oficial. Precio, reseñas, colas y fuerza de las clases son temporales. Una reseña puede explicar cómo leer esas señales, pero debe fechar sus supuestos y no convertir una primera impresión en una sentencia permanente.",
                "La conclusión corta es: compra cuando el bucle de extracción te atraiga, tu PC sea compatible y la evidencia viva de Steam coincida con tus expectativas. Espera si solo reaccionas al impulso de lanzamiento, a una cuenta atrás de descuento o a una supuesta mejor clase. Esa regla dura más que una nota numérica y deja espacio para futuros cambios."
            ]},
            {"type": "table", "title": "¿Comprar, esperar o pasar?", "headers": ["Situación", "Decisión práctica", "Motivo"], "rows": [
                ["Te gusta el PvPvE de extracción", "Considera comprar tras comprobar datos", "El bucle central encaja con tus gustos."],
                ["Quieres una campaña relajada", "Espera o pasa", "El riesgo de pérdida puede no encajarte."],
                ["Tienes un escuadrón fijo", "Comprueba la cobertura de roles", "La clase puede mejorar la experiencia del grupo."],
                ["Tu PC o región son inciertos", "Espera", "Confirma requisitos, precio y reseñas actuales."],
                ["Solo persigues la meta del momento", "No te apresures", "Los parches pueden cambiar las recomendaciones."]
            ]},
            {"type": "faq", "title": "Preguntas frecuentes de la reseña de Mistfall Hunter", "items": [
                ["¿Vale la pena comprar Mistfall Hunter?", "Puede valer la pena si te gustan el PvPvE de extracción, las partidas repetibles y decidir bajo presión. Comprueba precio, requisitos, reseñas recientes y actividad en Steam antes de pagar."],
                ["¿Es bueno para jugar en solo?", "Puede serlo, pero el solo exige más recuperación, información y una clase permisiva. Mercenary es una dirección práctica de inicio; pruébala antes de tomarla como definitiva."],
                ["¿Cuál es la mejor clase para empezar?", "Mercenary es la dirección de bajo riesgo más clara en el modelo de esta web. Withered Knight también es razonable si prefieres un rol resistente en escuadrón."],
                ["¿La reseña tiene una puntuación oficial?", "No. Es una reseña independiente hecha por fans y una guía de decisión. Una nota fija ocultaría cuánto depende la respuesta del modo, la clase, el PC y el equilibrio actual."],
                ["¿Dónde miro el precio y los jugadores actuales?", "Usa Steam oficial para el precio regional y los datos del producto. Después consulta un gráfico de SteamDB como señal externa de actividad; las guías de precio y jugadores explican la comparación."],
                ["¿Seguirá siendo válida después de un parche?", "El marco de decisión debería servir, pero fuerza de clases, rendimiento, colas y valor pueden cambiar. Revisa notas oficiales y evidencia reciente antes de confiar en detalles antiguos."]
            ]},
            {"type": "links", "title": "Fuentes y comprobaciones", "items": [
                ["Página oficial de Mistfall Hunter en Steam", OFFICIAL_STEAM_URL, "Identidad, plataforma, precio, requisitos, reseñas y estado actual.", "noopener"],
                ["Gráficos de Mistfall Hunter en SteamDB", STEAMDB_CHARTS_URL, "Contexto de jugadores actuales y picos; úsalo como señal direccional.", "nofollow noopener"],
                ["Política de reembolsos de Steam", "https://store.steampowered.com/steam_refunds/", "Consulta las reglas actuales antes de pagar.", "nofollow noopener"]
            ]},
            {"type": "related", "title": "Más guías relacionadas de Mistfall Hunter", "items": [
                ["Guía de clases de Mistfall Hunter", get_page_path("classes", "es"), "Compara roles, riesgo y direcciones para principiantes."],
                ["Planificador de builds de Mistfall Hunter", get_page_path("build-planner", "es"), "Une una clase con juego solo, dúo o escuadrón."],
                ["Guía de jugadores de Mistfall Hunter", get_page_path("player-count", "es"), "Lee señales de SteamDB y horarios de cola."],
                ["Guía de precio de Mistfall Hunter", get_page_path("price", "es"), "Revisa precio, descuentos y cautelas de compra."],
                ["Información de Mistfall Hunter en Steam", get_page_path("steam", "es"), "Comprueba datos oficiales de plataforma y lanzamiento."]
            ]}
        ]
    }
})


REVIEW_PAGE_DATA.update({
    "ja": {
        "page": {
            "title": "Mistfall Hunter 評価レビュー：Steamで買う価値はある？",
            "description": "Mistfall Hunter 評価を、脱出ループ、クラスの学習曲線、Steam価格、人口、購入前の確認点から整理します。",
            "h1": "Mistfall Hunter 評価レビュー：Steamで買う価値はある？",
            "kicker": "Mistfall Hunter 評価 | 2026年8月更新",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-review-verdict.webp", "alt": "Mistfall Hunterの脱出ルートを描いた編集用イラスト", "caption": "このファンレビューのために生成した編集用イラストです。公式ゲーム画面ではありません。"},
            {"type": "rich", "title": "先に結論：合う人には魅力的な脱出ARPG", "paragraphs": [
                "Mistfall Hunter 評価の結論は条件付きです。脱出PvPvE、繰り返すラン、装備を失うリスク、役割をプレイしながら覚える体験が好きなら、購入候補になります。一方、短いソロキャンペーンや、失敗しても進行が戻らないゲームを探しているなら、急いで買う必要はありません。重要なのは、全員におすすめできるかではなく、脱出するたびにもう一度試したくなる判断があるかです。",
                "このゲームは、プレッシャーの中で決めることを楽しめる人に向きます。ルートを選び、危険を読み、戦うか避けるかを決め、今持っている装備で帰るか探索を続けるかを比べます。だからクラス選択にも意味があります。前線役はミスを回収しやすく、瞬間火力や制御役は位置取りとタイミングをより正確に要求します。",
                "注意点は発売直後の新しさです。ルート、バランス、動作、マッチングの感覚はコミュニティの成長とともに変わります。このページは公式ティアリストではなく、独立した購入判断ガイドとして読んでください。支払う前にSteam公式ページ、最近のレビュー、PC環境、普段遊ぶ時間帯の人口を確認しましょう。"
            ]},
            {"type": "table", "title": "Mistfall Hunter 評価の要点", "headers": ["質問", "レビューの答え", "判断材料"], "rows": [
                ["どんなゲーム？", "脱出PvPvE ARPG", "戦闘、ルート、装備リスク、脱出判断を1ランで行います。"],
                ["誰に向く？", "緊張感のある反復ランが好きな人", "一度の物語完了より、判断と学習が中心です。"],
                ["初心者向き？", "クラスを選べば始めやすいが簡単ではない", "MercenaryやWithered Knightは学習中の余裕を作ります。"],
                ["すぐ買うべき？", "Steamの最新情報を確認してから", "価格、レビュー、必要環境、人口は変化します。"],
                ["このサイトの立場は？", "独立したファンガイド", "クラス評価は編集上の目安で、公式情報とは分けています。"]
            ]},
            {"type": "rich", "title": "脱出ループで求められる判断", "paragraphs": [
                "脱出ゲームでは最初から完璧な計画を持てません。ルート、敵、戦利品、他プレイヤーによって計画を変える必要があります。大切なのは、少しの利益で帰るべき時を知ることです。もう一つの宝箱や戦闘は成果を増やしますが、安全な脱出を装備の全損に変えることもあります。この緊張感が個性であり、一般的なアクションRPGより最初の数時間が難しく感じられる理由です。",
                "ループでは操作技術だけでなく情報が重要です。どの戦闘が有利か、クラスの強い時間帯はいつか、分隊が継続に必要な資源を使い切っていないかを見ます。ビルドはダメージ表だけではありません。位置取り、回復、離脱、そしてチームが共有できるリスクの範囲まで含めた方針です。",
                "ソロと分隊は別のゲームのように感じる場合があります。ソロでは自己回復と情報収集、失敗からの立て直しが中心です。連携分隊では制御、偵察、アンカー役が安全を共有できますが、意思疎通が必要です。購入判断の前に、実際に遊ぶ形式で何度かランを試してください。"
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "雪上で戦うMistfall Hunterの公式Steamアート", "caption": "ゲームの正しいストア情報を確認するための公式Steam素材です。性能評価の根拠ではありません。"},
            {"type": "rich", "title": "クラスと学習曲線", "paragraphs": [
                "クラスの評価は、万能な順位ではなく、プレイヤーとランの条件で見るのが実用的です。Mercenaryは前線の仕事が読みやすく、ミスを許容してほしい初心者に向きます。Withered Knightは耐久と空間制御で分隊を支える方向です。派手な瞬間火力は少なくても、ゲームの判断を理解しやすい入口になります。",
                "Blackarrow、Shadowstrix、Sorcererはより正確なタイミングを求めます。Blackarrowは距離、偵察、有利な戦闘選択を活かします。Shadowstrixは奇襲と離脱が強い一方、位置を誤るとすぐに弱点が出ます。Sorcererは瞬間火力と範囲制御を持ち、Seerは個人火力より情報、補助、分隊の安全な判断で価値が上がります。",
                "最初はクラスガイドとビルドプランナーを地図として使い、命令として扱わないでください。自分が説明できる役割を一つ選び、生存と意思疎通に本当に役立つかを試します。二つの候補が近いなら同点として、分隊に足りない役割を選べば、パッチ後も判断方法を保てます。"
            ]},
            {"type": "table", "title": "目的別の初期クラス", "headers": ["目的", "初期候補", "理解しておく弱点"], "rows": [
                ["初めてのソロ", "Mercenary", "ミスに強いが瞬間火力は控えめです。"],
                ["分隊のアンカー", "Withered Knight", "ダメージの一部を耐久と空間制御に回します。"],
                ["遠距離と偵察", "Blackarrow", "正面で受けず、位置と忍耐が必要です。"],
                ["攻撃的な側面攻撃", "Shadowstrix", "見返りが大きいぶん失敗の罰も大きいです。"],
                ["範囲攻撃または補助", "Sorcerer または Seer", "爆発的な制御かチーム情報かを選びます。"]
            ]},
            {"type": "rich", "title": "強み、弱み、購入前に確認すること", "paragraphs": [
                "Mistfall Hunterの強みは判断の密度です。短いランでも、時間、音、装備価値、敵の圧力、次の戦闘に必要な資源を比べます。何も考えずに進めないため、成功した脱出には手応えがあります。クラスプランナーもソロ、デュオ、分隊を分け、単一のスコアを全員に押しつけないことで、この強みを補助します。",
                "一方で、習慣が身につくまでは負荷を感じます。進行を失うこと、少ない戦利品で帰ること、同じルートを読み直すことが苦手なら、ループは摩擦に見えるでしょう。失敗を次の計画に変えることが好きなら、同じ摩擦が再挑戦の理由になります。これは上手さではなく適性の問題です。",
                "購入前に確認するのは、地域のSteam価格、最近のレビューの傾向、PCの必要環境と動作報告、普段遊ぶ時間帯の人口です。価格ガイドとプレイヤー数ガイドではそれぞれ詳しく整理しています。このレビューは確認すべき点を示しますが、公式ストアや現在のプレイヤー情報の代わりにはなりません。"
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "暗い森にあるMistfall Hunterの公式Steamヘッダー", "caption": "別作品との混同を避けるための公式Steamヘッダーです。ゲームプレイの証拠としては扱いません。"},
            {"type": "rich", "title": "購入前にこのレビューを使う手順", "paragraphs": [
                "まず実際に遊ぶ形式を決めます。ソロ中心ならクラスガイドのソロ部分を読み、ミスを回収しやすい候補を基準にします。友人と遊ぶなら、分隊にすでにある役割を確認して、足りない仕事をプランナーで試します。自分のグループの通信方法を無視して、想像上のメタだけを追う必要はありません。",
                "次に、変わりにくい事実と変化する信号を分けます。製品名、開発元、プラットフォーム、ストアの確認はSteam公式の役割です。価格、レビュー、待ち時間、クラスの強さは時間で変わります。レビューはそれらの読み方を説明できますが、前提日を示し、初期印象を永久の結論にしないことが大切です。",
                "短い結論は、脱出ループに魅力を感じ、PCが対応し、Steamの現在情報が期待と合うなら購入を検討する、です。発売直後の勢い、割引のカウントダウン、誰かの最強クラス発言だけで急がないでください。固定の点数より、こちらの判断基準の方がパッチ後にも使いやすいでしょう。"
            ]},
            {"type": "table", "title": "今買う、待つ、見送るの判断", "headers": ["状況", "おすすめ", "理由"], "rows": [
                ["脱出PvPvEが好き", "最新情報を確認して購入候補", "中心ループが好みに合う可能性があります。"],
                ["落ち着いたキャンペーンが欲しい", "待つか見送る", "装備を失う構造が合わないかもしれません。"],
                ["固定分隊がある", "役割の空きを先に確認", "クラスの相性で体験が変わります。"],
                ["PCや地域が不確実", "待つ", "必要環境、価格、レビューを確認します。"],
                ["一時的なメタだけが目的", "急がない", "パッチと検証でクラス評価は動きます。"]
            ]},
            {"type": "faq", "title": "Mistfall Hunter 評価 よくある質問", "items": [
                ["Mistfall Hunterは買う価値がありますか？", "脱出PvPvE、反復ラン、プレッシャー下の判断が好きなら購入候補です。支払う前にSteam価格、必要環境、最近のレビュー、活動状況を確認してください。"],
                ["ソロプレイヤーにも向いていますか？", "向いていますが、自己回復、情報、扱いやすいクラスがより重要です。Mercenaryから試し、最終結論にする前に実際のランを確認しましょう。"],
                ["初心者におすすめのクラスは？", "このサイトのモデルではMercenaryが低リスクの入口です。分隊で耐久役をしたい場合はWithered Knightも候補です。"],
                ["公式スコアはありますか？", "ありません。独立したファンレビューです。モード、クラス、PC、バランスで答えが変わるため固定点数を避けています。"],
                ["価格とプレイヤー数はどこで確認できますか？", "地域価格と製品情報はSteam公式、活動の目安はSteamDBのライブチャートで確認します。サイト内の価格ガイドとプレイヤー数ガイドも参照できます。"],
                ["パッチ後もレビューは使えますか？", "判断の枠組みは使えますが、クラス、性能、待ち時間、価格の価値は変化します。古い詳細は公式情報と最近のプレイヤー証拠で再確認してください。"]
            ]},
            {"type": "links", "title": "レビューの確認ソース", "items": [
                ["Mistfall Hunter Steam公式ページ", OFFICIAL_STEAM_URL, "製品名、平台、価格、必要環境、レビュー、販売状態を確認します。", "noopener"],
                ["SteamDB Mistfall Hunter チャート", STEAMDB_CHARTS_URL, "現在数とピークの第三者データ。方向性のある信号として読みます。", "nofollow noopener"],
                ["Steam返金ポリシー", "https://store.steampowered.com/steam_refunds/", "購入前に現在のプラットフォーム条件を確認します。", "nofollow noopener"]
            ]},
            {"type": "related", "title": "関連するMistfall Hunterガイド", "items": [
                ["Mistfall Hunter クラスガイド", get_page_path("classes", "ja"), "役割、リスク、初心者向け方向を比較します。"],
                ["Mistfall Hunter ビルドプランナー", get_page_path("build-planner", "ja"), "ソロ、デュオ、分隊に合う方向を探します。"],
                ["Mistfall Hunter プレイヤー数ガイド", get_page_path("player-count", "ja"), "SteamDBの信号と待ち時間を読みます。"],
                ["Mistfall Hunter 価格ガイド", get_page_path("price", "ja"), "価格、割引、購入前の注意を確認します。"],
                ["Mistfall Hunter Steam情報", get_page_path("steam", "ja"), "公式の平台と発売情報を確認します。"]
            ]}
        ]
    }
})


REVIEW_PAGE_DATA.update({
    "fr": {
        "page": {
            "title": "Avis Mistfall Hunter : faut-il l'acheter sur Steam ?",
            "description": "Avis pratique sur Mistfall Hunter : boucle d'extraction, classes, prix Steam, activité et critères avant achat.",
            "h1": "Avis Mistfall Hunter : faut-il l'acheter sur Steam ?",
            "kicker": "Avis Mistfall Hunter | Mis à jour en août 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-review-verdict.webp", "alt": "Illustration éditoriale d'une route d'extraction Mistfall Hunter", "caption": "Illustration éditoriale générée pour cet avis créé par des fans ; ce n'est pas une capture officielle."},
            {"type": "rich", "title": "Verdict rapide : une extraction ARPG pour le bon profil", "paragraphs": [
                "Notre avis Mistfall Hunter est nuancé : le jeu mérite votre attention si vous aimez le PvPvE d'extraction, les runs répétées, le risque de perdre un équipement et l'apprentissage d'un rôle en jouant. Il est moins adapté si vous cherchez une campagne solo courte ou une progression douce qui ne revient jamais en arrière. La vraie question n'est pas de savoir si le jeu plaît à tout le monde, mais si ses choix de route, de combat et d'extraction donnent envie de relancer une partie.",
                "Le jeu fonctionne surtout pour les joueurs qui aiment décider sous pression. Vous entrez avec un plan, vous lisez le danger, vous choisissez le moment du combat et vous comparez la valeur d'un butin supplémentaire au risque de ne pas sortir. Les classes comptent donc réellement : une classe de front pardonne davantage une erreur, alors qu'une classe burst ou contrôle demande un placement et un timing plus précis.",
                "Le principal point de prudence est la fraîcheur du jeu. Les routes, l'équilibrage, les performances et la sensation de matchmaking peuvent évoluer pendant que la communauté apprend. Lisez cette page comme un manuel indépendant, pas comme une tier list officielle. Vérifiez la page Steam, les avis récents, la compatibilité de votre PC et l'activité à votre heure habituelle avant de payer."
            ]},
            {"type": "table", "title": "Mistfall Hunter en un coup d'œil", "headers": ["Question", "Réponse de l'avis", "Pourquoi"], "rows": [
                ["Quel type de jeu ?", "ARPG PvPvE d'extraction", "Chaque run combine combat, route, butin à risque et choix de sortie."],
                ["Pour qui ?", "Les joueurs qui aiment les runs tendues", "L'intérêt vient des décisions et de l'apprentissage, pas d'une histoire unique."],
                ["Accessible aux débutants ?", "Oui avec la bonne classe, mais pas sans effort", "Mercenary et Withered Knight donnent plus de marge au départ."],
                ["Acheter tout de suite ?", "Vérifier Steam en direct avant", "Prix, avis, exigences et activité évoluent."],
                ["Position du site ?", "Ressource indépendante créée par des fans", "Les conseils de classes sont éditoriaux et séparés des faits Steam."]
            ]},
            {"type": "rich", "title": "Ce que demande la boucle d'extraction", "paragraphs": [
                "Un jeu d'extraction commence avec un plan incomplet. La route, les ennemis, le butin et les autres joueurs vous obligent à l'adapter. Le savoir-faire le plus important est souvent de reconnaître le moment où un petit gain suffit. Rester pour un coffre ou un combat de plus peut améliorer la run, mais aussi transformer une sortie sûre en perte d'équipement. Cette tension donne son identité au jeu et rend les premières heures moins confortables qu'un ARPG classique.",
                "La boucle récompense l'information autant que l'exécution. Il faut reconnaître un combat favorable, la fenêtre forte de sa classe et le moment où l'équipe a déjà dépensé les ressources nécessaires pour continuer. Une build n'est donc pas seulement une liste de dégâts : elle comprend le placement, la récupération, le désengagement et un niveau de risque que l'équipe peut communiquer.",
                "Le solo et l'escouade peuvent sembler être deux expériences différentes. En solo, l'auto-récupération, l'information et la correction des erreurs pèsent davantage. En groupe, le contrôle, l'éclaireur et le rôle d'ancrage créent une sécurité partagée, mais exigent de la coordination. Jouez plusieurs sessions dans le mode que vous utiliserez réellement avant de conclure."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Illustration Steam officielle de Mistfall Hunter dans une bataille enneigée", "caption": "Artwork Steam officiel utilisé pour identifier le jeu ; il ne mesure pas les performances."},
            {"type": "rich", "title": "Classes et courbe d'apprentissage", "paragraphs": [
                "Le meilleur moyen d'évaluer les classes Mistfall Hunter est de partir du besoin du joueur, pas d'un gagnant universel. Mercenary propose un rôle de front lisible et convient aux joueurs qui veulent une marge d'erreur. Withered Knight ajoute de la résistance et du contrôle d'espace pour ancrer une équipe. Ces choix offrent peut-être moins de moments spectaculaires, mais rendent les décisions plus faciles à comprendre.",
                "Blackarrow, Shadowstrix et Sorcerer demandent un timing plus précis. Blackarrow récompense la distance, l'exploration et une pression patiente. Shadowstrix crée de bonnes fenêtres d'embuscade et de retrait, mais expose vite les erreurs. Sorcerer apporte burst et contrôle de zone, tandis que Seer gagne de la valeur quand l'information, l'utilité et les appels d'escouade comptent plus que les dégâts personnels.",
                "Pour votre première session, utilisez le manuel des classes et le planificateur comme une carte, pas comme un ordre. Choisissez un travail que vous pouvez expliquer en une phrase, puis vérifiez s'il vous aide vraiment à survivre et à communiquer. Si deux options sont proches, considérez-les comme une égalité et choisissez le rôle manquant."
            ]},
            {"type": "table", "title": "Direction de départ selon le besoin", "headers": ["Besoin", "Direction", "Compromis"], "rows": [
                ["Premières sessions solo", "Mercenary", "Plus permissif, mais moins de burst."],
                ["Ancrer l'escouade", "Withered Knight", "Échange une partie des dégâts contre espace et endurance."],
                ["Distance et repérage", "Blackarrow", "Le placement et la patience deviennent essentiels."],
                ["Flancs agressifs", "Shadowstrix", "Le gain est fort, la sanction aussi."],
                ["Zone ou utilité", "Sorcerer ou Seer", "Choisir entre contrôle explosif et information d'équipe."]
            ]},
            {"type": "rich", "title": "Forces, limites et vérifications", "paragraphs": [
                "La force principale de Mistfall Hunter est la densité de décisions. Même une courte run demande de comparer le temps, le bruit, la valeur de l'équipement, la pression ennemie et les ressources de la prochaine rencontre. Une extraction réussie paraît méritée parce que le jeu ne joue pas à votre place. Le planificateur de classes complète cette idée en distinguant solo, duo et escouade plutôt qu'en imposant un score universel.",
                "Le compromis est une certaine exigence avant que les habitudes deviennent naturelles. Si vous n'aimez pas perdre une progression, repartir avec peu ou relire une route plusieurs fois, la boucle peut ressembler à une friction. Si vous aimez transformer une défaite en plan plus propre, cette friction devient une raison de revenir. C'est une question d'affinité, pas de talent.",
                "Avant l'achat, vérifiez quatre signaux actuels : prix Steam dans votre région, tendance des avis récents, exigences et performances sur votre PC, activité à votre heure de jeu. Les ressources prix et joueurs du site détaillent ces contrôles. Cet avis aide à savoir quoi regarder, mais ne remplace ni la boutique officielle ni les informations de la communauté."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Bannière Steam officielle de Mistfall Hunter dans une forêt sombre", "caption": "Bannière officielle utilisée comme seconde référence d'identité ; elle ne sert pas de preuve de gameplay."},
            {"type": "rich", "title": "Comment utiliser cet avis avant d'acheter", "paragraphs": [
                "Commencez par le mode que vous jouerez vraiment. Si vous jouez surtout en solo, consultez les conseils solo du manuel des classes et prenez une option permissive comme référence. Avec des amis, regardez les rôles déjà présents et testez le rôle manquant dans le planificateur. Cela évite d'acheter pour une méta imaginaire qui ne correspond pas à votre groupe.",
                "Séparez ensuite les faits stables des signaux changeants. Le nom du produit, la plateforme, le développeur et l'identité de la boutique se vérifient sur Steam officiel. Prix, avis, files d'attente et puissance des classes évoluent. Un avis peut expliquer comment lire ces signaux, mais doit dater ses hypothèses et éviter de transformer une première impression en verdict permanent.",
                "La conclusion est simple : envisagez l'achat si la boucle d'extraction vous attire, si votre PC est compatible et si les informations Steam actuelles correspondent à vos attentes. Attendez si vous réagissez seulement à l'élan du lancement, à un compte à rebours de remise ou à une prétendue meilleure classe. Cette règle résiste mieux qu'une note chiffrée."
            ]},
            {"type": "table", "title": "Acheter, attendre ou passer ?", "headers": ["Situation", "Choix pratique", "Raison"], "rows": [
                ["Vous aimez le PvPvE d'extraction", "Envisager après vérifications", "La boucle centrale peut correspondre à vos goûts."],
                ["Vous voulez une campagne tranquille", "Attendre ou passer", "Le risque de perte peut mal convenir."],
                ["Vous avez une escouade fixe", "Vérifier les rôles", "La couverture de classes change l'expérience."],
                ["PC ou région incertaine", "Attendre", "Confirmer exigences, prix et avis actuels."],
                ["Vous cherchez seulement la méta du jour", "Ne pas se presser", "Les patchs peuvent changer les conseils."]
            ]},
            {"type": "faq", "title": "Questions fréquentes sur l'avis Mistfall Hunter", "items": [
                ["Mistfall Hunter vaut-il son prix ?", "Le jeu mérite d'être envisagé si vous aimez le PvPvE d'extraction, les runs répétées et les choix sous pression. Vérifiez prix, exigences, avis récents et activité Steam avant de payer."],
                ["Mistfall Hunter convient-il au solo ?", "Oui, mais le solo demande davantage de récupération, d'information et une classe permissive. Mercenary est une direction de départ pratique ; testez-la avant de la considérer comme définitive."],
                ["Quelle classe choisir quand on débute ?", "Le modèle du site place Mercenary comme direction de faible risque. Withered Knight est une autre option logique si vous préférez ancrer une escouade."],
                ["Y a-t-il une note officielle dans cet avis ?", "Non. Il s'agit d'un avis indépendant créé par des fans et d'une aide à la décision. Une note fixe cacherait l'effet du mode, de la classe, du PC et de l'équilibrage."],
                ["Où vérifier le prix et les joueurs actuels ?", "Consultez Steam officiel pour le prix régional et les faits du produit, puis SteamDB pour un signal d'activité tiers. Les ressources prix et joueurs expliquent la lecture."],
                ["L'avis restera-t-il valable après un patch ?", "Le cadre de décision restera utile, mais classes, performances, files et valeur peuvent changer. Vérifiez les informations officielles et les témoignages récents avant de réutiliser un détail ancien."]
            ]},
            {"type": "links", "title": "Sources de vérification", "items": [
                ["Page Steam officielle de Mistfall Hunter", OFFICIAL_STEAM_URL, "Identité, plateforme, prix, exigences, avis et état actuel de la boutique.", "noopener"],
                ["Graphiques Mistfall Hunter sur SteamDB", STEAMDB_CHARTS_URL, "Contexte de joueurs et de pics ; un signal tiers à lire avec prudence.", "nofollow noopener"],
                ["Politique de remboursement Steam", "https://store.steampowered.com/steam_refunds/", "Vérifier les règles de la plateforme avant paiement.", "nofollow noopener"]
            ]},
            {"type": "related", "title": "Ressources Mistfall Hunter liées", "items": [
                ["Manuel des classes Mistfall Hunter", get_page_path("classes", "fr"), "Comparer rôles, risque et options de départ."],
                ["Planificateur de build Mistfall Hunter", get_page_path("build-planner", "fr"), "Associer une classe au solo, duo ou escouade."],
                ["Ressource joueurs Mistfall Hunter", get_page_path("player-count", "fr"), "Lire SteamDB et le contexte des files."],
                ["Ressource prix Mistfall Hunter", get_page_path("price", "fr"), "Vérifier prix, remise et précautions d'achat."],
                ["Infos Steam Mistfall Hunter", get_page_path("steam", "fr"), "Confirmer les faits officiels de plateforme et de sortie."]
            ]}
        ]
    }
})


REVIEW_PAGE_DATA.update({
    "de": {
        "page": {
            "title": "Mistfall Hunter Review: Lohnt sich der Kauf auf Steam?",
            "description": "Diese Mistfall Hunter Review bewertet Extraction-Loop, Klassen, Steam-Preis, Spieleraktivität und Kaufkriterien.",
            "h1": "Mistfall Hunter Review: Lohnt sich der Kauf auf Steam?",
            "kicker": "Mistfall Hunter Review | Aktualisiert: 2026-08",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-review-verdict.webp", "alt": "Redaktionelle Illustration einer Mistfall Hunter Extraktionsroute", "caption": "Für diese von Fans erstellte Review erzeugte redaktionelle Illustration; kein offizieller Gameplay-Screenshot."},
            {"type": "rich", "title": "Kurzfazit: ein Extraction-ARPG für den passenden Spielertyp", "paragraphs": [
                "Unser Mistfall Hunter Review fällt bewusst bedingt aus: Das Spiel ist interessant, wenn du Extraction-PvPvE, wiederholbare Runs, riskante Ausrüstung und das Lernen einer Rolle durch Spielen magst. Es ist weniger passend, wenn du eine kurze Einzelspieler-Kampagne oder einen ruhigen Fortschritt ohne Rückschritte suchst. Die nützlichere Frage lautet nicht, ob das Spiel jedem gefällt, sondern ob seine Entscheidungen über Route, Kampf und Extraktion dich zu einer weiteren Runde einladen.",
                "Mistfall Hunter funktioniert besonders gut für Spieler, die unter Druck entscheiden möchten. Du startest mit einem Plan, liest Gefahren, wählst deine Kämpfe und vergleichst zusätzlichen Loot mit dem Risiko, nicht mehr sicher herauszukommen. Deshalb ist die Klassenwahl wichtig: Eine Frontline-Klasse verzeiht Fehler eher, während Burst- und Kontrollrollen präziseres Timing und bessere Positionierung verlangen.",
                "Der wichtigste Vorbehalt ist die frühe Lebensphase des Spiels. Routen, Balance, Performance und Matchmaking können sich verändern, während die Community Erfahrungen sammelt. Lies diese Seite als unabhängigen Entscheidungsleitfaden, nicht als offizielle Tier-Liste. Prüfe vor dem Kauf die aktuelle Steam-Seite, neue Reviews, deine PC-Kompatibilität und die Aktivität zu deiner normalen Spielzeit."
            ]},
            {"type": "table", "title": "Mistfall Hunter Review auf einen Blick", "headers": ["Frage", "Antwort", "Warum es zählt"], "rows": [
                ["Was für ein Spiel ist es?", "Extraction-PvPvE-ARPG", "Runs verbinden Kampf, Route, Loot-Risiko und die Entscheidung zur Extraktion."],
                ["Für wen passt es?", "Spieler mit Freude an angespannten Runs", "Der Reiz liegt in Lernen und Entscheidungen, nicht nur im Story-Abschluss."],
                ["Ist der Einstieg einfach?", "Mit passender Klasse ja, aber nicht reibungslos", "Mercenary und Withered Knight geben am Anfang mehr Spielraum."],
                ["Sofort kaufen?", "Erst aktuelle Steam-Fakten prüfen", "Preis, Reviews, Anforderungen und Aktivität können wechseln."],
                ["Welche Haltung hat die Seite?", "Unabhängiger Fan-Leitfaden", "Klassenempfehlungen sind Redaktion und keine offiziellen Daten."]
            ]},
            {"type": "rich", "title": "Was der Extraction-Loop von dir verlangt", "paragraphs": [
                "Ein Extraction-Spiel beginnt mit einem unvollständigen Plan. Route, Gegner, Loot und andere Spieler zwingen dich, ihn anzupassen. Eine wichtige Fähigkeit ist zu erkennen, wann ein kleiner Gewinn genügt. Eine weitere Truhe kann den Run verbessern, aber auch eine sichere Rückkehr in verlorene Ausrüstung verwandeln. Diese Spannung gibt dem Spiel sein Profil und erklärt, warum die ersten Stunden härter wirken können als in einem normalen Action-RPG.",
                "Der Loop belohnt Information ebenso wie mechanische Ausführung. Du musst sehen, wann ein Kampf günstig ist, wann deine Klasse ihr stärkstes Fenster hat und wann das Team bereits zu viele Ressourcen für den Rückweg verbraucht hat. Ein Build ist daher nicht nur eine Schadensliste. Er umfasst Position, Erholung, Rückzug und ein Risiko, das die Gruppe verständlich kommunizieren kann.",
                "Solo und Gruppe können wie zwei verschiedene Spiele wirken. Solo zählen Selbstrettung, Informationen und Fehlerkorrektur stärker. Eine koordinierte Gruppe verwandelt Kontrolle, Scouten und eine Ankerrolle in gemeinsame Sicherheit, braucht aber Kommunikation. Spiele vor dem Urteil mehrere Sessions in der Spielart, die du tatsächlich nutzen willst."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Offizielles Steam-Artwork von Mistfall Hunter in einer verschneiten Schlacht", "caption": "Offizielles Steam-Artwork zur Identifikation des Spiels; kein Beleg für Performance."},
            {"type": "rich", "title": "Klassen und Lernkurve", "paragraphs": [
                "Klassen lassen sich sinnvoller über Spielerbedarf als über einen universellen Sieger bewerten. Mercenary bietet ein gut lesbares Frontline-Muster und passt zu Spielern, die Fehlerraum brauchen. Withered Knight bringt Widerstand und Raumkontrolle für die Rolle als Gruppenanker. Beide erzeugen vielleicht weniger spektakuläre Höhepunkte, machen aber die Sprache der Entscheidungen leichter verständlich.",
                "Blackarrow, Shadowstrix und Sorcerer verlangen bewussteres Timing. Blackarrow belohnt Distanz, Scouting und geduldigen Druck. Shadowstrix kann starke Ambush- und Rückzugsfenster schaffen, bestraft schlechte Position aber schnell. Sorcerer bietet Burst und Flächenkontrolle. Seer gewinnt vor allem dann an Wert, wenn Informationen, Utility und sichere Gruppenentscheidungen wichtiger sind als persönlicher Schaden.",
                "Nutze Klassenleitfaden und Build-Planer beim ersten Versuch als Karte, nicht als Befehl. Wähle eine Aufgabe, die du in einem Satz erklären kannst, und prüfe, ob sie Überleben und Kommunikation wirklich verbessert. Liegen zwei Optionen eng zusammen, behandle sie als Gleichstand und fülle die fehlende Gruppenrolle. Dieses Denken bleibt auch nach Balance-Patches brauchbar."
            ]},
            {"type": "table", "title": "Start-Richtung nach Spielerbedarf", "headers": ["Bedarf", "Gute Richtung", "Zu verstehender Nachteil"], "rows": [
                ["Erste Solo-Runs", "Mercenary", "Verzeiht mehr Fehler, bietet aber weniger Burst."],
                ["Gruppenanker", "Withered Knight", "Tauscht etwas Schaden gegen Raum und Haltbarkeit."],
                ["Distanz und Scouten", "Blackarrow", "Position und Geduld sind wichtiger als Face-Tanking."],
                ["Aggressive Flanken", "Shadowstrix", "Hoher Ertrag mit schärferer Fehlerstrafe."],
                ["Fläche oder Utility", "Sorcerer oder Seer", "Zwischen Burst-Kontrolle und Gruppeninformation wählen."]
            ]},
            {"type": "rich", "title": "Stärken, Nachteile und Prüfungen vor dem Kauf", "paragraphs": [
                "Die größte Stärke von Mistfall Hunter ist die Dichte der Entscheidungen. Selbst eine kurze Runde verlangt den Vergleich von Zeit, Lärm, Ausrüstungswert, Gegnerdruck und Ressourcen für den nächsten Kampf. Eine erfolgreiche Extraktion fühlt sich verdient an, weil nichts völlig automatisch läuft. Der Klassenplaner unterstützt das, indem er Solo, Duo und Gruppe trennt, statt eine Zahl auf alle Spieler zu übertragen.",
                "Der Nachteil ist die Anstrengung, bevor die Gewohnheiten sitzen. Wer verlorenen Fortschritt, vorsichtige Ausgänge oder das erneute Lesen einer Route nicht mag, erlebt den Loop vielleicht als Reibung. Wer aus einer Niederlage einen besseren Plan baut, findet darin den Grund für eine weitere Runde. Das ist eine Frage der Passung, kein Test von Können.",
                "Prüfe vor dem Kauf vier aktuelle Signale: regionaler Steam-Preis, Richtung der neuen Bewertungen, Anforderungen und Performance auf deinem PC sowie Spieleraktivität zu deiner üblichen Zeit. Die Preis- und Spielerzahlen-Leitfäden dieser Seite erklären die Details. Diese Review zeigt dir, was du prüfen solltest, ersetzt aber weder Steam noch aktuelle Community-Evidenz."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Offizieller Mistfall Hunter Steam-Header in einem dunklen Wald", "caption": "Offizieller Header als zweite Identitätsreferenz; nicht als Gameplay-Nachweis verwendet."},
            {"type": "rich", "title": "So nutzt du diese Review vor dem Kauf", "paragraphs": [
                "Beginne mit der Spielart, die du wirklich spielen wirst. Für Solo liest du die Solo-Hinweise im Klassenleitfaden und nimmst eine verzeihende Richtung als Basis. Mit Freunden prüfst du zuerst die vorhandenen Rollen und testest die Lücke im Build-Planer. So kaufst du nicht für eine gedachte Meta, die zu deiner Gruppe und ihrer Kommunikation gar nicht passt.",
                "Trenne danach stabile Fakten von veränderlichen Signalen. Produktname, Plattform, Entwickler und Store-Identität gehören zur offiziellen Steam-Seite. Preis, Reviews, Warteschlangen und Klassenstärke verändern sich. Eine Review kann zeigen, wie diese Signale zu lesen sind, sollte ihre Annahmen aber datieren und einen frühen Eindruck nicht als ewiges Urteil verkaufen.",
                "Das kurze Fazit lautet: Kaufe, wenn dich der Extraction-Loop selbst reizt, dein PC unterstützt wird und die aktuellen Steam-Fakten zu deinen Erwartungen passen. Warte, wenn du nur auf Launch-Hype, Rabattdruck oder eine angeblich beste Klasse reagierst. Diese Entscheidungsregel hält länger als eine feste Zahl und lässt Raum für Patches."
            ]},
            {"type": "table", "title": "Jetzt kaufen, warten oder auslassen?", "headers": ["Situation", "Praktische Wahl", "Grund"], "rows": [
                ["Du magst Extraction-PvPvE", "Nach Live-Check in Betracht ziehen", "Der Kern-Loop passt wahrscheinlich zu dir."],
                ["Du willst eine entspannte Kampagne", "Warten oder auslassen", "Verlustrisiko kann die falsche Struktur sein."],
                ["Du hast eine feste Gruppe", "Klassenabdeckung prüfen", "Rollenfit verändert das Gruppenerlebnis."],
                ["PC oder Region sind unsicher", "Warten", "Anforderungen, Preis und Reviews bestätigen."],
                ["Du jagst nur die aktuelle Meta", "Nicht überstürzen", "Patches können Empfehlungen verändern."]
            ]},
            {"type": "faq", "title": "Häufige Fragen zu Mistfall Hunter", "items": [
                ["Lohnt sich Mistfall Hunter?", "Das Spiel ist interessant, wenn du Extraction-PvPvE, wiederholbare Runs und Entscheidungen unter Druck magst. Prüfe Steam-Preis, Anforderungen, neue Reviews und Aktivität vor dem Kauf."],
                ["Ist Mistfall Hunter gut für Solo-Spieler?", "Es kann passen, aber Solo verlangt mehr Selbstrettung, Information und eine verzeihende Klasse. Mercenary ist eine praktische Richtung; teste sie, bevor du sie als endgültig annimmst."],
                ["Welche Klasse ist für Anfänger gut?", "Das Modell dieser Seite setzt Mercenary als klare Richtung mit geringem Risiko. Withered Knight ist sinnvoll, wenn du in einer Gruppe einen robusten Anker spielen willst."],
                ["Gibt diese Review eine offizielle Wertung?", "Nein. Es ist eine unabhängige, von Fans erstellte Review und Entscheidungshilfe. Eine feste Wertung würde Modus, Klasse, PC und aktuelle Balance zu stark vereinfachen."],
                ["Wo prüfe ich Preis und Spielerzahl?", "Nutze Steam offiziell für Regionalpreis und Produktfakten. SteamDB liefert ein externes Aktivitätssignal; die Preis- und Spielerzahlen-Leitfäden helfen bei der Einordnung."],
                ["Bleibt die Review nach Patches gültig?", "Der Entscheidungsrahmen bleibt nützlich, aber Klassen, Performance, Wartezeit und Wert können sich ändern. Prüfe offizielle Hinweise und aktuelle Spielerberichte erneut."]
            ]},
            {"type": "links", "title": "Review-Quellen und Prüfung", "items": [
                ["Offizielle Mistfall Hunter Steam-Seite", OFFICIAL_STEAM_URL, "Produktidentität, Plattform, Preis, Anforderungen, Bewertungen und aktueller Stand im Store.", "noopener"],
                ["Mistfall Hunter Charts auf SteamDB", STEAMDB_CHARTS_URL, "Drittanbieter-Kontext zu aktuellen Spielern und Peaks; nur als Richtungssignal lesen.", "nofollow noopener"],
                ["Steam-Rückerstattungsrichtlinie", "https://store.steampowered.com/steam_refunds/", "Aktuelle Plattformregeln vor dem Bezahlen prüfen.", "nofollow noopener"]
            ]},
            {"type": "related", "title": "Verwandte Mistfall Hunter Leitfäden", "items": [
                ["Mistfall Hunter Klassenleitfaden", get_page_path("classes", "de"), "Rollen, Risiko und Einsteiger-Richtungen vergleichen."],
                ["Mistfall Hunter Build-Planer", get_page_path("build-planner", "de"), "Klasse auf Solo-, Duo- oder Gruppenstil abstimmen."],
                ["Mistfall Hunter Spielerzahlen-Leitfaden", get_page_path("player-count", "de"), "SteamDB-Signale und Wartezeiten einordnen."],
                ["Mistfall Hunter Preisleitfaden", get_page_path("price", "de"), "Preis, Rabatt und Hinweise vor dem Kauf prüfen."],
                ["Mistfall Hunter Steam-Info", get_page_path("steam", "de"), "Offizielle Plattform- und Release-Fakten bestätigen."]
            ]}
        ]
    }
})


REVIEW_PAGE_DATA.update({
    "pt": {
        "page": {
            "title": "Análise de Mistfall Hunter: vale a pena comprar?",
            "description": "Análise prática de Mistfall Hunter sobre extração, classes, preço no Steam, atividade e critérios antes da compra.",
            "h1": "Análise de Mistfall Hunter: vale a pena comprar?",
            "kicker": "Análise de Mistfall Hunter | Atualizada em agosto de 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-review-verdict.webp", "alt": "Ilustração editorial de uma rota de extração de Mistfall Hunter", "caption": "Ilustração editorial gerada para esta análise feita por fãs; não é uma captura oficial do jogo."},
            {"type": "rich", "title": "Veredito rápido: um ARPG de extração para o jogador certo", "paragraphs": [
                "Nossa análise de Mistfall Hunter chega a um veredito condicional: o jogo merece atenção se você gosta de PvPvE de extração, partidas repetíveis, risco de perder equipamentos e aprender uma função jogando. Ele é menos indicado para quem procura uma campanha solo curta ou uma progressão tranquila sem retrocessos. A pergunta mais útil não é se o jogo é bom para todos, mas se suas decisões de rota, combate e extração dão vontade de iniciar outra partida.",
                "Mistfall Hunter funciona melhor para quem gosta de decidir sob pressão. Você entra com um plano, lê o perigo, escolhe quando lutar e compara o valor de continuar explorando com o valor de sair levando o que já encontrou. Por isso a escolha de classe importa: uma função de linha de frente tolera mais erros, enquanto uma classe de dano explosivo ou controle exige melhor posicionamento e timing.",
                "A principal cautela é a fase inicial do jogo. Rotas, balanceamento, desempenho e sensação de encontrar partidas podem mudar enquanto a comunidade aprende. Leia esta página como um guia independente, não como uma tier list oficial. Antes de pagar, confira a página do Steam, avaliações recentes, compatibilidade do PC e atividade no horário em que você costuma jogar."
            ]},
            {"type": "table", "title": "Mistfall Hunter em resumo", "headers": ["Pergunta", "Resposta da análise", "Por que importa"], "rows": [
                ["Que tipo de jogo é?", "ARPG PvPvE de extração", "Cada partida combina combate, rota, risco de loot e decisão de saída."],
                ["Para quem combina?", "Quem gosta de partidas tensas e repetíveis", "O apelo está em aprender e decidir, não apenas terminar uma história."],
                ["É fácil para iniciantes?", "Com a classe certa, sim; sem atrito, não", "Mercenary e Withered Knight dão mais margem no começo."],
                ["Devo comprar já?", "Confira os dados atuais do Steam antes", "Preço, avaliações, requisitos e atividade mudam."],
                ["Qual é a posição do site?", "Guia independente feito por fãs", "Recomendações de classe são editoriais, separadas dos fatos oficiais."]
            ]},
            {"type": "rich", "title": "O que o ciclo de extração exige", "paragraphs": [
                "Um jogo de extração começa com um plano incompleto. A rota, os inimigos, o loot e outros jogadores obrigam você a adaptá-lo. Uma habilidade importante é saber quando um ganho pequeno já é suficiente. Ficar para abrir outro baú pode melhorar a partida, mas também transformar uma saída segura em perda de equipamento. Essa tensão dá identidade ao jogo e explica por que as primeiras horas podem ser menos confortáveis do que em um ARPG tradicional.",
                "O ciclo recompensa informação tanto quanto execução mecânica. Você precisa reconhecer uma luta favorável, o momento mais forte da sua classe e quando o grupo já gastou recursos demais para continuar. Uma build, portanto, não é apenas uma lista de dano. Ela inclui posicionamento, recuperação, retirada e um nível de risco que o time consegue comunicar.",
                "Solo e equipe podem parecer jogos diferentes. No solo pesam mais a recuperação própria, a informação e a correção de erros. Em um grupo coordenado, controle, reconhecimento e uma função de âncora criam segurança compartilhada, mas exigem comunicação. Jogue algumas sessões no formato que realmente pretende usar antes de decidir se o jogo combina com você."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Arte oficial do Steam de Mistfall Hunter em uma batalha na neve", "caption": "Arte oficial do Steam usada para confirmar a identidade do jogo; não é prova de desempenho."},
            {"type": "rich", "title": "Classes e curva de aprendizado", "paragraphs": [
                "A forma mais prática de avaliar as classes de Mistfall Hunter é pensar na necessidade do jogador, não em um vencedor universal. Mercenary oferece uma linha de frente fácil de entender e funciona bem para quem quer margem para errar. Withered Knight acrescenta resistência e controle de espaço para quem quer ancorar a equipe. Essas opções talvez tenham menos momentos chamativos, mas tornam as decisões do jogo mais fáceis de ler.",
                "Blackarrow, Shadowstrix e Sorcerer pedem timing mais consciente. Blackarrow recompensa distância, reconhecimento e pressão paciente. Shadowstrix cria boas janelas de emboscada e retirada, mas pune rápido uma posição ruim. Sorcerer entrega dano explosivo e controle de área. Seer ganha valor quando informação, utilidade e decisões seguras da equipe importam mais do que dano individual.",
                "Na primeira sessão, use o guia de classes e o planejador como mapa, não como ordem. Escolha uma função que você consiga explicar em uma frase e verifique se ela realmente ajuda a sobreviver e a se comunicar. Se duas opções ficarem próximas, trate como empate e cubra o papel que falta no grupo. Esse raciocínio continua válido mesmo depois de um patch."
            ]},
            {"type": "table", "title": "Direção inicial por necessidade", "headers": ["Necessidade", "Direção", "Troca a entender"], "rows": [
                ["Primeiras partidas solo", "Mercenary", "Perdoa mais erros, mas tem menos explosão de dano."],
                ["Âncora da equipe", "Withered Knight", "Troca parte do dano por espaço e resistência."],
                ["Distância e reconhecimento", "Blackarrow", "Posicionamento e paciência são essenciais."],
                ["Flancos agressivos", "Shadowstrix", "Alto retorno com punição mais severa."],
                ["Área ou utilidade", "Sorcerer ou Seer", "Escolha entre controle explosivo e informação para o time."]
            ]},
            {"type": "rich", "title": "Pontos fortes, limites e checagens", "paragraphs": [
                "A maior força de Mistfall Hunter é a quantidade de decisões. Mesmo uma partida curta pede comparação entre tempo, barulho, valor do equipamento, pressão inimiga e recursos necessários para a próxima luta. Uma extração bem-sucedida parece merecida porque o jogo não decide tudo por você. O planejador de classes reforça isso ao separar solo, duo e equipe em vez de empurrar uma nota igual para todos.",
                "A troca é que o jogo pode parecer exigente antes de os hábitos ficarem naturais. Se você não gosta de perder progresso, sair com pouco ou repetir uma rota para entendê-la melhor, o ciclo pode parecer atrito. Se gosta de transformar uma derrota em plano melhor, o mesmo atrito vira motivo para voltar. É uma questão de encaixe, não de habilidade.",
                "Antes da compra, verifique quatro sinais atuais: preço regional no Steam, direção das avaliações recentes, requisitos e desempenho no seu PC, e atividade no horário em que joga. Os guias de preço e jogadores detalham esses pontos. Esta análise mostra o que observar, mas não substitui a loja oficial nem as evidências atuais dos jogadores."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Cabeçalho oficial de Mistfall Hunter no Steam em uma floresta escura", "caption": "Cabeçalho oficial usado como segunda referência de identidade; não é apresentado como prova de gameplay."},
            {"type": "rich", "title": "Como usar esta análise antes de comprar", "paragraphs": [
                "Comece pelo formato que você realmente vai jogar. Se for jogar solo, leia as orientações solo do guia de classes e use uma direção mais tolerante como base. Se for jogar com amigos, veja quais funções já existem e teste a lacuna no planejador. Assim você não compra para uma meta imaginária que não combina com a comunicação do seu grupo.",
                "Depois, separe fatos estáveis de sinais que mudam. Nome do produto, plataforma, desenvolvedor e identidade da loja devem ser confirmados no Steam oficial. Preço, avaliações, filas e força das classes mudam com o tempo. Uma análise pode explicar como ler esses sinais, mas precisa datar suas premissas e evitar transformar uma primeira impressão em veredito permanente.",
                "A conclusão curta é: compre quando o ciclo de extração em si parecer atraente, seu PC for compatível e os dados atuais do Steam confirmarem sua expectativa. Espere quando você estiver apenas reagindo ao impulso do lançamento, a uma contagem regressiva de desconto ou à suposta melhor classe. Essa regra dura mais do que uma nota fixa e permite mudanças futuras."
            ]},
            {"type": "table", "title": "Comprar, esperar ou deixar passar?", "headers": ["Situação", "Escolha prática", "Motivo"], "rows": [
                ["Você gosta de PvPvE de extração", "Considere após checar dados atuais", "O ciclo principal provavelmente combina com seu gosto."],
                ["Você quer uma campanha relaxada", "Espere ou deixe passar", "O risco de perder equipamento pode não combinar."],
                ["Você tem equipe fixa", "Confira a cobertura de funções", "O encaixe de classe muda a experiência do grupo."],
                ["PC ou região incertos", "Espere", "Confirme requisitos, preço e avaliações atuais."],
                ["Você só busca a meta do momento", "Não tenha pressa", "Patches podem mudar recomendações."]
            ]},
            {"type": "faq", "title": "Perguntas frequentes sobre a análise de Mistfall Hunter", "items": [
                ["Mistfall Hunter vale a pena?", "Vale considerar se você gosta de PvPvE de extração, partidas repetíveis e decisões sob pressão. Confira preço, requisitos, avaliações recentes e atividade no Steam antes de pagar."],
                ["Mistfall Hunter é bom para jogar solo?", "Pode ser, mas solo exige mais recuperação, informação e uma classe tolerante. Mercenary é uma direção prática; teste antes de tratá-la como definitiva."],
                ["Qual classe é boa para começar?", "O modelo deste site coloca Mercenary como direção de baixo risco. Withered Knight é uma opção lógica se você prefere uma âncora resistente para a equipe."],
                ["A análise tem uma nota oficial?", "Não. É uma análise independente feita por fãs e um guia de decisão. Uma nota fixa esconderia o efeito do modo, da classe, do PC e do balanceamento atual."],
                ["Onde vejo preço e jogadores atuais?", "Use o Steam oficial para preço regional e fatos do produto. Use o SteamDB como sinal externo de atividade; os guias de preço e jogadores explicam a leitura."],
                ["A análise continua válida depois de patches?", "O método de decisão continua útil, mas classes, desempenho, filas e valor podem mudar. Verifique informações oficiais e relatos recentes novamente."]
            ]},
            {"type": "links", "title": "Fontes e verificações", "items": [
                ["Página oficial de Mistfall Hunter no Steam", OFFICIAL_STEAM_URL, "Identidade, plataforma, preço, requisitos, avaliações e estado atual da loja.", "noopener"],
                ["Gráficos de Mistfall Hunter no SteamDB", STEAMDB_CHARTS_URL, "Contexto de jogadores e picos; use como sinal direcional de terceiros.", "nofollow noopener"],
                ["Política de reembolso do Steam", "https://store.steampowered.com/steam_refunds/", "Confira as regras atuais da plataforma antes de pagar.", "nofollow noopener"]
            ]},
            {"type": "related", "title": "Guias relacionados de Mistfall Hunter", "items": [
                ["Guia de classes de Mistfall Hunter", get_page_path("classes", "pt"), "Compare papéis, risco e direções para iniciantes."],
                ["Planejador de build de Mistfall Hunter", get_page_path("build-planner", "pt"), "Combine uma classe com jogo solo, duo ou equipe."],
                ["Guia de jogadores de Mistfall Hunter", get_page_path("player-count", "pt"), "Leia sinais do SteamDB e horários de fila."],
                ["Guia de preço de Mistfall Hunter", get_page_path("price", "pt"), "Confira preço, descontos e cuidados antes de comprar."],
                ["Mistfall Hunter no Steam", get_page_path("steam", "pt"), "Verifique fatos oficiais de plataforma e lançamento."]
            ]}
        ]
    }
})


REVIEW_PAGE_DATA.update({
    "ko": {
        "page": {
            "title": "Mistfall Hunter 리뷰: Steam에서 살 가치가 있을까?",
            "description": "Mistfall Hunter 리뷰에서 추출 루프, 클래스, Steam 가격, 플레이어 활동과 구매 전 확인점을 정리합니다.",
            "h1": "Mistfall Hunter 리뷰: Steam에서 살 가치가 있을까?",
            "kicker": "Mistfall Hunter 리뷰 | 2026년 8월 업데이트",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-review-verdict.webp", "alt": "Mistfall Hunter 탈출 경로를 표현한 편집용 일러스트", "caption": "이 팬 제작 리뷰를 위해 생성한 편집용 일러스트이며 공식 게임 화면이 아닙니다."},
            {"type": "rich", "title": "빠른 결론: 맞는 플레이어에게 매력적인 추출 ARPG", "paragraphs": [
                "Mistfall Hunter 리뷰의 결론은 조건부입니다. 추출 PvPvE, 반복 플레이, 장비를 잃을 수 있는 긴장감, 플레이하면서 역할을 익히는 과정을 좋아한다면 구매 후보가 됩니다. 반대로 짧은 싱글 캠페인이나 실패해도 진행이 되돌아가지 않는 편안한 게임을 원한다면 서두를 이유가 적습니다. 모든 사람에게 좋은지보다, 탈출에 성공하거나 실패한 뒤 다시 시도할 판단이 있는지가 더 중요한 질문입니다.",
                "이 게임은 압박 속에서 선택하는 것을 좋아하는 사람에게 잘 맞습니다. 진입 전에 계획을 세우고, 위험을 읽고, 싸울 때를 고르고, 더 탐색할 가치와 지금 탈출할 가치를 비교합니다. 그래서 클래스 선택도 중요합니다. 전방 역할은 실수를 회복할 여지가 크고, 폭발 피해나 제어 역할은 위치와 타이밍을 더 정확하게 요구합니다.",
                "가장 큰 주의점은 출시 초기라는 점입니다. 루트, 밸런스, 성능, 매칭 체감은 커뮤니티가 경험을 쌓으면서 바뀔 수 있습니다. 이 페이지는 공식 티어표가 아니라 독립적인 구매 판단 가이드로 읽으세요. 결제 전 Steam 공식 페이지, 최근 평가, PC 호환성, 평소 플레이 시간대의 활동을 확인하는 편이 안전합니다."
            ]},
            {"type": "table", "title": "Mistfall Hunter 리뷰 한눈에 보기", "headers": ["질문", "리뷰 답변", "판단 이유"], "rows": [
                ["어떤 게임인가요?", "추출 PvPvE ARPG", "전투, 루트 선택, 장비 위험, 탈출 판단이 한 판에 들어갑니다."],
                ["누구에게 맞나요?", "긴장감 있는 반복 플레이를 좋아하는 사람", "한 번의 스토리 완료보다 판단과 학습이 핵심입니다."],
                ["초보자도 할 만한가요?", "클래스를 고르면 가능하지만 쉽지만은 않음", "Mercenary와 Withered Knight가 초반 실수 여지를 만듭니다."],
                ["바로 사야 하나요?", "현재 Steam 정보를 먼저 확인", "가격, 평가, 사양, 활동은 바뀔 수 있습니다."],
                ["이 사이트의 입장은?", "독립 팬 가이드", "클래스 추천은 편집 판단이며 공식 정보와 분리합니다."]
            ]},
            {"type": "rich", "title": "추출 루프가 요구하는 것", "paragraphs": [
                "추출 게임은 완성된 계획으로 시작하지 않습니다. 이동 경로, 적, 전리품, 다른 플레이어 때문에 계획을 계속 바꿔야 합니다. 작은 이득만으로도 돌아갈 때를 아는 것이 중요한 능력입니다. 상자 하나를 더 열면 수익이 늘 수 있지만, 안전한 탈출을 장비 손실로 바꿀 수도 있습니다. 이 긴장감이 게임의 정체성이며 일반적인 액션 RPG보다 초반이 불편하게 느껴지는 이유입니다.",
                "루프는 조작 실력만큼 정보를 보상합니다. 싸워도 되는 상황인지, 클래스의 강한 타이밍이 언제인지, 팀이 계속하기 위한 자원을 이미 썼는지 읽어야 합니다. 따라서 빌드는 피해량 목록만이 아닙니다. 위치 선정, 회복, 이탈, 그리고 팀이 공유할 수 있는 위험 수준까지 포함합니다.",
                "솔로와 파티는 서로 다른 게임처럼 느껴질 수 있습니다. 솔로는 자기 회복, 정보 수집, 실수 복구가 더 중요합니다. 협동 파티는 제어, 정찰, 앵커 역할로 안전을 공유하지만 소통이 필요합니다. 실제로 플레이할 형식으로 여러 세션을 해 본 뒤 게임이 맞는지 판단하세요."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "눈 덮인 전투 장면을 보여주는 Mistfall Hunter 공식 Steam 아트", "caption": "게임의 공식 Steam 페이지를 확인하는 데 쓰는 이미지이며 성능의 근거는 아닙니다."},
            {"type": "rich", "title": "클래스와 학습 곡선", "paragraphs": [
                "Mistfall Hunter 클래스는 하나의 순위표보다 플레이어의 목적을 기준으로 보는 편이 좋습니다. Mercenary는 이해하기 쉬운 전방 패턴을 제공해 실수할 여지가 필요한 플레이어에게 적합합니다. Withered Knight는 내구도와 공간 제어로 파티를 받치는 방향입니다. 가장 화려한 장면을 만들지는 않아도 게임의 판단 구조를 배우기 좋은 입구입니다.",
                "Blackarrow, Shadowstrix, Sorcerer는 더 정확한 타이밍을 요구합니다. Blackarrow는 거리, 정찰, 신중한 압박을 보상합니다. Shadowstrix는 매복과 이탈 창이 강하지만 위치 실수를 빠르게 처벌합니다. Sorcerer는 폭발 피해와 범위 제어를 제공합니다. Seer는 개인 피해보다 정보, 유틸리티, 안전한 파티 판단이 중요할 때 가치가 올라갑니다.",
                "첫 세션에서는 클래스 가이드와 빌드 플래너를 명령이 아니라 지도처럼 사용하세요. 한 문장으로 설명할 수 있는 역할을 고르고 실제 생존과 소통에 도움이 되는지 확인합니다. 두 선택지의 점수가 가깝다면 동점으로 보고 파티에 없는 역할을 고르세요. 패치가 수치를 바꿔도 이 판단 방식은 남습니다."
            ]},
            {"type": "table", "title": "필요에 따른 시작 클래스", "headers": ["필요", "시작 방향", "이해할 단점"], "rows": [
                ["첫 솔로 세션", "Mercenary", "실수에 강하지만 폭발 피해는 낮습니다."],
                ["파티 앵커", "Withered Knight", "피해 일부를 공간과 내구도에 투자합니다."],
                ["거리와 정찰", "Blackarrow", "정면 대결보다 위치와 인내가 중요합니다."],
                ["공격적 측면 공격", "Shadowstrix", "보상이 큰 만큼 실패의 처벌도 큽니다."],
                ["범위 압박 또는 유틸리티", "Sorcerer 또는 Seer", "폭발 제어와 팀 정보 중 하나를 고릅니다."]
            ]},
            {"type": "rich", "title": "장점, 한계, 구매 전 확인", "paragraphs": [
                "Mistfall Hunter의 가장 큰 장점은 선택의 밀도입니다. 짧은 판도 시간, 소리, 장비 가치, 적의 압박, 다음 전투에 필요한 자원을 비교하게 합니다. 아무것도 자동으로 해결되지 않기 때문에 탈출 성공에 손맛이 있습니다. 클래스 플래너가 솔로, 듀오, 파티를 분리하는 것도 이 장점을 보완하는 방식입니다.",
                "반대로 익숙해지기 전에는 부담이 될 수 있습니다. 진행 손실, 적은 전리품으로 귀환, 같은 루트를 다시 읽는 과정이 싫다면 루프가 마찰처럼 느껴집니다. 실패를 다음 계획으로 바꾸는 것을 좋아한다면 같은 마찰이 다시 플레이할 이유가 됩니다. 실력 문제가 아니라 취향과의 적합성입니다.",
                "구매 전에는 지역 Steam 가격, 최근 평가의 방향, PC 사양과 성능 보고, 평소 플레이 시간대의 활동을 확인하세요. 이 사이트의 가격 가이드와 플레이어 수 가이드가 각각 자세히 다룹니다. 이 리뷰는 확인할 항목을 정리하지만 공식 상점이나 최신 플레이어 근거를 대신하지 않습니다."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "어두운 숲 속의 Mistfall Hunter 공식 Steam 헤더", "caption": "게임 정체성을 확인하는 공식 Steam 헤더이며 실제 플레이 증거로 사용하지 않습니다."},
            {"type": "rich", "title": "구매 전에 이 리뷰를 사용하는 방법", "paragraphs": [
                "실제로 플레이할 형식부터 정하세요. 솔로 중심이라면 클래스 가이드의 솔로 부분을 읽고 실수를 회복하기 쉬운 방향을 기준으로 삼습니다. 친구와 플레이한다면 팀에 이미 있는 역할을 보고 빌드 플래너로 빈 역할을 시험하세요. 자신의 파티 소통 방식을 무시하고 상상 속 메타만 쫓을 필요는 없습니다.",
                "그다음 변하지 않는 사실과 변하는 신호를 나눕니다. 제품명, 플랫폼, 개발사, 상점 정보는 Steam 공식 페이지에서 확인합니다. 가격, 평가, 대기 시간, 클래스 강점은 변합니다. 리뷰는 신호를 읽는 법을 설명할 수 있지만 전제 날짜를 밝혀야 하며 초기 인상을 영구적인 결론처럼 말하지 않아야 합니다.",
                "짧은 결론은 이렇습니다. 추출 루프 자체가 끌리고 PC가 지원되며 현재 Steam 정보가 기대와 맞으면 구매를 검토하세요. 출시 분위기, 할인 카운트다운, 누군가의 최강 클래스 주장만으로 서두르지는 마세요. 고정 점수보다 이 판단 기준이 패치 이후에도 오래갑니다."
            ]},
            {"type": "table", "title": "지금 구매, 대기, 보류", "headers": ["상황", "실용적인 선택", "이유"], "rows": [
                ["추출 PvPvE를 좋아함", "현재 정보 확인 후 고려", "핵심 루프가 취향에 맞을 가능성이 큽니다."],
                ["편안한 캠페인을 원함", "대기 또는 보류", "장비 손실 구조가 맞지 않을 수 있습니다."],
                ["고정 파티가 있음", "역할 구성을 먼저 확인", "클래스 조합이 경험을 바꿉니다."],
                ["PC나 지역이 불확실함", "대기", "사양, 가격, 최신 평가를 확인합니다."],
                ["현재 메타만 따라가려 함", "서두르지 않기", "패치가 추천을 바꿀 수 있습니다."]
            ]},
            {"type": "faq", "title": "Mistfall Hunter 리뷰 자주 묻는 질문", "items": [
                ["Mistfall Hunter는 살 만한가요?", "추출 PvPvE, 반복 플레이, 압박 속 판단을 좋아한다면 구매 후보입니다. 결제 전 Steam 가격, 사양, 최근 평가, 활동을 확인하세요."],
                ["솔로 플레이어에게 좋은가요?", "가능하지만 솔로는 자기 회복, 정보, 관대한 클래스가 더 중요합니다. Mercenary부터 시작하되 실제 세션으로 확인하세요."],
                ["초보자에게 좋은 클래스는 무엇인가요?", "이 사이트 모델에서는 Mercenary가 낮은 위험의 시작 방향입니다. 파티에서 튼튼한 앵커를 원하면 Withered Knight도 좋습니다."],
                ["공식 점수가 있나요?", "없습니다. 독립 팬 리뷰이자 판단 가이드입니다. 모드, 클래스, PC, 밸런스에 따라 답이 달라져 고정 점수를 피했습니다."],
                ["가격과 현재 플레이어 수는 어디서 보나요?", "지역 가격과 제품 정보는 Steam 공식 페이지에서, 활동 신호는 SteamDB 차트에서 확인하세요. 사이트의 가격 및 플레이어 수 가이드도 도움이 됩니다."],
                ["패치 후에도 리뷰가 유효한가요?", "판단 프레임은 유효하지만 클래스, 성능, 대기 시간, 가치는 바뀔 수 있습니다. 오래된 세부 정보는 최신 공식 자료와 플레이어 근거로 다시 확인하세요."]
            ]},
            {"type": "links", "title": "리뷰 확인 출처", "items": [
                ["Mistfall Hunter 공식 Steam 페이지", OFFICIAL_STEAM_URL, "제품 정체성, 플랫폼, 가격, 사양, 평가와 현재 상점 상태.", "noopener"],
                ["SteamDB Mistfall Hunter 차트", STEAMDB_CHARTS_URL, "현재 플레이어와 피크의 제3자 맥락; 방향성 신호로만 읽습니다.", "nofollow noopener"],
                ["Steam 환불 정책", "https://store.steampowered.com/steam_refunds/", "결제 전에 현재 플랫폼 규정을 확인합니다.", "nofollow noopener"]
            ]},
            {"type": "related", "title": "관련 Mistfall Hunter 가이드", "items": [
                ["Mistfall Hunter 클래스 가이드", get_page_path("classes", "ko"), "역할, 위험도, 초보자 방향을 비교합니다."],
                ["Mistfall Hunter 빌드 플래너", get_page_path("build-planner", "ko"), "솔로, 듀오, 파티에 맞는 클래스를 찾습니다."],
                ["Mistfall Hunter 플레이어 수 가이드", get_page_path("player-count", "ko"), "SteamDB 신호와 대기 시간 맥락을 읽습니다."],
                ["Mistfall Hunter 가격 가이드", get_page_path("price", "ko"), "가격, 할인, 구매 전 주의점을 확인합니다."],
                ["Mistfall Hunter Steam 정보", get_page_path("steam", "ko"), "공식 플랫폼과 출시 사실을 확인합니다."]
            ]}
        ]
    }
})


REVIEW_PAGE_DATA.update({
    "it": {
        "page": {
            "title": "Recensione Mistfall Hunter: vale la pena comprarlo?",
            "description": "Recensione pratica di Mistfall Hunter: loop extraction, classi, prezzo Steam, attivita e controlli prima dell'acquisto.",
            "h1": "Recensione Mistfall Hunter: vale la pena comprarlo?",
            "kicker": "Recensione Mistfall Hunter | Aggiornata ad agosto 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-review-verdict.webp", "alt": "Illustrazione editoriale di una rotta di estrazione di Mistfall Hunter", "caption": "Illustrazione editoriale generata per questa recensione realizzata dai fan; non è uno screenshot ufficiale."},
            {"type": "rich", "title": "Verdetto rapido: un extraction ARPG per il giocatore giusto", "paragraphs": [
                "La nostra recensione Mistfall Hunter arriva a un verdetto condizionato: il gioco merita attenzione se ti piacciono PvPvE extraction, run ripetute, rischio di perdere equipaggiamento e apprendimento di un ruolo attraverso il gioco. È meno adatto se cerchi una breve campagna single-player o una progressione tranquilla senza passi indietro. La domanda utile non è se sia buono per tutti, ma se le decisioni su rotta, combattimento ed estrazione ti spingano a fare un'altra partita.",
                "Mistfall Hunter funziona soprattutto per chi ama decidere sotto pressione. Entri con un piano, leggi il pericolo, scegli quando combattere e confronti il valore di restare con il valore di uscire con ciò che hai già trovato. Per questo la scelta della classe conta: una classe frontale perdona più errori, mentre burst e controllo richiedono posizione e tempismo più precisi.",
                "La cautela principale è la fase iniziale del gioco. Rotte, bilanciamento, prestazioni e sensazione del matchmaking possono cambiare mentre la community impara. Leggi questa pagina come guida indipendente, non come tier list ufficiale. Prima di pagare controlla la pagina Steam, le recensioni recenti, la compatibilità del PC e l'attività nella tua fascia oraria."
            ]},
            {"type": "table", "title": "Mistfall Hunter in breve", "headers": ["Domanda", "Risposta della recensione", "Perché conta"], "rows": [
                ["Che gioco è?", "ARPG PvPvE extraction", "Ogni run unisce combattimento, rotta, rischio del loot e scelta dell'uscita."],
                ["A chi si adatta?", "A chi ama run tese e ripetibili", "Il valore sta nelle decisioni e nell'apprendimento, non solo nella storia."],
                ["È facile per iniziare?", "Sì con la classe giusta, ma non senza attrito", "Mercenary e Withered Knight danno più margine all'inizio."],
                ["Conviene comprarlo subito?", "Controlla prima i dati Steam attuali", "Prezzo, recensioni, requisiti e attività cambiano."],
                ["Qual è la posizione del sito?", "Risorsa indipendente realizzata dai fan", "I consigli sulle classi sono editoriali e separati dai fatti ufficiali."]
            ]},
            {"type": "rich", "title": "Cosa richiede il loop di estrazione", "paragraphs": [
                "Un gioco extraction inizia con un piano incompleto. Rotta, nemici, loot e altri giocatori ti obbligano ad adattarlo. Una competenza importante è capire quando un guadagno piccolo è già sufficiente. Restare per un altro forziere può migliorare la run, ma trasformare un'uscita sicura in perdita dell'equipaggiamento. Questa tensione dà identità al gioco e rende le prime ore meno comode di un action RPG tradizionale.",
                "Il loop premia l'informazione quanto l'esecuzione. Devi riconoscere un combattimento favorevole, la finestra forte della tua classe e il momento in cui la squadra ha già speso troppe risorse per continuare. Una build non è quindi solo una lista di danni: comprende posizione, recupero, disimpegno e un rischio che il gruppo sappia comunicare.",
                "Solo e squadra possono sembrare due giochi diversi. In solo pesano di più recupero personale, informazioni e correzione degli errori. In gruppo, controllo, scouting e un ruolo d'ancora creano sicurezza condivisa, ma richiedono coordinazione. Gioca alcune sessioni nel formato che userai davvero prima di decidere se il gioco fa per te."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Artwork ufficiale Steam di Mistfall Hunter in una battaglia innevata", "caption": "Artwork ufficiale Steam usato per identificare il gioco; non è una prova delle prestazioni."},
            {"type": "rich", "title": "Classi e curva di apprendimento", "paragraphs": [
                "Il modo più utile per valutare le classi Mistfall Hunter è partire dal bisogno del giocatore, non da un vincitore universale. Mercenary offre una linea frontale facile da leggere e va bene per chi vuole margine d'errore. Withered Knight aggiunge resistenza e controllo dello spazio per chi vuole fare da ancora alla squadra. Forse producono meno momenti spettacolari, ma rendono più chiaro il linguaggio delle decisioni.",
                "Blackarrow, Shadowstrix e Sorcerer richiedono un tempismo più consapevole. Blackarrow premia distanza, scouting e pressione paziente. Shadowstrix crea buone finestre di imboscata e disimpegno, ma punisce presto una posizione sbagliata. Sorcerer offre burst e controllo ad area. Seer cresce di valore quando informazione, utilità e decisioni sicure della squadra contano più del danno personale.",
                "Nella prima sessione usa guida classi e planner build come una mappa, non come un ordine. Scegli un compito che puoi spiegare in una frase e verifica se aiuta davvero sopravvivenza e comunicazione. Se due opzioni sono vicine, considerale un pareggio e copri il ruolo mancante. Questo metodo resta utile anche dopo una patch."
            ]},
            {"type": "table", "title": "Direzione iniziale per esigenza", "headers": ["Esigenza", "Direzione", "Compromesso"], "rows": [
                ["Prime run solo", "Mercenary", "Perdona più errori, ma ha meno burst."],
                ["Ancora della squadra", "Withered Knight", "Scambia parte del danno con spazio e resistenza."],
                ["Distanza e scouting", "Blackarrow", "Posizione e pazienza contano più del faccia a faccia."],
                ["Fianchi aggressivi", "Shadowstrix", "Ricompensa alta con punizione più severa."],
                ["Area o utilità", "Sorcerer o Seer", "Scegli tra controllo esplosivo e informazione di squadra."]
            ]},
            {"type": "rich", "title": "Punti forti, limiti e controlli", "paragraphs": [
                "Il punto forte di Mistfall Hunter è la densità delle decisioni. Anche una run breve ti chiede di confrontare tempo, rumore, valore dell'equipaggiamento, pressione nemica e risorse per il prossimo combattimento. Un'estrazione riuscita sembra meritata perché il gioco non risolve tutto al posto tuo. Il planner classi aiuta separando solo, duo e squadra invece di applicare lo stesso punteggio a tutti.",
                "Il compromesso è la fatica prima che le abitudini diventino naturali. Se non ami perdere progressi, uscire con poco o rileggere una rotta più volte, il loop può sembrare attrito. Se ti piace trasformare una sconfitta in un piano migliore, lo stesso attrito diventa il motivo per tornare. È una questione di compatibilità, non di abilità.",
                "Prima dell'acquisto controlla quattro segnali attuali: prezzo regionale Steam, direzione delle recensioni recenti, requisiti e prestazioni sul tuo PC, attività nell'orario in cui giochi. Le risorse prezzo e giocatori del sito spiegano questi controlli. La recensione indica cosa guardare, ma non sostituisce store ufficiale o dati recenti della community."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Header ufficiale Steam di Mistfall Hunter in una foresta scura", "caption": "Header ufficiale come seconda verifica dell'identità; non viene presentato come prova di gameplay."},
            {"type": "rich", "title": "Come usare questa recensione prima di comprare", "paragraphs": [
                "Parti dal formato che giocherai davvero. Se giochi soprattutto solo, leggi i consigli solo della guida classi e usa una direzione permissiva come base. Con amici, controlla i ruoli già presenti e prova il ruolo mancante nel planner. Non devi comprare inseguendo una meta immaginaria che non coincide con la comunicazione della tua squadra.",
                "Poi separa fatti stabili e segnali variabili. Nome del prodotto, piattaforma, sviluppatore e identità dello store vanno verificati su Steam ufficiale. Prezzo, recensioni, code e forza delle classi cambiano. Una recensione può spiegare come leggere questi segnali, ma deve datare le sue premesse e non trasformare una prima impressione in un verdetto eterno.",
                "La conclusione breve è questa: valuta l'acquisto se il loop extraction ti attrae, il PC è compatibile e i dati Steam attuali confermano le tue aspettative. Aspetta se reagisci solo a hype di lancio, conto alla rovescia dello sconto o alla presunta classe migliore. Questa regola dura più di un voto fisso e lascia spazio alle patch."
            ]},
            {"type": "table", "title": "Comprare, aspettare o lasciare perdere?", "headers": ["Situazione", "Scelta pratica", "Motivo"], "rows": [
                ["Ti piace PvPvE extraction", "Valuta dopo i controlli live", "Il loop centrale probabilmente ti si adatta."],
                ["Vuoi una campagna rilassata", "Aspetta o lascia perdere", "Il rischio di perdita può essere inadatto."],
                ["Hai una squadra fissa", "Controlla la copertura dei ruoli", "Il fit delle classi cambia l'esperienza."],
                ["PC o regione incerti", "Aspetta", "Conferma requisiti, prezzo e recensioni attuali."],
                ["Insegui solo la meta attuale", "Non avere fretta", "Le patch possono cambiare i consigli."]
            ]},
            {"type": "faq", "title": "Domande frequenti sulla recensione Mistfall Hunter", "items": [
                ["Mistfall Hunter vale la pena?", "È da considerare se ti piacciono PvPvE extraction, run ripetibili e decisioni sotto pressione. Controlla prezzo, requisiti, recensioni recenti e attività Steam prima di pagare."],
                ["È adatto ai giocatori solo?", "Può esserlo, ma il solo richiede più recupero, informazioni e una classe permissiva. Mercenary è una direzione pratica; provala prima di considerarla definitiva."],
                ["Quale classe è buona per iniziare?", "Il modello del sito indica Mercenary come direzione a basso rischio. Withered Knight è sensata se vuoi fare da ancora resistente alla squadra."],
                ["La recensione dà un voto ufficiale?", "No. È una recensione indipendente realizzata dai fan e una guida decisionale. Un voto fisso nasconderebbe l'effetto di modalità, classe, PC e bilanciamento."],
                ["Dove controllo prezzo e giocatori attuali?", "Usa Steam ufficiale per prezzo regionale e fatti del prodotto. Usa SteamDB come segnale esterno di attività; le risorse prezzo e giocatori spiegano come leggerlo."],
                ["La recensione sarà valida dopo le patch?", "Il metodo resta utile, ma classi, prestazioni, code e valore possono cambiare. Ricontrolla informazioni ufficiali e testimonianze recenti."]
            ]},
            {"type": "links", "title": "Fonti e verifiche della recensione", "items": [
                ["Pagina Steam ufficiale di Mistfall Hunter", OFFICIAL_STEAM_URL, "Identità, piattaforma, prezzo, requisiti, recensioni e stato attuale dello store.", "noopener"],
                ["Grafici Mistfall Hunter su SteamDB", STEAMDB_CHARTS_URL, "Contesto terzo su giocatori e picchi; usalo come segnale direzionale.", "nofollow noopener"],
                ["Politica rimborsi Steam", "https://store.steampowered.com/steam_refunds/", "Controlla le regole attuali della piattaforma prima di pagare.", "nofollow noopener"]
            ]},
            {"type": "related", "title": "Risorse Mistfall Hunter correlate", "items": [
                ["Manuale classi Mistfall Hunter", get_page_path("classes", "it"), "Confronta ruoli, rischio e direzioni per principianti."],
                ["Planner build Mistfall Hunter", get_page_path("build-planner", "it"), "Abbina una classe a solo, duo o squadra."],
                ["Risorsa giocatori Mistfall Hunter", get_page_path("player-count", "it"), "Leggi segnali SteamDB e contesto delle code."],
                ["Risorsa prezzo Mistfall Hunter", get_page_path("price", "it"), "Controlla prezzo, sconti e note prima dell'acquisto."],
                ["Info Steam Mistfall Hunter", get_page_path("steam", "it"), "Verifica fatti ufficiali di piattaforma e uscita."]
            ]}
        ]
    }
})


for locale in LOCALE_ORDER:
    TEXT[locale]["pages"]["review"] = REVIEW_PAGE_DATA[locale]["page"]
    player_count_data = localized_player_count_data(locale)
    TEXT[locale]["pages"]["player-count"] = player_count_data["page"]


def get_route_matrix():
    """
    生成所有语言和页面的静态路由矩阵。

    :return: list[dict]，包含页面标识、语言和路径的路由列表
    """
    routes = []
    for locale in LOCALE_ORDER:
        for page_key in PAGE_ORDER:
            routes.append({"locale": locale, "page_key": page_key, "path": get_page_path(page_key, locale)})
    return routes


def get_alternate_urls(page_key):
    """
    生成当前页面的所有 hreflang 对应链接。

    :param page_key: 页面标识
    :return: dict，语言代码到绝对 URL 的映射
    """
    alternates = {}
    for locale in LOCALE_ORDER:
        alternates[locale] = f"{BASE_URL}{get_page_path(page_key, locale)}"
    alternates["x-default"] = f"{BASE_URL}{get_page_path(page_key, 'en')}"
    return alternates


def get_language_links(page_key):
    """
    生成语言切换器需要的当前页面等价链接。

    :param page_key: 页面标识
    :return: list[dict]，语言名称、代码和路径列表
    """
    return [
        {"code": locale, "name": LOCALES[locale]["name"], "url": get_page_path(page_key, locale)}
        for locale in LOCALE_ORDER
    ]


def localized_classes(locale):
    """
    生成指定语言的职业卡片数据。

    :param locale: 语言代码
    :return: list[dict]，本地化后的职业数据
    """
    text = get_locale_text(locale)
    rows = []
    for item in CLASS_STATS:
        role, best_for = text["classes"]["roles"][item["id"]]
        rows.append({**item, "role": role, "best_for": best_for, "risk_label": text["classes"]["risk"][item["risk"]]})
    return rows


def make_simple_sections(locale, page_key):
    """
    生成普通内容页的本地化正文区块。

    :param locale: 语言代码
    :param page_key: 页面标识
    :return: list[dict]，模板可渲染的正文区块列表
    """
    text = get_locale_text(locale)
    simple = text.get("simple", TEXT["en"].get("simple", {}))
    labels = SIMPLE_LABELS[locale]
    primary = KEYWORD_MAP[locale]["primary"]
    if page_key == "classes":
        return [
            {"type": "classes"},
            {"type": "rich", "title": simple.get("classes_title", text["pages"]["classes"]["h1"]), "paragraphs": simple.get("classes_paragraphs", [])},
            {"type": "table", "title": labels["class_table"], "headers": labels["class_headers"], "rows": [[c["name"], c["role"], c["best_for"]] for c in localized_classes(locale)]},
            {"type": "faq", "title": text["home"]["faq_title"], "items": text["home"]["faq"]},
        ]
    if page_key == "build-planner":
        return [
            {"type": "planner", "short": True},
            {"type": "rich", "title": text["pages"]["build-planner"]["h1"], "paragraphs": simple.get("build_paragraphs", [])},
            {"type": "table", "title": labels["planner_table"], "headers": labels["planner_headers"], "rows": [[text["planner"]["options"]["experience"]["new"], text["planner"]["options"]["format"]["solo"] + ", " + text["planner"]["options"]["style"]["balanced"] + ", " + text["planner"]["options"]["risk"]["low"], localized_classes(locale)[0]["name"]], [text["planner"]["options"]["format"]["squad"], text["planner"]["options"]["style"]["control"] + ", " + text["planner"]["options"]["risk"]["medium"], localized_classes(locale)[4]["name"] + " / " + localized_classes(locale)[5]["name"]], [text["planner"]["options"]["format"]["duo"], text["planner"]["options"]["style"]["burst"] + ", " + text["planner"]["options"]["risk"]["high"], localized_classes(locale)[2]["name"] + " / " + localized_classes(locale)[3]["name"]]]},
            {"type": "faq", "title": labels["planner_faq"], "items": text["home"]["faq"][:4]},
        ]
    if page_key == "steam":
        return [
            {"type": "steam"},
            {"type": "rich", "title": text["pages"]["steam"]["h1"], "paragraphs": simple.get("steam_paragraphs", [])},
            {"type": "faq", "title": labels["steam_faq"], "items": text["home"]["faq"][:3]},
            {"type": "related", "title": text["pages"]["player-count"]["h1"], "items": [[text["pages"]["player-count"]["h1"], get_page_path("player-count", locale), text["pages"]["player-count"]["description"]], [text["pages"]["price"]["h1"], get_page_path("price", locale), text["pages"]["price"]["description"]]]},
        ]
    if page_key == "price":
        related = PRICE_RELATED_COPY[locale]
        return PRICE_PAGE_DATA[locale]["sections"] + [
            {"type": "related", "title": related["title"], "items": [[related["steam_label"], get_page_path("steam", locale), related["steam_desc"]], [related["classes_label"], get_page_path("classes", locale), related["classes_desc"]], [related["planner_label"], get_page_path("build-planner", locale), related["planner_desc"]], [REVIEW_PAGE_DATA[locale]["page"]["h1"], get_page_path("review", locale), REVIEW_PAGE_DATA[locale]["page"]["description"]]]}
        ]
    if page_key == "player-count":
        return localized_player_count_data(locale)["sections"]
    if page_key == "review":
        return REVIEW_PAGE_DATA[locale]["sections"]
    if page_key == "about":
        return [{"type": "rich", "title": text["pages"]["about"]["h1"], "paragraphs": simple.get("about", [])}]
    if page_key == "contact":
        return [{"type": "rich", "title": text["pages"]["contact"]["h1"], "paragraphs": simple.get("contact", [])}]
    if page_key == "privacy-policy":
        return [{"type": "rich", "title": text["pages"]["privacy-policy"]["h1"], "paragraphs": simple.get("privacy", [])}]
    if page_key == "terms-of-service":
        return [{"type": "rich", "title": text["pages"]["terms-of-service"]["h1"], "paragraphs": simple.get("terms", [])}]
    return []


def build_site_data(page_key, locale="en"):
    """
    组装指定页面和语言的渲染数据。

    :param page_key: 页面标识
    :param locale: 语言代码
    :return: dict，模板渲染所需的站点、页面、导航和语言数据
    """
    if locale not in LOCALE_ORDER or page_key not in PAGE_ORDER:
        abort(404)
    text = get_locale_text(locale)
    page = {**text["pages"][page_key], "path": get_page_path(page_key, locale), "key": page_key}
    page_image = "images/mistfall/mistfall-hunter-review-verdict.webp" if page_key == "review" else "images/mistfall/mistfall-hunter-steam-hero.webp"
    return {
        "base_url": BASE_URL,
        "support_email": SUPPORT_EMAIL,
        "official_steam_url": OFFICIAL_STEAM_URL,
        "current_year": CURRENT_YEAR,
        "last_updated": LAST_UPDATED,
        "locale": locale,
        "locale_meta": LOCALES[locale],
        "locales": LOCALES,
        "site_name": text["site_name"],
        "text": text,
        "page_key": page_key,
        "page": page,
        "canonical_url": f"{BASE_URL}{page['path']}",
        "page_image_url": f"{BASE_URL}/static/{page_image}",
        "alternate_urls": get_alternate_urls(page_key),
        "x_default_url": f"{BASE_URL}{get_page_path(page_key, 'en')}",
        "language_links": get_language_links(page_key),
        "classes": localized_classes(locale),
        "planner_config": {"classes": localized_classes(locale), "text": text["planner"]},
        "keyword_map": REVIEW_KEYWORD_MAP[locale] if page_key == "review" else KEYWORD_MAP[locale],
        "labels": SIMPLE_LABELS[locale],
        "sections": make_simple_sections(locale, page_key),
    }


def render_site_page(page_key, locale="en"):
    """
    渲染指定语言的站点页面。

    :param page_key: 页面标识
    :param locale: 语言代码
    :return: str，渲染完成的 HTML 内容
    """
    template = "index.html" if page_key == "home" else "simple-page.html"
    return render_template(template, **build_site_data(page_key, locale))


@app.route("/")
def index():
    """
    渲染英文首页。

    :return: str，英文首页 HTML 内容
    """
    return render_site_page("home", "en")


@app.route("/<locale>/", strict_slashes=False)
def localized_index(locale):
    """
    渲染本地化首页。

    :param locale: 语言代码
    :return: str，本地化首页 HTML 内容
    """
    page_key = {slug: key for key, slug in PAGE_SLUGS.items() if slug}.get(locale)
    if page_key:
        return render_site_page(page_key, "en")
    if locale == "en":
        return render_site_page("home", "en")
    if locale not in LOCALE_ORDER:
        abort(404)
    return render_site_page("home", locale)


@app.route("/<page_slug>/", strict_slashes=False)
def english_page(page_slug):
    """
    渲染英文内页。

    :param page_slug: 页面路径段
    :return: str，英文内页 HTML 内容
    """
    page_key = {slug: key for key, slug in PAGE_SLUGS.items() if slug}.get(page_slug)
    if not page_key:
        abort(404)
    return render_site_page(page_key, "en")


@app.route("/<locale>/<page_slug>/", strict_slashes=False)
def localized_page(locale, page_slug):
    """
    渲染本地化内页。

    :param locale: 语言代码
    :param page_slug: 页面路径段
    :return: str，本地化内页 HTML 内容
    """
    if locale not in LOCALE_ORDER or locale == "en":
        abort(404)
    page_key = {slug: key for key, slug in PAGE_SLUGS.items() if slug}.get(page_slug)
    if not page_key:
        abort(404)
    return render_site_page(page_key, locale)


@app.errorhandler(404)
def page_not_found(error):
    """
    渲染 404 错误页面。

    :param error: Flask 传入的错误对象
    :return: tuple[str, int]，404 页面 HTML 和状态码
    """
    data = build_site_data("home", "en")
    data["page"] = {"path": "/404.html", "title": "Page Not Found", "description": "The requested Mistfall Hunter Classes page could not be found.", "h1": "Page Not Found", "kicker": "Mistfall Hunter Classes"}
    data["sections"] = [{"type": "rich", "title": "Page Not Found", "paragraphs": ["The requested page could not be found. Return to the Mistfall Hunter class planner."]}]
    return render_template("simple-page.html", **data), 404


def find_available_port(start_port):
    """
    从指定端口开始查找可用的本地服务端口。

    :param start_port: 起始端口号
    :return: int，可用于启动本地服务的端口号
    """
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
            port += 1


if __name__ == "__main__":
    app.run(debug=True, port=find_available_port(5001))
