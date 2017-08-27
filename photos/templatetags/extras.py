from django import template

register = template.Library()


@register.filter(name='chunks')
def chunks(iterable, chunk_size):
    if not hasattr(iterable, '__iter__'):
        # can't use "return" and "yield" in the same function
        yield iterable
    else:
        i = 0
        chunk = []
        for item in iterable:
            chunk.append(item)
            i += 1
            if not i % chunk_size:
                yield chunk
                chunk = []
        if chunk:
            # some items will remain which haven't been yielded yet,
            # unless len(iterable) is divisible by chunk_size
            yield chunk


@register.filter(name='pages')
def pages_filter(page):
    paginator = page.paginator
    num_pages = paginator.num_pages
    current_page = page.number

    if num_pages <= 11 or current_page <= 6:
        pages = [x for x in range(1, min(num_pages + 1, 12))]
    elif current_page > num_pages - 6:
        pages = [x for x in range(num_pages - 10, num_pages + 1)]
    else:
        pages = [x for x in range(current_page - 5, current_page + 6)]
    return pages


@register.filter(name='has_previous_pages')
def has_previous_pages(page):
    paginator = page.paginator
    num_pages = paginator.num_pages
    current_page = page.number

    if num_pages <= 11 or current_page <= 6:
        return False
    else:
        return True


@register.filter(name='has_next_pages')
def has_next_pages(page):
    paginator = page.paginator
    num_pages = paginator.num_pages
    current_page = page.number

    if num_pages <= 11:
        return False

    return current_page + 5 < num_pages
