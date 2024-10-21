from enum import IntEnum
from datetime import datetime, timedelta, timezone

class Rating(IntEnum):

    Fail = 0
    Pass = 1

class Card:

    box: int
    due: datetime

    def __init__(self):

        self.box = 1
        self.due = None

class ReviewLog:

    rating: int
    review_datetime: datetime
    box: int

    def __init__(self, rating, review_datetime, box):

        self.rating = rating
        self.review_datetime = review_datetime
        self.box = box

class LeitnerScheduler:

    box_intervals: list[int]
    start_datetime: datetime

    def __init__(self):

        self.box_intervals = [1, 2, 7] # how many days in between you review each box; default box1 - everyday, box2 - every 2 days, box3, every seven days
        self.start_datetime = datetime.now(timezone.utc)

    def review_card(self, card, rating):

        review_datetime = datetime.now(timezone.utc)

        review_log = ReviewLog(rating, review_datetime, card.box)

        if rating == Rating.Fail:

            card.box = 1

            # card will be due at the beginning of the next day
            # TODO: change this use self.box_intervals[0]
            card.due = (review_datetime + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        elif rating == Rating.Pass:

            if card.box < len(self.box_intervals):
                card.box += 1

            interval = self.box_intervals[card.box-1]

            begin_datetime = (self.start_datetime - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

            # TODO: find more efficient/clean way to find next due date
            i = 1
            next_due_date = begin_datetime + (timedelta(days=interval) * i)
            while next_due_date <= review_datetime:

                next_due_date = begin_datetime + (timedelta(days=interval) * i)

                i += 1

            card.due = next_due_date

        return card, review_log