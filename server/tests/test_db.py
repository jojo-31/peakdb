import os
import pytest

os.environ["MONGODB_HOSTNAME"] = "localhost"
os.environ["MONGODB_PORT"] = "27017"
os.environ["MONGODB_DATABASE"] = "peaks"
from database import db

PEAKS = [
    {"name": "Mont Valier", "altitude": 2838, "position": [42.79778, 1.08556]},
    {"name": "Pic de Maubermé", "altitude": 2880, "position": [42.79417, 0.91722]},
    {"name": "Pic de Crabère", "altitude": 2630, "position": [42.826039, 0.858633]},
]


@pytest.fixture
def db_instance():
    instance = db.DB()
    instance.db.posts.delete_many({})
    instance.db.posts.insert_many(PEAKS)
    return instance


def check_peaks_equal(peak, expected_peak):
    for prop in ["name", "altitude", "position"]:
        assert peak[prop] == expected_peak[prop]


def check_peak_list_equal(peaks, expected_peaks):
    for peak, expected_peak in zip(
        sorted(peaks, key=lambda x: x["name"]),
        sorted(expected_peaks, key=lambda x: x["name"]),
    ):
        check_peaks_equal(peak, expected_peak)


def test_get_peaks(db_instance):
    peaks = db_instance.get_peaks()
    check_peak_list_equal(peaks, PEAKS)


def test_add_peak(db_instance):
    new_peak = {"id": "", "name": "new", "altitude": 200, "position": [14, 20]}
    assert db_instance.add_peak(new_peak)

    peaks = db_instance.get_peaks()
    check_peak_list_equal(peaks, PEAKS + [new_peak])

    wrong_peak = {"id": "", "pouet": "new", "altitude": 200}
    with pytest.raises(KeyError):
        db_instance.add_peak(wrong_peak)

    wrong_peak = {"pouet": "new", "altitude": 200, "position": [14, 20]}
    with pytest.raises(KeyError):
        db_instance.add_peak(wrong_peak)

    peaks = db_instance.get_peaks()
    check_peak_list_equal(peaks, PEAKS + [new_peak])


def test_update_peak(db_instance):
    peaks = db_instance.get_peaks()
    peak_to_update = peaks[0]
    id_ = peak_to_update["id"]
    peak_to_update["name"] = "updated"
    peak_to_update["position"] = [4.1, 5.2]
    peak_to_update["altitude"] = 200.5

    assert db_instance.update_peak(id_, peak_to_update)

    peaks = db_instance.get_peaks()
    check_peak_list_equal(peaks, [peak_to_update] + PEAKS[1:])
    peak_to_update = peaks[0]
    peak_to_update["name"] = "updated2"
    peak_to_update["position"] = [1, 2]
    peak_to_update["altitude"] = 0.2

    assert db_instance.update_peak(id_, peak_to_update)

    peaks = db_instance.get_peaks()
    check_peak_list_equal(peaks, [peak_to_update] + PEAKS[1:])


def test_remove_peak(db_instance):
    peaks = db_instance.get_peaks()
    id_to_remove = peaks[0]["id"]

    assert db_instance.remove_peak(id_to_remove)

    updated_peaks = db_instance.get_peaks()
    check_peak_list_equal(updated_peaks, PEAKS[1:])

    assert not db_instance.remove_peak(id_to_remove)

    assert not db_instance.remove_peak("5f7855a1aadc9ab77b33fbb6")

    new_peak = {"id": "", "name": "new", "altitude": 200, "position": [14, 20]}
    new_peak = db_instance.add_peak(new_peak)
    assert db_instance.remove_peak(new_peak["id"])
    check_peak_list_equal(updated_peaks, PEAKS[1:])


def test_get_peaks_in_bb(db_instance):
    all_peaks = db_instance.get_peaks_in_bb([0, 0], [50, 50])

    check_peak_list_equal(all_peaks, PEAKS)

    no_peaks = db_instance.get_peaks_in_bb([-50, -50], [0, 0])
    assert no_peaks == []

    first_peak = db_instance.get_peaks_in_bb([42.79, 1.085], [42.8, 1.09])
    check_peak_list_equal(first_peak, [PEAKS[0]])