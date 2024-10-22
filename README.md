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
Rating.Fail # (=0) forgot the card
Rating.Pass # (=1) remembered the card
"""

rating = Rating.Pass

card, review_log = scheduler.review_card(card, rating)

print(f"Card in box {review_log.box}, rated {review_log.rating} \
on {review_log.review_datetime}")
# => Card in box 1, rated 1 on 2024-10-21 20:58:29.758259
```

See when the card is due next

```python
print(f"Card in box {card.box} due on {card.due}")
# => Card in box 2 due on 2024-10-22 00:00:00
```