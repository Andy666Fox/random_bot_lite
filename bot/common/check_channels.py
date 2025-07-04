import requests
import json
from time import sleep
import string
import argparse
from tqdm import tqdm


#cd ./random_bot_lite/bot
#uv run python common/check_channels.py -p ../raw_data/raw_channels.json -l 1000 -r 1020
def load_channles(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def check_channels_exists(channel_key):
    url = f"https://t.me/{channel_key}"

    try:
        response = requests.get(url, timeout=10)

        print(response.status_code)
        if 'class="tgme_page_context_link"' in response.text.lower():
            return True
        return False

    except requests.exceptions.RequestException as e:
        print(f"Failed check for {channel_key}: {e}")
        return False


def clean_channels(filename, l, r):
    channels = load_channles(filename)
    print(f"Validate from {l} to {r}")
    valid_channels = {}
    for channel_key in tqdm(list(channels.keys())[l:r]):
        print(f"Check for {channel_key}...")
        if len(channel_key) > 32:
            print(f"To much long name, refund: {channel_key}")
        elif channel_key[0] in string.digits + string.punctuation:
            print(f"Channel can start only with letters, refund: {channel_key}")
        elif channel_key.count("_") > 1:
            print(f"Much than one underscore, refund: {channel_key}")
        elif check_channels_exists(channel_key):
            valid_channels[channel_key] = 1
            print(f"Channel exists!, adding: {channel_key}")
            sleep(0.05)
        else:
            print(f"Channel does not exist, refund: {channel_key}")

    with open(f"validated_channels/{l}_{r}_check.json", "w", encoding="utf-8") as f:
        json.dump(valid_channels, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate tg channels")
    parser.add_argument("-p", "--path", required=False, help="path to validated json")
    parser.add_argument("-l", "--left", required=False, help="left bound")
    parser.add_argument("-r", "--right", required=False, help="right bound")
    args = parser.parse_args()
    clean_channels(str(args.path), int(args.left), int(args.right))
