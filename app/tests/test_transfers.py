import unittest

from ..Konto import Konto
from ..KontoOsobiste import KontoOsobiste
from ..KontoFirmowe import KontoFirmowe

class TestTransfer(unittest.TestCase):
    personal_data = {
        "name": "Dariusz",
        "surname": "Januszewski",
        "pesel": "89092909876",
    }
    company_data = {
        "name": "JDG",
        "nip": "1234567890"
    }
    def test_incoming_transfer(self):
        pierwsze_konto = Konto()
        pierwsze_konto.zaksieguj_przelew_przychodzacy(100)
        self.assertEqual(pierwsze_konto.saldo, 100, "Saldo nie jest poprawne!")

    def test_incoming_transfer_with_incorrect_amount(self):
        pierwsze_konto = Konto()
        pierwsze_konto.zaksieguj_przelew_przychodzacy(-100)
        self.assertEqual(pierwsze_konto.saldo, 0, "Saldo nie jest poprawne!")

    def test_outgoing_transfer(self):
        pierwsze_konto = Konto()
        pierwsze_konto.saldo = 120
        pierwsze_konto.przelew_wychodzacy(100)
        self.assertEqual(pierwsze_konto.saldo, 20, "Saldo nie jest poprawne!")
        
    def test_outgoing_transfer_amount_greater_than_saldo(self):
        pierwsze_konto = KontoOsobiste(self.personal_data["name"], self.personal_data["surname"], self.personal_data["pesel"])
        pierwsze_konto.saldo = 50
        pierwsze_konto.przelew_wychodzacy(100)
        self.assertEqual(pierwsze_konto.saldo, 50, "Saldo nie jest poprawne!")

    def test_outgoing_transfer_with_promo_code(self):
        konto = KontoOsobiste(self.personal_data["name"], self.personal_data["surname"], self.personal_data["pesel"], "PROM_123")
        konto.przelew_wychodzacy(20)
        self.assertEqual(konto.saldo, 50 - 20, "Saldo nie jest poprawne!")

    def test_series_of_transfers(self):
        konto = KontoFirmowe(self.company_data["name"], self.company_data["nip"])
        konto.zaksieguj_przelew_przychodzacy(100)
        konto.zaksieguj_przelew_przychodzacy(120)
        konto.przelew_wychodzacy(50)
        self.assertEqual(konto.saldo, 100+120-50, "Saldo nie jest poprawne!")

    def test_express_transfer_personal_account(self):
        konto = KontoOsobiste(self.personal_data["name"], self.personal_data["surname"], self.personal_data["pesel"])
        konto.przelew_wychodzacy_expressowy(50)