import asyncio
import concurrent.futures
import threading
from brotab.api import MultipleMediatorsAPI
from brotab.main import create_clients

def _etherscan_worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        api = MultipleMediatorsAPI(create_clients())
        
        raw_active = api.get_active_tabs([])
        
        active_ids = set()
        for item in raw_active:
            if isinstance(item, list):
                for subitem in item:
                    active_ids.add(subitem)
            else:
                active_ids.add(item)

        all_tabs = api.list_tabs([])
        
        for tab in all_tabs:
            parts = str(tab).split('\t')
            if len(parts) < 3: continue
            
            t_id, t_url = parts[0], parts[2]
            
            if "etherscan.io/" in t_url:
                if t_id in active_ids:
                    return t_url
        return "No tabs found"

    except Exception as e:
        return f"Error: {e}"
    finally:
        loop.close()

def get_active_etherscan_url():
    with  concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(_etherscan_worker)
        return future.result()

