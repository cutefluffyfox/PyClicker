from pickle import dump


def new_game():
    file = open('store.pckl', 'wb')
    dump(60, file)  # fps
    dump(0.5, file)  # volume
    file.close()


if __name__ == "__main__":
    new_game()
