# Asyncio Load Tester
## Quickstart
```
python3.5 --version  # Need Python 3.5 or higher
virtualenv env -ppython3.5
source env/bin/activate{.fish}  # consider using fish ;)
pip install -r requirements.txt
./run.py www.yourdomain.com 200
```

## Testing the examples
The `/examples` folder contain two versions of a server that generates a
streaming response. One is implemented in a non-blocking fashion using aiohttp,
the other is made with flask.

To try it out, run the following in your terminal.

```
python examples/run.py &
python examples/run_asyncio.py &
./run.py localhost:5000 20 # Slow!
./run.py localhost:6000 20 # Blazing fast!
```
