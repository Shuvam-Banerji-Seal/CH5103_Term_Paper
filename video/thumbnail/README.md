# Thumbnail

`ch5103-thumbnail.jpg` (and `.png`): the YouTube thumbnail, 1280×720.

* **Art:** `site/img/hero.webp`, made with OpenAI's `gpt-image-2.5-sunburst-2026-09-08` for the website (two orbital lobes,
  gold and teal, with opposite spin arrows). The image model is used only for decorative art, never for diagrams.
* **Text:** set in `thumbnail.html` with the video's own fonts (TeX Gyre Chorus, Libertinus Serif Bold, EB Garamond) and
  palette, so every word is exact; it stays legible down to 168×94 (YouTube's smallest list size). The bottom-right
  corner is left to YouTube's duration badge.

Render:

```sh
cd video/thumbnail
chromium --headless=new --hide-scrollbars --allow-file-access-from-files --force-device-scale-factor=1 \
  --window-size=1280,720 --virtual-time-budget=4000 --screenshot=$PWD/ch5103-thumbnail.png "file://$PWD/thumbnail.html"
magick ch5103-thumbnail.png -quality 92 ch5103-thumbnail.jpg
```

New art was also prompted (October 2026) but not generated: the API account had no credits left. The three prompts
(`video/build/thumbnail/req_{a,b,c}.json`, 1536×1024, right-hand composition with the left 55% empty for the title)
can be sent to `POST /v1/images/generations` with the key in `.env`, and the result swapped in for `hero.webp`.
