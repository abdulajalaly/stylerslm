"""Command-line entry point for a quick model health check."""

import argparse

from .predict import load_model


def main():
    parser = argparse.ArgumentParser(description="Inspect the StylerSLM model.")
    parser.add_argument("--model", help="Path to a model checkpoint.")
    args = parser.parse_args()
    load_model(args.model) if args.model else load_model()
    print("StylerSLM model loaded successfully.")


if __name__ == "__main__":
    main()