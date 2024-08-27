import math
import os
import sys

BOOK_PATH = 'book\some_text_book.txt'
PAGE_SIZE = 1050
book: dict[int, str] = {}

def _get_part_text(text: str, start: int, page_size=PAGE_SIZE) -> tuple[str, int]:
    symbl_lst = [',', '.', '!', '?', ':', ';']
    end_index: int

    for symbl in range(start, start+page_size, -1):
        if text[symbl] in symbl_lst:
            end_index = symbl
            break
    new_text = text[start:end_index+1]
    return (new_text, len(new_text))

print(*_get_part_text('Раз. Два. Три. Четыре. Пять. Прием!', 5, 9), sep='\n')

def prepare_book(path:str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        book_text = ' '.join([i.strip() for i in file.readlines()])
        start = 0
        for i in range(math.ceil(len(book_text)/PAGE_SIZE)):
            res = _get_part_text(book_text, start, PAGE_SIZE)
            book[i+1] = res[0]
            start += res[1] + 1
    return None


prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
