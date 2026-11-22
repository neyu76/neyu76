#!/usr/bin/env bash
# Re-download the Dark Atlas kit zip from Google Drive and restore the heavy media
# (music beds, sfx.wav, sample videos) that are not kept in git.
# Usage (from dark_atlas/):  bash tools/fetch_kit_media.sh
set -euo pipefail
ID="14jO5Kk1QWOZxeb--xqu9vKMYajXqho9m"
DA="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
curl -fL -o "$TMP/kit.zip" "https://drive.usercontent.google.com/download?id=$ID&export=download&confirm=t"
unzip -q "$TMP/kit.zip" -d "$TMP"
K="$TMP/DarkAtlas_US_States_Kit"
# copy only files that are missing locally (never overwrite your edits)
(cd "$K/dark_atlas" && find . -type f) | while read -r f; do
  [ -e "$DA/$f" ] || { mkdir -p "$DA/$(dirname "$f")"; cp "$K/dark_atlas/$f" "$DA/$f"; echo "restored $f"; }
done
mkdir -p "$DA/video_mau"
for f in "$K"/video_mau/*.mp4; do [ -e "$DA/video_mau/$(basename "$f")" ] || cp "$f" "$DA/video_mau/"; done
echo "done"
