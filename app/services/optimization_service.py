from datetime import time
from typing import Dict, List


class OptimizationService:
    def round_to_half(self, value: float) -> float:
        return round(value * 2) / 2

    def get_duration(self, start, end) -> float:
        def to_hour(value) -> float:
            if isinstance(value, time):
                return value.hour + value.minute / 60
            return float(str(value)[:2]) + float(str(value)[3:5]) / 60

        return to_hour(end) - to_hour(start)

    def calculate_real_free_time(
        self,
        days: int = 7,
        class_schedules: List[Dict] | None = None,
        fixed_slots: List[Dict] | None = None,
    ) -> float:
        total_possible = 11.0 * days
        occupied = 0.0

        for item in class_schedules or []:
            occupied += self.get_duration(item["start_time"], item["end_time"])
        for item in fixed_slots or []:
            occupied += self.get_duration(item["start_time"], item["end_time"])

        return round(max(0.0, total_possible - occupied), 2)

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
        used = 0.0
        for subject in subjects_by_priority[:-1]:
            hours = self.round_to_half(subject.get("priority", 5) / total_priority * total_study_time)
            allocation.append({"subject": subject["name"], "priority": subject.get("priority", 5), "hours": hours})
            used += hours

        last_subject = subjects_by_priority[-1]
        allocation.append(
            {
                "subject": last_subject["name"],
                "priority": last_subject.get("priority", 5),
                "hours": round(total_study_time - used, 2),
            }
        )
        return allocation

    def fill_schedule(self, allocation: List[Dict], days: int = 7) -> List[Dict]:
        daily_free = [11.0] * days
        schedule = []

        for item in sorted(allocation, key=lambda value: value["priority"], reverse=True):
            remaining = item["hours"]
            daily_hours = [0.0] * days

            for day in range(days):
                if remaining <= 0:
                    break

                hours = min(4.0, remaining, daily_free[day])
                daily_hours[day] = hours
                daily_free[day] -= hours
                remaining -= hours

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
        real_free_time = self.calculate_real_free_time(days, class_schedules, fixed_slots)
        allocation = self.allocate_percentages(subjects, real_free_time)

        return {
            "status": "Optimal",
            "objective_value": real_free_time,
            "schedule": self.fill_schedule(allocation, days),
            "message": f"Real available study time: {real_free_time} hours",
        }
