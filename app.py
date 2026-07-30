import socket

from flask import Flask, render_template


app = Flask(__name__)
app.config["FREEZER_DESTINATION"] = "build"

BASE_URL = "https://mistfallhunterclasses.blog"
SUPPORT_EMAIL = "support@mistfallhunterclasses.blog"


SITE_PAGES = {
    "home": {
        "path": "/",
        "template": "index.html",
        "title": "Mistfall Hunter Classes & Build Planner",
        "description": "Compare Mistfall Hunter classes, plan solo or squad builds, and check role recommendations with a fan-made class planner.",
        "h1": "Mistfall Hunter Classes & Build Planner",
    },
    "classes": {
        "path": "/classes/",
        "template": "simple-page.html",
        "title": "Mistfall Hunter Classes Guide",
        "description": "A practical Mistfall Hunter classes guide covering roles, strengths, risk level, and beginner picks.",
        "h1": "Mistfall Hunter Classes Guide",
    },
    "build-planner": {
        "path": "/build-planner/",
        "template": "simple-page.html",
        "title": "Mistfall Hunter Build Planner",
        "description": "Use the Mistfall Hunter build planner to match classes with solo, duo, and squad play styles.",
        "h1": "Mistfall Hunter Build Planner",
    },
    "steam": {
        "path": "/steam/",
        "template": "simple-page.html",
        "title": "Mistfall Hunter Steam Info",
        "description": "Mistfall Hunter Steam info for availability, platform facts, release date, developer, publisher, and official source links.",
        "h1": "Mistfall Hunter Steam Info",
    },
    "about": {
        "path": "/about/",
        "template": "simple-page.html",
        "title": "About Mistfall Hunter Classes",
        "description": "Learn how Mistfall Hunter Classes reviews public sources and keeps class guide recommendations transparent.",
        "h1": "About Mistfall Hunter Classes",
    },
    "contact": {
        "path": "/contact/",
        "template": "simple-page.html",
        "title": "Contact Mistfall Hunter Classes",
        "description": "Send corrections, source notes, class data updates, and site feedback to Mistfall Hunter Classes.",
        "h1": "Contact Mistfall Hunter Classes",
    },
    "privacy-policy": {
        "path": "/privacy-policy/",
        "template": "simple-page.html",
        "title": "Privacy Policy",
        "description": "Privacy policy for Mistfall Hunter Classes, a fan-made guide and build planner site.",
        "h1": "Privacy Policy",
    },
    "terms-of-service": {
        "path": "/terms-of-service/",
        "template": "simple-page.html",
        "title": "Terms of Service",
        "description": "Terms of service and fan-site disclaimer for Mistfall Hunter Classes.",
        "h1": "Terms of Service",
    },
}


CLASS_DATA = [
    {
        "name": "Mercenary",
        "role": "Frontline brawler",
        "best_for": "Players who want forgiving melee pressure and steady extractions.",
        "solo": 86,
        "squad": 78,
        "burst": 60,
        "control": 54,
        "risk": "Low",
    },
    {
        "name": "Blackarrow",
        "role": "Ranged pressure",
        "best_for": "Careful players who prefer scouting, poking, and choosing fights.",
        "solo": 74,
        "squad": 84,
        "burst": 78,
        "control": 64,
        "risk": "Medium",
    },
    {
        "name": "Shadowstrix",
        "role": "Assassin skirmisher",
        "best_for": "High-mobility players who like ambushes, flanks, and fast disengage.",
        "solo": 82,
        "squad": 70,
        "burst": 90,
        "control": 58,
        "risk": "High",
    },
    {
        "name": "Sorcerer",
        "role": "Area damage caster",
        "best_for": "Players who want spell burst, zone pressure, and group fight impact.",
        "solo": 66,
        "squad": 88,
        "burst": 92,
        "control": 82,
        "risk": "High",
    },
    {
        "name": "Seer",
        "role": "Support and information",
        "best_for": "Squads that value tracking, utility, and safer extraction decisions.",
        "solo": 58,
        "squad": 92,
        "burst": 42,
        "control": 86,
        "risk": "Medium",
    },
    {
        "name": "Withered Knight",
        "role": "Durable initiator",
        "best_for": "Players who like holding space, surviving trades, and protecting allies.",
        "solo": 78,
        "squad": 86,
        "burst": 64,
        "control": 76,
        "risk": "Medium",
    },
]


def build_site_data(page_key):
    """
    组装指定页面渲染所需的站点数据

    :param page_key: 页面标识，对应 SITE_PAGES 中的键
    :return: dict，包含页面元信息、导航、职业数据和站点公共配置
    """
    page = SITE_PAGES[page_key]
    return {
        "base_url": BASE_URL,
        "support_email": SUPPORT_EMAIL,
        "site_name": "Mistfall Hunter Classes",
        "page_key": page_key,
        "page": page,
        "pages": SITE_PAGES,
        "canonical_url": f"{BASE_URL}{page['path'] if page['path'] != '/' else '/'}",
        "classes": CLASS_DATA,
        "official_steam_url": "https://store.steampowered.com/app/3282300/Mistfall_Hunter/",
        "current_year": "2026",
    }


def render_site_page(page_key):
    """
    渲染指定站点页面

    :param page_key: 页面标识，对应 SITE_PAGES 中的键
    :return: str，渲染完成的 HTML 响应内容
    """
    data = build_site_data(page_key)
    return render_template(data["page"]["template"], **data)


@app.route("/")
def index():
    """
    渲染 Mistfall Hunter Classes 首页

    :return: str，首页 HTML 响应内容
    """
    return render_site_page("home")


@app.route("/classes/", strict_slashes=False)
def classes_page():
    """
    渲染 Mistfall Hunter 职业指南页面

    :return: str，职业指南页面 HTML 响应内容
    """
    return render_site_page("classes")


@app.route("/build-planner/", strict_slashes=False)
def build_planner():
    """
    渲染 Mistfall Hunter Build Planner 页面

    :return: str，Build Planner 页面 HTML 响应内容
    """
    return render_site_page("build-planner")


@app.route("/steam/", strict_slashes=False)
def steam_page():
    """
    渲染 Mistfall Hunter Steam 信息页面

    :return: str，Steam 信息页面 HTML 响应内容
    """
    return render_site_page("steam")


@app.route("/about/", strict_slashes=False)
def about():
    """
    渲染关于本站页面

    :return: str，关于页面 HTML 响应内容
    """
    return render_site_page("about")


@app.route("/contact/", strict_slashes=False)
def contact():
    """
    渲染联系页面

    :return: str，联系页面 HTML 响应内容
    """
    return render_site_page("contact")


@app.route("/privacy-policy/", strict_slashes=False)
def privacy_policy():
    """
    渲染隐私政策页面

    :return: str，隐私政策页面 HTML 响应内容
    """
    return render_site_page("privacy-policy")


@app.route("/terms-of-service/", strict_slashes=False)
def terms_of_service():
    """
    渲染服务条款页面

    :return: str，服务条款页面 HTML 响应内容
    """
    return render_site_page("terms-of-service")


@app.errorhandler(404)
def page_not_found(error):
    """
    渲染 404 错误页面

    :param error: Flask 传入的错误对象
    :return: tuple[str, int]，404 页面 HTML 和状态码
    """
    data = build_site_data("home")
    data["page"] = {
        "path": "/404.html",
        "title": "Page Not Found",
        "description": "The requested Mistfall Hunter Classes page could not be found.",
        "h1": "Page Not Found",
    }
    return render_template("simple-page.html", **data), 404


def find_available_port(start_port):
    """
    从指定端口开始查找可用的本地服务端口

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
