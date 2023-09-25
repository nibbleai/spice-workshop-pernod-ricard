from src.data import get_dataset, get_target, train_test_split
from src.preprocessing import preprocess
from src.features import registry
from spice import Generator


def main():
    data = get_dataset()

    target = get_target(data)
    data, target = preprocess(data, target)
    train_data, test_data = train_test_split(data)

    generator = Generator(registry)
    train_features = generator.fit_transform(train_data).to_pandas()
    test_features = generator.transform(test_data).to_pandas()


if __name__ == '__main__':
    main()
