"""Tests for the pagination data source module."""

import hiero_analytics.data_sources.pagination as pagination

# ---------------------------------------------------------
# page-number pagination
# ---------------------------------------------------------


def test_paginate_page_number_multiple_pages():
    """Test that multiple full pages are accumulated correctly."""
    pages = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [],
    }

    def fetch(page):
        return pages[page]

    results = pagination.paginate_page_number(fetch, page_size=3)

    assert results == [1, 2, 3, 4, 5, 6]


def test_paginate_page_number_partial_page_stops():
    """Test that pagination stops after a partial page is returned."""
    pages = {
        1: [1, 2, 3],
        2: [4],  # partial page
    }

    def fetch(page):
        return pages.get(page, [])

    results = pagination.paginate_page_number(fetch, page_size=3)

    assert results == [1, 2, 3, 4]


def test_paginate_page_number_empty_first_page():
    """Test that an empty first page returns an empty list immediately."""

    def fetch(_page):
        return []

    results = pagination.paginate_page_number(fetch)

    assert results == []


def test_paginate_page_number_max_pages_guard():
    """Test that max_pages limits the number of pages fetched."""

    def fetch(page):
        return [page] * 100

    results = pagination.paginate_page_number(
        fetch,
        page_size=100,
        max_pages=2,
    )

    assert len(results) == 200


# ---------------------------------------------------------
# cursor pagination
# ---------------------------------------------------------


def test_paginate_cursor_multiple_pages():
    """Test that cursor pagination accumulates items across multiple pages."""
    data = {
        None: ([1, 2], "A", True),
        "A": ([3, 4], "B", True),
        "B": ([5], None, False),
    }

    def fetch(cursor):
        return data[cursor]

    results = pagination.paginate_cursor(fetch)

    assert results == [1, 2, 3, 4, 5]


def test_paginate_cursor_single_page():
    """Test that a single-page cursor response returns all items and stops."""

    def fetch(_cursor):
        return ([1, 2], None, False)

    results = pagination.paginate_cursor(fetch)

    assert results == [1, 2]


def test_paginate_cursor_max_pages_guard():
    """Test that max_pages stops infinite cursor pagination."""

    def fetch(_cursor):
        return ([1], "next", True)

    results = pagination.paginate_cursor(
        fetch,
        max_pages=2,
    )

    assert len(results) == 2


def test_paginate_cursor_handles_empty_items():
    """Test that an empty items page returns an empty list."""
    calls = {None: ([], None, False)}

    def fetch(cursor):
        return calls[cursor]

    results = pagination.paginate_cursor(fetch)

    assert results == []
