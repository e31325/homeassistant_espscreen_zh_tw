Tessera screens-v0.4.97 - Traditional Chinese entity-name patch

Purpose
- Keep the Tessera UI language as English (LANGUAGE: en).
- Allow common Traditional Chinese Home Assistant entity/friendly names to pass the add-on text filter.
- Include a subsetted Noto Sans CJK TC font in the five main LVGL text fonts.

Files changed from the v0.4.97 source:
- packages/core.yaml
- screen_manager/app/header_bar.py
- fonts/NotoSansTC-Tessera.ttf (subset font)

Important limitations
- This patch includes a curated set of common Traditional Chinese glyphs, not the entire Big5 or CJK repertoire.
- If a name contains a missing character, it must be added to SCRIPT_GLYPHS_HAN and the font subset regenerated.
- This source ZIP is not a precompiled ESPHome firmware. It must be published to a GitHub repository and selected by the screen's ESPHome package URL/ref so ESPHome fetches the modified package and fonts.
- The add-on code (header_bar.py) must also run from this modified repository/version. Merely changing the ESPHome YAML package URL does not update an already-installed Screen Manager add-on's Python code. Follow the installation instructions supplied separately; do not flash until the add-on and firmware point to the same patched source.
- No physical Waveshare 7B compile/OTA test has been performed in this environment.
