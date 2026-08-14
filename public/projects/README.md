# Project media

Every file here is a **generated sample** — a mock UI made to look like the real
thing so the portfolio reads properly before you have real captures. Replace them
one by one; keep the filenames and nothing else has to change.

```
public/projects/
  mental-health-ai/   cover.jpg  1.jpg  2.jpg  3.jpg  4.jpg
  frd/                cover.jpg  1.jpg  2.jpg  3.jpg  4.jpg
  skillsync/          cover.jpg  1.jpg  2.jpg  3.jpg  4.jpg
  numenor/            cover.jpg  1.jpg  gameplay.mp4  3.jpg  4.jpg
```

- `cover` is the thumbnail on the portfolio grid card.
- `1–4` are the carousel slides on the project page, in order.
- Any slide can be a video instead of an image — give it an `.mp4`, `.webm` or
  `.mov` filename and it renders as an autoplaying, muted, looping clip.
  `numenor/gameplay.mp4` is the worked example.
- Anything missing falls back to the gradient placeholder, so a half-finished
  folder never shows a broken image.

Recommended for real captures: 16:9 images (1600×900), JPG quality ~80, under
~400 KB each. Videos: H.264 MP4, a few seconds, no audio (they play muted).

To add, remove or rename a slide, edit the `shots` array for that project in
`src/Portfolio.jsx`.

## Regenerating the samples

```
python scripts/generate-sample-media.py            # everything
python scripts/generate-sample-media.py --no-video # stills only, much faster
```

Needs Pillow and OpenCV. The clip is written through OpenCV's H.264 encoder,
which ignores quality settings and encodes at a fixed ~8 Mbps — frame size and
duration are the only levers on file size (currently 854×480 for 4 s ≈ 4 MB).
