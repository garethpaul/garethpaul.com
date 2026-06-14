#!/usr/bin/env python3
import re
import sys
from pathlib import Path


if len(sys.argv) != 5:
    raise SystemExit("usage: check-provider-json-media.py BASE INSTAGRAM TEST PLAN")

base = Path(sys.argv[1]).read_text()
instagram = Path(sys.argv[2]).read_text()
tests = Path(sys.argv[3]).read_text()
plan = Path(sys.argv[4]).read_text()

helper_start = base.find("def is_json_response(response):")
helper_end = base.find("\ndef read_url", helper_start)
if helper_start < 0 or helper_end < 0:
    raise SystemExit("Shared provider JSON media validator must remain defined before read_url.")
helper = base[helper_start:helper_end]
helper_required = (
    'hasattr(headers, "get_content_type")',
    'hasattr(headers, "gettype")',
    'media_type == "application/json"',
    'media_type.startswith("application/")',
    'media_type.endswith("+json")',
    'len(media_type) > len("application/+json")',
)
if any(helper.count(fragment) != 1 for fragment in helper_required):
    raise SystemExit("Provider JSON media validation must preserve the standard and vendor JSON allowlist.")

read_start = base.find("def read_url(url_or_request, expected_json=False):")
read_end = base.find("\ndef decode_json_object", read_start)
if read_start < 0 or read_end < 0:
    raise SystemExit("Bounded provider reads must retain the optional JSON media boundary.")
read_body = base[read_start:read_end]
contract = (
    "if expected_json and not is_json_response(response):",
    'raise ValueError("Provider response media type is not JSON")',
    "response.read(MAX_PROVIDER_RESPONSE_BYTES + 1)",
)
positions = [read_body.find(fragment) for fragment in contract]
if any(read_body.count(fragment) != 1 for fragment in contract) or positions != sorted(positions):
    raise SystemExit("Provider JSON media validation must reject before the bounded body read.")

if base.count("decode_json_object(read_url(url_or_request, expected_json=True))") != 1:
    raise SystemExit("Shared provider JSON-object reads must opt into media validation exactly once.")
if instagram.count("read_url(request, expected_json=True)") != 1:
    raise SystemExit("Instagram JSON reads must opt into media validation exactly once.")

required_tests = (
    "test_json_response_media_types_accept_standard_and_vendor_json",
    "test_read_url_rejects_non_json_media_before_read_and_closes_response",
    "test_read_url_preserves_generic_non_json_reads",
    "self.assertEqual([], response.read_sizes)",
    "self.assertTrue(captured[0][1])",
)
if any(tests.count(fragment) != 1 for fragment in required_tests):
    raise SystemExit("Provider JSON media regression coverage must remain executable and unique.")

frontmatter = plan.split("---", 2)[1]
statuses = re.findall(r"^status: .+$", frontmatter, flags=re.MULTILINE)
verification = plan.split("## Verification Completed\n", 1)[-1]
required_evidence = (
    "focused provider media tests passed",
    "seven hostile mutations were rejected",
    "external-directory Make gate passed",
    "No credentialed App Engine",
)
if (
    statuses != ["status: completed"]
    or "## Verification Completed\n" not in plan
    or any(item not in verification for item in required_evidence)
    or re.search(r"\b(?:pending|todo|tbd|not run|not yet)\b", verification, re.IGNORECASE)
):
    raise SystemExit("Provider JSON media plan must record completed status and actual verification.")

print("Provider JSON media type contract passed.")
