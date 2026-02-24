from math import floor

from django.views.generic import TemplateView

from .utils import (
    build_search_query_string,
    get_search_results,
    get_search_api_url,
    normalize_search_term,
    parse_comma_separated_tags,
    safe_int,
)


def get_page_links(pages_count, current_page, term, tags=None):
    page_links = []

    if pages_count > 1:
        if current_page == 1:
            from_page = 1
            to_page = from_page + 7
        elif current_page == pages_count + 1:
            from_page = to_page = current_page
        else:
            from_page = current_page - 4
            to_page = current_page + 5

        if from_page < 1:
            from_page = 1
        if to_page > pages_count:
            to_page = pages_count

        for page in range(from_page, to_page + 1):
            page_link = build_search_query_string(term, page=page, tags=tags)
            page_links.append({"page": page, "url": page_link})

    return page_links


def get_prev_next_links(next_page_number, prev_page_number, term, tags=None):
    next_link = build_search_query_string(term, page=next_page_number, tags=tags) if next_page_number else None
    prev_link = build_search_query_string(term, page=prev_page_number, tags=tags) if prev_page_number else None
    return [prev_link, next_link]


def get_prev_next_page_number(pages_count, current_page):
    current_page = safe_int(current_page, 1)
    pages_count = safe_int(pages_count, 0)

    prev_page_number = current_page - 1 if current_page > 1 else None
    next_page_number = current_page + 1 if current_page < pages_count else None
    return [prev_page_number, next_page_number]


def get_total_pages(total_hits):
    pages_count = floor(total_hits / 10)
    if total_hits % 10 > 0:
        pages_count += 1
    return pages_count


def get_api_re_path(term, current_page, tags=None):
    """Build the search API URL (delegates to utils for consistency)."""
    return get_search_api_url(term, current_page, tags=tags)


class SearchResult(TemplateView):

    template_name = "simplesitesearch/search_results.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # get term and optional tag(s) from url params (tag can be comma-separated)
        term = request.GET.get("q")
        tag_param = request.GET.get("tag") or request.GET.get("tags")
        tags_list = parse_comma_separated_tags(tag_param)
        honeypot_message = request.GET.get("message")

        current_page = safe_int(request.GET.get("page"), 1)

        if term and not honeypot_message:
            term = normalize_search_term(term)
            response_data = get_search_results(
                term, current_page, tags=tags_list or None
            )
            pages_count = get_total_pages(response_data["total_hits"])
            prev_page_number, next_page_number = get_prev_next_page_number(pages_count, current_page)
            prev_link, next_link = get_prev_next_links(
                next_page_number, prev_page_number, term, tags=tags_list or None
            )
            page_links = get_page_links(pages_count, current_page, term, tags=tags_list or None)

            context.update({
                "pages_count": pages_count,
                "current_page": current_page,
                "results_count": response_data["total_hits"],
                "prev_link": prev_link,
                "next_link": next_link,
                "page_links": page_links,
                "results": response_data["hits"],
            })
        else:
            context.update({"results": None})

        context.update({
            "query": term,
            "tag": tag_param or "",
        })

        return self.render_to_response(context)
