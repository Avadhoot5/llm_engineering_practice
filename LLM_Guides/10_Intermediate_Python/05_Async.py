import asyncio
import gradio as gr

async def say_hello():
    print('Hello')
    await asyncio.sleep(1)
    print('World')

# asyncio.run(say_hello())

async def greet(name):
    print(f'Hello, {name}')
    await asyncio.sleep(1)
    print(f'Goodbye, {name}')

async def main_fn():
    await greet('Andrew')

# asyncio.run(main_fn())

# using gradio 

async def slow_response(name):
    n = 2
    await asyncio.sleep(n)
    return f'Hello {name}! (after waiting for {n} seconds)'

# app = gr.Interface(fn=slow_response, inputs='text', outputs='text')
# app.launch()

# Part 6: Advanced Async – asyncio.gather

async def task(name, delay):
    await asyncio.sleep(delay)
    print(f'{name} delayed for {delay} seconds')
    return name

async def main_task():
    results = await asyncio.gather(
        task('A', 1),
        task('B', 2), 
        task('C', 3))
    print(results)

asyncio.run(main_task())



