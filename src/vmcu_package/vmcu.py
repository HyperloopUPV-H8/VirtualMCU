from user_code import UserCode

def main() -> int:
    lcu = UserCode("lcu", ["/path/to/lcu/executable"])

    lcu.start()

    try:
        lcu.stop(timeout=1.0)
    except TimeoutError:
        lcu.stop(force=True)

    return 0

if __name__ == "__main__":
    exit(main())