from datetime import time

STUDY_FRAMES = ((7.0, 11.0), (13.0, 17.0), (19.0, 22.0))
STUDY_HOURS_PER_DAY = sum(end - start for start, end in STUDY_FRAMES)


def time_to_hour(value: time | str) -> float:
    if isinstance(value, time):
        return value.hour + value.minute / 60

    parts = str(value).split(":")
    if len(parts) < 2:
        raise ValueError("Time must use HH:MM format")

    return int(parts[0]) + int(parts[1]) / 60


def is_within_study_frames(start_time: time, end_time: time) -> bool:
    start_hour = time_to_hour(start_time)
    end_hour = time_to_hour(end_time)
    return any(start <= start_hour and end_hour <= end for start, end in STUDY_FRAMES)


def get_overlap_with_study_frames(start_time: time | str, end_time: time | str) -> float:
    start_hour = time_to_hour(start_time)
    end_hour = time_to_hour(end_time)
    overlap = 0.0

    for frame_start, frame_end in STUDY_FRAMES:
        overlap_start = max(start_hour, frame_start)
        overlap_end = min(end_hour, frame_end)
        if overlap_end > overlap_start:
            overlap += overlap_end - overlap_start

    return round(overlap, 2)
