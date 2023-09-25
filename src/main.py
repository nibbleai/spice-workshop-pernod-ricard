from src.data import get_dataset, get_target, train_test_split
from src.preprocessing import preprocess
from src.features import registry
from spice import Generator


def main():
    data = get_dataset()

    target = get_target(data)
    data, target = preprocess(data, target)

    generator = Generator(registry)
    features = generator.fit_transform(data).to_pandas()
    print(features)


if __name__ == '__main__':
    main()
