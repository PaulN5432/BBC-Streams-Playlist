import requests
import time
import os

# Output directory
os.makedirs("output", exist_ok=True)

# Step 1: Fetch BBC channels list dynamically
channels_index_url = "https://open.live.bbc.co.uk/mediaselector/6/ps/version/2.0/mediaset/pc/format/json/cors/1"
response = requests.get(channels_index_url)
channels_data = response.json()

# Extract channels as tuples (channel_name, vpid)
channels = []
for item in channels_data.get("media", []):
    vpid = item.get("vpid")
    title = item.get("title")
    if vpid and title:
        channels.append((title, vpid))

print(f"Found {len(channels)} channels")

# Prepare outputs
m3u_entries = ["#EXTM3U"]
text_entries = []

# Step 2: Loop through channels and get stream URLs
for title, vpid in channels:
    url = f"https://open.live.bbc.co.uk/mediaselector/6/select/version/2.0/mediaset/pc/vpid/{vpid}/format/json/cors/1"
    stream_url = None
    retries = 3
    while retries > 0:
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
            versions = data.get("media", {}).get("versions", [])
            if not versions:
                raise ValueError("No versions found")
            
            # Prefer HD streams
            for v in versions:
                if v.get("format") == "hls" and "hd" in v.get("title", "").lower():
                    stream_url = v.get("url")
                    break
            
            # If no HD, take first HLS
            if not stream_url:
                for v in versions:
                    if v.get("format") == "hls":
                        stream_url = v.get("url")
                        break
            
            if stream_url:
                m3u_entries.append(f"#EXTINF:-1,{title}")
                m3u_entries.append(stream_url)
                text_entries.append(f"{title} -> {stream_url}")
                print(f"Added {title}")
            else:
                print(f"No valid stream for {title}")
            break  # exit retry loop
        except Exception as e:
            retries -= 1
            print(f"Failed {title}, retries left {retries}. Error: {e}")
            time.sleep(2)

# Step 3: Save outputs
with open("output/bbc_channels.m3u", "w") as f:
    f.write("\n".join(m3u_entries))

with open("output/bbc_channels.txt", "w") as f:
    f.write("\n".join(text_entries))

print("Files saved in output/: bbc_channels.m3u and bbc_channels.txt")
