import asyncio
from app import App


async def main():
    app = App()
    app.run()


if __name__ == '__main__':
    asyncio.run(main())
