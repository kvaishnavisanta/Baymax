import asyncio
from hume import HumeVoiceClient, MicrophoneInterface
from find_config import list_configs
from create_personality import create_personality_config


async def main() -> None:
    client = HumeVoiceClient("k4tzTx8wFZOGgmCKEes1khlzcLK1270ohsbcjKnoptT6FPyp")

    # Your menu system goes here
    while True:
        print("Menu:")
        print("1. Start to talk with Hume")
        print("2. Choose personality")
        print("3. Create your own personality")
        choice = input("Enter your choice: ")

        if choice == "1":
            async with client.connect(config_id="6aa1a7ca-d3d0-4ea9-9e7d-97b064e7c109") as socket:
                await MicrophoneInterface.start(socket)
        elif choice == "2":
            selected_config_name, selected_config_id = list_configs(client)  # Get the selected config (name, id)
            async with client.connect(config_id=selected_config_id) as socket:
                print(f"Using config: {selected_config_name}")
        elif choice == "3":
            create_personality_config(client)
        else:
            print("Invalid choice. Please choose again.")


asyncio.run(main())
