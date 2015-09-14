import random


class BarcodeType:
    @classmethod
    def generate(cls, barcode_prefix: str, count_of_numbers: int) -> str:
        return ('{}{}'.format(barcode_prefix, ''.join(random.sample('0123456789', count_of_numbers)))).upper()
