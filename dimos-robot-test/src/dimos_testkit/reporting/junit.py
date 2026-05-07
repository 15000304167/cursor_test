from __future__ import annotations

import os
from typing import Any


def attach_ci_properties() -> dict[str, str]:
    """Key/value metadata merged into session summary (CI can mirror to JUnit properties)."""
    return {
        "TEST_PROFILE": os.environ.get("TEST_PROFILE", ""),
        "GIT_SHA": os.environ.get("GIT_SHA", os.environ.get("GITHUB_SHA", "")),
        "DIMOS_SKIP_STACK": os.environ.get("DIMOS_SKIP_STACK", ""),
    }


def merge_junit_properties_xml_fragment(props: dict[str, Any]) -> str:
    """Optional helper if you post-process junit.xml to inject <properties>."""
    lines = ["<properties>"]
    for k, v in props.items():
        safe_k = str(k).replace("&", "&amp;").replace("<", "&lt;")
        safe_v = str(v).replace("&", "&amp;").replace("<", "&lt;")
        lines.append(f'  <property name="{safe_k}" value="{safe_v}"/>')
    lines.append("</properties>")
    return "\n".join(lines)
