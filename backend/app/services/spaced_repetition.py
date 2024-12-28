from datetime import datetime, timedelta
import math

class SpacedRepetition:
    """
    Implementation of SuperMemo 2 algorithm with modifications for ADHD support
    """
    
    @staticmethod
    def calculate_next_review(quality: int, ease_factor: float, interval: int) -> tuple[int, float]:
        """
        Calculate the next review interval and ease factor based on the quality of recall
        
        Args:
            quality: Integer from 0 to 5 representing recall quality
            ease_factor: Current ease factor
            interval: Current interval in days
            
        Returns:
            tuple: (new_interval, new_ease_factor)
        """
        if quality < 3:
            # If failed, reset interval but maintain some progress for ADHD support
            new_interval = max(1, int(interval * 0.5))
            # Reduce ease factor but not too drastically
            new_ease_factor = max(1.3, ease_factor - 0.15)
        else:
            if interval == 0:
                new_interval = 1
            elif interval == 1:
                new_interval = 6
            else:
                new_interval = int(interval * ease_factor)
            
            # Update ease factor
            new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            new_ease_factor = max(1.3, new_ease_factor)
        
        # Cap maximum interval at 365 days for ADHD support
        new_interval = min(new_interval, 365)
        
        return new_interval, new_ease_factor
    
    @staticmethod
    def get_next_review_date(interval: int) -> datetime:
        """Calculate the next review date based on the interval"""
        return datetime.now() + timedelta(days=interval)
    
    @staticmethod
    def get_due_cards(cards: list, limit: int = 20) -> list:
        """
        Get cards that are due for review, prioritizing:
        1. Overdue cards
        2. New cards
        3. Cards with lower ease factors
        """
        now = datetime.now()
        due_cards = [
            card for card in cards 
            if card.next_review is None or card.next_review <= now
        ]
        
        # Sort by priority
        due_cards.sort(key=lambda c: (
            c.next_review is None,  # New cards second
            c.next_review if c.next_review else now,  # Overdue cards first
            c.ease_factor  # Lower ease factor cards first
        ))
        
        return due_cards[:limit]
