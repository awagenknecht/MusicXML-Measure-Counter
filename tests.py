# Test cases for xml_measure_counter

import unittest
from unittest.mock import MagicMock
import xml_measure_counter
import music21
import tkinter as tk

class TestXMLMeasureCounter(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = xml_measure_counter.App(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_reset(self):
        self.app.total_measures = 10
        self.app.reset()
        self.assertEqual(self.app.total_measures, 0)

    def test_get_total_measures(self):
        score = music21.stream.Score()
        part = music21.stream.Part()
        measure = music21.stream.Measure()
        note = music21.note.Note(quarterLength=4)
        measure.append(note)
        part.append(measure)
        score.append(part)
        self.assertEqual(self.app.get_total_measures(score), 1)

    def test_get_total_measures_no_measures(self):
        score = music21.stream.Score()
        part = music21.stream.Part()
        score.append(part)
        self.assertEqual(self.app.get_total_measures(score), 0)

    def test_get_total_measures_duration_proportion_not_1(self):
        score = music21.stream.Score()
        part = music21.stream.Part()
        measure = music21.stream.Measure()
        measure.barDurationProportion = MagicMock(return_value=0.5)
        part.append(measure)
        score.append(part)
        self.assertEqual(self.app.get_total_measures(score), 0)

    def test_get_total_measures_multiple_parts(self):
        score = music21.stream.Score()
        part1 = music21.stream.Part()
        measure1 = music21.stream.Measure()
        note1 = music21.note.Note(quarterLength=4)
        measure1.append(note1)
        measure2 = music21.stream.Measure()
        measure2.append(note1)
        part1.append(measure1)
        part1.append(measure2)
        part2 = music21.stream.Part()
        measure3 = music21.stream.Measure()
        measure3.append(note1)
        part2.append(measure3)
        score.append(part1)
        score.append(part2)
        self.assertEqual(self.app.get_total_measures(score), 3)

    def test_parse_parts_to_exclude(self):
        self.assertEqual(self.app.parse_parts_to_exclude("Violin , Piano"), {"Violin", "Piano"})

    def test_get_total_measures_excluded_part(self):
        score = music21.stream.Score()
        part1 = music21.stream.Part()
        part1.partName = "Violin"
        measure1 = music21.stream.Measure()
        note1 = music21.note.Note(quarterLength=4)
        measure1.append(note1)
        part1.append(measure1)
        part2 = music21.stream.Part()
        part2.partName = "Piano"
        measure2 = music21.stream.Measure()
        measure2.append(note1)
        part2.append(measure2)
        score.append(part1)
        score.append(part2)
        self.app.parts_to_exclude.set("Violin")
        self.assertEqual(self.app.get_total_measures(score), 1)

if __name__ == '__main__':
    unittest.main()