from PoolTableChecker import PoolTableChecker

imgPath1 = "../testData/pool1.jpg"
imgPath2 = "../testData/pool1.jpg"

def main():
    pooltableChecker = PoolTableChecker()
    isSame = pooltableChecker.isTableFree(imgPath1, imgPath2)
    print(isSame)

if __name__ == "__main__":
    main()