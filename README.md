# Qrt - Website where I practice in Quart  

I am a Flask #1 ambassador, but during my last job I was often limited by the syncronous nature of Flask. Now I dicovered Quart, and I really want to experiment with it.  

## Installation  

You need to have `pipx` and `poetry` installed before running the app  

Install dependencies with poetry:

    poetry install

## Running and development  

> Note: poetry does not work well with quart's hot reload mechanism. If you want to run dev environment with hot reload, use:

    python src/qrt/serve.py dev

Run project using poetry scripts:

    poetry run dev

This command adresses qrt.serve module, where instructions for dev and prod are stated (difference is, prod instance runs with ASGI)

## Testing

    poetry run test

## Deployment  

    poetry run prod