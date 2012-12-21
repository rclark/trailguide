## trailguide: manage information about trails

### Installation
1. This app depends on GeoDjango and PostGIS. Make sure that they are installed correctly. Also make sure that GDAL is properly installed by checking the following:

        ./manage.py shell
        from django.contrib.gis import gdal
        gdal.HAS_GDAL # Should return True
        
2. Clone this repository into your Django project directory.
3. Add `trailguide` to your settings.INSTALLED_APPS.
4. Add the following custom settings to settings.py:

        # Indicate the model that persists a user's profile
        AUTH_PROFILE_MODULE = 'trailguide.UserProfile'