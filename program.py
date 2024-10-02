import argparse
import os

from CTFd_Crawler import CTFCrawler

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

BANNER = f"""
{GREEN}   ******  ********** ********      **         ******                               **               
  **////**/////**/// /**/////      /**        **////**                             /**               
 **    //     /**    /**           /**       **    //  ******  ******   ***     ** /**  *****  ****** 
{YELLOW}/**           /**    /*******   ******      /**       //**//* //////** //**  * /** /** **///**//**//* 
/**           /**    /**////   **///**      /**        /** /   *******  /** ***/** /**/******* /** /  
{CYAN}//**    **    /**    /**      /**  /**      //**    ** /**    **////**  /****/**** /**/**////  /**    
 //******     /**    /**      //******       //****** /***   //******** ***/ ///** ***//******/***    
{RED}  //////      //     //        //////         //////  ///     //////// ///    /// ///  ////// ///    
{RESET}
"""


def intro():
    print("-" * 101)
    print(BANNER)
    print("-" * 101)


def parse_arguments():
    parser = argparse.ArgumentParser(description="CTFd Crawler")
    parser.add_argument(
        "--input_json",
        type=str,
        help="Input json path",
    )
    parser.add_argument("--name", type=str, help="CTF name")
    parser.add_argument("--url", type=str, help="CTFd URL")
    parser.add_argument("--token", type=str, help="CTFd token")
    parser.add_argument(
        "--work_dir",
        type=str,
        default="./",
        help="Output directory (default: current directory)",
    )

    return parser.parse_args()


def main():
    intro()

    args = parse_arguments()

    if args.input_json:
        if not os.path.exists(args.input_json):
            raise FileNotFoundError(f"No such file: {args.input_json}")
        work_directory = os.path.dirname(args.input_json)
        print(f"{BLUE}CTF JSON file location: {args.input_json}{RESET}")
        print(
            f"{BLUE}Current work directory (save all information in this directory): {work_directory}{RESET}"
        )

        crawler = CTFCrawler()
        crawler.load(args.input_json)
        challenges = crawler.get_challenges()
        crawler.download_challenges()
        print(f"{GREEN}Downloaded {len(challenges)} challenges{RESET}")

    else:
        if not args.name:
            args.name = input("Enter CTF name: ")
        if not args.url:
            args.url = input("Enter CTFd URL: ")
        if not args.token:
            args.token = input("Enter CTFd token: ")

        print(f"{MAGENTA}Current work directory:{RESET}")
        print(f"{MAGENTA}Work directory: {args.work_dir}{RESET}")
        change_work_dir = input("Do you want to change the output directory? (y/n): ")
        if change_work_dir.lower() == "y":
            args.work_dir = input("Enter new output directory: ")

        print(f"{YELLOW}Current settings:{RESET}")
        print(f"{YELLOW}CTF name: {args.name}{RESET}")
        print(f"{YELLOW}CTFd URL: {args.url}{RESET}")
        print(f"{YELLOW}CTFd token: {args.token}{RESET}")
        print(f"{YELLOW}Output directory: {args.work_dir}{RESET}")

        crawler = CTFCrawler()
        crawler.self_load(args.name, args.url, args.token, args.work_dir)

        challenges = crawler.get_challenges()
        crawler.download_challenges()
        print(f"{GREEN}Downloaded {len(challenges)} challenges{RESET}")


if __name__ == "__main__":
    main()
