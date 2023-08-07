import asyncio
import datetime
import aiohttp
import time
import logging
import os
from Scripts.insertPlants import create_data_object
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY')

# last_plant = 10104
# Set up logging
logging.basicConfig(filename='fetchPlants.log', level=logging.DEBUG)

async def fetch_plant(session, plant_id, token_bucket):
    # variables
    url = f"https://perenual.com/api/species/details/{plant_id}?key={API_KEY}"
    logging.info(f"Fetching plant {plant_id} from URL: {url}")
    try:
        async with token_bucket:
            async with session.get(url) as response:
                plant = await response.json()
                logging.debug(f"Received response code {response.status} for plant {plant_id}")
                create_data_object(plant)
                # print(plant)
                return plant

    except aiohttp.ClientResponseError as e:
        await asyncio.sleep(10)
        logging.debug("Waiting for 10 sec before retrying")
        # fetch_plant(session, plant_id, token_bucket)
    except Exception as e:
        logging.error(
        f"Unhandled exception while fetching plant {plant_id}: {e}")
        print(f"Unhandled exception: {e}")


async def fetch_all_plants():
    logging.info(datetime.datetime.now().strftime("%I:%M %p"))
    logging.info("Fetching all plants")
    plant_id_range = range(1, 10105) #10105
    rate_limit = 700
    token_bucket = TokenBucket(rate_limit, rate_limit)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for plant_id in plant_id_range:
            tasks.append(asyncio.ensure_future(
                fetch_plant(session, plant_id, token_bucket)))
        results = await asyncio.gather(*tasks)
        # print(results)
        return results


class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.monotonic()

    async def __aenter__(self):
        await self.wait_for_tokens(100)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def wait_for_tokens(self, count):
        if count > self.capacity:
            raise ValueError(
                f"Requested tokens ({count}) exceeds bucket capacity ({self.capacity})")
        while self.tokens < count:
            time_to_wait = (count - self.tokens) / self.rate
            await asyncio.sleep(time_to_wait)
            now = time.monotonic()
            elapsed = now - self.last_refill
            refill_amount = int(elapsed * self.rate)
            self.tokens = min(self.capacity, self.tokens + refill_amount)
            self.last_refill = now
        self.tokens -= count


# if __name__ == '__main__':
#     asyncio.run(fetch_all_plants())
    # file = open("10104_plants.json", "a")
    # file.write(str(plants)
