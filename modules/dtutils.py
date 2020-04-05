from datetime import datetime, timedelta

def differential_date_str(dt):
        now = datetime.now()
        today = now.date()
        diff = now - dt
        if diff < timedelta(minutes=1):
            return 'now'
        if diff < timedelta(hours=1):
            return '{} minutes ago'.format(int(diff.total_seconds() / 60))
        if diff < timedelta(hours=2):
            return 'an hour ago'
        if dt.date() + timedelta(days=1) == today:
            return 'yesterday'
        if diff < timedelta(days=1):
            return '{} hours ago'.format(int(diff.total_seconds() / 60 / 60))
        if (dt.year == now.year and dt.month + 1 == now.month) or (dt.year + 1 == now.year and dt.month == 12 and now.month == 1):
            return 'last month'
        if diff < timedelta(days=31):
            return '{} days ago'.format(int(diff.total_seconds() / 60 / 60 / 24))
        if diff < timedelta(days=365):
            return '{} months ago'.format(int(diff.total_seconds() / 60 / 60 / 24 / 30))
        return '{} years ago'.format(int(diff.total_seconds() / 60 / 60 / 24 / 365))
