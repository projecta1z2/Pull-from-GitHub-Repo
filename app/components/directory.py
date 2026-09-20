import reflex as rx

from app.states.directory import DirectoryState


def brand_bar() -> rx.Component:
    return rx.el.header(
        rx.el.nav(
            rx.el.a(
                rx.icon("book-open", class_name="w-5 h-5 text-[#65765a]"),
                rx.el.span(
                    "The Username Index",
                    class_name="font-['Libre_Baskerville'] text-sm sm:text-base",
                ),
                href="/",
                class_name="flex items-center gap-3 text-[#23323a]",
            ),
            rx.el.a(
                "BROWSE THE INDEX",
                rx.icon("arrow-down-right", class_name="w-4 h-4"),
                href="#index",
                class_name="flex items-center gap-2 text-[10px] sm:text-xs tracking-widest text-[#65765a] hover:text-[#23323a]",
            ),
            class_name="max-w-7xl mx-auto px-6 lg:px-12 h-20 flex items-center justify-between gap-4",
            aria_label="Main navigation",
        ),
        class_name="border-b border-[#d6d5c9]",
    )


def hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.p(
                "A SMALL COLLECTION. AN ALPHABET OF POSSIBILITIES.",
                class_name="text-[10px] sm:text-xs tracking-[0.2em] text-[#65765a] mb-7",
            ),
            rx.el.h1(
                "A name for",
                rx.el.br(),
                rx.el.em("every letter."),
                class_name="font-['Libre_Baskerville'] text-4xl sm:text-6xl lg:text-7xl leading-[1.2] tracking-tight text-[#23323a]",
            ),
            rx.el.p(
                "An alphabetical collection of usernames. Find a name, follow a letter, or simply see what you discover.",
                class_name="text-sm sm:text-base leading-7 text-[#737d6d] max-w-lg mt-7",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.span(
                "A–Z",
                class_name="font-['Libre_Baskerville'] text-7xl lg:text-8xl tracking-tight text-[#65765a]",
            ),
            rx.el.div(class_name="w-12 border-t border-[#a7ae99] my-6"),
            rx.el.p(
                "THE USERNAME INDEX",
                class_name="text-[10px] tracking-[0.2em] text-[#65765a]",
            ),
            rx.el.p(
                "An alphabetical field guide",
                class_name="font-['Libre_Baskerville'] italic text-xs mt-3 text-[#737d6d]",
            ),
            class_name="hidden md:flex flex-col items-center justify-center w-72 lg:w-80 border-l border-[#d6d5c9] pl-12",
        ),
        class_name="flex gap-12 py-14 sm:py-20 border-b border-[#d6d5c9]",
    )


def letter_button(letter: str) -> rx.Component:
    return rx.el.button(
        letter,
        on_click=DirectoryState.select_initial(letter),
        aria_label=f"Filter by {letter}",
        aria_pressed=DirectoryState.initial == letter,
        class_name=rx.cond(
            DirectoryState.initial == letter,
            "h-12 sm:h-14 flex items-center justify-center border border-[#65765a] bg-[#65765a] text-[#f5f4ec] font-['Libre_Baskerville'] text-lg transition-colors focus-visible:outline-2 focus-visible:outline-offset-2",
            "h-12 sm:h-14 flex items-center justify-center border border-[#d6d5c9] bg-transparent text-[#23323a] font-['Libre_Baskerville'] text-lg hover:bg-[#e6e8dc] hover:border-[#65765a] transition-colors focus-visible:outline-2 focus-visible:outline-offset-2",
        ),
    )


