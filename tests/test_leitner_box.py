from leitner_box import Scheduler, Card, Rating, ReviewLog
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json
import pytest
from copy import deepcopy

class TestLeitnerBox:

    def test_basic_review_schedule(self):

        # create Leitner system at 2:30pm on Jan. 1, 2024
        start_datetime = datetime(2024, 1, 1, 14, 30, 0, 0)
        scheduler = Scheduler(start_datetime=start_datetime)

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
        scheduler = Scheduler(start_datetime=start_datetime, on_fail=on_fail)

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
        scheduler = Scheduler(start_datetime=start_datetime)

        # create new Card
        card = Card()

        assert card.box == 1
        assert card.due is None

        # fail the card 2:35pm on Jan. 1, 2024
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 1, 14, 35, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 1
        assert card.due == datetime(2024, 1, 2, 0, 0, 0, 0)
        assert card.due != datetime(2024, 1, 2, 0, 0, 0, 0, timezone.utc)

        # pass the card on Jan. 2
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 2, 0, 0, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        assert card.due == datetime(2024, 1, 4, 0, 0, 0, 0)

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
        assert card.due == datetime(2024, 1, 7, 0, 0, 0, 0)

        # pass card on Jan. 7
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 7, 0, 0, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card is still in box 3
        assert card.box == 3
        assert card.due == datetime(2024, 1, 14, 0, 0, 0, 0)

        # fail card on Jan. 14
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 14, 0, 0, 0, 0, timezone.utc)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card moves back to box 1
        assert card.box == 1
        assert card.due == datetime(2024, 1, 15, 0, 0, 0, 0)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 15, 0, 0, 0, 0, timezone.utc)

        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        # card is also due next day because that's a day that box 2 is repeated
        assert card.due == datetime(2024, 1, 16, 0, 0, 0, 0)

    def test_basic_review_schedule_with_la_timezone(self):

        # create Leitner system at 2:30pm on Jan. 1, 2024 UTC
        start_datetime = datetime(2024, 1, 1, 14, 30, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))
        scheduler = Scheduler(start_datetime=start_datetime)

        # create new Card
        card = Card()

        assert card.box == 1
        assert card.due is None

        # fail the card 2:35pm on Jan. 1, 2024
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 1, 14, 35, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 1
        assert card.due == datetime(2024, 1, 2, 0, 0, 0, 0)
        assert card.due != datetime(2024, 1, 2, 0, 0, 0, 0, timezone.utc)
        assert card.due != datetime(2024, 1, 2, 0, 0, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))

        # pass the card on Jan. 2
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 2, 0, 0, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        assert card.due == datetime(2024, 1, 4, 0, 0, 0, 0)

        # attempt to pass the card on Jan. 3 when it is not due
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 3, 0, 0, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))
        with pytest.raises(RuntimeError):
            card, review_log = scheduler.review_card(card, rating, review_datetime)

        # pass card on Jan. 4
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 4, 0, 0, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 3
        assert card.due == datetime(2024, 1, 7, 0, 0, 0, 0)

        # pass card on Jan. 7
        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 7, 0, 0, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card is still in box 3
        assert card.box == 3
        assert card.due == datetime(2024, 1, 14, 0, 0, 0, 0)

        # fail card on Jan. 14
        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 14, 0, 0, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        # card moves back to box 1
        assert card.box == 1
        assert card.due == datetime(2024, 1, 15, 0, 0, 0, 0)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 15, 0, 0, 0, 0, tzinfo=ZoneInfo('America/Los_Angeles'))

        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        # card is also due next day because that's a day that box 2 is repeated
        assert card.due == datetime(2024, 1, 16, 0, 0, 0, 0)

    def test_box_intervals(self):

        # create Leitner system at 2:30pm on Jan. 1, 2024
        box_intervals = [1,2,3,5]
        start_datetime = datetime(2024, 1, 1, 14, 30, 0, 0)
        scheduler = Scheduler(box_intervals=box_intervals, start_datetime=start_datetime)

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

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 4, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 3
        assert card.due == datetime(2024, 1, 6, 0, 0, 0, 0)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 6, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 4
        assert card.due == datetime(2024, 1, 10, 0, 0, 0, 0)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 10, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 4
        assert card.due == datetime(2024, 1, 15, 0, 0, 0, 0)

        rating = Rating.Fail
        review_datetime = datetime(2024, 1, 15, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 1
        assert card.due == datetime(2024, 1, 16, 0, 0, 0, 0)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 16, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 2
        assert card.due == datetime(2024, 1, 18, 0, 0, 0, 0)

        rating = Rating.Pass
        review_datetime = datetime(2024, 1, 18, 0, 0, 0, 0)
        card, review_log = scheduler.review_card(card, rating, review_datetime)

        assert card.box == 3
        assert card.due == datetime(2024, 1, 21, 0, 0, 0, 0)

    def test_serialize(self):

        scheduler = Scheduler()

        card = Card()
        old_card = deepcopy(card)

        # card and scheduler are json-serializable
        assert type(json.dumps(scheduler.to_dict())) is str
        assert type(json.dumps(card.to_dict())) is str

        # card can be serialized and de-serialized while remaining the same
        card_dict = card.to_dict()
        copied_card = Card.from_dict(card_dict)
        assert vars(card) == vars(copied_card)
        assert card.to_dict() == copied_card.to_dict()

        # scheduler can be serialized and de-serialized while remaining the same
        scheduler_dict = scheduler.to_dict()
        copied_scheduler = Scheduler.from_dict(scheduler_dict)
        assert vars(scheduler) == vars(copied_scheduler)
        assert scheduler.to_dict() == copied_scheduler.to_dict()

        # review the card and perform more tests
        rating = Rating.Pass
        review_duration = 3000
        card, review_log = scheduler.review_card(card=card, rating=rating, review_duration=review_duration)

        # review log is json-serializable
        assert type(json.dumps(review_log.to_dict())) is str

        # the new reviewed card can be serialized and de-serialized while remaining the same
        card_dict = card.to_dict()
        copied_card = Card.from_dict(card_dict)
        assert vars(card) == vars(copied_card)
        assert card.to_dict() == copied_card.to_dict()

        # review_log can be serialized and de-serialized while remaining the same
        review_log_dict = review_log.to_dict()
        copied_review_log = ReviewLog.from_dict(review_log_dict)
        assert review_log.to_dict() == copied_review_log.to_dict()
        assert copied_review_log.review_duration == review_duration
        # can use the review log to recreate the card that was reviewed
        assert old_card.to_dict() == Card.from_dict(review_log.to_dict()['card']).to_dict()