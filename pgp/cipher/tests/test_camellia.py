# python-pgp A Python OpenPGP implementation
# Copyright (C) 2014 Richard Mitchell
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest
import warnings

from Crypto.SelfTest.Cipher.common import make_block_tests

from pgp.cipher import camellia


# This is a list of (plaintext, ciphertext, key) tuples.
test_data = [
    # Test vectors from RFC 3713, A
    ('0123456789abcdeffedcba9876543210', '67673138549669730857065648eabe43',
     '0123456789abcdeffedcba9876543210',
     '128-bit key'),

    ('0123456789abcdeffedcba9876543210', 'b4993401b3e996f84ee5cee7d79b09b9',
     '0123456789abcdeffedcba98765432100011223344556677',
     '192-bit key'),

    ('0123456789abcdeffedcba9876543210', '9acc237dff16d76c20ef7c919e3a7509',
     '0123456789abcdeffedcba98765432100011223344556677889900aabbccddeeff',
     '256-bit key'),

    # Test vectors from CryptX
    # https://metacpan.org/release/CryptX
    # http://bit.ly/R2HGpB

    # ECB-CAMELLIA128.Encrypt and ECB-CAMELLIA128.Decrypt
    ('6BC1BEE22E409F96E93D7E117393172A', '432FC5DCD628115B7C388D770B270C96',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'ECB-CAMELLIA128 1'),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '0BE1F14023782A22E8384C5ABB7FAB2B',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'ECB-CAMELLIA128 2'),

    ('30C81C46A35CE411E5FBC1191A0A52EF', 'A0A1ABCD1893AB6FE0FE5B65DF5F8636',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'ECB-CAMELLIA128 3'),

    ('F69F2445DF4F9B17AD2B417BE66C3710', 'E61925E0D5DFAA9BB29F815B3076E51A',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'ECB-CAMELLIA128 4'),

    # ECB-CAMELLIA192.Encrypt and ECB-CAMELLIA192.Decrypt
    ('6BC1BEE22E409F96E93D7E117393172A', 'CCCC6C4E138B45848514D48D0D3439D3',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'ECB-CAMELLIA192 1'),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '5713C62C14B2EC0F8393B6AFD6F5785A',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'ECB-CAMELLIA192 2'),

    ('30C81C46A35CE411E5FBC1191A0A52EF', 'B40ED2B60EB54D09D030CF511FEEF366',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'ECB-CAMELLIA192 3'),

    ('F69F2445DF4F9B17AD2B417BE66C3710', '909DBD95799096748CB27357E73E1D26',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'ECB-CAMELLIA192 4'),

    # ECB-CAMELLIA256.Encrypt and ECB-CAMELLIA256.Decrypt
    ('6BC1BEE22E409F96E93D7E117393172A', 'BEFD219B112FA00098919CD101C9CCFA',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'ECB-CAMELLIA256 1'),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', 'C91D3A8F1AEA08A9386CF4B66C0169EA',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'ECB-CAMELLIA256 2'),

    ('30C81C46A35CE411E5FBC1191A0A52EF', 'A623D711DC5F25A51BB8A80D56397D28',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'ECB-CAMELLIA256 3'),

    ('F69F2445DF4F9B17AD2B417BE66C3710', '7960109FB6DC42947FCFE59EA3C5EB6B',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'ECB-CAMELLIA256 4'),

    # CBC-CAMELLIA128.Encrypt and CBC-CAMELLIA128.Decrypt
    ('6BC1BEE22E409F96E93D7E117393172A', '1607CF494B36BBF00DAEB0B503C831AB',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'CBC-CAMELLIA128 1',
     dict(mode='CBC', iv='000102030405060708090A0B0C0D0E0F')
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', 'A2F2CF671629EF7840C5A5DFB5074887',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'CBC-CAMELLIA128 2',
     dict(mode='CBC', iv='1607CF494B36BBF00DAEB0B503C831AB')
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', '0F06165008CF8B8B5A63586362543E54',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'CBC-CAMELLIA128 3',
     dict(mode='CBC', iv='A2F2CF671629EF7840C5A5DFB5074887')
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', '74C64268CDB8B8FAF5B34E8AF3732980',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'CBC-CAMELLIA128 4',
     dict(mode='CBC', iv='36A84CDAFD5F9A85ADA0F0A993D6D577')
     ),

    # CBC-CAMELLIA192.Encrypt and CBC-CAMELLIA192.Decrypt
    ('6BC1BEE22E409F96E93D7E117393172A', '2A4830AB5AC4A1A2405955FD2195CF93',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'CBC-CAMELLIA192 1',
     dict(mode='CBC', iv='000102030405060708090A0B0C0D0E0F')
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '5D5A869BD14CE54264F892A6DD2EC3D5',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'CBC-CAMELLIA192 2',
     dict(mode='CBC', iv='1607CF494B36BBF00DAEB0B503C831AB')
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', '37D359C3349836D884E310ADDF68C449',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'CBC-CAMELLIA192 3',
     dict(mode='CBC', iv='A2F2CF671629EF7840C5A5DFB5074887')
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', '01FAAA930B4AB9916E9668E1428C6B08',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'CBC-CAMELLIA192 4',
     dict(mode='CBC', iv='36A84CDAFD5F9A85ADA0F0A993D6D577')
     ),

    # CBC-CAMELLIA256.Encrypt and CBC-CAMELLIA256.Decrypt
    ('6BC1BEE22E409F96E93D7E117393172A', 'E6CFA35FC02B134A4D2C0B6737AC3EDA',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'CBC-CAMELLIA256 1',
     dict(mode='CBC', iv='000102030405060708090A0B0C0D0E0F')
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '36CBEB73BD504B4070B1B7DE2B21EB50',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'CBC-CAMELLIA256 2',
     dict(mode='CBC', iv='1607CF494B36BBF00DAEB0B503C831AB')
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', 'E31A6055297D96CA3330CDF1B1860A83',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'CBC-CAMELLIA256 3',
     dict(mode='CBC', iv='A2F2CF671629EF7840C5A5DFB5074887')
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', '5D563F6D1CCCF236051C0C5C1C58F28F',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'CBC-CAMELLIA256 4',
     dict(mode='CBC', iv='36A84CDAFD5F9A85ADA0F0A993D6D577')
     ),

    # CFB128-CAMELLIA128.Encrypt
    ('6BC1BEE22E409F96E93D7E117393172A', '14F7646187817EB586599146B82BD719',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'CFB128-CAMELLIA128 1',
     dict(mode='CFB', iv='000102030405060708090A0B0C0D0E0F', segment_size=128)
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', 'A53D28BB82DF741103EA4F921A44880B',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'CFB128-CAMELLIA128 2',
     dict(mode='CFB', iv='14F7646187817EB586599146B82BD719', segment_size=128)
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', '9C2157A664626D1DEF9EA420FDE69B96',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'CFB128-CAMELLIA128 3',
     dict(mode='CFB', iv='A53D28BB82DF741103EA4F921A44880B', segment_size=128)
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', '742A25F0542340C7BAEF24CA8482BB09',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'CFB128-CAMELLIA128 4',
     dict(mode='CFB', iv='9C2157A664626D1DEF9EA420FDE69B96', segment_size=128)
     ),

    # CFB128-CAMELLIA192.Encrypt
    ('6BC1BEE22E409F96E93D7E117393172A', 'C832BB9780677DAA82D9B6860DCD565E',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'CFB128-CAMELLIA192 1',
     dict(mode='CFB', iv='000102030405060708090A0B0C0D0E0F', segment_size=128)
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '86F8491627906D780C7A6D46EA331F98',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'CFB128-CAMELLIA192 2',
     dict(mode='CFB', iv='C832BB9780677DAA82D9B6860DCD565E', segment_size=128)
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', '69511CCE594CF710CB98BB63D7221F01',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'CFB128-CAMELLIA192 3',
     dict(mode='CFB', iv='86F8491627906D780C7A6D46EA331F98', segment_size=128)
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', 'D5B5378A3ABED55803F25565D8907B84',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'CFB128-CAMELLIA192 4',
     dict(mode='CFB', iv='69511CCE594CF710CB98BB63D7221F01', segment_size=128)
     ),

    # CFB128-CAMELLIA256.Encrypt
    ('6BC1BEE22E409F96E93D7E117393172A', 'CF6107BB0CEA7D7FB1BD31F5E7B06C93',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'CFB128-CAMELLIA256 1',
     dict(mode='CFB', iv='000102030405060708090A0B0C0D0E0F', segment_size=128)
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '89BEDB4CCDD864EA11BA4CBE849B5E2B',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'CFB128-CAMELLIA256 2',
     dict(mode='CFB', iv='CF6107BB0CEA7D7FB1BD31F5E7B06C93', segment_size=128)
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', '555FC3F34BDD2D54C62D9E3BF338C1C4',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'CFB128-CAMELLIA256 3',
     dict(mode='CFB', iv='89BEDB4CCDD864EA11BA4CBE849B5E2B', segment_size=128)
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', '5953ADCE14DB8C7F39F1BD39F359BFFA',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'CFB128-CAMELLIA256 4',
     dict(mode='CFB', iv='555FC3F34BDD2D54C62D9E3BF338C1C4', segment_size=128)
     ),

    # OFB-CAMELLIA128.Encrypt
    ('6BC1BEE22E409F96E93D7E117393172A', '14F7646187817EB586599146B82BD719',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'OFB-CAMELLIA128 1',
     dict(mode='OFB', iv='000102030405060708090A0B0C0D0E0F')
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '25623DB569CA51E01482649977E28D84',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'OFB-CAMELLIA128 2',
     dict(mode='OFB', iv='50FE67CC996D32B6DA0937E99BAFEC60')
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', 'C776634A60729DC657D12B9FCA801E98',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'OFB-CAMELLIA128 3',
     dict(mode='OFB', iv='D9A4DADA0892239F6B8B3D7680E15674')
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', 'D776379BE0E50825E681DA1A4C980E8E',
     '2B7E151628AED2A6ABF7158809CF4F3C',
     'OFB-CAMELLIA128 4',
     dict(mode='OFB', iv='A78819583F0308E7A6BF36B1386ABF23')
     ),

    # OFB-CAMELLIA192.Encrypt
    ('6BC1BEE22E409F96E93D7E117393172A', 'C832BB9780677DAA82D9B6860DCD565E',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'OFB-CAMELLIA192 1',
     dict(mode='OFB', iv='000102030405060708090A0B0C0D0E0F')
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '8ECEB7D0350D72C7F78562AEBDF99339',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'OFB-CAMELLIA192 2',
     dict(mode='OFB', iv='A609B38DF3B1133DDDFF2718BA09565E')
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', 'BDD62DBBB9700846C53B507F544696F0',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'OFB-CAMELLIA192 3',
     dict(mode='OFB', iv='52EF01DA52602FE0975F78AC84BF8A50')
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', 'E28014E046B802F385C4C2E13EAD4A72',
     '8E73B0F7DA0E6452C810F32B809079E562F8EAD2522C6B7B',
     'OFB-CAMELLIA192 4',
     dict(mode='OFB', iv='BD5286AC63AABD7EB067AC54B553F71D')
     ),

    # OFB-CAMELLIA256.Encrypt
    ('6BC1BEE22E409F96E93D7E117393172A', 'CF6107BB0CEA7D7FB1BD31F5E7B06C93',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'OFB-CAMELLIA256 1',
     dict(mode='OFB', iv='000102030405060708090A0B0C0D0E0F')
     ),

    ('AE2D8A571E03AC9C9EB76FAC45AF8E51', '127AD97E8E3994E4820027D7BA109368',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'OFB-CAMELLIA256 2',
     dict(mode='OFB', iv='B7BF3A5DF43989DD97F0FA97EBCE2F4A')
     ),

    ('30C81C46A35CE411E5FBC1191A0A52EF', '6BFF6265A6A6B7A535BC65A80B17214E',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'OFB-CAMELLIA256 3',
     dict(mode='OFB', iv='E1C656305ED1A7A6563805746FE03EDC')
     ),

    ('F69F2445DF4F9B17AD2B417BE66C3710', '0A4A0404E26AA78A27CB271E8BF3CF20',
     '603DEB1015CA71BE2B73AEF0857D77811F352C073B6108D72D9810A30914DFF4',
     'OFB-CAMELLIA256 4',
     dict(mode='OFB', iv='41635BE625B48AFC1666DD42A09D96E7')
     ),
]


def get_tests(config={}):
    return make_block_tests(camellia, "Camellia", test_data)


def test_camellia():
    if camellia is None:
        warnings.warn(
            "Camellia not available on this system. Skipping its tests."
            )
        return

    for testcase in get_tests():
        yield testcase


if hasattr(unittest, 'skip'):
    # Python >= 3.1
    test_camellia = unittest.skipIf(
                        camellia is None,
                        "Camellia not available on this system."
                    )(test_camellia)
