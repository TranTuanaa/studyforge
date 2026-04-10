from typing import List, Dict, Any
import math
from datetime import time

class OptimizationService:
    def __init__(self):
        self.prob = None

    def round_to_half(self, x: float) -> float:
        return round(x * 2) / 2

    def is_in_allowed_frame(self, start, end) -> bool:
        """Kiểm tra slot có giao với 3 khung giờ cho phép không"""
        allowed_frames = [(7, 11), (13, 17), (19, 22)]
        s = self._to_hour(start)
        e = self._to_hour(end)
        for frame_start, frame_end in allowed_frames:
            if max(s, frame_start) < min(e, frame_end):
                return True
        return False

    def _to_hour(self, t) -> float:
        """Chuyển thời gian thành số giờ (hỗ trợ string và datetime.time)"""
        if isinstance(t, time):
            return t.hour + t.minute / 60.0
        else:
            return float(str(t)[:2]) + float(str(t)[3:5]) / 60.0

    def get_duration(self, start, end) -> float:
        """Tính số tiếng"""
        return self._to_hour(end) - self._to_hour(start)

    def calculate_real_free_time(self, days: int = 7, class_schedules: List[Dict] = None, fixed_slots: List[Dict] = None) -> float:
        """Tính thời gian rảnh thực tế - CHỈ trừ phần nằm trong 3 khung giờ"""
        if class_schedules is None:
            class_schedules = []
        if fixed_slots is None:
            fixed_slots = []

        total_possible = 11.0 * days

        occupied = 0.0

        # Chỉ trừ class_schedule nằm trong 3 khung giờ
        for cs in class_schedules:
            if self.is_in_allowed_frame(cs.get("start_time"), cs.get("end_time")):
                occupied += self.get_duration(cs.get("start_time"), cs.get("end_time"))

        # Chỉ trừ fixed_slot nằm trong 3 khung giờ
        for fs in fixed_slots:
            if self.is_in_allowed_frame(fs.get("start_time"), fs.get("end_time")):
                occupied += self.get_duration(fs.get("start_time"), fs.get("end_time"))

        real_free_time = max(0.0, total_possible - occupied)
        return round(real_free_time, 2)

    # Phần allocate_percentages, fill_schedule, optimize_schedule giữ nguyên như trước
    def allocate_percentages(self, subjects: List[Dict], total_study_time: float) -> List[Dict]:
        if not subjects:
            return []
        total_priority = sum(s.get("priority", 5) for s in subjects)
        if total_priority == 0:
            total_priority = len(subjects) * 5

        sorted_subjects = sorted(subjects, key=lambda s: s.get("priority", 5), reverse=True)
        allocation = []
        used_hours = 0.0

        for s in sorted_subjects[:-1]:
            percent = (s.get("priority", 5) / total_priority) * 100
            hours_raw = (percent / 100) * total_study_time
            hours = self.round_to_half(hours_raw)
            allocation.append({
                "subject": s.get("name"),
                "priority": s.get("priority", 5),
                "percent": round(percent, 2),
                "hours": hours
            })
            used_hours += hours

        highest = sorted_subjects[-1]
        remaining_hours = round(total_study_time - used_hours, 2)

        allocation.append({
            "subject": highest.get("name"),
            "priority": highest.get("priority", 5),
            "percent": round((highest.get("priority", 5) / total_priority) * 100, 2),
            "hours": remaining_hours
        })
        return allocation

    def fill_schedule(self, allocation: List[Dict], days: int = 7) -> List[Dict]:
        sorted_alloc = sorted(allocation, key=lambda x: x["priority"], reverse=True)
        schedule = []
        daily_free = [11.0] * days

        for item in sorted_alloc:
            remaining = item["hours"]
            daily_hours = [0.0] * days
            for d in range(days):
                if remaining <= 0:
                    break
                can_fill = min(4.0, remaining, daily_free[d])
                if can_fill > 0:
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
        real_free_time = self.calculate_real_free_time(days, class_schedules, fixed_slots)
        allocation = self.allocate_percentages(subjects, real_free_time)
        schedule = self.fill_schedule(allocation, days)

        return {
            "status": "Optimal",
            "objective_value": real_free_time,
            "schedule": schedule,
            "message": f"Thời gian rảnh thực tế: {real_free_time} tiếng (đã trừ đúng phần trong 3 khung giờ)"
        }