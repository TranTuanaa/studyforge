from typing import Dict, List

from app.core.study_frames import STUDY_HOURS_PER_DAY, get_overlap_with_study_frames


class OptimizationService:
    ALLOCATION_STEP = 0.5

    def round_to_half(self, value: float) -> float:
        return round(value * 2) / 2

    def get_daily_free_time(
        self,
        days: int = 7,
        class_schedules: List[Dict] | None = None,
        fixed_slots: List[Dict] | None = None,
    ) -> List[float]:
        daily_free_time = [STUDY_HOURS_PER_DAY] * days

        for item in (class_schedules or []) + (fixed_slots or []):
            day = item.get("day_of_week")
            if day not in range(days):
                continue

            occupied = get_overlap_with_study_frames(item["start_time"], item["end_time"])
            daily_free_time[day] = round(max(0.0, daily_free_time[day] - occupied), 2)

        return daily_free_time

    def allocate_percentages(self, subjects: List[Dict], total_study_time: float) -> List[Dict]:
        if not subjects:
            return []

        total_priority = sum(subject.get("priority", 5) for subject in subjects)
        if total_priority <= 0:
            total_priority = len(subjects)
            for subject in subjects:
                subject["priority"] = 1

        subjects_by_priority = sorted(subjects, key=lambda subject: subject.get("priority", 5), reverse=True)

        allocation = []
        remaining = total_study_time
        for subject in subjects_by_priority[:-1]:
            hours = self.round_to_half(subject.get("priority", 5) / total_priority * total_study_time)
            hours = min(hours, remaining)
            allocation.append({"subject": subject["name"], "priority": subject.get("priority", 5), "hours": hours})
            remaining = round(remaining - hours, 2)

        last_subject = subjects_by_priority[-1]
        allocation.append(
            {
                "subject": last_subject["name"],
                "priority": last_subject.get("priority", 5),
                "hours": round(max(0.0, remaining), 2),
            }
        )
        return allocation

    def fill_schedule(self, allocation: List[Dict], daily_free_time: List[float]) -> List[Dict]:
        daily_free = daily_free_time.copy()
        schedule = []

        for item in sorted(allocation, key=lambda value: value["priority"], reverse=True):
            remaining = item["hours"]
            daily_hours = [0.0] * len(daily_free)

            while remaining > 0:
                allocated_in_pass = False

                for day in range(len(daily_free)):
                    if remaining <= 0:
                        break

                    hours = min(self.ALLOCATION_STEP, remaining, daily_free[day])
                    if hours <= 0:
                        continue

                    daily_hours[day] = round(daily_hours[day] + hours, 2)
                    daily_free[day] = round(daily_free[day] - hours, 2)
                    remaining = round(remaining - hours, 2)
                    allocated_in_pass = True

                if not allocated_in_pass:
                    break

            schedule.append(
                {
                    "subject": item["subject"],
                    "daily_hours": [round(hours, 2) for hours in daily_hours],
                    "total_hours": item["hours"],
                }
            )

        return schedule

    def optimize_schedule(
        self,
        subjects: List[Dict],
        class_schedules: List[Dict] | None = None,
        fixed_slots: List[Dict] | None = None,
        days: int = 7,
    ) -> Dict:
        daily_free_time = self.get_daily_free_time(days, class_schedules, fixed_slots)
        real_free_time = round(sum(daily_free_time), 2)
        allocation = self.allocate_percentages(subjects, real_free_time)

        return {
            "status": "Optimal",
            "objective_value": real_free_time,
            "schedule": self.fill_schedule(allocation, daily_free_time),
            "message": f"Real available study time inside study frames: {real_free_time} hours",
        }
