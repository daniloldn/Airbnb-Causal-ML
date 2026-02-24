from clean_data import clean_data
from feature_eng import feature_eng



def main():


    print("calling clean_data")

    clean_data()

    print("calling feature_eng")

    feature_eng()

    return None


if __name__ == "__main__":
    main()
