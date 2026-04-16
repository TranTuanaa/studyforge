from typing import List, Dict
import math
from datetime import time

class OptimizationService:
    def round_to_half(self, x: float) -> float:
        return round(x * 2) / 2

    def get_duration(self, start, end) -> float:
        """Hỗ trợ cả str và datetime.time"""
        def to_hour(t):
            if isinstance(t, time):
                return t.hour + t.minute / 60.0
            return float(str(t)[:2]) + float(str(t)[3:5]) / 60.0
        return to_hour(end) - to_hour(start)

    def calculate_real_free_time(self, days: int = 7, class_schedules: List[Dict] = None, fixed_slots: List[Dict] = None) -> float:
        total_possible = 11.0 * days
        occupied = 0.0

        for cs in (class_schedules or []):
            occupied += self.get_duration(cs.get("start_time"), cs.get("end_time"))
        for fs in (fixed_slots or []):
            occupied += self.get_duration(fs.get("start_time"), fs.get("end_time"))

        return round(max(0.0, total_possible - occupied), 2)

    def allocate_percentages(self, subjects: List[Dict], total_study_time: float) -> List[Dict]:
        if not subjects:
            return []
        total_priority = sum(s.get("priority", 5) for s in subjects) or len(subjects) * 5
        sorted_subjects = sorted(subjects, key=lambda s: s.get("priority", 5), reverse=True)

        allocation = []
        used = 0.0
        for s in sorted_subjects[:-1]:
            percent = (s.get("priority", 5) / total_priority) * 100
            hours = self.round_to_half((percent / 100) * total_study_time)
            allocation.append({"subject": s["name"], "priority": s.get("priority", 5), "hours": hours})
            used += hours

        # Môn cao nhất lấy phần còn lại
        highest = sorted_subjects[-1]
        remaining = round(total_study_time - used, 2)
        allocation.append({"subject": highest["name"], "priority": highest.get("priority", 5), "hours": remaining})
        return allocation

    def fill_schedule(self, allocation: List[Dict], days: int = 7) -> List[Dict]:
        daily_free = [11.0] * days
        schedule = []
        for item in sorted(allocation, key=lambda x: x["priority"], reverse=True):
            remaining = item["hours"]
            daily_hours = [0.0] * days
            for d in range(days):
                if remaining <= 0:
                    break
                can_fill = min(4.0, remaining, daily_free[d])
                daily_hours[d] = can_fill
                daily_free[d] -= can_fill
                remaining -= can_fill
            schedule.append({
                "subject": item["subject"],
                "daily_hours": [round(h, 2) for h in daily_hours],
                "total_hours": item["hours"]
            })
        return schedule

    def optimize_schedule(self, subjects: List[Dict], class_schedules: List[Dict] = None, fixed_slots: List[Dict] = None, days: int = 7) -> Dict:
        real_free = self.calculate_real_free_time(days, class_schedules, fixed_slots)
        allocation = self.allocate_percentages(subjects, real_free)
        schedule = self.fill_schedule(allocation, days)

        return {
            "status": "Optimal",
            "objective_value": real_free,
            "schedule": schedule,
            "message": f"Thời gian rảnh thực tế: {real_free} tiếng (3 khung giờ)"
        }