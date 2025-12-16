#!/bin/bash
# Script to serve Jekyll site locally using the local theme gem
# This avoids SSL certificate issues with remote_theme

cd "$(dirname "$0")"
eval "$(rbenv init - zsh)"
bundle exec jekyll serve --config _config.yml,_config_local.yml --host 0.0.0.0

