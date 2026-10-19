# DPlexBio Company Landing Page

Digital PCR powered by Artificial Intelligence

Email info@dplexbio.com

## Site structure

The site is a single landing page, `index.html`, built with Jekyll:

- `_layouts/onepage.html`: page shell (head, fonts, CSS/JS links)
- `assets/css/onepage.css`, `assets/js/onepage.js`: styles and behaviour
- `assets/images/onepage/`: page images; `_includes/onepage/`: inline SVG figures
- `assets/DPB-Tech-explainer.mp4`: overview video (encoded with faststart so it begins playing quickly)
- `index3.html`: redirect stub that forwards the old preview URL to `/`

## Local preview

Requires Ruby with DevKit (Windows: `winget install RubyInstallerTeam.RubyWithDevKit.3.3`).

```
bundle install
bundle exec jekyll serve --livereload
```

Then open http://localhost:4000. The `github-pages` gem keeps Jekyll and its plugins at the versions GitHub Pages uses.
