import reflex as rx

import logging
from string import ascii_uppercase
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.models import Username


SAMPLE_USERNAMES = (
    "amber",
    "boon",
    "clover",
    "drift",
    "ember",
    "fern",
    "grove",
    "harbor",
    "indigo",
    "juniper",
    "kestrel",
    "linden",
    "moss",
    "north",
    "olive",
    "paper",
    "quill",
    "river",
    "sage",
    "timber",
    "umber",
    "violet",
    "willow",
    "xenon",
    "yarrow",
    "zephyr",
)


class DirectoryState(rx.State):
    search: str = ""
    initial: str = "All"
    letters: list[str] = list(ascii_uppercase)
    entries: list[dict[str, str]] = []
    total: int = 0
    indexed: int = 0
    loading: bool = True
    error: str = ""

    @rx.var
    def rows(self) -> list[dict[str, str]]:
        query = self.search.strip().casefold()
        return [
            row
            for row in self.entries
            if (self.initial == "All" or row["initial"] == self.initial)
            and query in row["username"].casefold()
        ]

    @rx.var
    def result_count(self) -> int:
        return len(self.rows)

    @rx.var
    def has_filters(self) -> bool:
        return bool(self.search or self.initial != "All")

    @rx.event
    def set_search(self, value: str):
        self.search = value

    @rx.event
    def select_initial(self, letter: str):
        if letter == "All" or letter in self.letters:
            self.initial = letter

    @rx.event
    def clear_search(self):
        self.search = ""

    @rx.event
    def clear_filters(self):
        self.search = ""
        self.initial = "All"

    @rx.event(background=True)
    async def load(self):
        async with self:
            self.loading = True
            self.error = ""
        try:
            async with rx.asession() as session:
                await session.execute(
                    insert(Username)
                    .values(
                        [
                            {
                                "username": name,
                                "initial_letter": name[0].upper(),
                            }
                            for name in SAMPLE_USERNAMES
                        ]
                    )
                    .on_conflict_do_nothing()
                )
                await session.commit()
                records = (
                    await session.scalars(
                        select(Username).order_by(
                            Username.initial_letter, Username.username
                        )
                    )
                ).all()
                entries = [
                    {
                        "username": record.username,
                        "initial": record.initial_letter,
                        "record": f"{record.id:03d}",
                    }
                    for record in records
                ]
            async with self:
                self.entries = entries
                self.total = len(entries)
                self.indexed = len({row["initial"] for row in entries})
        except Exception as e:
            logging.exception(f"Error: {e}")
            async with self:
                self.error = "The index couldn't be loaded. Please try again."
        finally:
            async with self:
                self.loading = False
