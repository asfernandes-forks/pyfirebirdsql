import unittest
from firebirdsql.tests import base
from firebirdsql import srp

class TestSrp(base.TestBase):
    def test_srp(self):
        user = b'sysdba'
        password = b'masterkey'
    
        # Client send A to Server
        A, a = srp.client_seed(user, password)
    
        # Server send B, salt to Client
        salt = srp.get_salt()
        v = srp.get_verifier(user, password, salt)
        B, b = srp.server_seed(v)
    
        # Client send M to Server
        M, clientKey = srp.client_proof(user, password, salt, A, B, a)
    
        # Server send serverProof to Client
        serverProof, serverKey = srp.server_proof(user, salt, A, B, M, b, v)
    
        # Client can verify by serverProof
        srp.verify_server_proof(clientKey, A, M, serverProof)
    
        # Client and Server has same key
        self.assertEqual(clientKey, serverKey)

    def test_hex_to_bytes(self):
        s = b'37313243354638413244423832343634433444363430414539373130323541413530414236343930364434463034344638323245384146384135384144414242444245314546414241303042434344344344414138413935354243343343333630304245414239454242394244343141434335364533374631413438463137323933463234453837364235334545413641363037313244334639343337363930353642363332303234313638323742343030453136324138433039333844343832323734333037353835453042433144394444353245464137333330423238453431423743464345464439453835323346443131343430454535444539334138'
        b = srp.hex_to_bytes(s)
        self.assertEqual(b, b'712C5F8A2DB82464C4D640AE971025AA50AB64906D4F044F822E8AF8A58ADABBDBE1EFABA00BCCD4CDAA8A955BC43C3600BEAB9EBB9BD41ACC56E37F1A48F17293F24E876B53EEA6A60712D3F943769056B63202416827B400E162A8C0938D482274307585E0BC1D9DD52EFA7330B28E41B7CFCEFD9E8523FD11440EE5DE93A8')
        self.assertEqual(srp.bytes_to_hex(b), s)


