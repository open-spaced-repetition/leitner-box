# leitner-box

Python package implementing the [Leitner system](https://en.wikipedia.org/wiki/Leitner_system) for spaced repetition scheduling.

### Quickstart


Import and initialize the Leitner scheduler

```python
from leitner_box import LeitnerScheduler, Card, Rating, ReviewLog

scheduler = LeitnerScheduler()
```

Create a new Card object

```python
card = Card()

print(f"card is in box {card.box}") # card is in box 1
```

Choose a rating and review the card

```python
"""
Rating.Fail # forgot the card
Rating.Pass # remembered the card
"""

rating = Rating.Pass

card, review_log = scheduler.review_card(card, rating)
```

See when the card is due next

```python
print(f"card is in box {card.box}") # card is in box 2
```