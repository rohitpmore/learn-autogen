import asyncio


async def simulate_ai_call(model_name:str, delay:float=1.0):
    print(f"Simulating {model_name} call with {delay} second delay")
    await asyncio.sleep(delay)
    print(f"{model_name} call completed")

async def run_sequential_calls():
    print("Starting sequential calls")
    await simulate_ai_call("Model A", 2.0)
    await simulate_ai_call("Model B", 1.5)
    await simulate_ai_call("Model C", 3.0)
    print("All sequential calls completed")

async def run_concurrent_calls():
    print("Starting concurrent calls")
    tasks = [simulate_ai_call("Model A", 2.0), simulate_ai_call("Model B", 1.5), simulate_ai_call("Model C", 3.0)]
    await asyncio.gather(*tasks)
    print("All concurrent calls completed")

async def main():
    print("Starting main function")
    start_time = asyncio.get_event_loop().time()
    await run_sequential_calls()
    end_time = asyncio.get_event_loop().time()
    print(f"Sequential calls took {end_time - start_time:.2f} seconds")
    start_time = asyncio.get_event_loop().time()
    await run_concurrent_calls()
    end_time = asyncio.get_event_loop().time()
    print(f"Concurrent calls took {end_time - start_time:.2f} seconds")
    print("Main function completed")

asyncio.run(main())