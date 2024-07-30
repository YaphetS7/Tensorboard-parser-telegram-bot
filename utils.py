from tensorboard.backend.event_processing import event_accumulator
from collections import defaultdict
from typing import Dict, List, Any
import os
import io
from tensorboard.backend.event_processing import event_accumulator
from collections import defaultdict
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import matplotlib
from config import F_SCORES_DEFAULT_TITLE, LOSSES_DEFAULT_TITLE

matplotlib.use('agg')


def read_scalars_from_tfevents_tensorboardx(file_path: str) -> Dict[str, List[Any]]:
    """Чтение скалярных значений из `.tfevents` файла с помощью `tensorboardX`.

    Args:
        file_path (str): Путь к файлу `.tfevents`.

    Returns:
        Dict[str, List[Any]]: Словарь, где ключи — имена скаляров, а значения — списки значений скаляров.
    """
    scalars = defaultdict(list)

    ea = event_accumulator.EventAccumulator(file_path)
    ea.Reload()

    for tag in ea.Tags()['scalars']:
        events = ea.Scalars(tag)
        scalars[tag] = [event.value for event in events]

    return scalars




def parse_tfevent(path):
    common_d = dict()

    for feature in os.listdir(path):
        if 'tfevents' in feature:
            continue

        cur_path = os.path.join(path, feature)
        common_d[feature] = []

        for tfevent in os.listdir(cur_path):
            path2event = os.path.join(cur_path, tfevent)
            cur_d = read_scalars_from_tfevents_tensorboardx(path2event)

            common_d[feature] = list(cur_d.values())[0]

    return common_d


def get_all_paths(root):
  return os.listdir(root)




def draw(
        xlabel,
        data_dict,
        f_score_title: str = F_SCORES_DEFAULT_TITLE,
        losses_title: str = LOSSES_DEFAULT_TITLE,
):
    fiure, (f_scores_ax, losses_ax)= plt.subplots(1, 2, figsize=(15, 5))
    for k, v in data_dict.items():
        # plt.plot(v, label=k)
        if 'f-scores' in k.lower():
            f_scores_ax.plot(v, label=k)
        elif 'losses' in k.lower():
            losses_ax.plot(v, label=k)
    f_scores_ax.set_title(f_score_title)
    f_scores_ax.legend()
    f_scores_ax.set_xlabel(xlabel)
    losses_ax.set_title(losses_title)
    losses_ax.legend()
    losses_ax.set_xlabel(xlabel)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer