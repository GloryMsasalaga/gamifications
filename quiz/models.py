from django.db import models
import json


class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    score = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    badges = models.CharField(max_length=500, blank=True, default="")
    current_question_id = models.IntegerField(default=1)  # Track current question per user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-score', '-updated_at']
    
    def __str__(self):
        return f"{self.phone_number} - Score: {self.score}"
    
    def add_badge(self, badge_emoji, badge_name):
        """Add a badge if not already present"""
        badge_text = f"{badge_emoji} {badge_name}"
        current_badges = self.badges.split(", ") if self.badges else []
        if badge_text not in current_badges:
            current_badges.append(badge_text)
            self.badges = ", ".join(current_badges)
    
    def has_badge(self, badge_name):
        """Check if user has a specific badge"""
        return badge_name in self.badges
    
    def get_badges_list(self):
        """Return badges as a list"""
        return [badge.strip() for badge in self.badges.split(", ") if badge.strip()]


class Question(models.Model):
    text = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=100)
    options = models.JSONField(default=list)  # Store answer choices as JSON array
    difficulty_level = models.IntegerField(default=1)  # 1=easy, 2=medium, 3=hard
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Q{self.id}: {self.text[:50]}..."
    
    def get_options_text(self):
        """Return formatted options for SMS"""
        if not self.options:
            return ""
        options_text = []
        letters = ['A', 'B', 'C', 'D']
        for i, option in enumerate(self.options):
            if i < len(letters):
                options_text.append(f"{letters[i]}) {option}")
        return "\n".join(options_text)
