import os
import shutil
import sys

from app import BASE_URL, LAST_UPDATED, PAGE_LASTMOD, PAGE_ORDER, PAGE_SLUGS, app, get_page_path, get_route_matrix, page_not_found
from werkzeug.exceptions import NotFound


def ensure_dir(path):
    """
    确保指定目录存在。

    :param path: 需要创建或确认存在的目录路径
    :return: None，无返回值
    """
    os.makedirs(path, exist_ok=True)


def page_path_for_url(url):
    """
    将站点 URL 路径转换为静态 HTML 输出路径。

    :param url: 站点页面路径
    :return: str，构建目录中的相对 HTML 文件路径
    """
    if url == "/":
        return "index.html"
    clean_url = url.lstrip("/")
    if clean_url.endswith("/"):
        return os.path.join(clean_url, "index.html")
    if clean_url.endswith(".html"):
        return clean_url
    return os.path.join(clean_url, "index.html")


def save_page(url, content, build_dir):
    """
    保存静态页面内容到构建目录。

    :param url: 站点页面路径
    :param content: 页面 HTML 内容
    :param build_dir: 构建输出目录
    :return: None，无返回值
    """
    file_path = os.path.join(build_dir, page_path_for_url(url))
    ensure_dir(os.path.dirname(file_path) or build_dir)
    content = "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
    with open(file_path, "w", encoding="utf-8") as output:
        output.write(content)


def safe_reset_build_dir(build_dir):
    """
    安全清空当前项目内的构建目录。

    :param build_dir: 构建输出目录
    :return: None，无返回值
    """
    project_root = os.path.abspath(os.getcwd())
    target = os.path.abspath(build_dir)
    if not target.startswith(project_root + os.sep):
        raise RuntimeError(f"Refusing to remove build directory outside project: {target}")
    if os.path.exists(target):
        shutil.rmtree(target)
    ensure_dir(target)


def write_sitemap(static_dir):
    """
    根据语言路由矩阵生成 sitemap.xml。

    :param static_dir: 静态源文件目录
    :return: None，无返回值
    """
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for route in get_route_matrix():
        lastmod = PAGE_LASTMOD.get(route["page_key"], LAST_UPDATED)
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE_URL}{route['path']}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(static_dir, "sitemap.xml"), "w", encoding="utf-8") as output:
        output.write("\n".join(lines) + "\n")


def write_redirects(static_dir):
    """
    生成 Cloudflare Pages 的显式尾斜杠重定向规则。

    :param static_dir: 静态源文件目录
    :return: None，无返回值
    """
    redirects = []
    for route in get_route_matrix():
        path = route["path"]
        if path != "/" and path.endswith("/"):
            redirects.append(f"{path.rstrip('/')} {path} 301")
    with open(os.path.join(static_dir, "_redirects"), "w", encoding="utf-8") as output:
        output.write("\n".join(sorted(set(redirects))) + "\n")


