from enum import IntEnum
from datetime import datetime, timedelta
from typing import Optional, Union, Any

class Rating(IntEnum):

    Fail = 0
    Pass = 1

class Card:

    box: int
    due: Optional[datetime]

    def __init__(self, box: int=1, due: Optional[datetime]=None) -> None:

        self.box = box
        self.due = due

    def to_dict(self) -> dict[str, Union[int, str]]:

        return_dict: dict[str, Union[int, str]] = {
            "box": self.box,
        }

        if self.due is not None:

            return_dict["due"] = self.due.isoformat()

        return return_dict
    
    @staticmethod
    def from_dict(source_dict: dict[str, Any]) -> "Card":

        box = int(source_dict['box'])

        if "due" in source_dict:

            due = datetime.fromisoformat(source_dict["due"])
        else:
            due = None

        return Card(box=box, due=due)


class ReviewLog:

    rating: Rating
    review_datetime: datetime
    box: int

    def __init__(self, rating: Rating, review_datetime: datetime, box: int) -> None:

        self.rating = rating
        self.review_datetime = review_datetime
        self.box = box

    def to_dict(self) -> dict[str, Union[int, str]]:

        return_dict = {
            "rating": self.rating.value,
            "review_datetime": self.review_datetime.isoformat(),
            "box": self.box
        }

        return return_dict
    
    @staticmethod
    def from_dict(source_dict: dict[str, Any]) -> "ReviewLog":

        rating = Rating(int(source_dict["rating"]))
        review_datetime = datetime.fromisoformat(source_dict["review_datetime"])
        box = int(source_dict["box"])

        return ReviewLog(rating=rating, review_datetime=review_datetime, box=box)

class LeitnerScheduler:

    box_intervals: list[int]
    start_datetime: datetime
    on_fail: str

    def __init__(self, box_intervals: list[int]=[1, 2, 7], start_datetime: Optional[datetime]=None, on_fail: str='first_box') -> None:

        if box_intervals[0] != 1:

            raise ValueError("Box 1 must have an interval of 1 day. This may change in future versions.")

        self.box_intervals = box_intervals # how many days in between you review each box; default box1 - everyday, box2 - every 2 days, box3, every seven days
        if start_datetime is None:
            self.start_datetime = datetime.now()
        else:
            self.start_datetime = start_datetime

        self.on_fail = on_fail

    def review_card(self, card: Card, rating: Rating, review_datetime: Optional[datetime]=None) -> tuple[Card, ReviewLog]:

        # the card to be returned after review
        new_card = Card(box=card.box, due=card.due)

        if review_datetime is None:
            review_datetime = datetime.now()

        if new_card.due is None:
            new_card.due = review_datetime.replace(hour=0, minute=0, second=0, microsecond=0) # beginning of the day of review

        card_is_due = review_datetime >= new_card.due
        if not card_is_due:
            raise RuntimeError(f"Card is not due for review until {new_card.due}.")

        review_log = ReviewLog(rating, review_datetime, new_card.box)

        if rating == Rating.Fail:

            if self.on_fail == 'first_box':
                new_card.box = 1
            elif self.on_fail == 'prev_box' and new_card.box > 1:
                new_card.box -= 1

        elif rating == Rating.Pass:

            if new_card.box < len(self.box_intervals):
                new_card.box += 1

        interval = self.box_intervals[new_card.box-1]

        begin_datetime = (self.start_datetime - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        i = 1
        next_due_date = begin_datetime + (timedelta(days=interval) * i)
        while next_due_date <= review_datetime:

            next_due_date = begin_datetime + (timedelta(days=interval) * i)
            i += 1

        new_card.due = next_due_date

        return new_card, review_log
    
    def to_dict(self) -> dict[str, Union[list[int], int, str]]:

        return_dict: dict[str, Union[list[int], int, str]] = {
            "box_intervals": self.box_intervals,
            "start_datetime": self.start_datetime.isoformat(),
            "on_fail": self.on_fail
        }

        return return_dict
    
    @staticmethod
    def from_dict(source_dict: dict[str, Any]) -> "LeitnerScheduler":

        box_intervals = source_dict['box_intervals']
        start_datetime = datetime.fromisoformat(source_dict['start_datetime'])
        on_fail = source_dict['on_fail']

        return LeitnerScheduler(box_intervals=box_intervals, start_datetime=start_datetime, on_fail=on_fail)