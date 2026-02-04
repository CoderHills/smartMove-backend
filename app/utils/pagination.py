def paginate_results(query, page, per_page):
    """Paginates a SQLAlchemy query and returns a dict with metadata."""
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": paginated.items,
        "meta": {
            "total_items": paginated.total,
            "total_pages": paginated.pages,
            "current_page": paginated.page,
            "per_page": paginated.per_page,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev,
        },
    }
