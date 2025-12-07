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
            CREATE TABLE IF NOT EXISTS matches(
                match_id TEXT PRIMARY KEY,
                winner TEXT,
                team_1 TEXT,
                team_2 TEXT
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

        team_1 = adapter.get("team_1")
        if isinstance(team_1, list):
            team_1 = ", ".join(team_1)

        team_2 = adapter.get("team_2")
        if isinstance(team_2, list):
            team_2 = ", ".join(team_2)

        self.cur.execute(
            """
            INSERT OR IGNORE INTO matches (match_id, winner, team_1, team_2)
            VALUES (?, ?, ?, ?)
            """,
            (
                match_id,
                winner,
                team_1,
                team_2,
            ),
        )
        self.con.commit()
        return item

    def close_spider(self, spider):
        self.con.close()
