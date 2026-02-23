from datetime import date

from app.utils.utils import age_from_birthdate, get_db


def test_birthday_is_today():
    """Return the difference N in years if the birthday is today"""

    # Arrange
    today = date.today()
    N: int = 25
    birthdate = date(today.year - N, today.month, today.day)

    # Act
    res = age_from_birthdate(birthdate)

    # Assert
    assert res == N


def test_birthday_already_passed_this_year():
    """
    Return the difference N in years if the birthday has already occurred this year
    """

    # Arrange
    today = date.today()
    N: int = 40
    birthdate = date(today.year - N, 1, 1)

    # Act
    res = age_from_birthdate(birthdate)

    # Assert
    assert res == N


def test_birthday_not_yet_reached_this_year():
    """
    Return the difference N-1 in years if the birthday has not yet occurred this year
    """

    # Arrange
    today = date.today()
    N: int = 20
    birthdate = date(today.year - N, 12, 31)
    expected = N if (today.month, today.day) >= (12, 31) else N - 1

    # Act
    res = age_from_birthdate(birthdate)

    # Assert
    assert res == expected


def test_newborn_age_is_zero():
    """Return 0 if the birthday is today (newborn)"""
    # Arrange
    today = date.today()

    # Act
    res = age_from_birthdate(today)

    # Assert
    assert res == 0


# ---------------------------------------------------------------------------
# get_db
# ---------------------------------------------------------------------------

def test_get_db_yields_a_session(mocker):
    """get_db should yield a database session"""
    # Arrange
    mock_session = mocker.MagicMock()
    mocker.patch("app.utils.utils.SESSION_LOCAL", return_value=mock_session)

    # Act
    gen = get_db()
    session = next(gen)

    # Assert
    assert session is mock_session


def test_get_db_closes_session_after_use(mocker):
    """get_db should close the session once the generator is exhausted"""
    # Arrange
    mock_session = mocker.MagicMock()
    mocker.patch("app.utils.utils.SESSION_LOCAL", return_value=mock_session)

    # Act
    gen = get_db()
    next(gen)
    try:
        next(gen)
    except StopIteration:
        pass

    # Assert
    mock_session.close.assert_called_once()
