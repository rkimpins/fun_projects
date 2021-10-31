

def tens(integer):
    oneToNineteenList = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    twentyToNinetyList = ["", "", "Twenty", "Thirty", "Fourty", "Fiftey", "Sixty", "Seventy", "Eighty", "Ninety"]
    if integer < 20:
        return oneToNineteenList[integer]
    else:
        result = ""
        intString = str(integer)
        return twentyToNinetyList[int(intString[-2])] + " " + oneToNineteenList[int(intString[-1])]

def handleThreeDigits(integer):
    result = ""
    if integer > 100:
        result = f"{tens(int(str(integer)[-3]))} Hundred "
        integer = integer % 100
    result += tens(integer)
    return result

def integerToWord(integer):
    numbers = ["", "Thousand", "Million", "Billion", "Trillion", "Quadrillion", "Quintillion", "Sextillion", "Septillion", "Octillion", "Nonillion", "Decillion", "Undecillion", "Duodecillion", "Tredecillion", "Quattuordecillion", "Quindecillion", "Sexdecillion", "Septendecillion", "Octodecillion", "Novemdecillion", "Vigintillion"]
    pointer = 0

    result = ""
    while integer > 0:
        result = f"{handleThreeDigits(integer % 1000)} {numbers[pointer]} {result}"
        pointer += 1
        integer = integer // 1000
    return result

def main():
    integer = 123456789123456789123456789
    word = integerToWord(integer)
    print(f"{integer} -> {word}")

if __name__ == "__main__":
    main()
