from django.db import migrations
import redis
import logging

logger = logging.getLogger(__name__)


def backfill_specs_from_redis_or_defaults(apps, schema_editor):
    BikeTrip = apps.get_model('bike_app', 'BikeTrip')
    from django.conf import settings

    r = None
    try:
        redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379')
        r = redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=2)
        r.ping()
    except Exception as e:
        logger.warning(f"[Migration 0009] Redis unavailable for backfill: {e}. Will use default specs.")
        r = None

    trips_to_backfill = BikeTrip.objects.filter(capacity__isnull=True) | BikeTrip.objects.filter(mileage__isnull=True)

    for trip in trips_to_backfill.distinct():
        updated = False
        capacity_val = trip.capacity
        mileage_val = trip.mileage

        # 1. Attempt to pull from legacy Redis hash 'trip:<id>:specs'
        if r is not None:
            try:
                specs_key = f"trip:{trip.id}:specs"
                specs = r.hgetall(specs_key)
                if specs:
                    if capacity_val is None and 'capacity' in specs:
                        try:
                            capacity_val = float(specs['capacity'])
                        except (ValueError, TypeError):
                            pass
                    if mileage_val is None and 'mileage' in specs:
                        try:
                            mileage_val = float(specs['mileage'])
                        except (ValueError, TypeError):
                            pass
            except Exception as e:
                logger.warning(f"[Migration 0009] Error reading Redis key trip:{trip.id}:specs: {e}")

        # 2. Sensible motorcycle touring fallbacks if still null
        if capacity_val is None:
            capacity_val = 15.0
        if mileage_val is None:
            mileage_val = 35.0

        if trip.capacity != capacity_val or trip.mileage != mileage_val:
            trip.capacity = capacity_val
            trip.mileage = mileage_val
            trip.save(update_fields=['capacity', 'mileage'])


class Migration(migrations.Migration):

    dependencies = [
        ('bike_app', '0008_biketrip_whatsapp_group_link'),
    ]

    operations = [
        migrations.RunPython(
            backfill_specs_from_redis_or_defaults,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
