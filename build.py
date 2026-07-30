import os
import shutil
import sys

from app import SITE_PAGES, app, page_not_found
from werkzeug.exceptions import NotFound


def ensure_dir(path):
    """
    确保指定目录存在

    :param path: 需要创建或确认存在的目录路径
    :return: None，无返回值
    """
    os.makedirs(path, exist_ok=True)


def page_path_for_url(url):
    """
    将站点 URL 路径转换为静态 HTML 输出路径

    :param url: 站点页面路径
    :return: str，静态构建目录中的相对 HTML 文件路径
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
    保存静态页面内容到构建目录

    :param url: 站点页面路径
    :param content: 页面 HTML 内容
    :param build_dir: 构建输出目录
    :return: None，无返回值
    """
    file_path = os.path.join(build_dir, page_path_for_url(url))
    ensure_dir(os.path.dirname(file_path) or build_dir)
    with open(file_path, "w", encoding="utf-8") as output:
        output.write(content)


def copy_static_assets(build_dir):
    """
    复制静态资源和根目录公开文件到构建目录

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
    生成 Mistfall Hunter Classes 的静态站点文件

    :return: None，无返回值
    """
    build_dir = "build"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    ensure_dir(build_dir)

    with app.test_client() as client:
        for page in SITE_PAGES.values():
            response = client.get(page["path"])
            if response.status_code == 200:
                save_page(page["path"], response.data.decode("utf-8"), build_dir)
                print(f"Generated: {page['path']}")

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
