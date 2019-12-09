import datetime as dt
import math
import statistics
from collections import deque


class FaceMetricsController:
    # Время жизни групп метрик. Если группа не обновлялась больше указанного
    # времени - она удаляется
    metric_group_live_time_sec = None

    # Максимальное количество групп
    max_groups_size = None

    # Точность, которой достаточно для того, что бы новые метрики попали в
    # текущую группу
    allowable_matching_precision = None

    # Метрики сгруппированные по подобию
    face_metrics_groups = []

    def __init__(self, max_groups_size=50, allowable_matching_precision=0.9,
                 metric_group_live_time_sec=5):
        self.max_group_size = max_groups_size
        self.allowable_matching_precision = allowable_matching_precision
        self.metric_group_live_time_sec = metric_group_live_time_sec
        self.max_groups_size = max_groups_size

    # face data is a tuple of (face_metrics, image_data)
    def put_metrics(self, face_data):
        fixation_time = dt.datetime.now()

        if self.face_metrics_groups.__len__() == 0:
            self.face_metrics_groups.append(
                FaceMetricsGroup(face_data, fixation_time))
            return

        # Тут мы тупо бежим по всем группам, пытаясь найти наиболее
        # подходяющу группу для входящего массива метрик
        best_matched_group = None
        best_similarity = 0
        for current_metrics_group in self.face_metrics_groups:
            assert isinstance(current_metrics_group, FaceMetricsGroup)
            current_similarity = current_metrics_group.calculate_similarity(
                face_data[0])
            if current_similarity > best_similarity:
                best_matched_group = current_metrics_group
                best_similarity = current_similarity

        if best_similarity >= self.allowable_matching_precision:
            assert isinstance(best_matched_group, FaceMetricsGroup)
            best_matched_group.add_metrics(face_data, fixation_time)
        else:
            self.face_metrics_groups.append(
                FaceMetricsGroup(face_data, fixation_time))
        self.clean()

    def get_active_groups(self):
        active_groups = []
        for group in self.face_metrics_groups:
            if group.face_data_stack.__len__() >= 8:
                active_groups.append(group.face_data_stack)
        return active_groups

    # Пока метод бежит по всем текущим группам и оставляет только те, которые
    # не протухли
    def clean(self):
        if self.face_metrics_groups.__len__() < self.max_groups_size:
            return

        actual_metrics_groups = []
        current_time = dt.datetime.now()
        for face_metrics_group in self.face_metrics_groups:
            assert isinstance(face_metrics_group, FaceMetricsGroup)
            last_update_time = face_metrics_group.last_update_time
            time_delta_sec = (current_time - last_update_time).total_seconds()
            if time_delta_sec <= self.metric_group_live_time_sec:
                actual_metrics_groups.append(face_metrics_group)

            if actual_metrics_groups.__len__() == self.max_groups_size:
                break

        print("Clean metrics groups: %d to %d" % (
            self.face_metrics_groups.__len__(),
            actual_metrics_groups.__len__()))
        self.face_metrics_groups = actual_metrics_groups


class FaceMetricsGroup:
    # Время последнего обновления группы
    last_update_time = None

    # Стек числовых лицевых метрик [0.1 -3.21 ...]
    face_data_stack = None

    def __init__(self, face_data, fixation_time):
        self.face_data_stack = deque(maxlen=8)
        self.add_metrics(face_data, fixation_time)

    def add_metrics(self, face_data, fixation_time):
        self.last_update_time = fixation_time
        self.face_data_stack.append(face_data)

    def get_last_update(self):
        return self.last_update_time

    # TODO Здесь надо подсчитать степень схожести face_metrics с метриками из
    #  текущей группы
    def calculate_similarity(self, face_metrics):
        match_results = [None] * self.face_data_stack.__len__()
        for face_idx in range(self.face_data_stack.__len__()):
            face = self.face_data_stack[face_idx][0]
            assert isinstance(face, list)
            matched_metrics_cnt = 0
            for metric_idx in range(face.__len__()):
                if math.fabs(face[metric_idx] - face_metrics[metric_idx]) < 0.6:
                    matched_metrics_cnt += 1
            match_results[face_idx] = matched_metrics_cnt / face.__len__()

        return statistics.mean(match_results)