def write_llms_files(static_dir):
    """
    生成根目录 llms.txt 和 llms-full.txt 文件。

    :param static_dir: 静态源文件目录
    :return: None，无返回值
    """
    core_links = [
        ("Main planner", get_page_path("home"), "Interactive Mistfall Hunter class planner and role overview."),
        ("Classes guide", get_page_path("classes"), "Class role profiles, risk notes, and beginner direction."),
        ("Build planner", get_page_path("build-planner"), "Dedicated planner page for build-intent searches."),
        ("Price guide", get_page_path("price"), "Steam price snapshot, launch discount, buyer checks, and refund-source guidance."),
        ("Player count guide", get_page_path("player-count"), "SteamDB chart interpretation, current-player signals, and queue-timing guidance."),
        ("Map guide", get_page_path("map-guide"), "Map markers, key-route decisions, community map references, and extraction planning."),
        ("Tier list guide", get_page_path("tier-list"), "Mode-specific class tier list with solo, duo, squad, and beginner decisions."),
        ("PS5 guide", get_page_path("ps5"), "Official Mistfall Hunter PS5 availability, release, price, and platform comparison checks."),
        ("Crossplay guide", get_page_path("crossplay"), "PC, PS5, and Xbox crossplay checks, friend invites, progression limits, and source boundaries."),
        ("Steam info", get_page_path("steam"), "Official Steam facts and safe source links."),
        ("Review guide", get_page_path("review"), "Independent Mistfall Hunter review covering the game loop, class fit, buyer checks, and tradeoffs."),
        ("Gameplay guide", get_page_path("gameplay"), "Mistfall Hunter gameplay guide covering the extraction loop, combat decisions, class rhythm, and beginner mistakes."),
    ]
    common_links = [
        ("About", get_page_path("about"), "Editorial policy and source handling."),
        ("Contact", get_page_path("contact"), "Correction and feedback contact route."),
        ("Privacy Policy", get_page_path("privacy-policy"), "Privacy and planner data handling."),
        ("Terms of Service", get_page_path("terms-of-service"), "Fan-site disclaimer and usage terms."),
    ]
    llms_lines = [
        "# Mistfall Hunter Classes",
        "",
        "> Mistfall Hunter Classes is a fan-made guide and build planner for comparing roles, risk, and build direction before a run.",
        "",
        "## Core Content",
    ]
    llms_lines.extend([f"- [{title}]({BASE_URL}{path}): {description}" for title, path, description in core_links])
    llms_lines.extend(["", "## Common Resources"])
    llms_lines.extend([f"- [{title}]({BASE_URL}{path}): {description}" for title, path, description in common_links])
    llms_lines.extend([f"- [PS5 guide]({BASE_URL}{get_page_path('ps5')}): Added on 2026-08-19 with official PlayStation, Xbox, and Steam checks, three visual points, localized FAQ content, and platform comparison guidance.", f"- [Crossplay guide]({BASE_URL}{get_page_path('crossplay')}): Added on 2026-08-19 with PC, PS5, and Xbox platform checks, crossplay versus progression boundaries, three visual points, localized FAQ content, and official source links."])
    llms_lines.extend(["", "## Latest Updates", f"- [Tier list guide]({BASE_URL}{get_page_path('tier-list')}): Added on 2026-08-15 with mode-specific class comparisons, three visual points, localized FAQ content, and related class resources.", f"- [Map guide]({BASE_URL}{get_page_path('map-guide')}): Added on 2026-08-10 with map-route decisions, attributed community map references, a conceptual route diagram, localized FAQ content, and related class resources.", f"- [Gameplay guide]({BASE_URL}{get_page_path('gameplay')}): Added on 2026-08-08 with an extraction-loop explanation, localized gameplay guidance, three visual points, FAQ content, and related class resources."])
    with open(os.path.join(static_dir, "llms.txt"), "w", encoding="utf-8") as output:
        output.write("\n".join(llms_lines) + "\n")

    full_lines = [
        "# Mistfall Hunter Classes: Complete Site Guide",
        "",
        "> Mistfall Hunter Classes is an independent fan-made class guide and build planner for players comparing Mistfall Hunter roles before they choose a solo, duo, or squad setup. The site links to official Steam information for platform and release facts and keeps class recommendations editorial rather than official.",
        "",
        "## Site Background",
        "Mistfall Hunter Classes exists to help players make class and build decisions with clear assumptions. The site separates official Steam facts from fan-made scoring. Platform, developer, publisher, and release details are tied to the official Steam listing, while class recommendations are transparent editorial guidance that should be revised when verified patch notes, class values, or repeated gameplay evidence changes the balance picture. Corrections can be sent through the contact page with a source URL and the affected page path.",
        "",
        "## Content Category Details",
    ]
    for title, path, description in core_links:
        full_lines.extend([f"### [{title}]({BASE_URL}{path})", description + " The page is implemented as crawlable static HTML and is included in the sitemap.", ""])
    full_lines.extend([
        "## User Value",
        "The site helps users pick a practical class direction, compare role risk, understand when a recommendation should be treated as a tie, and verify safe official Steam availability without confusing guide content with downloads, keys, or unofficial mirrors.",
        "",
        "## Platform Availability",
        f"### [Mistfall Hunter PS5 guide]({BASE_URL}{get_page_path('ps5')})",
        "Updated on 2026-08-19 to verify official PlayStation, Xbox, and Steam platform pages, date the checked release and price context, separate console availability from unsupported performance claims, and connect the page to related buyer and gameplay resources.",
        "",
        "## Latest Update Content",
        f"### [Multilingual tier list update]({BASE_URL}{get_page_path('tier-list')})",
        "Updated on 2026-08-15 to add mode-specific class comparisons, an explicit non-official ranking method, three visual points, localized metadata, FAQ content, related class resources, sitemap entries, and language switching.",
        "",
        f"### [Multilingual map guide update]({BASE_URL}{get_page_path('map-guide')})",
        "Updated on 2026-08-10 to add the multilingual Mistfall Hunter map guide, attributed community map references, a conceptual route visual, localized metadata, FAQ content, related class resources, sitemap entries, and language switching.",
        "",
        f"### [Multilingual gameplay update]({BASE_URL}{get_page_path('gameplay')})",
        "Updated on 2026-08-08 to add the multilingual Mistfall Hunter gameplay guide, localized metadata, gameplay-loop media, source links, FAQ content, related class resources, sitemap entries, and language switching.",
    ])
    with open(os.path.join(static_dir, "llms-full.txt"), "w", encoding="utf-8") as output:
        output.write("\n".join(full_lines) + "\n")


