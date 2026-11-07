"""Test the ACE 1.1 contract without falsely claiming Java has run locally."""

import tempfile
import unittest
from pathlib import Path

from anamu.jsymbolic_ace import read_jsymbolic_ace, read_jsymbolic_definitions


class JsymbolicAceTests(unittest.TestCase):
    def parse(self, content: str):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "feature_values.xml"
            path.write_text(content, encoding="utf-8")
            return read_jsymbolic_ace(path)

    def definitions(self, content: str):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "feature_defs.xml"
            path.write_text(content, encoding="utf-8")
            return read_jsymbolic_definitions(path)

    def test_windowed_vectors_and_whole_piece_features_remain_distinct(self):
        parsed = self.parse("""<?xml version="1.0"?>
<feature_vector_file><comments>Original jSymbolic ACE 1.1 shape</comments>
  <data_set><data_set_id>piano.mid</data_set_id>
    <section start="0.0" stop="5.0">
      <feature><name>Note Density</name><v>12.5</v></feature>
      <feature><name>Pitch Class Histogram</name><v>1</v><v>0</v><v>3</v></feature>
    </section>
    <section start="2.5" stop="7.5">
      <feature><name>Note Density</name><v>14</v></feature>
    </section>
    <feature><name>Overall Dynamic Range</name><v>30</v></feature>
  </data_set>
</feature_vector_file>""")
        self.assertEqual(parsed["data_set_count"], 1)
        self.assertEqual(parsed["window_count"], 2)
        result = parsed["data_sets"][0]
        self.assertEqual(result["whole_piece_features"]["Overall Dynamic Range"], [30.0])
        self.assertEqual(result["windows"][0]["features"]["Pitch Class Histogram"],
                         [1.0, 0.0, 3.0])
        self.assertEqual(result["windows"][1]["start_seconds_if_j_symbolic_windowed"], 2.5)
        self.assertEqual(result["windows"][0]["stop_seconds_if_j_symbolic_windowed"], 5.0)

    def test_missing_timestamp_is_not_invented(self):
        result = self.parse("""<feature_vector_file><data_set>
<data_set_id>x.mid</data_set_id><section>
<feature><name>F</name><v>1</v></feature>
</section></data_set></feature_vector_file>""")
        self.assertIsNone(result["data_sets"][0]["windows"][0]
                          ["start_seconds_if_j_symbolic_windowed"])

    def test_reject_bad_or_duplicate_feature_values(self):
        for content in ("<feature><name>F</name><v>NaN</v></feature>",
                        "<feature><name>F</name><v>Infinity</v></feature>",
                        "<feature><name>F</name><v>abc</v></feature>",
                        "<feature><name>F</name><v>1</v></feature>"
                        "<feature><name>F</name><v>2</v></feature>"):
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.parse("<feature_vector_file><data_set><data_set_id>x</data_set_id>"
                           + content + "</data_set></feature_vector_file>")

    def test_reject_untrusted_doctype_and_inconsistent_timestamps(self):
        for content in ("""<!DOCTYPE feature_vector_file [<!ENTITY x "hi">]>
<feature_vector_file><data_set><data_set_id>x</data_set_id></data_set></feature_vector_file>""",
                        """<feature_vector_file><data_set><data_set_id>x</data_set_id>
<section start="5" stop="1"><feature><name>F</name><v>1</v></feature></section>
</data_set></feature_vector_file>""",
                        """<feature_vector_file><data_set><data_set_id>x</data_set_id>
<section start="5"><feature><name>F</name><v>1</v></feature></section>
</data_set></feature_vector_file>"""):
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.parse(content)

    def test_official_ace_11_internal_dtd_is_read_without_entity_expansion(self):
        # This declaration is taken from the upstream source file
        # DDMAL/jSymbolic2/manual/api_files/ExtractedFeatureValues.xml.
        dtd = '''<?xml version="1.0"?>
<!DOCTYPE feature_vector_file [
   <!ELEMENT feature_vector_file (comments, data_set+)>
   <!ELEMENT comments (#PCDATA)>
   <!ELEMENT data_set (data_set_id, section*, feature*)>
   <!ELEMENT data_set_id (#PCDATA)>
   <!ELEMENT section (feature+)>
   <!ATTLIST section start CDATA ""
                     stop CDATA "">
   <!ELEMENT feature (name, v+)>
   <!ELEMENT name (#PCDATA)>
   <!ELEMENT v (#PCDATA)>
]>
<feature_vector_file><comments></comments><data_set>
  <data_set_id>x.mid</data_set_id>
  <section start="0" stop="2"><feature><name>Mean Pitch</name><v>6E1</v>
  </feature></section>
</data_set></feature_vector_file>'''
        parsed = self.parse(dtd)
        self.assertEqual(parsed["window_count"], 1)
        self.assertEqual(parsed["data_sets"][0]["windows"][0]["features"]["Mean Pitch"],
                         [60.0])

    def test_reject_different_dtd_even_without_entities(self):
        with self.assertRaisesRegex(ValueError, "unrecognized_doctype"):
            self.parse('''<!DOCTYPE feature_vector_file [<!ELEMENT feature_vector_file ANY>]>
<feature_vector_file><data_set><data_set_id>x</data_set_id></data_set></feature_vector_file>''')

    def test_original_ace_feature_definitions_include_semantics_and_dimensions(self):
        result = self.definitions('''<?xml version="1.0"?>
<!DOCTYPE feature_key_file [
   <!ELEMENT feature_key_file (comments, feature+)>
   <!ELEMENT comments (#PCDATA)>
   <!ELEMENT feature (name, description?, is_sequential, parallel_dimensions)>
   <!ELEMENT name (#PCDATA)>
   <!ELEMENT description (#PCDATA)>
   <!ELEMENT is_sequential (#PCDATA)>
   <!ELEMENT parallel_dimensions (#PCDATA)>
]>
<feature_key_file><comments></comments><feature>
<name>Mean Pitch</name><description>Average MIDI pitch.</description>
<is_sequential>true</is_sequential><parallel_dimensions>1</parallel_dimensions>
</feature><feature><name>Pitch Class Histogram</name>
<is_sequential>false</is_sequential><parallel_dimensions>12</parallel_dimensions>
</feature></feature_key_file>''')
        self.assertEqual(result["feature_definition_count"], 2)
        self.assertTrue(result["definitions"]["Mean Pitch"]["is_sequential"])
        self.assertEqual(result["definitions"]["Pitch Class Histogram"]["parallel_dimensions"], 12)
        self.assertIsNone(result["definitions"]["Pitch Class Histogram"]["description_from_upstream"])

    def test_reject_invalid_or_duplicate_feature_definitions(self):
        head = '<feature_key_file><feature><name>F</name>'
        tail = '</feature></feature_key_file>'
        for body in ('<is_sequential>sometimes</is_sequential><parallel_dimensions>2</parallel_dimensions>',
                     '<is_sequential>true</is_sequential><parallel_dimensions>NaN</parallel_dimensions>',
                     '<is_sequential>true</is_sequential><parallel_dimensions>-4</parallel_dimensions>'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.definitions(head + body + tail)
        with self.assertRaisesRegex(ValueError, "ace_duplicate_definition"):
            self.definitions('<feature_key_file>' + (
                '<feature><name>F</name><is_sequential>true</is_sequential>'
                '<parallel_dimensions>1</parallel_dimensions></feature>') * 2
                + '</feature_key_file>')

    def test_reject_oversized_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "x.xml"
            path.write_text("a" * 101)
            with self.assertRaisesRegex(ValueError, "ace_file_over_size_limit"):
                read_jsymbolic_ace(path, max_bytes=100)


if __name__ == "__main__":
    unittest.main()
