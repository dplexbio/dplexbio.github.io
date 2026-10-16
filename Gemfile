source "https://rubygems.org"

# Pins Jekyll and plugins to the versions GitHub Pages uses in production.
gem "github-pages", group: :jekyll_plugins

# Windows does not ship timezone data or a native file watcher.
platforms :windows, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end
gem "wdm", "~> 0.1", platforms: [:windows]

# Ruby 3.x no longer bundles webrick, which `jekyll serve` needs.
gem "webrick", "~> 1.8"

# Silences a warning from the github-pages metadata plugin.
gem "faraday-retry"
