# Method

## 1. Match Similar Agents

Each synthetic activity row is matched to a de-identified real Veraset agent.
The primary match uses home TAZ, employment class, and activity type. When an
exact TAZ match is unavailable, the nearest same-employment agent observed
performing that activity is used.

## 2. Transfer Relative Trajectories

Absolute real-agent destinations cannot be copied directly because the
synthetic person may live elsewhere. The method preserves the displacement
between the real home and activity location:

```text
target_lat = synthetic_home_lat + real_activity_lat - real_home_lat
target_lon = synthetic_home_lon + real_activity_lon - real_home_lon
```

The production workflow also records the analogous TAZ offset:

```text
target_activity_taz =
    synthetic_home_taz + (real_activity_taz - real_home_taz)
```

Coordinates, rather than numeric TAZ identifiers alone, should be used for the
final distance calculation.

## 3. Assign POIs

For each translated target, the nearest POI compatible with the activity label
is selected. Production runs use spatial indices and hierarchical fallback
rings when the target TAZ contains no compatible POI.

## 4. Validate

Validation covers assignment success, distance distributions, activity
coverage, POI diversity, TAZ separation, and confidence/quality scores.
