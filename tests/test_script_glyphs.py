"""The letters of a language written in another script (docs/TRANSLATING.md, "Letters"): only a screen built in such a
language carries them in its five text fonts, and the app keeps them only in what it sends to such a screen.

- packages/core.yaml has one list per script (SCRIPT_GLYPHS_CYRILLIC) and SCRIPT_GLYPHS picks it by LANGUAGE; the text
  fonts end on "${SCRIPT_GLYPHS}", empty for every other language, so no other screen spends flash on them.
- header_bar.SCRIPT_GLYPHS has the same letters, and clean_text keeps them for a screen whose language's `_meta.script`
  names that script; every other screen gets them dropped, as before.
- The languages SCRIPT_GLYPHS takes are exactly the translation files that say `"script": "cyrillic"`.
"""
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'screen_manager/app'))
import profiles  # noqa: E402
import header_bar  # noqa: E402
import i18n  # noqa: E402

CORE = (ROOT / 'packages/core.yaml').read_text(encoding='utf-8')
TEXT_FONTS = ('headline', 'watch_value', 'label', 'sublabel', 'sublabel_big')


def core_list(script):
    return re.search(r'(?m)^  SCRIPT_GLYPHS_' + script.upper() + r': "([^"]*)"', CORE).group(1)


class FirmwareLetters(unittest.TestCase):
    def test_the_app_and_the_firmware_name_the_same_letters(self):
        for script in ('cyrillic', 'han'):
            self.assertEqual(set(core_list(script)), set(header_bar.SCRIPT_GLYPHS[script]))
            self.assertEqual(len(core_list(script)), len(set(core_list(script))), 'a letter twice')
            self.assertFalse(set(core_list(script)) & set(header_bar.GLYPHS))

    def test_every_text_font_takes_the_letters_of_its_language_last(self):
        for font in TEXT_FONTS:
            start = CORE.index('    id: ' + font + '\n')
            glyphs = CORE[CORE.index('    glyphs: [', start):]
            glyphs = glyphs[:glyphs.index(']\n') + 1]
            self.assertTrue(glyphs.endswith('"${SCRIPT_GLYPHS}"]'), font)

    def test_the_letters_go_only_into_a_screen_built_in_such_a_language(self):
        expression = re.search(r"(?m)^  SCRIPT_GLYPHS: '(.*)'$", CORE).group(1)
        for language, carried in (('en', ''), ('nl', ''), ('pt-BR', ''), ('ru', core_list('cyrillic')), ('zh-TW', core_list('han'))):
            with self.subTest(language=language):
                values = {'LANGUAGE': language, 'SCRIPT_GLYPHS_CYRILLIC': core_list('cyrillic'), 'SCRIPT_GLYPHS_HAN': core_list('han')}
                self.assertEqual(profiles.resolve(expression, values), carried)

    def test_the_languages_it_takes_are_the_cyrillic_translation_files(self):
        named = set(re.findall(r'"([a-z]{2,3})"', re.search(r'(?m)^  SCRIPT_GLYPHS: (.*)$', CORE).group(1)))
        files = {path.stem.split('-')[0] for path in (ROOT / 'screen_manager/translations').glob('*.json')
                 if json.loads(path.read_text(encoding='utf-8')).get('_meta', {}).get('script') in {'cyrillic', 'han'}}
        self.assertEqual(named, files)


class AppLetters(unittest.TestCase):
    def tearDown(self):
        i18n.SCREEN.set(None)

    def test_a_russian_screen_keeps_its_letters_and_any_other_drops_them(self):
        i18n.SCREEN.set({'language': 'ru', 'legacy': False})
        self.assertEqual(i18n.screen_script(), 'cyrillic')
        self.assertEqual(header_bar.clean_text('Кухня, свет 2'), 'Кухня, свет 2')
        i18n.SCREEN.set({'language': 'nl', 'legacy': False})
        self.assertEqual(i18n.screen_script(), 'latin')
        self.assertEqual(header_bar.clean_text('Свет 2'), '2')
        # Firmware from before the languages draws the old letters only, whatever the language.
        i18n.SCREEN.set({'language': 'ru', 'legacy': True})
        self.assertEqual(header_bar.clean_text('Кухня'), '')

    def test_a_traditional_chinese_screen_keeps_han_characters(self):
        i18n.SCREEN.set({'language': 'zh-TW', 'legacy': False})
        self.assertEqual(i18n.screen_script(), 'han')
        self.assertEqual(header_bar.clean_text('設定亮度'), '設定亮度')


if __name__ == '__main__':
    unittest.main()
