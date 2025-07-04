from crud import insert_channels_from_csv
import asyncio


if __name__ == "__main__":
    result = asyncio.run(insert_channels_from_csv("bot/val_channels.csv"))
    print(result)