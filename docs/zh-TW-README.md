# 繁體中文（zh-TW）試作支援

本分支加入 zh-TW 翻譯檔、Han 字元過濾，以及 Noto Sans CJK TC 子集字型。字型只包含本翻譯檔使用字元及一組常用繁體中文字，避免將完整 CJK 字型塞入 ESP32-S3 韌體。

## 目前狀態

- 螢幕 `screen`：已翻譯常用操作、狀態、設定、燈光、冷氣、掃地機器人及日期文字；未涵蓋的字串仍會沿用英文。
- 附加元件 `addon` 與編輯器 `editor`：目前保留英文原文，尚未完成整套繁體中文翻譯。
- `_meta.checked` 保持 `false`，這是未經完整母語校對的試作，不應視為正式完整翻譯。
- 字型目前含 606 個 Han 字元；使用者自訂名稱若出現清單外漢字，會被過濾。

## 7B 使用

編譯此分支時將螢幕語言設為 `zh-TW`。需使用支援 ESP32-S3 7B 的 Tessera 7B profile，不能拿一般 Waveshare 7 吋設定檔替代。更新前請備份目前可正常啟動的韌體與設定。

## 加入更多中文字

將缺少字元加入 `packages/core.yaml` 的 `SCRIPT_GLYPHS_HAN`，並同步加入 `screen_manager/app/header_bar.py` 的 `SCRIPT_GLYPHS['han']`；重新以 Noto Sans CJK TC 子集化 `fonts/NotoSansTC-Tessera.ttf`，確保三處字元集合一致。
