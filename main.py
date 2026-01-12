import sys
import time
import crawl
import pprint
import asyncio
import csv_report

async def main():
    if len(sys.argv) < 2:
        print('no website provided')
        sys.exit(1)
    if len(sys.argv) > 4:
        print('too many arguments provided')
        sys.exit(1)
    
    url_to_crawl = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    print(f'starting crawl of: {url_to_crawl}')
    start_time = time.time()

    '''
    page_data = {}
    try: page_data = await crawl.crawl_site_async(url_to_crawl, max_concurrency, max_pages)
    except Exception as e:
        print(f'error: {e} from {url_to_crawl}')
        sys.exit(1)
    '''

    page_data = await crawl.crawl_site_async(url_to_crawl, max_concurrency, max_pages)

    print(time.time() - start_time)
    print(f'len of data pages is {len(page_data)}')

    csv_report.write_csv_report(page_data)

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())

