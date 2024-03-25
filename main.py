from fund import Fund


def main():
    ykt = Fund('ykt')
    # yas = Fund('yas')
    # yay = Fund('yay')
    # ybe = Fund('ybe')

    ykt.loadFromWeb()
    # yas.loadFromWeb()
    # yay.loadFromWeb()
    # ybe.loadFromWeb()

    ykt.saveToJson()
    # ykt.loadFromJson()

    print(ykt)
    # print(yas)
    # print(yay)
    # print(ybe)

        
if __name__ == "__main__":
    main()
