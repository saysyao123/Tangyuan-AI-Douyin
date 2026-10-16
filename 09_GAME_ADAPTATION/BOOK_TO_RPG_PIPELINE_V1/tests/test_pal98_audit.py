import importlib.util, json, pathlib, struct, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('pal98_audit',ROOT/'tools/pal98_audit.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def mkf(chunks):
    offset=4*(len(chunks)+1);table=[offset]
    for chunk in chunks:offset+=len(chunk);table.append(offset)
    return struct.pack('<'+'I'*len(table),*table)+b''.join(chunks)
class MkfMetadataTests(unittest.TestCase):
    def test_fake_metadata_and_message_index(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)
            ss=mkf([bytes(32),bytes(8),bytes(14),struct.pack('<II',0,3),struct.pack('<HHHHHHHH',9,0,0,0,0xffff,0,0,0)])
            data=mkf([b'\x01\x02'])
            for name,value in [('Sss.mkf',ss),('Data.mkf',data),('M.msg',b'abc'),('Word.dat',b'abcdefghij')]:
                (p/name).write_bytes(value)
            result=m.inspect(p/'Sss.mkf',p/'Data.mkf',p/'M.msg',p/'Word.dat')
            self.assertEqual(result['script_records_8_byte'],2)
            self.assertEqual(result['distinct_opcode_values'],2)
            self.assertEqual(result['special_value_0xFFFF'],1)
            self.assertEqual(result['message_offset_entries'],2)
            self.assertTrue(result['message_index_matches_file_size'])
            self.assertEqual(result['word_records_if_10byte'],1)
    def test_bad_offsets_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/'broken.mkf';p.write_bytes(struct.pack('<II',8,9999))
            with self.assertRaises(ValueError):m.mkf(p)
if __name__=='__main__':unittest.main()