def alphabet_index() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Browse by letter",
                class_name="font-['Libre_Baskerville'] text-xl",
            ),
            rx.el.span(
                f"{DirectoryState.indexed} LETTERS · {DirectoryState.total} USERNAMES",
                class_name="text-[10px] tracking-widest text-[#737d6d]",
            ),
            class_name="flex flex-wrap items-center justify-between gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "All",
                on_click=DirectoryState.select_initial("All"),
                aria_pressed=DirectoryState.initial == "All",
                class_name=rx.cond(
                    DirectoryState.initial == "All",
                    "h-12 sm:h-14 border border-[#65765a] bg-[#65765a] text-[#f5f4ec] font-['Libre_Baskerville'] text-sm focus-visible:outline-2",
                    "h-12 sm:h-14 border border-[#d6d5c9] bg-transparent text-[#23323a] font-['Libre_Baskerville'] text-sm hover:bg-[#e6e8dc] focus-visible:outline-2",
                ),
            ),
            rx.foreach(DirectoryState.letters, letter_button),
            class_name="grid grid-cols-7 sm:grid-cols-9 lg:grid-cols-[repeat(27,minmax(0,1fr))] gap-1.5",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("search", class_name="w-4 h-4 text-[#737d6d] shrink-0"),
                rx.el.input(
                    default_value=DirectoryState.search,
                    on_change=DirectoryState.set_search.debounce(200),
                    placeholder="Search for a username…",
                    aria_label="Search usernames",
                    type="search",
                    class_name="w-full bg-transparent text-[#23323a] text-sm py-3 outline-hidden placeholder:text-[#8a9183]",
                ),
                rx.cond(
                    DirectoryState.search != "",
                    rx.el.button(
                        rx.icon("x", class_name="w-4 h-4"),
                        on_click=DirectoryState.clear_search,
                        aria_label="Clear search",
                        class_name="p-2 text-[#737d6d] hover:text-[#23323a]",
                    ),
                ),
                class_name="flex items-center gap-3 px-4 border border-[#bfc3b3] focus-within:border-[#65765a] w-full sm:max-w-md bg-[#f9f8f2]",
            ),
            rx.cond(
                DirectoryState.has_filters,
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="w-3.5 h-3.5"),
                    "Reset filters",
                    on_click=DirectoryState.clear_filters,
                    class_name="flex items-center gap-2 text-xs text-[#65765a] hover:text-[#23323a] py-2",
                ),
                rx.el.span(
                    "Find something that feels like you.",
                    class_name="text-xs text-[#8a9183] italic",
                ),
            ),
            class_name="flex flex-wrap items-center justify-between gap-4 mt-7",
        ),
        id="index",
        class_name="py-9 sm:py-11 scroll-mt-6",
    )


def result_row(row: dict[str, str]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    row["username"],
                    class_name="font-['Libre_Baskerville'] text-base text-[#23323a]",
                ),
                rx.el.button(
                    rx.icon("copy", class_name="w-3.5 h-3.5"),
                    on_click=[
                        rx.set_clipboard(row["username"]),
                        rx.toast("Username copied"),
                    ],
                    aria_label=f"Copy {row['username']}",
                    title="Copy username",
                    class_name="p-2 text-[#8a9183] hover:text-[#23323a] sm:opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity",
                ),
                class_name="flex items-center justify-between gap-3 max-w-sm",
            ),
            class_name="px-4 sm:px-6 py-3",
        ),
        rx.el.td(
            rx.el.span(
                row["initial"],
                class_name="inline-flex w-7 h-7 items-center justify-center bg-[#e7eadd] text-[#65765a] text-xs",
            ),
            class_name="px-3 py-3",
        ),
        rx.el.td(
            f"NO. {row['record']}",
            class_name="px-4 sm:px-6 py-3 text-right text-[10px] sm:text-xs tabular-nums tracking-wider text-[#8a9183]",
        ),
        key=row["username"],
        class_name="group border-b border-[#e0e0d5] last:border-b-0 even:bg-[#f0f1e8] hover:bg-[#e9ecdf] transition-colors",
    )


