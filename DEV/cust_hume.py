import asyncio

from hume import HumeVoiceClient, MicrophoneInterface


async def main() -> None:
    client = HumeVoiceClient("HUME_API_KEY_HERE")

    async with client.connect(config_id="6aa1a7ca-d3d0-4ea9-9e7d-97b064e7c109") as socket:
        await MicrophoneInterface.start(socket)


asyncio.run(main())
