# leitner-box

Python package implementing the [Leitner system](https://en.wikipedia.org/wiki/Leitner_system) for spaced repetition scheduling.

## Quickstart


Import and initialize the Leitner scheduler

```python
from leitner_box import LeitnerScheduler, Card, Rating, ReviewLog

scheduler = LeitnerScheduler()
```

Create a new Card object

```python
card = Card()

print(f"Card is in box {card.box}")
 # => Card is in box 1
```

Choose a rating and review the card

```python
"""
Rating.Fail # (==0) forgot the card
Rating.Pass # (==1) remembered the card
"""

rating = Rating.Pass

card, review_log = scheduler.review_card(card, rating)

print(f"Card in box {review_log.box} rated {review_log.rating} \
on {review_log.review_datetime}")
# => Card in box 1 rated 1 on 2024-10-21 20:58:29.758259
```

See when the card is due next

```python
print(f"Card in box {card.box} due on {card.due}")
# => Card in box 2 due on 2024-10-22 00:00:00
```

## Usage

### The scheduler

The `LeitnerScheduler` has three parameters: 1) `box_intervals`, 2) `start_datetime`, and 3) `on_fail`.

#### `box_intervals` 
is a list of integers corresponding to the interval lengths of each box. 

In the following example, cards in box 1 are reviewed every day, cards in box 2 are reviewed every 2 days and cards in box 3 are reviewed every 7 days. There are only three boxes in this example.

```python
box_intervals = [1,2,7] # this also the default
scheduler = LeitnerScheduler(box_intervals=box_intervals)
```

Note: in the current version of this package, the interval for box 1 must always be set 1 day. There may be more flexible options in future versions.

#### `start_datetime` 
is the datetime that you first created the Leitner System. It is an important parameter in determining when the cards in each box are reviewed. It should be noted that the important information lies in which day the Leitner System was created, not the exact hour, minute, etc. This is because because the scheduler schedules cards to be due at the beginning of each day.

```python
from datetime import datetime

start_datetime = datetime.now() # also default datetime if not specified

scheduler = LeitnerScheduler(start_datetime=start_datetime)

print(f"Scheduler created on {scheduler.start_datetime}")
# => Scheduler created on 2024-10-21 21:15:23.491825

card = Card()

rating = Rating.Pass
card, review_log = scheduler.review_card(card, rating)

print(f"Card is due on {card.due}")
# => Card is due on 2024-10-22 00:00:00
```

In the above example, even though the scheduler was created in the evening of 2024-10-21 (and the card was also reviewed late in the evening of 2024-10-21), the card becomes due first thing the next day - *not* a full 24 hours later.

#### `on_fail`

has two possible values 1) `first_box` or 2) `prev_box`.

If `on_fail='first_box'`, cards that are failed will be put back in box 1 and if `on_fail='prev_box'`, failed cards will be put in the previous box. `on_fail='first_box'` is the default.

### Serialization

`LeitnerScheduler`, `Card` and `ReviewLog` objects are all json-serializable via their `to_dict` and `from_dict` methods for easy database storage:

```python
# serialize before storage
scheduler_dict = scheduler.to_dict()
card_dict = card.to_dict()
review_log_dict = review_log.to_dict()

# deserialize from dict
scheduler = LeitnerScheduler(scheduler_dict)
card = Card.from_dict(card_dict)
review_log = ReviewLog.from_dict(review_log_dict)
```

### Best practices

**Re-use the same scheduler for the same cards**

```python
scheduler = LeitnerScheduler(box_intervals=[1,2,7])
card = Card()

rating = Rating.Pass
card, review_log = scheduler.review_card(card, rating)

# (...wait till next day)

different_scheduler = LeitnerScheduler(box_intervals=[1,2,3,4,5])

rating = Rating.Pass
#card, review_log = different_scheduler.review_card(card, rating) # wrong
card, review_log = scheduler.review_card(card, rating) # correct
```

In general, you should continue using the same scheduler that you first reviewed the card with. Otherwise this could lead to scheduling issues.

**Check if a card is due before attempting to review it**

If you try to review a card that is not due, you will get an error:
```python
print(f"Card is due on {card.due}")
# => Card is due on 2024-10-22 00:00:00

print(f"Current datetime: {datetime.now()}")
# => Current datetime: 2024-10-21 21:15:23.491825

rating = Rating.Pass
card, review_log = scheduler.review_card(card, rating)
# RuntimeError: Card is not due for review until 2024-10-22 00:00:00.
```

**Be explicit about datetimes and use a local timezone**

Even though you can initialize the scheduler and review cards without explicitly specifying a time (it defaults to `datetime.now()`), you should consider explicitly specifying the datetimes with local timezones included if you plan on building any sort of application.

```python
from leitner_box import LeitnerScheduler, Card, Rating, ReviewLog
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# e.g., if you're in Los Angeles
start_datetime = datetime.now(ZoneInfo('America/Los_Angeles'))
scheduler = LeitnerScheduler(start_datetime=start_datetime)

card = Card()

rating = Rating.Pass
review_datetime = datetime.now(ZoneInfo('America/Los_Angeles'))
card, review_log = scheduler.review_card(card, rating, review_datetime)
```

To re-iterate, the reason you should opt for a local timezone is because the `LeitnerScheduler` schedules cards at the beginning of each day, and when each day begins depends on the timezone of the user. 