# BBC Streams Playlist

This repository dynamically generates a weekly updated playlist of BBC live streams in **M3U** and **plain text** formats.

## Files

- `output/bbc_channels.m3u` – Playlist ready for VLC, Kodi, or other media players.
- `output/bbc_channels.txt` – Simple text file: `Channel Name -> Stream URL`.

## How it Works

- `fetch_streams.py` fetches BBC channel data and stream URLs automatically.
- Streams are selected with preference for **HD HLS streams**.
- The GitHub Actions workflow updates the playlist **every week** (Sunday UTC) and pushes updates to the repository.

## Usage

1. Clone the repo:
```bash
git clone https://github.com/<your-username>/bbc-streams.git
cd bbc-streams
