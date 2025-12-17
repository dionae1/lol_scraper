import sqlite3
from itemadapter import ItemAdapter


class SQLitePipeline:
    def __init__(self):
        self.con = sqlite3.connect("games.db")
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS matches
            (
                match_id
                TEXT
                PRIMARY
                KEY,
                winner
                TEXT,
                blue_team
                TEXT,
                red_team
                TEXT
            )
            """
        )

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        match_id = adapter.get("match_id")
        if isinstance(match_id, list):
            match_id = match_id[0] if match_id else None

        winner = adapter.get("winner")
        if isinstance(winner, list):
            winner = winner[0] if winner else None

        blue_team = adapter.get("blue_team")
        if isinstance(blue_team, list):
            blue_team = ", ".join(blue_team)

        red_team = adapter.get("red_team")
        if isinstance(red_team, list):
            red_team = ", ".join(red_team)

        self.cur.execute(
            """
            INSERT
            OR IGNORE INTO matches (match_id, winner, blue_team, red_team)
            VALUES (?, ?, ?, ?)
            """,
            (
                match_id,
                winner,
                blue_team,
                red_team,
            ),
        )
        self.con.commit()
        return item

    def close_spider(self, spider):
        self.con.close()
