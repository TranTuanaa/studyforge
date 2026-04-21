from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.study_frames import STUDY_FRAMES, STUDY_HOURS_PER_DAY, time_to_hour
from app.crud.class_schedule import get_class_schedules
from app.crud.fixed_time_slot import get_fixed_time_slots
from app.crud.subject import get_subjects


class StudyPlanService:
    ALLOCATION_STEP = 0.5

    def round_to_half_hour(self, hours: float) -> float:
        return round(hours * 2) / 2

    def get_busy_segments_within_frames(self, start_time, end_time) -> list[tuple[float, float]]:
        start_hour = time_to_hour(start_time)
        end_hour = time_to_hour(end_time)
        segments: list[tuple[float, float]] = []

        for frame_start, frame_end in STUDY_FRAMES:
            overlap_start = max(start_hour, frame_start)
            overlap_end = min(end_hour, frame_end)
            if overlap_end > overlap_start:
                segments.append((overlap_start, overlap_end))

        return segments

    def merge_overlapping_segments(self, segments: list[tuple[float, float]]) -> list[tuple[float, float]]:
        if not segments:
            return []

        sorted_segments = sorted(segments)
        merged = [sorted_segments[0]]

        for start, end in sorted_segments[1:]:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1] = (last_start, max(last_end, end))
            else:
                merged.append((start, end))

        return merged

    def calculate_daily_free_hours(
        self,
        days: int = 7,
        class_schedules: list[dict] | None = None,
        fixed_time_slots: list[dict] | None = None,
    ) -> list[float]:
        busy_segments_by_day: list[list[tuple[float, float]]] = [[] for _ in range(days)]

        for item in (class_schedules or []) + (fixed_time_slots or []):
            day = item.get("day_of_week")
            if day not in range(days):
                continue

            busy_segments_by_day[day].extend(
                self.get_busy_segments_within_frames(item["start_time"], item["end_time"])
            )

        daily_free_hours = []
        for segments in busy_segments_by_day:
            merged_segments = self.merge_overlapping_segments(segments)
            busy_hours = sum(end - start for start, end in merged_segments)
            daily_free_hours.append(round(max(0.0, STUDY_HOURS_PER_DAY - busy_hours), 2))

        return daily_free_hours

    def calculate_hour_allocation(self, subjects: list[dict], total_free_hours: float) -> list[dict]:
        if not subjects:
            return []

        total_priority = sum(subject.get("priority", 5) for subject in subjects)
        if total_priority <= 0:
            total_priority = len(subjects)
            for subject in subjects:
                subject["priority"] = 1

        subjects_by_priority = sorted(subjects, key=lambda subject: subject.get("priority", 5), reverse=True)

        hour_allocation = []
        remaining_hours = total_free_hours
        for subject in subjects_by_priority[:-1]:
            allocated_hours = self.round_to_half_hour(
                subject.get("priority", 5) / total_priority * total_free_hours
            )
            allocated_hours = min(allocated_hours, remaining_hours)
            hour_allocation.append(
                {
                    "subject": subject["name"],
                    "priority": subject.get("priority", 5),
                    "allocated_hours": allocated_hours,
                }
            )
            remaining_hours = round(remaining_hours - allocated_hours, 2)

        last_subject = subjects_by_priority[-1]
        hour_allocation.append(
            {
                "subject": last_subject["name"],
                "priority": last_subject.get("priority", 5),
                "allocated_hours": round(max(0.0, remaining_hours), 2),
            }
        )
        return hour_allocation

    def distribute_hours_across_days(
        self, hour_allocation: list[dict], daily_free_hours: list[float]
    ) -> list[dict]:
        remaining_daily_free_hours = daily_free_hours.copy()
        study_plan = []

        for item in sorted(hour_allocation, key=lambda value: value["priority"], reverse=True):
            remaining_hours = item["allocated_hours"]
            daily_hours = [0.0] * len(remaining_daily_free_hours)

            while remaining_hours > 0:
                allocated_in_round = False

                for day_index in range(len(remaining_daily_free_hours)):
                    if remaining_hours <= 0:
                        break

                    hours_to_add = min(
                        self.ALLOCATION_STEP,
                        remaining_hours,
                        remaining_daily_free_hours[day_index],
                    )
                    if hours_to_add <= 0:
                        continue

                    daily_hours[day_index] = round(daily_hours[day_index] + hours_to_add, 2)
                    remaining_daily_free_hours[day_index] = round(
                        remaining_daily_free_hours[day_index] - hours_to_add, 2
                    )
                    remaining_hours = round(remaining_hours - hours_to_add, 2)
                    allocated_in_round = True

                if not allocated_in_round:
                    break

            study_plan.append(
                {
                    "subject": item["subject"],
                    "allocated_hours": item["allocated_hours"],
                    "daily_hours": [round(hours, 2) for hours in daily_hours],
                }
            )

        return study_plan

    def generate_study_plan(
        self,
        subjects: list[dict],
        class_schedules: list[dict] | None = None,
        fixed_time_slots: list[dict] | None = None,
        days: int = 7,
    ) -> dict:
        daily_free_hours = self.calculate_daily_free_hours(days, class_schedules, fixed_time_slots)
        total_free_hours = round(sum(daily_free_hours), 2)
        hour_allocation = self.calculate_hour_allocation(subjects, total_free_hours)

        return {
            "status": "generated",
            "total_free_hours": total_free_hours,
            "study_plan": self.distribute_hours_across_days(hour_allocation, daily_free_hours),
            "message": (
                f"Priority-based study plan generated from {total_free_hours} free hours inside study frames."
            ),
        }


def subject_to_payload(subject) -> dict:
    return {
        "name": subject.name,
        "priority": subject.priority,
    }


def busy_time_block_to_payload(item) -> dict:
    return {
        "day_of_week": item.day_of_week,
        "start_time": item.start_time,
        "end_time": item.end_time,
    }


def build_study_plan(db: Session, service: StudyPlanService | None = None) -> dict:
    subjects = get_subjects(db, limit=None)
    if not subjects:
        raise HTTPException(status_code=400, detail="Add at least one subject before generating a study plan")

    plan_service = service or StudyPlanService()
    return plan_service.generate_study_plan(
        subjects=[subject_to_payload(subject) for subject in subjects],
        class_schedules=[busy_time_block_to_payload(item) for item in get_class_schedules(db, limit=None)],
        fixed_time_slots=[busy_time_block_to_payload(item) for item in get_fixed_time_slots(db, limit=None)],
        days=7,
    )
