from leitner_box import LeitnerScheduler, Card, Rating, ReviewLog
from datetime import datetime, timezone
import pytest

class TestLeitnerBox:

    def test_basic_review_schedule(self):

        # create Leitner system at 2:30pm on Jan. 1, 2024
        start_datetime = datetime(2024, 1, 1, 14, 30, 0, 0)
        scheduler = LeitnerScheduler(start_datetime=start_datetime)

        # create new Card
        card = Card()

        assert card.box == 1
        assert card.due is None

        # fail the card 2:35pm on Jan. 1, 2024
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 1, 14, 35, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 1
        assert card.due == datetime(2024, 1, 2, 0, 0, 0, 0)

        # pass the card on Jan. 2
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 2, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        assert card.due == datetime(2024, 1, 4, 0, 0, 0, 0)

        # attempt to pass the card on Jan. 3 when it is not due
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 3, 0, 0, 0, 0)
        with pytest.raises(RuntimeError):
            card, review_log = scheduler.review_card(card, rating, review_datetime)

        # pass card on Jan. 4
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 4, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 3
        assert card.due == datetime(2024, 1, 7, 0, 0, 0, 0)

        # pass card on Jan. 7
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 7, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card is still in box 3
        assert card.box == 3
        assert card.due == datetime(2024, 1, 14, 0, 0, 0, 0)

        # fail card on Jan. 14
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 14, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card moves back to box 1
        assert card.box == 1
        assert card.due == datetime(2024, 1, 15, 0, 0, 0, 0)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 15, 0, 0, 0, 0)

        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        # card is also due next day because that's a day that box 2 is repeated
        assert card.due == datetime(2024, 1, 16, 0, 0, 0, 0)

    def test_basic_review_schedule_with_on_fail_prev_box(self):

        # create Leitner system at 2:30pm on Jan. 1, 2024
        start_datetime = datetime(2024, 1, 1, 14, 30, 0, 0)
        on_fail = 'prev_box'
        scheduler = LeitnerScheduler(start_datetime=start_datetime, on_fail=on_fail)

        # create new Card
        card = Card()

        assert card.box == 1
        assert card.due is None

        # fail the card 2:35pm on Jan. 1, 2024
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 1, 14, 35, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 1
        assert card.due == datetime(2024, 1, 2, 0, 0, 0, 0)

        # pass the card on Jan. 2
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 2, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        assert card.due == datetime(2024, 1, 4, 0, 0, 0, 0)

        # attempt to pass the card on Jan. 3 when it is not due
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 3, 0, 0, 0, 0)
        with pytest.raises(RuntimeError):
            card, review_log = scheduler.review_card(card, rating, review_datetime)

        # pass card on Jan. 4
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 4, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 3
        assert card.due == datetime(2024, 1, 7, 0, 0, 0, 0)

        # pass card on Jan. 7
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 7, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card is still in box 3
        assert card.box == 3
        assert card.due == datetime(2024, 1, 14, 0, 0, 0, 0)

        # fail card on Jan. 14
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 14, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card moves back to box 1
        assert card.box == 2
        assert card.due == datetime(2024, 1, 16, 0, 0, 0, 0)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 16, 0, 0, 0, 0)

        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 3
        assert card.due == datetime(2024, 1, 21, 0, 0, 0, 0)

    def test_basic_review_schedule_with_utc(self):

        # create Leitner system at 2:30pm on Jan. 1, 2024 UTC
        start_datetime = datetime(2024, 1, 1, 14, 30, 0, 0, timezone.utc)
        scheduler = LeitnerScheduler(start_datetime=start_datetime)

        # create new Card
        card = Card()

        assert card.box == 1
        assert card.due is None

        # fail the card 2:35pm on Jan. 1, 2024
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 1, 14, 35, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 1
        assert card.due != datetime(2024, 1, 2, 0, 0, 0, 0)
        assert card.due == datetime(2024, 1, 2, 0, 0, 0, 0, timezone.utc)

        # pass the card on Jan. 2
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 2, 0, 0, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        assert card.due == datetime(2024, 1, 4, 0, 0, 0, 0, timezone.utc)

        # attempt to pass the card on Jan. 3 when it is not due
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 3, 0, 0, 0, 0, timezone.utc)
        with pytest.raises(RuntimeError):
            card, review_log = scheduler.review_card(card, rating, review_datetime)

        # pass card on Jan. 4
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 4, 0, 0, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 3
        assert card.due == datetime(2024, 1, 7, 0, 0, 0, 0, timezone.utc)

        # pass card on Jan. 7
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 7, 0, 0, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card is still in box 3
        assert card.box == 3
        assert card.due == datetime(2024, 1, 14, 0, 0, 0, 0, timezone.utc)

        # fail card on Jan. 14
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 14, 0, 0, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card moves back to box 1
        assert card.box == 1
        assert card.due == datetime(2024, 1, 15, 0, 0, 0, 0, timezone.utc)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 15, 0, 0, 0, 0, timezone.utc)

        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        # card is also due next day because that's a day that box 2 is repeated
        assert card.due == datetime(2024, 1, 16, 0, 0, 0, 0, timezone.utc)