def refresh_static_metadata():
    """
    刷新 sitemap、redirects 和 AI 可见性文件。

    :return: None，无返回值
    """
    static_dir = "static"
    write_sitemap(static_dir)
    write_redirects(static_dir)
    write_llms_files(static_dir)


def copy_static_assets(build_dir):
    """
    复制静态资源和根目录公开文件到构建目录。

    :param build_dir: 构建输出目录
    :return: None，无返回值
    """
    static_build = os.path.join(build_dir, "static")
    ensure_dir(static_build)
    asset_files = [
        os.path.join("css", "mistfall.css"),
        os.path.join("js", "mistfall-planner.js"),
        os.path.join("images", "mistfall", "mistfall-hunter-steam-hero.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-steam-header.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-price-check.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-review-verdict.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-gameplay-loop.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-tier-list-modes.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-tier-list-roles.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-map-route-concept.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-ps5-console-concept.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-crossplay-platforms.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-map-shenwood.webp"),
        os.path.join("images", "mistfall", "mistfall-hunter-map-brand-keep.webp"),
        os.path.join("videos", "mistfall-hunter-build-guide.mp4"),
        "logo.png",
        "favicon.ico",
    ]
    for filename in asset_files:
        source = os.path.join("static", filename)
        if os.path.exists(source):
            destination = os.path.join(static_build, filename)
            ensure_dir(os.path.dirname(destination))
            shutil.copy2(source, destination)
    for filename in ["robots.txt", "sitemap.xml", "favicon.ico", "llms.txt", "llms-full.txt", "_redirects", "_worker.js"]:
        source = os.path.join("static", filename)
        if os.path.exists(source):
            shutil.copy2(source, os.path.join(build_dir, filename))


def build_site():
    """
    生成 Mistfall Hunter Classes 的多语言静态站点文件。

    :return: None，无返回值
    """
    build_dir = "build"
    refresh_static_metadata()
    safe_reset_build_dir(build_dir)

    with app.test_client() as client:
        for route in get_route_matrix():
            response = client.get(route["path"])
            if response.status_code != 200:
                raise RuntimeError(f"Route failed: {route['path']} returned {response.status_code}")
            save_page(route["path"], response.data.decode("utf-8"), build_dir)
            print(f"Generated: {route['path']}")

        with app.test_request_context("/missing-page/"):
            response_content, _ = page_not_found(NotFound())
            save_page("/404.html", response_content, build_dir)
            print("Generated: /404.html")

    copy_static_assets(build_dir)
    print("Static files generation completed.")


if __name__ == "__main__":
    try:
        build_site()
    except Exception as exc:
        print(f"Error during build process: {exc}", file=sys.stderr)
        sys.exit(1)
