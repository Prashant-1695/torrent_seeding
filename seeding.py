import libtorrent as lt
import time
import os

def seed_dead_magnet_links(magnet_links, save_path):
    # Create a session
    session = lt.session()
    session.listen_on(6881, 6891)  # Listen to incoming connections on specified ports

    # Ensure the save_path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for magnet in magnet_links:
        print(f"Attempting to seed: {magnet}")
        try:
            # Parse the magnet link into add_torrent_params
            params = lt.parse_magnet_uri(magnet)
            params.save_path = save_path  # Set the save path

            torrent_handle = session.add_torrent(params)

            # Wait for the torrent to start
            print("Starting the torrent...")
            for i in range(30):  # Wait for 30 seconds
                s = torrent_handle.status()
                print(f"Progress: {s.progress * 100:.2f}%, State: {s.state}, Peers: {s.num_peers}")
                time.sleep(1)

            # Check if the torrent is seeding
            if s.state == lt.torrent_status.seeding:
                print(f"Successfully seeded: {magnet}")
            else:
                print(f"Failed to seed: {magnet}. Final state: {s.state}, Peers: {s.num_peers}")

        except Exception as e:
            print(f"Error seeding {magnet}: {e}")

if __name__ == "__main__":
    # List of dead magnet links (example links)
    dead_magnet_links = [
        "magnet:?xt=urn:btih:4f703145d5f471718c13e4ca659e86916ff3b9a7&dn=%5BINDEX%5D%20Yondemasu%20yo%20Azazel-san%20%7BSeason%201%2C%20You%27re%20Being%20Summoned%2C%20Azazel%7D%20%5BJP.BD%5D%5BAV1%5D%5BHi10%5D%5B1080p%5D%5BFLAC%5D%20%28English%20Subbed%29&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce",
    ]

    # Set your desired save path for the downloaded files
    save_path = "./torrents"

    seed_dead_magnet_links(dead_magnet_links, save_path)