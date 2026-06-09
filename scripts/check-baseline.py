#!/usr/bin/env python3
from pathlib import Path
import py_compile
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-legacy-api-baseline.md"
HTTPS_PLAN = ROOT / "docs/plans/2026-06-09-private-endpoint-https.md"
HTTPS_HOST_PLAN = ROOT / "docs/plans/2026-06-09-private-endpoint-host-validation.md"
INSTAGRAM_HOST_PLAN = ROOT / "docs/plans/2026-06-09-instagram-pagination-host-validation.md"
TEMPLATE_GLASS_PLAN = ROOT / "docs/plans/2026-06-09-template-glass-url-validation.md"
PRIVATE_URL_PARTS_PLAN = ROOT / "docs/plans/2026-06-09-private-endpoint-url-parts.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
PICASA_EMPTY_FEED_PLAN = ROOT / "docs/plans/2026-06-09-picasa-empty-feed-guard.md"
TEMPLATE_EXTERNAL_HTTPS_PLAN = ROOT / "docs/plans/2026-06-09-template-external-https.md"
BUG = ROOT / "docs/bugs/p2-python-access-token-in-url-query-c765eb4838c12375.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def main():
    failures = []
    required_files = [
        ".gitignore",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "app.yaml",
        "base.py",
        "cache.py",
        "glass.py",
        "instagram.py",
        "main.py",
        "map.py",
        "picasa.py",
        "templates/base.html",
        "templates/stream.html",
        "docs/plans/2026-06-08-legacy-api-baseline.md",
        "docs/plans/2026-06-09-private-endpoint-https.md",
        "docs/plans/2026-06-09-private-endpoint-host-validation.md",
        "docs/plans/2026-06-09-private-endpoint-url-parts.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-09-picasa-empty-feed-guard.md",
        "docs/plans/2026-06-09-template-external-https.md",
        "docs/plans/2026-06-09-instagram-pagination-host-validation.md",
        "docs/plans/2026-06-09-template-glass-url-validation.md",
        "docs/bugs/p2-python-access-token-in-url-query-c765eb4838c12375.md",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    instagram_source = read("instagram.py")
    base_source = read("base.py")
    glass_source = read("glass.py")
    main_source = read("main.py")
    map_source = read("map.py")
    picasa_source = read("picasa.py")
    base_template = read("templates/base.html")
    readme_text = read("README.md")
    vision_text = read("VISION.md")
    changes_text = read("CHANGES.md")
    gitignore_text = read(".gitignore")
    bug_text = BUG.read_text(encoding="utf-8") if BUG.exists() else ""
    plan_text = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    https_plan_text = HTTPS_PLAN.read_text(encoding="utf-8") if HTTPS_PLAN.exists() else ""
    https_host_plan_text = HTTPS_HOST_PLAN.read_text(encoding="utf-8") if HTTPS_HOST_PLAN.exists() else ""
    instagram_host_plan_text = INSTAGRAM_HOST_PLAN.read_text(encoding="utf-8") if INSTAGRAM_HOST_PLAN.exists() else ""
    template_glass_plan_text = TEMPLATE_GLASS_PLAN.read_text(encoding="utf-8") if TEMPLATE_GLASS_PLAN.exists() else ""
    private_url_parts_plan_text = PRIVATE_URL_PARTS_PLAN.read_text(encoding="utf-8") if PRIVATE_URL_PARTS_PLAN.exists() else ""
    app_yaml = read("app.yaml")
    makefile_text = read("Makefile")

    require("runtime: python27" in app_yaml,
            "app.yaml should continue to document the legacy Python 2 App Engine runtime",
            failures)
    require("debug=False" in main_source and "debug=True" not in main_source,
            "main.py must keep public webapp2 debug output disabled",
            failures)
    require(".PHONY: build check lint test" in makefile_text and "lint test build: check" in makefile_text,
            "Makefile must expose lint, test, build, and check gate targets",
            failures)
    require("const.py" in gitignore_text and ".env" in gitignore_text,
            "private local configuration files must stay ignored",
            failures)

    require("access_token=" not in instagram_source,
            "instagram.py must not build access-token query strings",
            failures)
    require("instagram_url" not in instagram_source,
            "instagram.py must not keep token-bearing module-level URLs",
            failures)
    require("Authorization" in instagram_source and "Bearer " in instagram_source,
            "instagram.py must send Instagram tokens through an authorization header",
            failures)
    require("_without_access_token_query" in instagram_source and "parse_qsl" in instagram_source,
            "instagram.py must strip access_token from provider pagination URLs",
            failures)
    require("INSTAGRAM_API_HOST" in instagram_source and "api.instagram.com" in instagram_source and "def require_instagram_api_url" in instagram_source,
            "instagram.py must define the allowed Instagram API host",
            failures)
    require('parts.scheme != "https"' in instagram_source and "parts.netloc.lower() != INSTAGRAM_API_HOST" in instagram_source,
            "instagram.py must reject non-HTTPS or non-Instagram API URLs before sending bearer credentials",
            failures)
    require("require_instagram_api_url(_without_access_token_query(url))" in instagram_source,
            "instagram.py must validate stripped Instagram URLs before creating authorized requests",
            failures)

    require("https://api.openweathermap.org" in map_source and "http://api.openweathermap.org" not in map_source,
            "map.py must use HTTPS for OpenWeather requests",
            failures)
    require("urllib.urlencode" in map_source,
            "map.py should use structured query encoding for external API URLs",
            failures)
    require("url_string" not in map_source and "cache_key = self.request.path_qs" in map_source,
            "map.py must write memcache entries with a defined request cache key",
            failures)
    require("memcache.set(key=cache_key" in map_source,
            "map.py must use the defined cache key when writing map responses",
            failures)
    require("if not results:" in map_source and 'return ""' in map_source,
            "map.py must handle empty geocoding responses",
            failures)
    require("def require_https_url" in base_source and "urlparse.urlsplit" in base_source and "parsed.netloc" in base_source,
            "base.py must validate private endpoint URL schemes and hosts",
            failures)
    require("parsed.username" in base_source and "parsed.password" in base_source and "parsed.fragment" in base_source,
            "base.py must reject private endpoint URL credentials and fragments",
            failures)
    require('require_https_url(const.glass_url, "glass_url")' in base_source,
            "base.py must validate the template-facing Glass URL before rendering it",
            failures)
    require('require_https_url(const.map_api, "map_api")' in map_source,
            "map.py must validate the private map API endpoint before fetching it",
            failures)
    require('require_https_url(const.picasa_api, "picasa_api")' in picasa_source,
            "picasa.py must validate the private Picasa endpoint before fetching it",
            failures)
    require("data.get('feed', {}).get('entry', [])" in picasa_source,
            "picasa.py must handle empty or missing Picasa feed entries",
            failures)
    require('require_https_url(const.glass_api, "glass_api")' in glass_source,
            "glass.py must validate the private Glass endpoint before fetching it",
            failures)
    require('href="//' not in base_template and 'src="//' not in base_template and "'//www.google-analytics.com/analytics.js'" not in base_template,
            "templates/base.html must not use protocol-relative external browser asset URLs",
            failures)
    require("https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" in base_template and "https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" in base_template and "https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js" in base_template and "https://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js" in base_template and "https://www.google-analytics.com/analytics.js" in base_template,
            "templates/base.html must pin external browser assets to HTTPS URLs",
            failures)

    require("make lint" in readme_text and "make test" in readme_text and "make build" in readme_text and "make check" in readme_text and "scripts/check-baseline.py" in readme_text,
            "README must document the local baseline check",
            failures)
    require("private endpoints" in readme_text and "HTTPS URLs with hosts" in readme_text,
            "README must document the private endpoint HTTPS host guard",
            failures)
    require("no embedded credentials or fragments" in readme_text,
            "README must document the private endpoint URL-parts guard",
            failures)
    require("template-facing Glass URL" in readme_text,
            "README must document the template-facing Glass URL guard",
            failures)
    require("Empty Picasa feed responses" in readme_text,
            "README must document the Picasa empty-feed guard",
            failures)
    require("External template assets" in readme_text and "explicit HTTPS URLs" in readme_text,
            "README must document the template external asset HTTPS guard",
            failures)
    require("Instagram pagination URLs" in readme_text and "https://api.instagram.com" in readme_text,
            "README must document the Instagram pagination host guard",
            failures)
    require("const.py" in readme_text and "Python 2 App Engine" in readme_text,
            "README must document private config and legacy runtime expectations",
            failures)
    require("scripts/check-baseline.py" in vision_text and "make lint" in vision_text and "make test" in vision_text and "make build" in vision_text and "access-token query strings" in vision_text,
            "VISION must describe the current integration guardrails",
            failures)
    require("Private integration endpoints" in vision_text and "HTTPS URLs with hosts" in vision_text,
            "VISION must describe the private endpoint HTTPS host guard",
            failures)
    require("no embedded credentials or fragments" in vision_text,
            "VISION must describe the private endpoint URL-parts guard",
            failures)
    require("template-facing Glass URL" in vision_text,
            "VISION must describe the template-facing Glass URL guard",
            failures)
    require("Empty Picasa feed responses" in vision_text,
            "VISION must describe the Picasa empty-feed guard",
            failures)
    require("External template assets" in vision_text and "explicit HTTPS URLs" in vision_text,
            "VISION must describe the template external asset HTTPS guard",
            failures)
    require("Instagram pagination host" in vision_text and "https://api.instagram.com" in vision_text,
            "VISION must describe the Instagram pagination host guard",
            failures)
    require("make lint" in changes_text and "make test" in changes_text and "make build" in changes_text and "access-token query string" in changes_text and "map API cache" in changes_text and "Instagram pagination URLs" in changes_text and "template-facing Glass URL" in changes_text and "embedded credentials or fragments" in changes_text and "empty Picasa feed" in changes_text and "protocol-relative template asset URLs" in changes_text,
            "CHANGES must record the API-token, map-cache, URL-parts, Instagram pagination host, and template asset fixes",
            failures)
    require("Resolved" in bug_text and "Authorization header" in bug_text,
            "recorded bug must describe the resolved access-token handling",
            failures)
    require("status: completed" in plan_text,
            "plan must be marked completed",
            failures)
    require("status: completed" in https_plan_text,
            "private endpoint HTTPS plan must be marked completed",
            failures)
    require("status: completed" in https_host_plan_text,
            "private endpoint HTTPS host plan must be marked completed",
            failures)
    require("status: completed" in instagram_host_plan_text,
            "Instagram pagination host plan must be marked completed",
            failures)
    require("status: completed" in template_glass_plan_text,
            "template-facing Glass URL plan must be marked completed",
            failures)
    require("status: completed" in private_url_parts_plan_text,
            "private endpoint URL-parts plan must be marked completed",
            failures)
    make_gates_plan_text = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    require("status: completed" in make_gates_plan_text,
            "Make gate alias plan must be marked completed",
            failures)
    picasa_empty_feed_plan_text = PICASA_EMPTY_FEED_PLAN.read_text(encoding="utf-8") if PICASA_EMPTY_FEED_PLAN.exists() else ""
    require("status: completed" in picasa_empty_feed_plan_text,
            "Picasa empty-feed plan must be marked completed",
            failures)
    template_external_https_plan_text = TEMPLATE_EXTERNAL_HTTPS_PLAN.read_text(encoding="utf-8") if TEMPLATE_EXTERNAL_HTTPS_PLAN.exists() else ""
    require("status: completed" in template_external_https_plan_text,
            "template external asset HTTPS plan must be marked completed",
            failures)

    for path in sorted(ROOT.glob("*.py")) + [ROOT / "scripts/check-baseline.py"]:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as error:
            failures.append(str(error))

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("garethpaul.com legacy API baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
