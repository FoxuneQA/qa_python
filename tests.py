import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


def test_add_new_book_adds_book_to_books_genre(collector):
    collector.add_new_book("Гарри Поттер")
    assert "Гарри Поттер" in collector.get_books_genre()
    assert collector.get_book_genre("Гарри Поттер") == ""


@pytest.mark.parametrize("book_name", ["", "A" * 41])
def test_add_new_book_invalid_name_not_added(collector, book_name):
    collector.add_new_book(book_name)
    assert book_name not in collector.get_books_genre()


def test_set_book_genre_sets_valid_genre(collector):
    collector.add_new_book("Гарри Поттер")
    collector.set_book_genre("Гарри Поттер", "Фантастика")
    assert collector.get_book_genre("Гарри Поттер") == "Фантастика"


def test_set_book_genre_does_not_set_invalid_genre(collector):
    collector.add_new_book("Гарри Поттер")
    collector.set_book_genre("Гарри Поттер", "Неизвестный жанр")
    assert collector.get_book_genre("Гарри Поттер") == ""


def test_get_book_genre_returns_genre_by_name(collector):
    collector.add_new_book("Гарри Поттер")
    collector.set_book_genre("Гарри Поттер", "Фантастика")
    assert collector.get_book_genre("Гарри Поттер") == "Фантастика"


def test_get_books_with_specific_genre_returns_only_requested_genre(collector):
    collector.add_new_book("Гарри Поттер")
    collector.set_book_genre("Гарри Поттер", "Фантастика")
    collector.add_new_book("Оно")
    collector.set_book_genre("Оно", "Ужасы")
    books = collector.get_books_with_specific_genre("Фантастика")
    assert books == ["Гарри Поттер"]


def test_get_books_genre_returns_full_books_genre_dict(collector):
    collector.add_new_book("Гарри Поттер")
    collector.set_book_genre("Гарри Поттер", "Фантастика")
    collector.add_new_book("Оно")
    collector.set_book_genre("Оно", "Ужасы")
    books_genre = collector.get_books_genre()
    assert books_genre == {
        "Гарри Поттер": "Фантастика",
        "Оно": "Ужасы",
    }


def test_get_books_for_children_excludes_age_restricted_genres(collector):
    collector.add_new_book("Гарри Поттер")
    collector.set_book_genre("Гарри Поттер", "Фантастика")
    collector.add_new_book("Оно")
    collector.set_book_genre("Оно", "Ужасы")
    collector.add_new_book("Шерлок Холмс")
    collector.set_book_genre("Шерлок Холмс", "Детективы")
    children_books = collector.get_books_for_children()
    assert "Гарри Поттер" in children_books
    assert "Оно" not in children_books
    assert "Шерлок Холмс" not in children_books


def test_add_book_in_favorites_adds_only_once(collector):
    collector.add_new_book("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")
    favorites = collector.get_list_of_favorites_books()
    assert favorites == ["Гарри Поттер"]


def test_delete_book_from_favorites_removes_book(collector):
    collector.add_new_book("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")
    collector.delete_book_from_favorites("Гарри Поттер")
    favorites = collector.get_list_of_favorites_books()
    assert favorites == []


def test_get_list_of_favorites_books_returns_current_favorites(collector):
    collector.add_new_book("Гарри Поттер")
    collector.add_new_book("Оно")
    collector.add_book_in_favorites("Гарри Поттер")
    collector.add_book_in_favorites("Оно")
    favorites = collector.get_list_of_favorites_books()
    assert favorites == ["Гарри Поттер", "Оно"]