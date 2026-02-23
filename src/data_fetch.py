import asyncio
import json
import os
import aiohttp
import polars as pl
from datetime import datetime

BINANCE_WS_URL = "wss://fstream.binance.com/ws/btcusdt@depth20@100ms"
BUFFER_SIZE = 10000
OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

class Data_Fetch:
    def __init__(self):
        self.buffer = []
        self.file_index = 0

    async def flush(self):
        if not self.buffer:
            return

        print("Flushing buffer")

        df = pl.DataFrame(self.buffer)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"btcusdt_{self.file_index}_{timestamp}.parquet"
        filepath = os.path.join(OUTPUT_DIR, filename)

        df.write_parquet(filepath, compression="snappy")
        self.buffer = []
        self.file_index += 1

        print("Flushed buffer")

    async def connect(self):
        print("Connecting to Binance")
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(BINANCE_WS_URL) as ws:
                print("Connected to Binance")
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)

                        row = {
                            "event_time": data["E"],
                            "server_time": data["T"]
                        }

                        for i, ask in enumerate(data["a"]):
                            row[f"ask_{i}_p"] = float(ask[0])
                            row[f"ask_{i}_q"] = float(ask[1])

                        for i, bid in enumerate(data["b"]):
                            row[f"bid_{i}_p"] = float(bid[0])
                            row[f"bid_{i}_q"] = float(bid[1])

                        self.buffer.append(row)

                        if len(self.buffer) > BUFFER_SIZE:
                            await self.flush()
                        #print(bid, ask, event_time)

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print("Connection closed by server")
                        break

    async def run(self):
        while True:
            try:
                await self.connect()
            except Exception as e:
                print("Error connecting to Binance", e, " trying again")
                await asyncio.sleep(5)

if __name__ == '__main__':
    fetch = data_fetch()
    try:
        asyncio.run(fetch.run())
    except KeyboardInterrupt:
        asyncio.run(fetch.flush())

