"""Mistfall Hunter PS5 页面内容、关键词边界和多语言编辑数据。"""


PS5_KEYWORD_MAP = {
    "en": {
        "market": "US",
        "primary": "Mistfall Hunter PS5",
        "related": ["Mistfall Hunter on PS5", "Mistfall Hunter PS5 release date", "Mistfall Hunter PS5 price", "Mistfall Hunter Xbox"],
        "rejected": ["Mistfall Hunter PS5 performance benchmark", "Mistfall Hunter PS5 crossplay"],
        "evidence": "Similarweb global phrase match exact: average volume 1384, 28-day window volume 39280, difficulty 25; official PlayStation Store page returned 200.",
        "confidence": "high",
    },
    "es": {
        "market": "US / Latin America",
        "primary": "Mistfall Hunter en PS5",
        "related": ["fecha de lanzamiento de Mistfall Hunter en PS5", "precio de Mistfall Hunter PS5", "Mistfall Hunter Xbox", "Mistfall Hunter consola"],
        "rejected": ["rendimiento PS5 garantizado", "crossplay de Mistfall Hunter"],
        "evidence": "Similarweb localized probe returned no rows; wording follows neutral Spanish game-search usage and the global platform cluster.",
        "confidence": "low",
    },
    "ja": {
        "market": "Japan",
        "primary": "Mistfall Hunter PS5",
        "related": ["Mistfall Hunter PS5 発売日", "Mistfall Hunter PS5 価格", "Mistfall Hunter PS5 対応機種", "Mistfall Hunter Xbox"],
        "rejected": ["Mistfall Hunter PS5 動作保証", "Mistfall Hunter PS5 クロスプレイ"],
        "evidence": "Similarweb localized probe returned no rows; Japanese terms are natural platform-search forms bounded by the official PS5 product source.",
        "confidence": "low",
    },
    "fr": {
        "market": "France",
        "primary": "Mistfall Hunter sur PS5",
        "related": ["date de sortie de Mistfall Hunter sur PS5", "prix de Mistfall Hunter PS5", "Mistfall Hunter Xbox", "Mistfall Hunter console"],
        "rejected": ["performances PS5 garanties", "cross-play confirmé Mistfall Hunter"],
        "evidence": "Similarweb localized probe returned no rows; French platform wording is bounded by the global PS5 cluster and official platform pages.",
        "confidence": "low",
    },
    "de": {
        "market": "Germany",
        "primary": "Mistfall Hunter auf PS5",
        "related": ["Mistfall Hunter PS5 Release", "Mistfall Hunter PS5 Preis", "Mistfall Hunter Xbox", "Mistfall Hunter Konsole"],
        "rejected": ["PS5 FPS Garantie", "bestätigtes Crossplay Mistfall Hunter"],
        "evidence": "Similarweb localized probe returned no rows; German release and price forms follow the official platform entity.",
        "confidence": "low",
    },
    "pt": {
        "market": "Brazil",
        "primary": "Mistfall Hunter no PS5",
        "related": ["data de lançamento de Mistfall Hunter no PS5", "preço de Mistfall Hunter PS5", "Mistfall Hunter Xbox", "Mistfall Hunter console"],
        "rejected": ["desempenho PS5 garantido", "crossplay confirmado de Mistfall Hunter"],
        "evidence": "Similarweb localized probe returned no rows; Brazilian Portuguese platform wording is bounded by the global exact cluster.",
        "confidence": "low",
    },
    "ko": {
        "market": "Korea",
        "primary": "Mistfall Hunter PS5",
        "related": ["Mistfall Hunter PS5 출시일", "Mistfall Hunter PS5 가격", "Mistfall Hunter PS5 지원 기기", "Mistfall Hunter Xbox"],
        "rejected": ["Mistfall Hunter PS5 프레임 보장", "Mistfall Hunter PS5 크로스플레이 확정"],
        "evidence": "Similarweb localized probe returned no rows; Korean platform terms are natural forms bounded by official PS5 and Xbox sources.",
        "confidence": "low",
    },
    "it": {
        "market": "Italy",
        "primary": "Mistfall Hunter su PS5",
        "related": ["data di uscita di Mistfall Hunter su PS5", "prezzo Mistfall Hunter PS5", "Mistfall Hunter Xbox", "Mistfall Hunter console"],
        "rejected": ["prestazioni PS5 garantite", "crossplay confermato Mistfall Hunter"],
        "evidence": "Similarweb localized probe returned no rows; Italian platform wording is bounded by the global PS5 cluster and official pages.",
        "confidence": "low",
    },
}


PS5_RELATED_TITLES = {
    "en": "Related Mistfall Hunter guides",
    "es": "Guias relacionadas de Mistfall Hunter",
    "ja": "関連するMistfall Hunterガイド",
    "fr": "Ressources Mistfall Hunter liees",
    "de": "Verwandte Mistfall Hunter Ressourcen",
    "pt": "Guias relacionados de Mistfall Hunter",
    "ko": "관련 Mistfall Hunter 가이드",
    "it": "Risorse Mistfall Hunter correlate",
}


