from EventParser import EventParser, load_text, INCREMENT, WINDOW_SIZE
from API import LLMFactory
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run the Event Parser on a text file.")
    parser.add_argument("--file", type=str, help="Path to the text file to parse.")
    parser.add_argument("--provider", type=str, default="openai", help="provider of LLM")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="model of LLM")
    parser.add_argument("--increment", type=int, default=INCREMENT, help="Increment size for sliding window.")
    parser.add_argument("--window_size", type=int, default=WINDOW_SIZE, help="Window size for sliding window.")
    parser.add_argument("--save_dir", type=str, default="result", help="Directory to save the output files.")
    return parser.parse_args()


def main():
    args = parse_args()
    text = load_text(args.file)
    llm = LLMFactory.get_llm(provider=args.provider, model_name=args.model)
    
    parser = EventParser(args.save_dir,text, llm, increment=args.increment, window_size=args.window_size)
    parser.run()
    parser.save()

if __name__ == "__main__":
    main()