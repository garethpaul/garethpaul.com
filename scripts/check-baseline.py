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
PICASA_ENTRY_SHAPE_PLAN = ROOT / "docs/plans/2026-06-09-picasa-entry-shape-guard.md"
CI_CHARACTERIZATION_PLAN = ROOT / "docs/plans/2026-06-10-ci-and-characterization-tests.md"
TEMPLATE_IMAGE_DOM_PLAN = ROOT / "docs/plans/2026-06-10-template-image-dom-safety.md"
OUTBOUND_TIMEOUT_PLAN = ROOT / "docs/plans/2026-06-12-outbound-http-timeouts.md"
PROVIDER_RESPONSE_LIMIT_PLAN = ROOT / "docs/plans/2026-06-12-provider-response-size-limit.md"
CI_SECURITY_PLAN = ROOT / "docs/plans/2026-06-12-ci-least-privilege-contract.md"
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
        ".github/workflows/check.yml",
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
        "templates/picture.html",
        "templates/stream.html",
        "tests/test_integration_guards.py",
        "tests/test_template_image_rendering.py",
        "docs/plans/2026-06-08-legacy-api-baseline.md",
        "docs/plans/2026-06-09-private-endpoint-https.md",
        "docs/plans/2026-06-09-private-endpoint-host-validation.md",
        "docs/plans/2026-06-09-private-endpoint-url-parts.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-09-picasa-empty-feed-guard.md",
        "docs/plans/2026-06-09-picasa-entry-shape-guard.md",
        "docs/plans/2026-06-09-template-external-https.md",
        "docs/plans/2026-06-09-instagram-pagination-host-validation.md",
        "docs/plans/2026-06-09-template-glass-url-validation.md",
        "docs/plans/2026-06-10-ci-and-characterization-tests.md",
        "docs/plans/2026-06-10-template-image-dom-safety.md",
        "docs/plans/2026-06-12-outbound-http-timeouts.md",
        "docs/plans/2026-06-12-provider-response-size-limit.md",
        "docs/plans/2026-06-12-ci-least-privilege-contract.md",
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
    picture_template = read("templates/picture.html")
    stream_template = read("templates/stream.html")
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
    ci_characterization_plan_text = CI_CHARACTERIZATION_PLAN.read_text(encoding="utf-8") if CI_CHARACTERIZATION_PLAN.exists() else ""
    template_image_dom_plan_text = TEMPLATE_IMAGE_DOM_PLAN.read_text(encoding="utf-8") if TEMPLATE_IMAGE_DOM_PLAN.exists() else ""
    outbound_timeout_plan_text = OUTBOUND_TIMEOUT_PLAN.read_text(encoding="utf-8") if OUTBOUND_TIMEOUT_PLAN.exists() else ""
    provider_response_limit_plan_text = PROVIDER_RESPONSE_LIMIT_PLAN.read_text(encoding="utf-8") if PROVIDER_RESPONSE_LIMIT_PLAN.exists() else ""
    ci_security_plan_text = CI_SECURITY_PLAN.read_text(encoding="utf-8") if CI_SECURITY_PLAN.exists() else ""
    app_yaml = read("app.yaml")
    makefile_text = read("Makefile")
    workflow_text = read(".github/workflows/check.yml")
    integration_guard_tests = read("tests/test_integration_guards.py")

    require("runtime: python27" in app_yaml,
            "app.yaml should continue to document the legacy Python 2 App Engine runtime",
            failures)
    require("debug=False" in main_source and "debug=True" not in main_source,
            "main.py must keep public webapp2 debug output disabled",
            failures)
    require(".PHONY: build check lint test" in makefile_text and "lint build: check" in makefile_text and "python3 -m unittest discover -s tests" in makefile_text,
            "Makefile must expose lint, test, build, and check gate targets with characterization tests",
            failures)
    expected_workflow_text = """name: Check

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  check:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.12", "3.14"]
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6.2.0
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run baseline
        run: make check
"""
    require(workflow_text == expected_workflow_text,
            "GitHub Actions must exactly match the pinned, least-privilege multi-version Python contract",
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
    require("HTTP_TIMEOUT_SECONDS = 10" in base_source and "def open_url(url_or_request):" in base_source and "urllib2.urlopen(url_or_request, timeout=HTTP_TIMEOUT_SECONDS)" in base_source,
            "base.py must enforce the shared 10-second outbound provider timeout",
            failures)
    require("MAX_PROVIDER_RESPONSE_BYTES = 1024 * 1024" in base_source and "def read_url(url_or_request):" in base_source and "response.read(MAX_PROVIDER_RESPONSE_BYTES + 1)" in base_source and "response.close()" in base_source and "len(payload) > MAX_PROVIDER_RESPONSE_BYTES" in base_source,
            "base.py must bound and close provider response bodies before JSON decoding",
            failures)
    provider_sources = [glass_source, instagram_source, map_source, picasa_source]
    require(all("urllib2.urlopen(" not in source for source in provider_sources),
            "provider handlers must not bypass base.open_url with direct urllib2.urlopen calls",
            failures)
    require(all("read_url(" in source for source in provider_sources),
            "every provider handler must route payload reads through base.read_url",
            failures)
    require(all(".read()" not in source for source in provider_sources),
            "provider handlers must not perform unbounded response reads",
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
    require("def picasa_entry_src" in picasa_source and "isinstance(entry, dict)" in picasa_source and "isinstance(content, dict)" in picasa_source,
            "picasa.py must parse album entry image sources through a shape guard",
            failures)
    require("img_src = picasa_entry_src(i)" in picasa_source and "if img_src:" in picasa_source,
            "picasa.py must skip malformed Picasa entries instead of raising",
            failures)
    require("base.require_https_url" in integration_guard_tests and "base.open_url" in integration_guard_tests and "base.HTTP_TIMEOUT_SECONDS" in integration_guard_tests and "base.read_url" in integration_guard_tests and "base.MAX_PROVIDER_RESPONSE_BYTES" in integration_guard_tests and "response.closed" in integration_guard_tests and "instagram.instagram_request" in integration_guard_tests and "picasa.picasa_entry_src" in integration_guard_tests,
            "integration characterization tests must exercise private URL, timeout, response-size, Instagram, and Picasa guards",
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
    require("function appendHttpsImage" in base_template and 'typeof source !== "string"' in base_template and "/^https:\\/\\//i.test(source)" in base_template and '$("<img>").addClass(className).attr("src", source)' in base_template,
            "templates must render provider images through the shared HTTPS DOM helper",
            failures)
    require('appendHttpsImage(".photos", "instagram", img)' in picture_template and stream_template.count('appendHttpsImage(".photos", "glass",') == 2 and "html +=" not in picture_template + stream_template,
            "picture and stream templates must not concatenate provider values into HTML",
            failures)
    require("encodeURIComponent(val)" in stream_template and '"/img?token=" + val' not in stream_template,
            "stream template must encode Glass token values before URL construction",
            failures)

    require("make lint" in readme_text and "make test" in readme_text and "make build" in readme_text and "make check" in readme_text and "scripts/check-baseline.py" in readme_text and "tests/test_integration_guards.py" in readme_text,
            "README must document the local baseline and characterization checks",
            failures)
    require("GitHub Actions" in readme_text and ".github/workflows/check.yml" in readme_text,
            "README must document the CI check",
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
    require("Malformed Picasa album entries" in readme_text,
            "README must document the Picasa entry shape guard",
            failures)
    require("DOM property assignment" in readme_text and "HTTPS image URLs" in readme_text,
            "README must document safe provider image rendering",
            failures)
    require("External template assets" in readme_text and "explicit HTTPS URLs" in readme_text,
            "README must document the template external asset HTTPS guard",
            failures)
    require("Instagram pagination URLs" in readme_text and "https://api.instagram.com" in readme_text,
            "README must document the Instagram pagination host guard",
            failures)
    require("shared 10-second" in readme_text and "base.open_url" in readme_text and "1 MiB" in readme_text and "base.read_url" in readme_text,
            "README must document the outbound provider timeout and response-size boundaries",
            failures)
    require("const.py" in readme_text and "Python 2 App Engine" in readme_text,
            "README must document private config and legacy runtime expectations",
            failures)
    require("scripts/check-baseline.py" in vision_text and "tests/test_integration_guards.py" in vision_text and "make lint" in vision_text and "make test" in vision_text and "make build" in vision_text and "GitHub Actions" in vision_text and "access-token query strings" in vision_text,
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
    require("Malformed Picasa album entries" in vision_text,
            "VISION must describe the Picasa entry shape guard",
            failures)
    require("External template assets" in vision_text and "explicit HTTPS URLs" in vision_text,
            "VISION must describe the template external asset HTTPS guard",
            failures)
    require("Instagram pagination host" in vision_text and "https://api.instagram.com" in vision_text,
            "VISION must describe the Instagram pagination host guard",
            failures)
    require("shared 10-second deadline" in vision_text and "urllib2.urlopen" in vision_text,
            "VISION must describe the outbound provider timeout boundary",
            failures)
    require("GitHub Actions" in changes_text and "characterization tests" in changes_text and "make lint" in changes_text and "make test" in changes_text and "make build" in changes_text and "access-token query string" in changes_text and "map API cache" in changes_text and "Instagram pagination URLs" in changes_text and "template-facing Glass URL" in changes_text and "embedded credentials or fragments" in changes_text and "empty Picasa feed" in changes_text and "malformed Picasa album entries" in changes_text and "protocol-relative template asset URLs" in changes_text,
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
    picasa_entry_shape_plan_text = PICASA_ENTRY_SHAPE_PLAN.read_text(encoding="utf-8") if PICASA_ENTRY_SHAPE_PLAN.exists() else ""
    require("status: completed" in picasa_entry_shape_plan_text,
            "Picasa entry shape plan must be marked completed",
            failures)
    require("status: completed" in ci_characterization_plan_text,
            "CI and characterization plan must be marked completed",
            failures)
    require("status: completed" in template_image_dom_plan_text and "Mutations restoring HTML concatenation or removing token encoding must fail" in template_image_dom_plan_text,
            "Template image DOM safety plan must record completed mutation verification",
            failures)
    require("status: completed" in outbound_timeout_plan_text and "10-second timeout" in outbound_timeout_plan_text and "direct provider `urllib2.urlopen` call" in outbound_timeout_plan_text,
            "Outbound HTTP timeout plan must record the completed deadline and mutation contract",
            failures)
    require("status: completed" in provider_response_limit_plan_text and "1 MiB" in provider_response_limit_plan_text and "extra-byte read" in provider_response_limit_plan_text,
            "Provider response-size plan must record the completed memory and mutation contract",
            failures)
    require("status: completed" in ci_security_plan_text and "persist-credentials: false" in ci_security_plan_text and "duplicate" in ci_security_plan_text,
            "CI least-privilege plan must record the completed credential and duplicate-key mutation contract",
            failures)

    python_paths = sorted(ROOT.glob("*.py")) + sorted((ROOT / "tests").glob("*.py")) + [ROOT / "scripts/check-baseline.py"]
    for path in python_paths:
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
