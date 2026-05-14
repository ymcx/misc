from database import Database
import speedtest
import time


def main() -> None:
    database = Database()
    database.open()

    try:
        while True:
            result = speedtest.run()
            print(result)
            database.insert(result)
            time.sleep(60 * 5)
    except KeyboardInterrupt:
        database.close()


if __name__ == "__main__":
    main()
