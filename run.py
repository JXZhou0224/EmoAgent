# from EventParser import EventParser, load_text, INCREMENT, WINDOW_SIZE
from EmoParser.EmoParser import EmoParser,WINDOW_SIZE,OVERLAP
from API import LLMFactory
from utils import load_text
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run the Event Parser on a text file.")
    parser.add_argument("--file", type=str, help="Path to the text file to parse.")
    parser.add_argument("--main_character", type=str,help="The main character to extract in the text")
    parser.add_argument("--provider", type=str, default="openai", help="provider of LLM")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="model of LLM")
    parser.add_argument("--overlap", type=int, default=OVERLAP, help="Increment size for sliding window.")
    parser.add_argument("--window_size", type=int, default=WINDOW_SIZE, help="Window size for sliding window.")
    parser.add_argument("--save_dir", type=str, default="result", help="Directory to save the output files.")
    return parser.parse_args()


def main():
    args = parse_args()
    text = load_text(args.file)
    llm = LLMFactory.get_llm(provider=args.provider, model_name=args.model)
    
    parser = EmoParser(args.save_dir,llm, text,args.main_character,window_size=args.window_size,overlap=args.overlap)
    parser.run()
    parser.save()

if __name__ == "__main__":
    main()