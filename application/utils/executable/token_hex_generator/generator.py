from secrets import token_hex


def main():
    SECRET = token_hex()
    print(SECRET)


if __name__ == "__main__":
    main()