def result_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        rx.el.span(
                            rx.icon("at-sign", class_name="w-3 h-3"),
                            "USERNAME",
                            class_name="flex items-center gap-2",
                        ),
                        scope="col",
                        class_name="px-4 sm:px-6 py-3 font-medium w-2/3",
                    ),
                    rx.el.th(
                        rx.el.span(
                            rx.icon("a-large-small", class_name="w-3 h-3"),
                            "INITIAL",
                            class_name="flex items-center gap-2",
                        ),
                        scope="col",
                        class_name="px-3 py-3 font-medium",
                    ),
                    rx.el.th(
                        rx.el.span(
                            rx.icon("hash", class_name="w-3 h-3"),
                            "RECORD",
                            class_name="flex justify-end items-center gap-2",
                        ),
                        scope="col",
                        class_name="px-4 sm:px-6 py-3 font-medium",
                    ),
                    class_name="text-left text-[10px] tracking-widest text-[#737d6d] bg-[#eeefe5] border-b border-[#d9dacf]",
                )
            ),
            rx.el.tbody(rx.foreach(DirectoryState.rows, result_row)),
            class_name="table-auto w-full",
            aria_label="Username directory",
        ),
        class_name="overflow-hidden border border-[#d9dacf] rounded-sm",
    )


def results() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                rx.cond(
                    DirectoryState.initial == "All",
                    "The collection",
                    f"The letter {DirectoryState.initial}",
                ),
                class_name="font-['Libre_Baskerville'] text-xl",
            ),
            rx.el.span(
                f"{DirectoryState.result_count} of {DirectoryState.total} usernames",
                class_name="text-xs text-[#737d6d]",
                aria_live="polite",
            ),
            class_name="flex flex-wrap justify-between items-center gap-3 mb-5",
        ),
        rx.cond(
            DirectoryState.loading,
            rx.el.div(
                rx.icon(
                    "loader-circle",
                    class_name="w-5 h-5 animate-spin text-[#65765a]",
                ),
                "Opening the index…",
                role="status",
                class_name="flex items-center justify-center gap-3 h-52 border border-[#d9dacf] text-sm text-[#737d6d]",
            ),
            rx.cond(
                DirectoryState.error != "",
                rx.el.div(
                    rx.icon(
                        "circle-alert", class_name="w-6 h-6 text-[#65765a]"
                    ),
                    rx.el.p(DirectoryState.error),
                    rx.el.button(
                        "Try again",
                        on_click=DirectoryState.load,
                        class_name="px-5 py-2 border border-[#65765a] text-[#65765a] hover:bg-[#e7eadd]",
                    ),
                    role="alert",
                    class_name="flex flex-col items-center gap-4 py-14 border border-[#d9dacf] text-sm text-[#737d6d]",
                ),
                rx.cond(
                    DirectoryState.result_count == 0,
                    rx.el.div(
                        rx.icon("search", class_name="w-7 h-7 text-[#737d6d]"),
                        rx.el.h3(
                            "No names on this page.",
                            class_name="font-['Libre_Baskerville'] text-xl text-[#23323a]",
                        ),
                        rx.el.p(
                            "Try another search or explore a different letter.",
                            class_name="text-sm text-[#737d6d]",
                        ),
                        rx.el.button(
                            "Clear filters",
                            on_click=DirectoryState.clear_filters,
                            class_name="border-b border-[#65765a] text-sm text-[#65765a] pb-1 hover:text-[#23323a]",
                        ),
                        role="status",
                        class_name="flex flex-col items-center text-center gap-4 py-16 px-5 border border-[#d9dacf]",
                    ),
                    result_table(),
                ),
            ),
        ),
        class_name="pb-12",
        aria_busy=DirectoryState.loading,
    )


def directory() -> rx.Component:
    return rx.el.div(
        brand_bar(),
        rx.el.main(
            hero(),
            alphabet_index(),
            results(),
            class_name="w-full max-w-7xl mx-auto px-6 lg:px-12",
        ),
        rx.el.footer(
            rx.el.span(
                "The Username Index", class_name="font-['Libre_Baskerville']"
            ),
            rx.el.span("A–Z, and everything in between.", class_name="text-xs"),
            class_name="max-w-7xl mx-auto px-6 lg:px-12 py-7 border-t border-[#d6d5c9] flex flex-wrap gap-4 items-center justify-between text-[#777e70]",
        ),
        class_name="min-h-screen bg-[#f5f4ec] text-[#23323a] font-['Inter']",
    )
