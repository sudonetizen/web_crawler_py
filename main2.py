import sys
import time
import crawl
import pprint

def main():
    if len(sys.argv) < 2:
        print('no website provided')
        sys.exit(1)
    if len(sys.argv) > 2:
        print('too many arguments provided')
        sys.exit(1)
    
    url_to_crawl = sys.argv[1]
    print(f'starting crawl of: {url_to_crawl}')
    start_time = time.time()

    page_data = {}
    try: page_data = crawl.crawl_page(url_to_crawl, url_to_crawl, page_data)    
    except Exception as e:
        print(f'error: {e} from {url_to_crawl}')
        sys.exit(1)
    
    print(time.time() - start_time)

    pprint.pprint(page_data, indent=4)

    sys.exit(0)


if __name__ == "__main__":
    main()
