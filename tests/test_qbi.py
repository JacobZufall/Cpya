# test_qbi.py

from src.taxpy.deductions.qbi import Qbi

if __name__ == "__main__":
    myQbi: Qbi = Qbi(2022, "s", 400_000.0, 148_000.0, 50_000.0, 30_000.0, 7_500.0)
    print(myQbi.qbi)
