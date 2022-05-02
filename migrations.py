class Migrations():
    def __init__(self, db):
        self.db = db

    def create_table(self):
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS migrations (id INTEGER PRIMARY KEY, version INTEGER)"
        )

    def add_migration(self, version):
        self.db.execute(
            "INSERT INTO migrations (version) VALUES (?)", (version,)
        )

    def get_migrations(self):
        return self.db.execute("SELECT version FROM migrations")

    def get_last_migration(self):
        return self.db.execute("SELECT version FROM migrations ORDER BY version DESC LIMIT 1")

    def get_migration_by_version(self, version):
        return self.db.execute(
            "SELECT version FROM migrations WHERE version = ?", (version,)
        )

    def delete_migration(self, version):
        self.db.execute(
            "DELETE FROM migrations WHERE version = ?", (version,)
        )