PS5_PAGE_DATA = {
    "en": {
        "page": {
            "title": "Mistfall Hunter PS5: Release Date, Price & How to Play",
            "description": "Mistfall Hunter PS5 guide: check the official PS5 release date, price, platform status, and how PS5 compares with Steam and Xbox.",
            "h1": "Mistfall Hunter PS5: Release Date, Price, and How to Play",
            "kicker": "Mistfall Hunter PS5 | Checked August 19, 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-ps5-console-concept.webp", "alt": "Editorial concept illustration comparing a PS5 setup with a PC setup for Mistfall Hunter", "caption": "Editorial concept illustration for this guide. It is not an official PlayStation listing or gameplay screenshot."},
            {"type": "rich", "title": "Quick answer: Mistfall Hunter is listed for PS5", "paragraphs": [
                "Yes. The official PlayStation Store page checked on August 19, 2026 lists Mistfall Hunter as a PS5 product. Its product data shows a July 30, 2026 release date and a US price of $24.99 at the time of the check. Store prices, taxes, editions, and availability can vary by country, so treat the US figure as a reference rather than a universal price.",
                "The official Mistfall Hunter website also links to PlayStation and Xbox destinations alongside Steam. That matters because older launch coverage may describe the game as a PC release only. The practical answer for a PS5 player is to open the live PlayStation page, confirm that the product is available in your region, and check the current edition before buying.",
                "This guide separates verified platform facts from questions the checked sources do not settle. The PS5 listing proves platform availability, but it does not by itself promise a particular frame rate, cross-play rule, cross-save behavior, or identical performance to a gaming PC. Those details should come from a current platform notice, patch note, or repeatable test rather than a guessed number."
            ]},
            {"type": "table", "title": "Mistfall Hunter platforms at a glance", "headers": ["Platform", "Checked official status", "What to verify before buying"], "rows": [
                ["PS5", "Official PlayStation product page; July 30, 2026 release shown", "Regional price, edition, PS5 availability, and current store notices."],
                ["Xbox", "Official Xbox Store product page; July 30, 2026 release shown", "Region, Xbox edition, subscription or purchase terms, and current availability."],
                ["PC / Steam", "Official Steam page; July 29, 2026 release shown", "Windows requirements, 45 GB storage line, recent reviews, and PC performance."],
                ["Cross-play / cross-save", "Not confirmed by the checked pages", "Do not assume that console and PC accounts share progress or matchmaking."],
            ]},
            {"type": "rich", "title": "What the official PS5 page tells you", "paragraphs": [
                "A platform store page is the strongest place to answer whether a game is actually listed for a console. The PlayStation page identifies Mistfall Hunter as a full game, names the PS5 platform, shows a product price in the checked US region, and includes an official release date. It is more useful for this question than a forum comment or a recycled pre-release article.",
                "The page is still time-sensitive. A store can change price, edition packaging, promotion, age-rating display, or regional availability without changing the game title. Before you pay, open the page from the official site or the PlayStation Store directly, confirm the platform label says PS5, and make sure the product is not a similarly named add-on or bundle.",
                "The Xbox listing is useful as a second console reference, not as proof that every platform has identical features. The official Xbox page checked for this guide lists the game and a July 30, 2026 release date. If you are choosing between console ecosystems, compare the live store page, controller preference, friend list, and edition terms that apply to your account."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Official Steam artwork showing Mistfall Hunter characters in a snowy battle", "caption": "Official Steam store artwork used to identify the game. It is PC store media, not a PS5 performance capture."},
            {"type": "rich", "title": "PS5 vs Steam vs Xbox: which version fits?", "paragraphs": [
                "Choose PS5 when you want the console version in a living-room setup and would rather avoid comparing Windows components. The decision is straightforward when your friends, purchase region, and preferred controller are already tied to PlayStation. Check the store listing for the exact edition and live price before you place the order.",
                "Choose Steam when you want to evaluate PC requirements, recent review direction, graphics settings, or upgrade flexibility. Steam is the clearest source for the Windows specification table, including the listed operating system, processor, memory, graphics card, DirectX version, network connection, and 45 GB storage requirement. Those values are useful for PC buyers but should not be copied onto the PS5 page as if they were console requirements.",
                "Choose Xbox when your group and account already live in that ecosystem or the official Xbox listing is the better regional option. The presence of an Xbox page does not answer cross-platform matchmaking or cross-progression. Keep those as separate checks, because a store listing and a multiplayer policy answer different questions.",
                "For activity and buyer context, use the site's existing player-count and price guides after opening the correct platform store. The player-count guide explains SteamDB signals, while the price guide focuses on regional price and refund checks. The review page adds a fit-based opinion, not an official score."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Official Mistfall Hunter Steam header art used as a product identity reference", "caption": "Official store header used as a product identity reference; this guide does not treat store art as a console screenshot."},
            {"type": "rich", "title": "How to verify PS5 availability after an update", "paragraphs": [
                "First, start with the official Mistfall Hunter website or the PlayStation Store product page. Search results, social posts, and videos can lag behind a regional store change. The official page should be the source for a current listing, price, edition, and platform label.",
                "Second, write down the date and region you checked. The release date is stable as a historical fact, but price, bundles, discounts, and account restrictions are time-sensitive. A dated check makes the difference between a useful guide and a page that quietly turns an old screenshot into a permanent claim.",
                "Third, separate availability from performance. If you need to know whether the PS5 version is smooth, look for current patch notes and repeatable tests from the platform you use. Do not use the Steam PC requirements table, an unrelated YouTube thumbnail, or one early comment as a PS5 benchmark.",
                "Finally, confirm the account and multiplayer details that matter to your group. Cross-play, cross-save, voice chat, regional matchmaking, and entitlement transfer may have different rules. If the official store or developer documentation does not state a feature, this page leaves it unconfirmed instead of guessing."
            ]},
            {"type": "faq", "title": "Mistfall Hunter PS5 FAQ", "items": [
                ["Is Mistfall Hunter on PS5?", "Yes. The official PlayStation Store page checked on August 19, 2026 lists Mistfall Hunter as a PS5 full-game product. Open the live regional page before buying because price and availability can vary."],
                ["When was the Mistfall Hunter PS5 release date?", "The official PlayStation product data checked for this guide showed July 30, 2026. Keep the date as a historical reference and use the current store page for regional availability."],
                ["How much does Mistfall Hunter cost on PS5?", "The checked US PlayStation page showed $24.99. That is a dated US reference, not a promise about your region, tax, discount, bundle, or currency."],
                ["Is Mistfall Hunter better on PS5 or PC?", "There is no universal answer. PS5 is simpler when you want a console setup; PC gives you component, settings, and upgrade choices. Compare your own platform, friends, controller preference, and current performance evidence."],
                ["Does Mistfall Hunter support PS5 and PC cross-play?", "The checked official pages did not provide enough evidence to confirm cross-play or cross-save. Do not assume those features; check current developer or platform documentation."],
                ["Do the Steam system requirements apply to PS5?", "No. Steam requirements describe the Windows PC version. They can help a PC buyer, but they are not a PS5 hardware specification and should not be used to predict console performance."],
                ["Is Mistfall Hunter available on Xbox too?", "The official Xbox Store page checked for this guide lists Mistfall Hunter with a July 30, 2026 release date. Verify your regional Xbox page and edition terms before purchasing."],
            ]},
            {"type": "links", "title": "Official platform sources", "items": [
                ["Mistfall Hunter on PlayStation Store", "https://store.playstation.com/en-us/concept/10017212", "PS5 product identity, platform, release data, and region-specific price page.", "noopener"],
                ["Mistfall Hunter on Xbox Store", "https://www.xbox.com/games/store/mistfall-hunter/9p8x6tvw9zw8", "Xbox product and availability reference.", "noopener"],
                ["Mistfall Hunter on Steam", "https://store.steampowered.com/app/3282300/Mistfall_Hunter/", "Windows PC facts, system requirements, reviews, and official store state.", "noopener"],
                ["Official Mistfall Hunter website", "https://mistfallhunter.com/", "Developer-facing platform links and current announcements.", "noopener"],
            ]},
        ],
    },
    "es": {
        "page": {
            "title": "Mistfall Hunter en PS5: fecha, precio y disponibilidad",
            "description": "Guia de Mistfall Hunter en PS5: comprueba la fecha oficial, el precio de referencia y las diferencias frente a Steam y Xbox.",
            "h1": "Mistfall Hunter en PS5: fecha, precio y como jugar",
            "kicker": "Mistfall Hunter en PS5 | Comprobado el 19 de agosto de 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-ps5-console-concept.webp", "alt": "Ilustracion conceptual que compara una configuracion PS5 y una PC para Mistfall Hunter", "caption": "Ilustracion conceptual editorial. No es una captura oficial de PlayStation ni una imagen real de gameplay."},
            {"type": "rich", "title": "Respuesta rapida: Mistfall Hunter aparece para PS5", "paragraphs": [
                "Si. La pagina oficial de PlayStation Store consultada el 19 de agosto de 2026 muestra Mistfall Hunter como un producto para PS5. Sus datos de producto indican el 30 de julio de 2026 como fecha de lanzamiento y mostraban 24,99 USD en la pagina de Estados Unidos. El precio, los impuestos, las ediciones y la disponibilidad dependen de la region.",
                "El sitio oficial de Mistfall Hunter tambien enlaza con PlayStation, Xbox y Steam. Por eso conviene separar la informacion actual de las noticias antiguas de lanzamiento. Abre la tienda oficial de tu region, comprueba que la plataforma diga PS5 y revisa la edicion antes de comprar.",
                "La ficha de PS5 confirma la plataforma, pero no confirma por si sola FPS, juego cruzado, guardado cruzado o rendimiento identico al de una PC. Esta guia deja esas funciones sin confirmar cuando las fuentes revisadas no las explican."
            ]},
            {"type": "table", "title": "Plataformas de Mistfall Hunter de un vistazo", "headers": ["Plataforma", "Estado oficial comprobado", "Que revisar antes de comprar"], "rows": [
                ["PS5", "Pagina oficial de PlayStation; lanzamiento mostrado: 30 de julio de 2026", "Precio regional, edicion y disponibilidad actual."],
                ["Xbox", "Pagina oficial de Xbox; lanzamiento mostrado: 30 de julio de 2026", "Region, condiciones de compra y edicion."],
                ["PC / Steam", "Pagina oficial de Steam; lanzamiento mostrado: 29 de julio de 2026", "Windows, requisitos, 45 GB, reseñas y rendimiento."],
                ["Juego cruzado / guardado cruzado", "No confirmado en las paginas revisadas", "No lo des por hecho sin documentacion actual."],
            ]},
            {"type": "rich", "title": "Como leer la pagina oficial de PS5", "paragraphs": [
                "Una ficha de tienda oficial es la mejor fuente para saber si un juego esta listado para una consola. La pagina de PlayStation identifica Mistfall Hunter como juego completo, muestra PS5 y ofrece datos de producto. Es mas fiable para esta pregunta que un comentario de foro o un video antiguo.",
                "Aun asi, la tienda puede cambiar precios, descuentos, paquetes y disponibilidad por region. Comprueba la fecha, el pais y el nombre exacto de la edicion. No confundas un juego completo con un complemento o un paquete de mejora.",
                "La pagina oficial de Xbox sirve como segunda referencia de consola, pero no prueba que todas las plataformas tengan las mismas funciones. Para elegir entre PS5, Xbox y PC, combina tienda, amigos, mando preferido y condiciones de cuenta."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Arte oficial de Steam de Mistfall Hunter en una batalla nevada", "caption": "Arte oficial de la tienda Steam para identificar el juego; no es una captura de rendimiento en PS5."},
            {"type": "rich", "title": "PS5 frente a Steam y Xbox", "paragraphs": [
                "PS5 encaja si quieres jugar desde el salon y no quieres comparar componentes de Windows. Steam es mejor punto de partida si necesitas revisar requisitos, ajustes graficos y reseñas recientes. Xbox puede ser la opcion natural si tu grupo y tu cuenta ya estan en ese ecosistema.",
                "Los requisitos de Steam describen la version de PC: Windows, procesador, memoria, grafica, DirectX, red y 45 GB de almacenamiento. No son requisitos de PS5 y no deben usarse para prometer FPS en consola.",
                "Para precio y actividad, consulta las guias existentes de precio y jugadores del sitio despues de abrir la tienda correcta. La reseña del sitio es una opinion independiente y no una puntuacion oficial."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Cabecera oficial de Steam de Mistfall Hunter usada para verificar la identidad del producto", "caption": "Cabecera oficial de la tienda como referencia de identidad; no se presenta como captura de consola."},
            {"type": "rich", "title": "Como volver a comprobar la disponibilidad", "paragraphs": [
                "Empieza por la web oficial de Mistfall Hunter o por la pagina de PlayStation Store. Anota la fecha y la region, porque precio, paquetes y descuentos pueden cambiar. Despues separa disponibilidad de rendimiento: para FPS o estabilidad necesitas notas de parche y pruebas actuales de la plataforma.",
                "Por ultimo, revisa juego cruzado, guardado cruzado, chat y emparejamiento si vas a jugar con amigos. Si la documentacion oficial no confirma una funcion, dejala como no confirmada en vez de convertir una suposicion en un hecho."
            ]},
            {"type": "faq", "title": "Preguntas frecuentes sobre Mistfall Hunter en PS5", "items": [
                ["¿Mistfall Hunter esta en PS5?", "Si. La pagina oficial de PlayStation consultada el 19 de agosto de 2026 muestra el producto para PS5. Comprueba siempre la pagina regional antes de comprar."],
                ["¿Cual es la fecha de lanzamiento de Mistfall Hunter en PS5?", "La ficha oficial consultada muestra el 30 de julio de 2026. La disponibilidad y el precio de tu region deben revisarse en directo."],
                ["¿Cuanto cuesta Mistfall Hunter PS5?", "La pagina estadounidense mostraba 24,99 USD en la fecha de comprobacion. No es un precio universal: cambia por region, impuestos y descuentos."],
                ["¿Es mejor PS5 o PC?", "Depende de tu plataforma, amigos, mando y tolerancia a revisar requisitos. No hay una conclusion universal ni un benchmark oficial comun en las fuentes consultadas."],
                ["¿Tiene crossplay entre PS5 y PC?", "Las paginas oficiales revisadas no aportaron evidencia suficiente para confirmarlo. Comprueba la documentacion actual del desarrollador."],
                ["¿Los requisitos de Steam sirven para PS5?", "No. Son requisitos de Windows para PC y no describen el hardware ni el rendimiento de la version de PS5."],
                ["¿Tambien esta en Xbox?", "La pagina oficial de Xbox consultada lista Mistfall Hunter y muestra el 30 de julio de 2026. Revisa la tienda de tu region."],
            ]},
            {"type": "links", "title": "Fuentes oficiales de plataforma", "items": [
                ["Mistfall Hunter en PlayStation Store", "https://store.playstation.com/en-us/concept/10017212", "Producto PS5, datos de lanzamiento y precio regional.", "noopener"],
                ["Mistfall Hunter en Xbox Store", "https://www.xbox.com/games/store/mistfall-hunter/9p8x6tvw9zw8", "Referencia oficial de Xbox.", "noopener"],
                ["Mistfall Hunter en Steam", "https://store.steampowered.com/app/3282300/Mistfall_Hunter/", "Datos de PC, requisitos y reseñas.", "noopener"],
                ["Web oficial de Mistfall Hunter", "https://mistfallhunter.com/", "Enlaces de plataforma y anuncios.", "noopener"],
            ]},
        ],
    },
    "ja": {
        "page": {
            "title": "Mistfall Hunter PS5：発売日・価格・遊び方",
            "description": "Mistfall Hunter PS5の発売日と価格を確認し、SteamやXboxとの違い、購入前の確認点を整理します。",
            "h1": "Mistfall Hunter PS5：発売日・価格・遊び方",
            "kicker": "Mistfall Hunter PS5 | 2026年8月19日確認",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-ps5-console-concept.webp", "alt": "Mistfall HunterのPS5環境とPC環境を比較する編集用コンセプトイラスト", "caption": "この記事のために作成した編集用コンセプトイラストです。公式のPlayStation画面やゲームプレイ画像ではありません。"},
            {"type": "rich", "title": "結論：Mistfall HunterはPS5向けに掲載されています", "paragraphs": [
                "はい。2026年8月19日に確認したPlayStation Store公式ページでは、Mistfall HunterがPS5向けのフルゲームとして掲載されています。商品データには2026年7月30日の発売日が表示され、米国ページでは確認時点で24.99米ドルでした。価格、税、エディション、販売状況は地域で変わるため、日本のページでは必ず現地表示を確認してください。",
                "公式サイトにはPlayStation、Xbox、Steamへのリンクがあります。発売前の記事だけを見てPC専用だと判断せず、購入前に公式ストアでPS5表記、エディション、地域価格を確認するのが安全です。",
                "PS5の掲載は対応プラットフォームの根拠になりますが、FPS、クロスプレイ、クロスセーブ、PCと同じ性能まで自動的に保証するものではありません。公式のパッチノートや現在の検証がない項目は、推測で埋めないようにします。"
            ]},
            {"type": "table", "title": "Mistfall Hunterの対応プラットフォーム", "headers": ["プラットフォーム", "確認できた公式情報", "購入前に見る点"], "rows": [
                ["PS5", "PlayStation公式商品ページ、発売日は2026年7月30日表示", "日本地域の価格、エディション、現在の販売表示"],
                ["Xbox", "Xbox公式ストア、発売日は2026年7月30日表示", "地域、購入条件、エディション"],
                ["PC / Steam", "Steam公式ページ、発売日は2026年7月29日表示", "Windows要件、45 GB、レビュー、PC性能"],
                ["クロスプレイ / クロスセーブ", "確認したページでは確定情報なし", "公式の案内がない限り前提にしない"],
            ]},
            {"type": "rich", "title": "PS5の公式ページで確認できること", "paragraphs": [
                "コンソール対応を調べるときは、公式ストアの商品ページが最も直接的です。PlayStationページにはゲーム名、PS5プラットフォーム、商品価格、発売日の情報があります。掲示板の投稿や古い動画より、現在の地域ページを優先してください。",
                "ストアの価格、割引、セット内容、年齢表示、地域ごとの販売状況は変わることがあります。購入時には、PS5の表示とフルゲームの商品名を確認し、追加コンテンツやアップグレード商品と取り違えないようにします。",
                "Xboxの公式ページも別のコンソール情報として確認できますが、全プラットフォームの機能が同じだとは限りません。友達の環境、コントローラー、アカウント、地域の条件を合わせて判断してください。"
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "雪原で戦うMistfall Hunterの公式Steamアート", "caption": "ゲームの識別に使った公式Steamストアアートです。PS5の性能検証画面ではありません。"},
            {"type": "rich", "title": "PS5・Steam・Xboxの選び方", "paragraphs": [
                "リビングで遊びたい、Windowsのパーツを比較したくない、友達がPlayStationにいるという場合はPS5が自然です。PCの必要環境、画質設定、レビューを自分で確認したい場合はSteamが向いています。Xboxのフレンドやアカウントを中心に遊ぶなら公式Xboxページを基準にしてください。",
                "Steamのシステム要件はWindows版の情報です。OS、CPU、メモリ、GPU、DirectX、ネットワーク、45 GBの容量はPC購入者には役立ちますが、PS5の要件やFPSを意味しません。",
                "価格やプレイヤー状況を調べるときは、正しいストアを開いたあとで、このサイトの価格ガイド、プレイヤー数ガイド、レビューも参照してください。レビューは公式スコアではなく、購入判断のための編集意見です。"
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "商品確認用のMistfall Hunter公式Steamヘッダーアート", "caption": "商品名を確認するための公式ストアヘッダーです。コンソール画面として扱っていません。"},
            {"type": "rich", "title": "アップデート後にPS5対応を確認する手順", "paragraphs": [
                "まずMistfall Hunter公式サイトまたはPlayStation Storeの商品ページを開きます。次に確認日と地域を記録します。発売日は過去の事実として残りますが、価格、割引、セット、アカウント条件は変化するからです。",
                "最後に対応状況と性能を分けて確認してください。FPSや安定性は現在のパッチノートと再現可能な検証が必要です。クロスプレイ、クロスセーブ、ボイスチャット、地域マッチングも、公式の記載がなければ未確認として扱います。"
            ]},
            {"type": "faq", "title": "Mistfall Hunter PS5 よくある質問", "items": [
                ["Mistfall HunterはPS5で遊べますか？", "はい。2026年8月19日に確認したPlayStation Store公式ページでは、PS5向けのフルゲームとして掲載されていました。購入前に日本地域のページを確認してください。"],
                ["Mistfall Hunter PS5の発売日はいつですか？", "確認した公式商品データでは2026年7月30日です。地域の販売状態や価格は現在のストアで確認します。"],
                ["PS5版の価格はいくらですか？", "確認時点の米国ページでは24.99米ドルでした。日本の価格、税、セール、エディションは別表示になる可能性があります。"],
                ["PS5とPCはどちらが良いですか？", "友達の環境、コントローラー、PCの必要環境を確認したいかで変わります。全員に当てはまる性能比較は確認できていません。"],
                ["PS5とPCのクロスプレイに対応していますか？", "確認した公式ページだけでは確定できません。開発元の最新案内を確認してください。"],
                ["Steamの必要環境はPS5にも適用されますか？", "いいえ。Steamの表はWindows PC向けです。PS5のハードウェアや性能を説明するものではありません。"],
                ["Xbox版もありますか？", "確認した公式XboxページにはMistfall Hunterが掲載され、発売日は2026年7月30日表示でした。地域ページを確認してください。"],
            ]},
            {"type": "links", "title": "公式プラットフォーム情報", "items": [
                ["PlayStation StoreのMistfall Hunter", "https://store.playstation.com/en-us/concept/10017212", "PS5の商品、発売日、地域価格を確認します。", "noopener"],
                ["Xbox StoreのMistfall Hunter", "https://www.xbox.com/games/store/mistfall-hunter/9p8x6tvw9zw8", "Xboxの公式商品情報です。", "noopener"],
                ["SteamのMistfall Hunter", "https://store.steampowered.com/app/3282300/Mistfall_Hunter/", "Windows版の必要環境、レビュー、商品情報です。", "noopener"],
                ["Mistfall Hunter公式サイト", "https://mistfallhunter.com/", "プラットフォームリンクと告知を確認します。", "noopener"],
            ]},
        ],
    },
    "fr": {
        "page": {
            "title": "Mistfall Hunter sur PS5 : date, prix et disponibilité",
            "description": "Dossier Mistfall Hunter sur PS5 : vérifiez la date officielle, le prix de référence et les différences avec Steam et Xbox.",
            "h1": "Mistfall Hunter sur PS5 : date, prix et disponibilité",
            "kicker": "Mistfall Hunter sur PS5 | Vérifié le 19 août 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-ps5-console-concept.webp", "alt": "Illustration conceptuelle comparant une installation PS5 et un PC pour Mistfall Hunter", "caption": "Illustration conceptuelle éditoriale. Ce n’est ni une page PlayStation officielle ni une capture de jeu."},
            {"type": "rich", "title": "Réponse courte : Mistfall Hunter est listé sur PS5", "paragraphs": [
                "Oui. La page officielle du PlayStation Store consultée le 19 août 2026 présente Mistfall Hunter comme un jeu complet pour PS5. Les données du produit indiquent une sortie le 30 juillet 2026 et la page américaine affichait 24,99 $ au moment de la vérification. Le prix, les taxes, les éditions et la disponibilité dépendent de votre région.",
                "Le site officiel de Mistfall Hunter renvoie également vers PlayStation, Xbox et Steam. Il vaut donc mieux ouvrir la fiche officielle de votre pays, vérifier la mention PS5 et lire le contenu de l’édition avant de payer, plutôt que de suivre une ancienne information de lancement.",
                "La fiche PS5 confirme la plateforme, mais ne suffit pas à confirmer un nombre d’images par seconde, le cross-play, la sauvegarde partagée ou une performance identique à celle d’un PC. Quand les sources vérifiées ne répondent pas à une question, cette page la laisse non confirmée."
            ]},
            {"type": "table", "title": "Les plateformes de Mistfall Hunter en un coup d’œil", "headers": ["Plateforme", "Statut officiel vérifié", "À vérifier avant l’achat"], "rows": [
                ["PS5", "Fiche PlayStation officielle; sortie affichée le 30 juillet 2026", "Prix régional, édition et disponibilité actuelle."],
                ["Xbox", "Fiche Xbox officielle; sortie affichée le 30 juillet 2026", "Région, conditions d’achat et édition."],
                ["PC / Steam", "Fiche Steam officielle; sortie affichée le 29 juillet 2026", "Windows, configuration, 45 Go, avis et performances."],
                ["Jeu croisé / sauvegarde partagée", "Non confirmé par les pages consultées", "Ne pas supposer une fonction sans annonce actuelle."],
            ]},
            {"type": "rich", "title": "Ce que vérifie la page PlayStation officielle", "paragraphs": [
                "Pour répondre à une question de disponibilité console, une fiche de boutique officielle est la source la plus directe. La page PlayStation identifie le jeu, la plateforme PS5, le type de produit, la date et le prix de la région consultée. Elle est plus solide qu’un commentaire ou qu’une vidéo ancienne.",
                "Les prix, promotions, bundles et règles régionales peuvent évoluer. Vérifiez le pays, le nom exact du produit et la mention PS5 au moment de l’achat. Ne confondez pas un jeu complet avec un contenu additionnel ou une mise à niveau.",
                "La fiche Xbox donne un second point de contrôle pour les consoles, mais ne prouve pas que toutes les versions partagent les mêmes fonctions. Tenez compte de vos amis, de votre compte, de votre manette et de votre région."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Illustration Steam officielle de Mistfall Hunter dans une bataille enneigée", "caption": "Illustration officielle Steam utilisée pour identifier le jeu; ce n’est pas une capture de performance PS5."},
            {"type": "rich", "title": "PS5, Steam ou Xbox : quelle version choisir ?", "paragraphs": [
                "La PS5 convient si vous jouez dans le salon et ne voulez pas comparer des composants Windows. Steam convient si vous voulez contrôler la configuration, les options graphiques et les avis récents. Xbox est logique si votre groupe et votre compte sont déjà dans cet écosystème.",
                "Les exigences Steam décrivent uniquement la version PC Windows : processeur, mémoire, carte graphique, DirectX, réseau et 45 Go de stockage. Elles ne sont pas des exigences PS5 et ne permettent pas de promettre un FPS console.",
                "Après avoir ouvert la bonne boutique, utilisez aussi les guides de prix, de joueurs et la revue du site. La revue est une opinion indépendante, pas une note officielle."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Bannière Steam officielle de Mistfall Hunter utilisée comme référence produit", "caption": "Bannière officielle utilisée comme référence d’identité; elle ne représente pas une capture console."},
            {"type": "rich", "title": "Vérifier la disponibilité après une mise à jour", "paragraphs": [
                "Commencez par le site officiel de Mistfall Hunter ou par la fiche PlayStation Store. Notez la date et la région, car prix, offres et disponibilité peuvent changer. Ensuite, séparez disponibilité et performance : les performances demandent des notes de mise à jour et des tests actuels.",
                "Enfin, vérifiez séparément le cross-play, la sauvegarde partagée, le chat vocal et le matchmaking régional. Une fonction non documentée officiellement doit rester non confirmée."
            ]},
            {"type": "faq", "title": "Questions fréquentes sur Mistfall Hunter sur PS5", "items": [
                ["Mistfall Hunter est-il disponible sur PS5 ?", "Oui. La page PlayStation officielle consultée le 19 août 2026 listait le jeu complet pour PS5. Vérifiez la fiche de votre région avant l’achat."],
                ["Quelle est la date de sortie de Mistfall Hunter sur PS5 ?", "Les données officielles consultées indiquaient le 30 juillet 2026. La disponibilité régionale doit être vérifiée en direct."],
                ["Quel est le prix de Mistfall Hunter sur PS5 ?", "La page américaine affichait 24,99 $ lors de la vérification. Le prix local peut différer selon la devise, les taxes et les promotions."],
                ["Mistfall Hunter est-il meilleur sur PS5 ou PC ?", "Cela dépend de votre matériel, de vos amis, de votre manette et de votre envie de régler le PC. Les sources consultées ne donnent pas de benchmark universel."],
                ["Le cross-play PS5-PC est-il confirmé ?", "Les pages officielles vérifiées ne suffisent pas à le confirmer. Consultez la documentation actuelle du développeur."],
                ["Les exigences Steam s’appliquent-elles à la PS5 ?", "Non. Elles concernent Windows PC et ne décrivent pas le matériel ou les performances PS5."],
                ["Existe-t-il une version Xbox ?", "La fiche Xbox officielle consultée listait Mistfall Hunter avec une sortie affichée au 30 juillet 2026. Vérifiez votre région."],
            ]},
            {"type": "links", "title": "Sources officielles des plateformes", "items": [
                ["Mistfall Hunter sur PlayStation Store", "https://store.playstation.com/en-us/concept/10017212", "Produit PS5, date et prix de la région consultée.", "noopener"],
                ["Mistfall Hunter sur Xbox Store", "https://www.xbox.com/games/store/mistfall-hunter/9p8x6tvw9zw8", "Référence officielle Xbox.", "noopener"],
                ["Mistfall Hunter sur Steam", "https://store.steampowered.com/app/3282300/Mistfall_Hunter/", "Faits PC, configuration et avis.", "noopener"],
                ["Site officiel de Mistfall Hunter", "https://mistfallhunter.com/", "Liens de plateformes et annonces.", "noopener"],
            ]},
        ],
    },
    "de": {
        "page": {
            "title": "Mistfall Hunter auf PS5: Release, Preis und Verfügbarkeit",
            "description": "Prüfe, ob Mistfall Hunter auf PS5 verfügbar ist, welches offizielle Release-Datum gilt und wie PS5, Steam und Xbox einzuordnen sind.",
            "h1": "Mistfall Hunter auf PS5: Release, Preis und Verfügbarkeit",
            "kicker": "Mistfall Hunter auf PS5 | Geprüft am 19.08.2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-ps5-console-concept.webp", "alt": "Redaktionelle Konzeptgrafik mit PS5- und PC-Setup für Mistfall Hunter", "caption": "Redaktionelle Konzeptgrafik für diesen Leitfaden. Kein offizieller PlayStation-Bildschirm und kein echtes Gameplay-Screenshot."},
            {"type": "rich", "title": "Kurzantwort: Mistfall Hunter ist für PS5 gelistet", "paragraphs": [
                "Ja. Die offizielle PlayStation-Store-Seite, die am 19.08.2026 geprüft wurde, listet Mistfall Hunter als vollständiges PS5-Spiel. Die Produktdaten zeigen den 30.07.2026 als Release-Datum; auf der US-Seite standen zum Prüfzeitpunkt 24,99 US-Dollar. Preis, Steuern, Edition und Verfügbarkeit können je nach Region abweichen.",
                "Auch die offizielle Mistfall-Hunter-Website verlinkt PlayStation, Xbox und Steam. Deshalb solltest du die aktuelle Store-Seite deiner Region öffnen, die PS5-Plattform prüfen und den genauen Editionstext lesen, statt dich auf alte Launch-Artikel zu verlassen.",
                "Die PS5-Produktseite bestätigt die Plattform, aber nicht automatisch FPS, Crossplay, gemeinsame Spielstände oder identische PC-Leistung. Wo die geprüften Quellen keine Antwort liefern, bleibt die Aussage auf dieser Seite unbestätigt."
            ]},
            {"type": "table", "title": "Mistfall Hunter Plattformen im Überblick", "headers": ["Plattform", "Offiziell geprüft", "Vor dem Kauf prüfen"], "rows": [
                ["PS5", "Offizielle PlayStation-Seite; Release 30.07.2026 angezeigt", "Regionaler Preis, Edition und aktuelle Verfügbarkeit."],
                ["Xbox", "Offizielle Xbox-Seite; Release 30.07.2026 angezeigt", "Region, Kaufbedingungen und Edition."],
                ["PC / Steam", "Offizielle Steam-Seite; Release 29.07.2026 angezeigt", "Windows-Anforderungen, 45 GB, Reviews und PC-Leistung."],
                ["Crossplay / gemeinsame Spielstände", "Auf den geprüften Seiten nicht bestätigt", "Keine Funktion ohne aktuelle offizielle Info voraussetzen."],
            ]},
            {"type": "rich", "title": "Was die offizielle PS5-Seite aussagt", "paragraphs": [
                "Für eine Konsolenfrage ist eine offizielle Store-Seite die direkteste Quelle. Die PlayStation-Seite nennt Mistfall Hunter, die PS5-Plattform, den Produkttyp, ein Release-Datum und den Preis der geprüften Region. Das ist belastbarer als ein altes Video oder ein Forumspost.",
                "Preise, Rabatte, Bundles und regionale Verfügbarkeit können sich ändern. Kontrolliere beim Kauf Land, exakten Produktnamen und die PS5-Kennzeichnung. Verwechsle das vollständige Spiel nicht mit einem Zusatzinhalt oder Upgrade.",
                "Die Xbox-Seite ist eine zweite Konsolenquelle, beweist aber keine identischen Funktionen auf allen Plattformen. Berücksichtige Freunde, Konto, Controller und Region gemeinsam."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Offizielles Steam-Artwork von Mistfall Hunter in einer verschneiten Schlacht", "caption": "Offizielles Steam-Store-Artwork zur Spielidentifikation; kein PS5-Leistungstest."},
            {"type": "rich", "title": "PS5, Steam oder Xbox: Welche Version passt?", "paragraphs": [
                "PS5 passt, wenn du im Wohnzimmer spielst und keine Windows-Komponenten vergleichen willst. Steam passt, wenn du Anforderungen, Grafikeinstellungen und aktuelle Reviews selbst prüfen möchtest. Xbox ist naheliegend, wenn deine Gruppe und dein Konto bereits dort sind.",
                "Die Steam-Systemanforderungen beschreiben Windows-PC: Prozessor, Arbeitsspeicher, Grafikkarte, DirectX, Netzwerk und 45 GB Speicher. Sie sind keine PS5-Anforderungen und keine Grundlage für ein Konsolen-FPS-Versprechen.",
                "Nach dem Öffnen der passenden Store-Seite helfen auch die Preis-, Spielerzahl- und Review-Ressourcen der Website. Die Review ist eine unabhängige Einschätzung und kein offizieller Score.",
                "Wenn du bereits eine PlayStation besitzt, ist der wichtigste Vergleich nicht ein allgemeiner Konsolenkrieg, sondern dein konkreter Kaufweg. Prüfe, ob dein Konto die richtige Region verwendet, ob die gewünschte Edition als PS5-Version gekennzeichnet ist und ob ein Rabatt den Preis zum Zeitpunkt des Kaufs verändert. Ein alter Preis auf einer Seite ist nur eine Momentaufnahme.",
                "Für eine Gruppe solltest du außerdem klären, wo deine Mitspieler spielen und welche Funktionen sie tatsächlich benötigen. Ein gemeinsamer Plattformkauf kann die Organisation vereinfachen, während ein PC mehr Einstellungen ermöglicht. Beides beantwortet aber nicht automatisch die Frage nach Crossplay oder gemeinsamen Spielständen. Diese Funktionen brauchen eine eigene offizielle Bestätigung.",
                "Ein letzter Kaufcheck betrifft die Rückgabe und die Erwartungen an die Plattform. Lies die Bedingungen des jeweiligen Stores und entscheide erst danach, ob der aktuelle Preis zu deinem Spielstil passt. So bleibt die PS5-Entscheidung an überprüfbaren Fakten und nicht an einer alten Werbeaussage hängen."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Offizielles Mistfall-Hunter-Steam-Headerbild als Produktreferenz", "caption": "Offizielles Store-Headerbild als Identitätsreferenz; keine Konsolenaufnahme."},
            {"type": "rich", "title": "PS5-Verfügbarkeit nach einem Update prüfen", "paragraphs": [
                "Starte mit der offiziellen Mistfall-Hunter-Website oder der PlayStation-Store-Seite. Notiere Datum und Region, weil Preise, Angebote und Account-Bedingungen wechseln können. Trenne danach Verfügbarkeit und Leistung: Für Leistung brauchst du aktuelle Patch-Infos und reproduzierbare Tests.",
                "Prüfe außerdem Crossplay, gemeinsame Spielstände, Sprachchat und regionales Matchmaking separat. Was die offizielle Dokumentation nicht bestätigt, sollte als unbestätigt gelten."
            ]},
            {"type": "faq", "title": "Häufige Fragen zu Mistfall Hunter PS5", "items": [
                ["Ist Mistfall Hunter auf PS5 verfügbar?", "Ja. Die am 19.08.2026 geprüfte offizielle PlayStation-Seite listete das vollständige Spiel für PS5. Vor dem Kauf die regionale Seite öffnen."],
                ["Wann war der Mistfall Hunter PS5 Release?", "Die geprüften offiziellen Produktdaten zeigten den 30.07.2026. Die aktuelle regionale Verfügbarkeit prüfst du direkt im Store."],
                ["Was kostet Mistfall Hunter auf PS5?", "Die US-Seite zeigte zum Prüfzeitpunkt 24,99 US-Dollar. Lokale Währung, Steuern, Rabatte und Bundles können abweichen."],
                ["Ist PS5 oder PC besser?", "Das hängt von Hardware, Freunden, Controller und deiner Bereitschaft zur PC-Konfiguration ab. Die Quellen liefern keinen universellen Benchmark."],
                ["Ist Crossplay zwischen PS5 und PC bestätigt?", "Die geprüften offiziellen Seiten reichen dafür nicht aus. Prüfe aktuelle Entwickler-Dokumentation."],
                ["Gelten Steam-Anforderungen auch für PS5?", "Nein. Sie beziehen sich auf Windows-PC und beschreiben weder PS5-Hardware noch Konsolenleistung."],
                ["Gibt es Mistfall Hunter auch auf Xbox?", "Die geprüfte offizielle Xbox-Seite listete das Spiel mit dem 30.07.2026 als angezeigtem Release. Region prüfen."],
            ]},
            {"type": "links", "title": "Offizielle Plattformquellen", "items": [
                ["Mistfall Hunter im PlayStation Store", "https://store.playstation.com/en-us/concept/10017212", "PS5-Produkt, Release und regionaler Preis.", "noopener"],
                ["Mistfall Hunter im Xbox Store", "https://www.xbox.com/games/store/mistfall-hunter/9p8x6tvw9zw8", "Offizielle Xbox-Referenz.", "noopener"],
                ["Mistfall Hunter auf Steam", "https://store.steampowered.com/app/3282300/Mistfall_Hunter/", "PC-Fakten, Anforderungen und Reviews.", "noopener"],
                ["Offizielle Mistfall-Hunter-Website", "https://mistfallhunter.com/", "Plattformlinks und aktuelle Hinweise.", "noopener"],
            ]},
        ],
    },
    "pt": {
        "page": {
            "title": "Mistfall Hunter no PS5: data, preço e disponibilidade",
            "description": "Guia Mistfall Hunter no PS5: veja a data oficial, o preço de referência e as diferenças entre PS5, Steam e Xbox.",
            "h1": "Mistfall Hunter no PS5: data, preço e como jogar",
            "kicker": "Mistfall Hunter no PS5 | Verificado em 19 de agosto de 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-ps5-console-concept.webp", "alt": "Ilustração conceitual comparando uma configuração de PS5 e PC para Mistfall Hunter", "caption": "Ilustração conceitual editorial. Não é uma página oficial da PlayStation nem uma captura real de gameplay."},
            {"type": "rich", "title": "Resposta rápida: Mistfall Hunter está listado para PS5", "paragraphs": [
                "Sim. A página oficial da PlayStation Store consultada em 19 de agosto de 2026 apresenta Mistfall Hunter como um jogo completo para PS5. Os dados do produto mostram 30 de julho de 2026 como data de lançamento; na página dos Estados Unidos, o preço exibido na verificação era US$ 24,99. Preço, impostos, edição e disponibilidade variam por região.",
                "O site oficial de Mistfall Hunter também aponta para PlayStation, Xbox e Steam. Por isso, abra a loja oficial do seu país, confirme a indicação PS5 e confira a edição antes de comprar, em vez de confiar em uma notícia antiga de lançamento.",
                "A página do PS5 confirma a plataforma, mas não confirma sozinha FPS, crossplay, progresso compartilhado ou desempenho igual ao de um PC. Quando as fontes verificadas não explicam uma função, este guia mantém a informação como não confirmada."
            ]},
            {"type": "table", "title": "Plataformas de Mistfall Hunter", "headers": ["Plataforma", "Situação oficial verificada", "O que conferir antes da compra"], "rows": [
                ["PS5", "Página oficial da PlayStation; lançamento exibido em 30/07/2026", "Preço regional, edição e disponibilidade atual."],
                ["Xbox", "Página oficial do Xbox; lançamento exibido em 30/07/2026", "Região, condições de compra e edição."],
                ["PC / Steam", "Página oficial da Steam; lançamento exibido em 29/07/2026", "Windows, requisitos, 45 GB, avaliações e desempenho."],
                ["Crossplay / progresso compartilhado", "Não confirmado nas páginas consultadas", "Não presuma a função sem documentação atual."],
            ]},
            {"type": "rich", "title": "O que a página oficial do PS5 confirma", "paragraphs": [
                "Para saber se um jogo está disponível em um console, a loja oficial é a fonte mais direta. A página da PlayStation identifica Mistfall Hunter, mostra PS5, informa o tipo de produto e apresenta dados de preço e lançamento da região consultada.",
                "Preços, descontos, pacotes e disponibilidade podem mudar. Confira país, nome completo do produto e o rótulo PS5 na hora da compra. Não confunda o jogo completo com uma expansão ou upgrade.",
                "A página do Xbox é uma segunda referência de console, mas não prova que as funções sejam iguais em todas as plataformas. Compare amigos, conta, controle e região antes de decidir."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Arte oficial da Steam mostrando Mistfall Hunter em uma batalha na neve", "caption": "Arte oficial da loja Steam para identificar o jogo; não é uma captura de desempenho no PS5."},
            {"type": "rich", "title": "PS5, Steam ou Xbox: qual versão escolher?", "paragraphs": [
                "O PS5 faz sentido para quem quer jogar na sala e não quer comparar componentes do Windows. A Steam é melhor para quem precisa conferir requisitos, configurações gráficas e avaliações recentes. O Xbox é natural quando seu grupo e sua conta já estão nesse ecossistema.",
                "Os requisitos da Steam descrevem o PC Windows: processador, memória, placa de vídeo, DirectX, rede e 45 GB. Eles não são requisitos de PS5 e não permitem prometer FPS no console.",
                "Depois de abrir a loja correta, use também os guias de preço, jogadores e análise do site. A análise é uma opinião independente, não uma nota oficial."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Cabeçalho oficial da Steam de Mistfall Hunter usado como referência do produto", "caption": "Cabeçalho oficial da loja como referência de identidade; não é uma captura de console."},
            {"type": "rich", "title": "Como verificar a disponibilidade depois de uma atualização", "paragraphs": [
                "Comece pelo site oficial de Mistfall Hunter ou pela página do produto na PlayStation Store. Anote a data e a região, porque preço, promoções e condições de conta mudam. Depois, separe disponibilidade de desempenho: desempenho exige notas de atualização e testes atuais.",
                "Confira também crossplay, progresso compartilhado, chat e matchmaking regional. Se a documentação oficial não confirmar uma função, trate-a como não confirmada."
            ]},
            {"type": "faq", "title": "Perguntas frequentes sobre Mistfall Hunter no PS5", "items": [
                ["Mistfall Hunter está no PS5?", "Sim. A página oficial da PlayStation consultada em 19 de agosto de 2026 listava o jogo completo para PS5. Confira a página da sua região antes de comprar."],
                ["Qual é a data de lançamento de Mistfall Hunter no PS5?", "Os dados oficiais consultados mostravam 30 de julho de 2026. A disponibilidade e o preço regionais devem ser conferidos ao vivo."],
                ["Quanto custa Mistfall Hunter no PS5?", "A página dos Estados Unidos mostrava US$ 24,99 na data da consulta. Moeda, impostos, descontos e pacotes podem alterar o valor local."],
                ["É melhor jogar no PS5 ou no PC?", "Depende do seu hardware, grupo, controle e vontade de ajustar o PC. As fontes consultadas não fornecem um benchmark universal."],
                ["Existe crossplay entre PS5 e PC?", "As páginas oficiais verificadas não foram suficientes para confirmar. Consulte a documentação atual do desenvolvedor."],
                ["Os requisitos da Steam valem para o PS5?", "Não. Eles descrevem o PC Windows e não o hardware ou desempenho do PS5."],
                ["Mistfall Hunter também está no Xbox?", "A página oficial do Xbox consultada listava Mistfall Hunter e mostrava 30 de julho de 2026 como lançamento. Confira sua região."],
            ]},
            {"type": "links", "title": "Fontes oficiais de plataforma", "items": [
                ["Mistfall Hunter na PlayStation Store", "https://store.playstation.com/en-us/concept/10017212", "Produto PS5, data e preço da região consultada.", "noopener"],
                ["Mistfall Hunter no Xbox Store", "https://www.xbox.com/games/store/mistfall-hunter/9p8x6tvw9zw8", "Referência oficial do Xbox.", "noopener"],
                ["Mistfall Hunter na Steam", "https://store.steampowered.com/app/3282300/Mistfall_Hunter/", "Dados de PC, requisitos e avaliações.", "noopener"],
                ["Site oficial de Mistfall Hunter", "https://mistfallhunter.com/", "Links de plataforma e anúncios.", "noopener"],
            ]},
        ],
    },
    "ko": {
        "page": {
            "title": "Mistfall Hunter PS5: 출시일, 가격, 플레이 방법",
            "description": "Mistfall Hunter PS5의 공식 출시일과 가격, Steam·Xbox와의 차이, 구매 전 확인 사항을 알아보세요.",
            "h1": "Mistfall Hunter PS5: 출시일, 가격, 플레이 방법",
            "kicker": "Mistfall Hunter PS5 | 2026년 8월 19일 확인",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-ps5-console-concept.webp", "alt": "Mistfall Hunter의 PS5와 PC 환경을 비교하는 편집용 콘셉트 일러스트", "caption": "이 가이드를 위해 만든 편집용 콘셉트 일러스트입니다. 공식 PlayStation 화면이나 실제 게임플레이 캡처가 아닙니다."},
            {"type": "rich", "title": "빠른 답변: Mistfall Hunter는 PS5용으로 등록되어 있습니다", "paragraphs": [
                "네. 2026년 8월 19일 확인한 PlayStation Store 공식 페이지에는 Mistfall Hunter가 PS5 풀게임으로 등록되어 있습니다. 상품 데이터에는 2026년 7월 30일 출시일이 표시되었고, 미국 페이지 확인 시 가격은 24.99달러였습니다. 가격, 세금, 에디션과 판매 여부는 지역에 따라 달라질 수 있습니다.",
                "Mistfall Hunter 공식 사이트도 PlayStation, Xbox, Steam 링크를 함께 제공합니다. 구매 전에는 오래된 출시 전 글보다 본인 지역의 공식 스토어를 열어 PS5 표시와 에디션을 확인하는 것이 좋습니다.",
                "PS5 상품 페이지는 플랫폼을 확인해 주지만 FPS, 크로스플레이, 크로스세이브, PC와 동일한 성능까지 자동으로 보장하지는 않습니다. 확인한 공식 자료에 없는 내용은 추측하지 않고 미확인으로 둡니다."
            ]},
            {"type": "table", "title": "Mistfall Hunter 플랫폼 한눈에 보기", "headers": ["플랫폼", "확인된 공식 상태", "구매 전 확인할 내용"], "rows": [
                ["PS5", "PlayStation 공식 상품 페이지, 2026년 7월 30일 출시 표시", "지역 가격, 에디션, 현재 판매 상태"],
                ["Xbox", "Xbox 공식 스토어, 2026년 7월 30일 출시 표시", "지역, 구매 조건, 에디션"],
                ["PC / Steam", "Steam 공식 페이지, 2026년 7월 29일 출시 표시", "Windows 요구 사항, 45 GB, 리뷰와 PC 성능"],
                ["크로스플레이 / 크로스세이브", "확인한 페이지에서 확정되지 않음", "최신 공식 문서 없이는 가정하지 않기"],
            ]},
            {"type": "rich", "title": "PS5 공식 페이지에서 확인할 수 있는 것", "paragraphs": [
                "콘솔 지원 여부는 공식 스토어 상품 페이지가 가장 직접적인 근거입니다. PlayStation 페이지에는 게임명, PS5 플랫폼, 상품 유형, 출시일과 확인 지역의 가격 정보가 있습니다. 오래된 영상이나 포럼 댓글보다 현재 지역 페이지를 우선하세요.",
                "가격, 할인, 번들, 지역 판매 여부는 바뀔 수 있습니다. 구매 시 국가, 정확한 상품명과 PS5 표시를 확인하고 풀게임과 추가 콘텐츠를 구분하세요.",
                "Xbox 페이지도 콘솔 정보를 확인하는 공식 출처지만 모든 플랫폼의 기능이 같다는 뜻은 아닙니다. 친구, 계정, 컨트롤러와 지역을 함께 비교하세요."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "눈 덮인 전투를 보여주는 Mistfall Hunter 공식 Steam 아트", "caption": "게임 식별을 위한 공식 Steam 스토어 아트이며 PS5 성능 캡처가 아닙니다."},
            {"type": "rich", "title": "PS5, Steam, Xbox 중 무엇을 고를까?", "paragraphs": [
                "거실에서 플레이하고 Windows 부품을 비교하고 싶지 않다면 PS5가 편합니다. 요구 사항, 그래픽 설정과 최근 리뷰를 직접 확인하려면 Steam이 유용합니다. 친구와 계정이 Xbox 생태계에 있다면 공식 Xbox 페이지를 기준으로 확인하세요.",
                "Steam 시스템 요구 사항은 Windows PC용입니다. CPU, 메모리, GPU, DirectX, 네트워크와 45 GB 정보는 PC 구매자에게 유용하지만 PS5 요구 사항이나 콘솔 FPS를 뜻하지 않습니다.",
                "올바른 스토어를 연 뒤 사이트의 가격, 플레이어 수, 리뷰 가이드도 참고하세요. 리뷰는 공식 점수가 아니라 독립적인 편집 의견입니다."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "상품 확인용 Mistfall Hunter 공식 Steam 헤더 아트", "caption": "상품 정체성을 확인하기 위한 공식 헤더이며 콘솔 화면으로 제시하지 않습니다."},
            {"type": "rich", "title": "업데이트 후 PS5 지원을 다시 확인하는 방법", "paragraphs": [
                "Mistfall Hunter 공식 사이트나 PlayStation Store 상품 페이지에서 시작하세요. 확인 날짜와 지역을 기록하면 가격, 할인, 번들 변화와 오래된 정보를 구분할 수 있습니다. 그 다음 지원 여부와 성능을 나눠 확인하세요. 성능은 최신 패치 노트와 반복 가능한 테스트가 필요합니다.",
                "크로스플레이, 크로스세이브, 음성 채팅과 지역 매칭도 따로 확인하세요. 공식 문서가 기능을 명시하지 않았다면 미확인으로 두는 편이 정확합니다."
            ]},
            {"type": "faq", "title": "Mistfall Hunter PS5 자주 묻는 질문", "items": [
                ["Mistfall Hunter는 PS5에서 플레이할 수 있나요?", "네. 2026년 8월 19일 확인한 PlayStation 공식 페이지에 PS5 풀게임으로 등록되어 있었습니다. 구매 전 한국 지역 페이지를 확인하세요."],
                ["Mistfall Hunter PS5 출시일은 언제인가요?", "확인한 공식 상품 데이터에는 2026년 7월 30일이 표시되어 있었습니다. 현재 판매 여부와 가격은 스토어에서 확인합니다."],
                ["PS5판 가격은 얼마인가요?", "확인 시점 미국 페이지에는 24.99달러가 표시되었습니다. 지역 통화, 세금, 할인과 번들에 따라 달라질 수 있습니다."],
                ["PS5와 PC 중 어느 쪽이 더 좋은가요?", "하드웨어, 친구, 컨트롤러와 PC 설정 의향에 따라 다릅니다. 확인한 자료만으로 보편적인 벤치마크를 제시할 수는 없습니다."],
                ["PS5와 PC 크로스플레이가 확정됐나요?", "확인한 공식 페이지로는 충분히 확정할 수 없습니다. 최신 개발사 문서를 확인하세요."],
                ["Steam 시스템 요구 사항이 PS5에도 적용되나요?", "아니요. Windows PC용 정보이며 PS5 하드웨어나 성능을 설명하지 않습니다."],
                ["Xbox 버전도 있나요?", "확인한 공식 Xbox 페이지에는 Mistfall Hunter가 등록되어 있고 2026년 7월 30일 출시가 표시되어 있습니다. 지역 스토어를 확인하세요."],
            ]},
            {"type": "links", "title": "공식 플랫폼 출처", "items": [
                ["PlayStation Store의 Mistfall Hunter", "https://store.playstation.com/en-us/concept/10017212", "PS5 상품과 출시일, 지역 가격을 확인합니다.", "noopener"],
                ["Xbox Store의 Mistfall Hunter", "https://www.xbox.com/games/store/mistfall-hunter/9p8x6tvw9zw8", "Xbox 공식 상품 정보입니다.", "noopener"],
                ["Steam의 Mistfall Hunter", "https://store.steampowered.com/app/3282300/Mistfall_Hunter/", "PC 요구 사항과 리뷰, 상품 정보입니다.", "noopener"],
                ["Mistfall Hunter 공식 사이트", "https://mistfallhunter.com/", "플랫폼 링크와 공지를 확인합니다.", "noopener"],
            ]},
        ],
    },
    "it": {
        "page": {
            "title": "Mistfall Hunter su PS5: uscita, prezzo e disponibilità",
            "description": "Guida Mistfall Hunter su PS5: controlla data ufficiale, prezzo di riferimento e differenze tra PS5, Steam e Xbox.",
            "h1": "Mistfall Hunter su PS5: uscita, prezzo e disponibilità",
            "kicker": "Mistfall Hunter su PS5 | Verificato il 19 agosto 2026",
        },
        "sections": [
            {"type": "image", "src": "images/mistfall/mistfall-hunter-ps5-console-concept.webp", "alt": "Illustrazione concettuale che confronta una configurazione PS5 e PC per Mistfall Hunter", "caption": "Illustrazione concettuale editoriale. Non è una pagina PlayStation ufficiale né una schermata di gioco reale."},
            {"type": "rich", "title": "Risposta breve: Mistfall Hunter è disponibile su PS5", "paragraphs": [
                "Sì. La pagina ufficiale del PlayStation Store controllata il 19 agosto 2026 presenta Mistfall Hunter come gioco completo per PS5. I dati del prodotto mostrano il 30 luglio 2026 come data di uscita; nella pagina statunitense il prezzo mostrato al controllo era 24,99 dollari. Prezzo, tasse, edizione e disponibilità cambiano in base alla regione.",
                "Il sito ufficiale di Mistfall Hunter collega anche PlayStation, Xbox e Steam. Prima di acquistare, apri la pagina ufficiale della tua regione, verifica la piattaforma PS5 e controlla il nome dell’edizione invece di affidarti a un vecchio articolo di lancio.",
                "La scheda PS5 conferma la piattaforma, ma non conferma automaticamente FPS, cross-play, salvataggio condiviso o prestazioni uguali a quelle di un PC. Quando le fonti controllate non rispondono, questa guida lascia il punto non confermato."
            ]},
            {"type": "table", "title": "Piattaforme di Mistfall Hunter", "headers": ["Piattaforma", "Stato ufficiale verificato", "Cosa controllare prima dell’acquisto"], "rows": [
                ["PS5", "Pagina PlayStation ufficiale; uscita mostrata il 30 luglio 2026", "Prezzo regionale, edizione e disponibilità."],
                ["Xbox", "Pagina Xbox ufficiale; uscita mostrata il 30 luglio 2026", "Regione, condizioni di acquisto edizione."],
                ["PC / Steam", "Pagina Steam ufficiale; uscita mostrata il 29 luglio 2026", "Windows, requisiti, 45 GB, recensioni e prestazioni."],
                ["Cross-play / salvataggio condiviso", "Non confermati nelle pagine controllate", "Non presumere funzioni senza documentazione attuale."],
            ]},
            {"type": "rich", "title": "Cosa conferma la pagina ufficiale PS5", "paragraphs": [
                "Per una domanda sulla disponibilità console, la pagina dello store ufficiale è la fonte più diretta. La pagina PlayStation identifica il gioco, mostra PS5, indica il prodotto e fornisce data e prezzo della regione controllata. È più affidabile di un commento o di un vecchio video.",
                "Prezzi, sconti, bundle e disponibilità regionali possono cambiare. Controlla il paese, il nome completo del prodotto e l’etichetta PS5 al momento dell’acquisto. Non confondere il gioco completo con un contenuto aggiuntivo o un upgrade.",
                "La pagina Xbox è un secondo riferimento console, ma non dimostra che tutte le piattaforme abbiano le stesse funzioni. Confronta amici, account, controller e regione."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-hero.webp", "alt": "Artwork ufficiale Steam di Mistfall Hunter durante una battaglia innevata", "caption": "Artwork ufficiale Steam usato per identificare il gioco; non è una cattura delle prestazioni PS5."},
            {"type": "rich", "title": "PS5, Steam o Xbox: quale versione scegliere?", "paragraphs": [
                "PS5 è adatta se vuoi giocare in salotto e non vuoi confrontare componenti Windows. Steam è utile se vuoi controllare requisiti, impostazioni grafiche e recensioni recenti. Xbox è naturale quando il tuo gruppo e il tuo account sono già in quell’ecosistema.",
                "I requisiti Steam descrivono il PC Windows: processore, memoria, scheda grafica, DirectX, rete e 45 GB. Non sono requisiti PS5 e non consentono di promettere un FPS console.",
                "Dopo aver aperto lo store corretto, consulta anche le risorse del sito su prezzo, giocatori e recensione. La recensione è un parere indipendente, non un voto ufficiale.",
                "Se possiedi già una PlayStation, il confronto più utile riguarda il tuo account e il tuo acquisto concreto. Controlla regione, edizione PS5, valuta, tasse e sconti attivi. Un prezzo riportato in una guida è una fotografia datata, non una garanzia per il tuo negozio locale.",
                "Se giochi con amici, verifica anche dove giocano e quali funzioni servono davvero al gruppo. Una console può semplificare la configurazione, mentre il PC offre più opzioni; nessuna delle due scelte conferma automaticamente cross-play o salvataggio condiviso. Per questi aspetti serve una dichiarazione ufficiale aggiornata."
            ]},
            {"type": "image", "src": "images/mistfall/mistfall-hunter-steam-header.webp", "alt": "Header ufficiale Steam di Mistfall Hunter usato come riferimento del prodotto", "caption": "Header ufficiale dello store come riferimento d’identità; non rappresenta una schermata console."},
            {"type": "rich", "title": "Come verificare la disponibilità dopo un aggiornamento", "paragraphs": [
                "Parti dal sito ufficiale di Mistfall Hunter o dalla pagina prodotto del PlayStation Store. Annota data e regione, perché prezzi, offerte e condizioni dell’account possono cambiare. Poi separa disponibilità e prestazioni: per le prestazioni servono patch note e test attuali.",
                "Controlla anche cross-play, salvataggio condiviso, chat vocale e matchmaking regionale. Se la documentazione ufficiale non conferma una funzione, considerala non confermata."
            ]},
            {"type": "faq", "title": "Domande frequenti su Mistfall Hunter su PS5", "items": [
                ["Mistfall Hunter è su PS5?", "Sì. La pagina PlayStation ufficiale controllata il 19 agosto 2026 elencava il gioco completo per PS5. Verifica la pagina italiana prima dell’acquisto."],
                ["Qual è la data di uscita di Mistfall Hunter su PS5?", "I dati ufficiali controllati mostravano il 30 luglio 2026. Disponibilità e prezzo regionali vanno verificati nello store."],
                ["Quanto costa Mistfall Hunter su PS5?", "La pagina statunitense mostrava 24,99 dollari al momento del controllo. Valuta, tasse, sconti e bundle possono cambiare il prezzo locale."],
                ["È meglio PS5 o PC?", "Dipende da hardware, amici, controller e voglia di configurare il PC. Le fonti controllate non offrono un benchmark universale."],
                ["Il cross-play PS5-PC è confermato?", "Le pagine ufficiali controllate non bastano a confermarlo. Consulta la documentazione attuale dello sviluppatore."],
                ["I requisiti Steam valgono per PS5?", "No. Riguardano Windows PC e non descrivono hardware o prestazioni PS5."],
                ["Esiste anche la versione Xbox?", "La pagina Xbox ufficiale controllata elencava Mistfall Hunter e mostrava il 30 luglio 2026 come uscita. Verifica la tua regione."],
            ]},
            {"type": "links", "title": "Fonti ufficiali delle piattaforme", "items": [
                ["Mistfall Hunter sul PlayStation Store", "https://store.playstation.com/en-us/concept/10017212", "Prodotto PS5, data e prezzo della regione controllata.", "noopener"],
                ["Mistfall Hunter su Xbox Store", "https://www.xbox.com/games/store/mistfall-hunter/9p8x6tvw9zw8", "Riferimento ufficiale Xbox.", "noopener"],
                ["Mistfall Hunter su Steam", "https://store.steampowered.com/app/3282300/Mistfall_Hunter/", "Dati PC, requisiti e recensioni.", "noopener"],
                ["Sito ufficiale di Mistfall Hunter", "https://mistfallhunter.com/", "Link alle piattaforme e annunci.", "noopener"],
            ]},
        ],
    },
}
