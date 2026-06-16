#!/usr/bin/env python3
from pathlib import Path
import py_compile
import re
import subprocess
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
PROVIDER_JSON_OBJECT_PLAN = ROOT / "docs/plans/2026-06-13-provider-json-object-shape.md"
PICASA_FEED_SHAPE_PLAN = ROOT / "docs/plans/2026-06-13-picasa-feed-container-shape.md"
INSTAGRAM_CONTAINER_SHAPE_PLAN = ROOT / "docs/plans/2026-06-13-instagram-container-shape.md"
LOCATION_INDEPENDENT_MAKE_PLAN = ROOT / "docs/plans/2026-06-13-location-independent-make.md"
PROVIDER_REDIRECT_PLAN = ROOT / "docs/plans/2026-06-14-provider-redirect-boundary.md"
PROVIDER_JSON_MEDIA_PLAN = ROOT / "docs/plans/2026-06-14-provider-json-media-type-boundary.md"
PROVIDER_JSON_MEDIA_CHECK = ROOT / "scripts/check-provider-json-media.py"
PYTHON_PREFLIGHT_PLAN = ROOT / "docs/plans/2026-06-16-python-verification-preflight.md"
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
        "scripts/check-provider-json-media.py",
        "scripts/check-python3.sh",
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
        "docs/plans/2026-06-13-provider-json-object-shape.md",
        "docs/plans/2026-06-13-picasa-feed-container-shape.md",
        "docs/plans/2026-06-13-instagram-container-shape.md",
        "docs/plans/2026-06-13-location-independent-make.md",
        "docs/plans/2026-06-14-provider-redirect-boundary.md",
        "docs/plans/2026-06-14-provider-json-media-type-boundary.md",
        "docs/plans/2026-06-16-python-verification-preflight.md",
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
    security_text = read("SECURITY.md")
    vision_text = read("VISION.md")
    changes_text = read("CHANGES.md")
    agents_text = read("AGENTS.md")
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
    provider_json_object_plan_text = PROVIDER_JSON_OBJECT_PLAN.read_text(encoding="utf-8") if PROVIDER_JSON_OBJECT_PLAN.exists() else ""
    picasa_feed_shape_plan_text = PICASA_FEED_SHAPE_PLAN.read_text(encoding="utf-8") if PICASA_FEED_SHAPE_PLAN.exists() else ""
    instagram_container_shape_plan_text = INSTAGRAM_CONTAINER_SHAPE_PLAN.read_text(encoding="utf-8") if INSTAGRAM_CONTAINER_SHAPE_PLAN.exists() else ""
    location_independent_make_plan_text = LOCATION_INDEPENDENT_MAKE_PLAN.read_text(encoding="utf-8") if LOCATION_INDEPENDENT_MAKE_PLAN.exists() else ""
    provider_redirect_plan_text = PROVIDER_REDIRECT_PLAN.read_text(encoding="utf-8") if PROVIDER_REDIRECT_PLAN.exists() else ""
    python_preflight_plan_text = PYTHON_PREFLIGHT_PLAN.read_text(encoding="utf-8") if PYTHON_PREFLIGHT_PLAN.exists() else ""
    python_preflight_text = read("scripts/check-python3.sh")
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
    require(".PHONY: build check lint test" in makefile_text
            and "lint build: check" in makefile_text
            and 'ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))' in makefile_text
            and "PYTHON ?= python3" in makefile_text
            and makefile_text.count('PYTHON="$(PYTHON)" "$(ROOT)/scripts/check-python3.sh"') == 2
            and 'cd "$(ROOT)" && "$(PYTHON)" scripts/check-baseline.py' in makefile_text
            and makefile_text.count('cd "$(ROOT)" && "$(PYTHON)" -m unittest discover -s tests') == 2,
            "Makefile must expose lint, test, build, and check gate targets with characterization tests",
            failures)
    require(
        'PYTHON=${PYTHON:-python3}' in python_preflight_text
        and 'command -v "$PYTHON"' in python_preflight_text
        and 'sys.stdout.write(str(sys.version_info[0]))' in python_preflight_text
        and 'if [ "$python_major" != "3" ]; then' in python_preflight_text
        and "Python 3 command not found:" in python_preflight_text
        and "Verification requires Python 3:" in python_preflight_text,
        "Python verification must fail fast through the shared Python 3 preflight",
        failures,
    )
    python_preflight_guidance = (
        "Offline verification uses one explicit, fail-fast Python 3 command while the "
        "deployment remains Python 2."
    )
    require(
        all(
            python_preflight_guidance in re.sub(r"\s+", " ", text)
            for text in (readme_text, agents_text, vision_text, changes_text)
        ),
        "Project guidance must distinguish the Python 3 verification command from the Python 2 deployment runtime",
        failures,
    )
    require(
        "## Status: Completed" in python_preflight_plan_text
        and "repository root and external working directory" in python_preflight_plan_text
        and "explicit compatible Python command override" in python_preflight_plan_text
        and "missing-command and non-Python-3 preflights" in python_preflight_plan_text
        and "hostile mutations were rejected" in python_preflight_plan_text,
        "Python verification preflight plan must record completed status and actual verification",
        failures,
    )
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
    require("HTTP_TIMEOUT_SECONDS = 10" in base_source
            and "class RejectRedirectHandler(urllib2.HTTPRedirectHandler):" in base_source
            and "def redirect_request(self, req, fp, code, msg, headers, newurl):" in base_source
            and "    return None" in base_source
            and "PROVIDER_OPENER = urllib2.build_opener(RejectRedirectHandler())" in base_source
            and "def open_url(url_or_request):" in base_source
            and "PROVIDER_OPENER.open(url_or_request, timeout=HTTP_TIMEOUT_SECONDS)" in base_source,
            "base.py must enforce the shared no-redirect opener and 10-second provider timeout",
            failures)
    require("MAX_PROVIDER_RESPONSE_BYTES = 1024 * 1024" in base_source and "def read_url(url_or_request, expected_json=False):" in base_source and "response.read(MAX_PROVIDER_RESPONSE_BYTES + 1)" in base_source and "response.close()" in base_source and "len(payload) > MAX_PROVIDER_RESPONSE_BYTES" in base_source,
            "base.py must bound and close provider response bodies before JSON decoding",
            failures)
    provider_sources = [glass_source, instagram_source, map_source, picasa_source]
    require(all("urllib2.urlopen(" not in source for source in provider_sources),
            "provider handlers must not bypass base.open_url with direct urllib2.urlopen calls",
            failures)
    require("urllib2.urlopen(" not in base_source,
            "base.py must not bypass the no-redirect provider opener",
            failures)
    require("def decode_json_object(payload):" in base_source and "json.loads(payload)" in base_source and "isinstance(payload, dict)" in base_source and "def read_json_object(url_or_request):" in base_source and "decode_json_object(read_url(url_or_request, expected_json=True))" in base_source,
            "base.py must decode provider JSON through one top-level object guard",
            failures)
    require("decode_json_object(instagram_request(url))" in instagram_source
            and all("read_json_object(" in source for source in [glass_source, map_source, picasa_source]),
            "every provider handler must route JSON decoding through the shared object guard",
            failures)
    require(all("json.loads(" not in source for source in provider_sources),
            "provider handlers must not bypass the shared JSON object decoder",
            failures)
    require(all(".read()" not in source for source in provider_sources),
            "provider handlers must not perform unbounded response reads",
            failures)
    require("def instagram_page(data):" in instagram_source
            and "isinstance(pagination, dict)" in instagram_source
            and "isinstance(media, list)" in instagram_source
            and instagram_source.count("instagram_page(") == 3
            and "next_url, d = instagram_page(data)" in instagram_source
            and "_, second_page = instagram_page(data_2)" in instagram_source,
            "instagram.py must normalize both pages before pagination and media concatenation",
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
    require("def picasa_entries(data):" in picasa_source
            and "isinstance(feed, dict)" in picasa_source
            and "isinstance(entries, list)" in picasa_source
            and "entries = picasa_entries(data)" in picasa_source,
            "picasa.py must normalize malformed feed and entry containers before iteration",
            failures)
    require("def picasa_entry_src" in picasa_source and "isinstance(entry, dict)" in picasa_source and "isinstance(content, dict)" in picasa_source,
            "picasa.py must parse album entry image sources through a shape guard",
            failures)
    require("img_src = picasa_entry_src(i)" in picasa_source and "if img_src:" in picasa_source,
            "picasa.py must skip malformed Picasa entries instead of raising",
            failures)
    require("base.require_https_url" in integration_guard_tests and "base.open_url" in integration_guard_tests and "base.HTTP_TIMEOUT_SECONDS" in integration_guard_tests and "base.PROVIDER_OPENER" in integration_guard_tests and "base.RejectRedirectHandler" in integration_guard_tests and "test_redirect_handler_refuses_redirect_request_creation" in integration_guard_tests and "test_provider_opener_installs_one_redirect_rejection_handler" in integration_guard_tests and "base.read_url" in integration_guard_tests and "base.MAX_PROVIDER_RESPONSE_BYTES" in integration_guard_tests and "response.closed" in integration_guard_tests and "instagram.instagram_request" in integration_guard_tests and "picasa.picasa_entries" in integration_guard_tests and "picasa.picasa_entry_src" in integration_guard_tests,
            "integration characterization tests must exercise private URL, redirect, timeout, response-size, Instagram, and Picasa guards",
            failures)
    require("test_picasa_entries_returns_expected_entry_list" in integration_guard_tests
            and "test_picasa_entries_ignores_malformed_feed_containers" in integration_guard_tests,
            "integration characterization tests must cover valid and malformed Picasa feed containers",
            failures)
    require("test_instagram_page_returns_expected_pagination_and_media" in integration_guard_tests
            and "test_instagram_page_ignores_malformed_containers" in integration_guard_tests
            and "instagram.instagram_page" in integration_guard_tests,
            "integration characterization tests must cover valid and malformed Instagram containers",
            failures)
    require("test_read_json_object_accepts_object_payload" in integration_guard_tests and "test_read_json_object_rejects_malformed_json" in integration_guard_tests and "test_read_json_object_rejects_non_object_json" in integration_guard_tests and "b'[]'" in integration_guard_tests and "b'null'" in integration_guard_tests,
            "integration characterization tests must cover accepted objects, malformed JSON, and non-object JSON values",
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
    require("Malformed Picasa `feed` objects" in readme_text and "non-list `feed.entry` values" in readme_text,
            "README must document the Picasa feed-container shape guard",
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
    require("Malformed Instagram pagination objects" in readme_text and "non-list media containers" in readme_text,
            "README must document the Instagram container-shape guard",
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
    require("Malformed Picasa feed objects" in vision_text and "non-list entry containers" in vision_text,
            "VISION must describe the Picasa feed-container shape guard",
            failures)
    require("Picasa feed containers should be type-checked" in security_text
            and "Normalize malformed Picasa feed objects" in agents_text
            and "Normalized malformed Picasa feed objects" in changes_text,
            "Project guidance must document the Picasa feed-container shape guard",
            failures)
    require("External template assets" in vision_text and "explicit HTTPS URLs" in vision_text,
            "VISION must describe the template external asset HTTPS guard",
            failures)
    require("Instagram pagination host" in vision_text and "https://api.instagram.com" in vision_text,
            "VISION must describe the Instagram pagination host guard",
            failures)
    require("Malformed Instagram pagination objects" in vision_text and "non-list media containers" in vision_text,
            "VISION must describe the Instagram container-shape guard",
            failures)
    require("Instagram pagination and media containers should be type-checked" in security_text
            and "Normalize malformed Instagram pagination and media containers" in agents_text
            and "Normalized malformed Instagram pagination and media containers" in changes_text,
            "Project guidance must document the Instagram container-shape guard",
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
    provider_response_statuses = re.findall(
        r"^status: .+$", provider_response_limit_plan_text, flags=re.MULTILINE
    )
    provider_response_sections = provider_response_limit_plan_text.split(
        "## Verification Completed\n", 1
    )
    provider_response_verification = (
        provider_response_sections[1] if len(provider_response_sections) == 2 else ""
    )
    provider_response_required_evidence = (
        "All four Make gates, 13 characterization tests",
        "push run `27393292065`",
        "pull-request run `27393296845`",
        "push run `27393311075`",
        "CodeQL run `27402321576`",
        "Mutations removing the extra-byte read",
    )
    require(provider_response_statuses == ["status: completed"]
            and all(item in provider_response_verification for item in provider_response_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", provider_response_verification, re.IGNORECASE) is None,
            "Provider response-size plan must record completed status and actual verification",
            failures)
    require("status: completed" in ci_security_plan_text and "persist-credentials: false" in ci_security_plan_text and "duplicate" in ci_security_plan_text,
            "CI least-privilege plan must record the completed credential and duplicate-key mutation contract",
            failures)
    provider_json_statuses = re.findall(
        r"^status: .+$", provider_json_object_plan_text, flags=re.MULTILINE
    )
    provider_json_sections = provider_json_object_plan_text.split(
        "## Verification Completed\n", 1
    )
    provider_json_verification = (
        provider_json_sections[1] if len(provider_json_sections) == 2 else ""
    )
    provider_json_required_evidence = (
        "All four Make gates and all 16 characterization tests passed",
        "Python 3 and Python 2 compilation passed",
        "non-object JSON mutation failed",
        "direct provider `json.loads` mutation failed",
        "removed non-object test-contract mutation failed",
        "hosted pull-request and CodeQL snapshot",
    )
    require(provider_json_statuses == ["status: completed"]
            and all(item in provider_json_verification for item in provider_json_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", provider_json_verification, re.IGNORECASE) is None,
            "Provider JSON object-shape plan must record completed status and actual verification",
            failures)
    picasa_feed_statuses = re.findall(
        r"^status: .+$", picasa_feed_shape_plan_text, flags=re.MULTILINE
    )
    picasa_feed_sections = picasa_feed_shape_plan_text.split(
        "## Verification Completed\n", 1
    )
    picasa_feed_verification = (
        picasa_feed_sections[1] if len(picasa_feed_sections) == 2 else ""
    )
    picasa_feed_required_evidence = (
        "focused and all characterization tests passed",
        "All four Make gates passed",
        "feed-type guard mutation failed",
        "entry-list guard mutation failed",
        "handler bypass mutation failed",
        "hosted push, pull-request, and CodeQL snapshot",
    )
    require(picasa_feed_statuses == ["status: completed"]
            and all(item in picasa_feed_verification for item in picasa_feed_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", picasa_feed_verification, re.IGNORECASE) is None,
            "Picasa feed-container plan must record completed status and actual verification",
            failures)
    instagram_container_statuses = re.findall(
        r"^status: .+$", instagram_container_shape_plan_text, flags=re.MULTILINE
    )
    instagram_container_sections = instagram_container_shape_plan_text.split(
        "## Verification Completed\n", 1
    )
    instagram_container_verification = (
        instagram_container_sections[1] if len(instagram_container_sections) == 2 else ""
    )
    instagram_container_required_evidence = (
        "focused and all characterization tests passed",
        "All four Make gates passed",
        "pagination-object guard mutation failed",
        "media-list guard mutation failed",
        "second-page helper bypass mutation failed",
        "hosted push, pull-request, and code-scanning snapshot",
    )
    require(instagram_container_statuses == ["status: completed"]
            and all(item in instagram_container_verification for item in instagram_container_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", instagram_container_verification, re.IGNORECASE) is None,
            "Instagram container-shape plan must record completed status and actual verification",
            failures)
    location_independent_make_statuses = re.findall(
        r"^status: .+$", location_independent_make_plan_text, flags=re.MULTILINE
    )
    location_independent_make_sections = location_independent_make_plan_text.split(
        "## Verification Completed\n", 1
    )
    location_independent_make_verification = (
        location_independent_make_sections[1]
        if len(location_independent_make_sections) == 2
        else ""
    )
    location_independent_make_required_evidence = (
        "20 tests",
        "All four Make gates",
        "from /tmp",
        "root-derivation mutation failed",
        "checker-command mutation failed",
        "unittest-command mutation failed",
        "plan-status mutation failed",
        "plan-evidence mutation failed",
        "documentation mutation failed",
    )
    require(location_independent_make_statuses == ["status: completed"]
            and all(item in location_independent_make_verification for item in location_independent_make_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", location_independent_make_verification, re.IGNORECASE) is None,
            "Location-independent Make plan must record completed status and actual verification",
            failures)
    require("absolute Makefile path" in readme_text
            and "Made legacy API verification independent" in changes_text,
            "README and CHANGES must document location-independent Make verification",
            failures)
    provider_redirect_statuses = re.findall(
        r"^status: .+$", provider_redirect_plan_text, flags=re.MULTILINE
    )
    provider_redirect_sections = provider_redirect_plan_text.split(
        "## Verification Completed\n", 1
    )
    provider_redirect_verification = (
        provider_redirect_sections[1] if len(provider_redirect_sections) == 2 else ""
    )
    provider_redirect_required_evidence = (
        "focused and complete characterization tests passed",
        "Python 2 production-module compilation passed",
        "All four Make gates passed",
        "direct urlopen mutation failed",
        "redirect-allow mutation failed",
        "per-request opener mutation failed",
        "timeout propagation mutation failed",
        "focused test mutation failed",
        "plan evidence mutation failed",
        "hosted pull-request and code-scanning snapshot",
    )
    require(provider_redirect_statuses == ["status: completed"]
            and all(item in provider_redirect_verification for item in provider_redirect_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run|not yet)\b", provider_redirect_verification, re.IGNORECASE) is None,
            "Provider redirect plan must record completed status and actual verification",
            failures)
    require("automatic provider redirects fail closed" in readme_text
            and "must not follow automatic redirects" in security_text
            and "Refuse automatic provider redirects" in vision_text
            and "Rejected automatic provider redirects" in changes_text
            and "must refuse automatic redirects" in agents_text,
            "Project guidance must document the provider redirect boundary",
            failures)

    media_check = subprocess.run(
        [sys.executable, str(PROVIDER_JSON_MEDIA_CHECK), "base.py", "instagram.py",
         "tests/test_integration_guards.py", str(PROVIDER_JSON_MEDIA_PLAN)],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    require(media_check.returncode == 0,
            media_check.stderr.strip() or "Provider JSON media type contract failed",
            failures)

    python_paths = sorted(ROOT.glob("*.py")) + sorted((ROOT / "tests").glob("*.py")) + [ROOT / "scripts/check-baseline.py", PROVIDER_JSON_MEDIA_CHECK]
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
