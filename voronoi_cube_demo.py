import argparse

from voronoi_cube import NoiseType, VoronoiCube


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    args = NoiseType.get_all()
    group.add_argument("-f", "--file", help="file_path")
    group.add_argument("-n", "--noise", choices=args)
    args = parser.parse_args()

    return args.file, args.noise


def main():
    file_path, noise_type = parse_arguments()

    if file_path:
        app = VoronoiCube(file_path=file_path)
    else:
        app = VoronoiCube(noise_type=noise_type)

    app.run()


if __name__ == '__main__':
    main()