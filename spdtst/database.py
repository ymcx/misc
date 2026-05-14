from datetime import datetime
import sqlite3


class Database:
    def __init__(self, filename: str = "results.sqlite") -> None:
        self.filename = filename

    def open(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS result (
                date TEXT,
                server TEXT,
                download REAL,
                upload REAL,
                ping REAL,
                jitter REAL
            )
        """

        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def parse_result(
        self, result: dict | None
    ) -> tuple[str, str, float, float, int, int]:
        date = datetime.now().isoformat()

        if result is None:
            return date, "", 0.0, 0.0, 0, 0

        server = result["server"]["host"]
        download = float(result["download"]) / 10**6
        upload = float(result["upload"]) / 10**6
        ping = int(result["ping"])
        jitter = int(result["jitter"])

        return date, server, download, upload, ping, jitter

    def insert(self, result: dict | None) -> None:
        query = """
            INSERT INTO result (date, server, download, upload, ping, jitter)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        parameters = self.parse_result(result)

        self.cursor.execute(query, parameters)
        self.connection.commit()
