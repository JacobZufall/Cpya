from src.cpya.tax_def.standard_deduction import StandardDeduction

if __name__ == "__main__":
    std_ded: StandardDeduction = StandardDeduction(2022)

    print(std_ded.__getattribute__("sngl"))
