import asyncio
import aiohttp
import random 
import matplotlib.pyplot as plt
from urllib.parse import urlencode

async def send_request(session, url, num_requests):
    request_id = random.randint(1, num_requests)
    params = {'id': request_id}
    url_with_params = f"{url}?{urlencode(params)}"
    async with session.get(url_with_params) as response:
        try:
            return await response.json()
        except aiohttp.ContentTypeError:
            text = await response.text()
            print(f"Non-JSON response received: {text}")
            return {"server": -1}

async def experiment_A1(url, num_servers, num_requests):
    server_counts = [0] * num_servers
    error_count = 0
    
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url, num_requests) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)
        
    for response in responses:
        server_index = response['mapped_server']
        if server_index == -1:
            error_count += 1
        else:
            server_counts[server_index] += 1
    
    if error_count > 0:
        print(f"{error_count} requests resulted in non-JSON responses.")
    
    return server_counts

async def experiment_A2(url, max_servers, num_requests_per_run):
    average_loads = []
    
    for num_servers in range(2, max_servers+1):
        server_counts = await experiment_A1(url, num_servers, num_requests_per_run)
        average_load = sum(server_counts) / num_servers
        average_loads.append(average_load)
    
    return average_loads

if __name__ == "__main__":
    base_url = "http://localhost:5000/map_request"  # Replace with your load balancer URL
    num_requests = 10000
    max_servers = 6
    num_requests_per_run = 200
    
    # Experiment A-1
    loop = asyncio.get_event_loop()
    server_counts = loop.run_until_complete(experiment_A1(base_url, 3, num_requests))
    print("Experiment A-1 Results:")
    print("Server Counts:", server_counts)
    
    # Plotting A-1 Results
    plt.bar(range(1, 4), server_counts)
    plt.xlabel('Server Instance')
    plt.ylabel('Request Count')
    plt.title('Load Distribution among Server Instances (Experiment A-1)')
    plt.show()
    
    # Experiment A-2
    # average_loads = loop.run_until_complete(experiment_A2(base_url, max_servers, num_requests_per_run))
    # print("\nExperiment A-2 Results:")
    # print("Average Loads:", average_loads)
    
    # # Plotting A-2 Results
    # plt.plot(range(2, max_servers+1), average_loads, marker='o')
    # plt.xlabel('Number of Server Instances')
    # plt.ylabel('Average Load')
    # plt.title('Scalability of Load Balancer (Experiment A-2)')
    # plt.xticks(range(2, max_servers+1))
    # plt.grid(True)
    # plt.show()
