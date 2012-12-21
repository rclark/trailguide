## trailguide: manage information about trails

### Installation
1. Clone this repository into your Django project directory.
2. Add `trailguide` to your settings.INSTALLED_APPS.
3. Add the following custom settings to settings.py:

        # Indicate the model that persists a user's profile
        AUTH_PROFILE_MODULE = 'trailguide.UserProfile'