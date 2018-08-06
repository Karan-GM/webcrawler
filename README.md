# Objective
  Crawl Internet documents to construct a document collection focused on a particular topic
  
# Requirements
1. Crawl 10000 documents
2. Crawler must strictly observe this politeness policy at all times, including during development and testing
   - Make no more than one HTTP request per second from any given domain. You may crawl multiple pages from different domains at the same time
   - Before you crawl the first page from a given domain, fetch its robots.txt file and make sure your crawler strictly obeys the file.
3. Crawling strategy
   - Seed URLs should always be crawled first.
   - Must use BFS as the baseline graph traversal (variations and optimizations allowed) 
4. Avoid crawling to same pages using url canonicalization. Following are the canonicalization rules:
   - Convert the scheme and host to lower case: HTTP://www.Example.com/SomeFile.html → http://www.example.com/SomeFile.html
   - Remove port 80 from http URLs, and port 443 from HTTPS URLs: http://www.example.com:80 → http://www.example.com
   - Make relative URLs absolute: if you crawl http://www.example.com/a/b.html and find the URL ../c.html, it should canonicalize to http://www.example.com/c.html.
   - Remove the fragment, which begins with #: http://www.example.com/a.html#anything → http://www.example.com/a.html
   - Remove duplicate slashes: http://www.example.com//a.html → http://www.example.com/a.html

# Output
1. a xml file for each document with following format
   - root element - items
   - subitem - item
   - fields
      - docno - canonicalized url
      - http_header - url response headers
      - title - title of html page
      - text - text of html page
      - html_source - source code of html page
      - author - your name
      - depth - wave number in BFS
      - url - canonicalized url
 2. Maintain a separate inlinks and outlinks file. 
      - Outlinks - The first URL is a document you crawled, and the remaining URLs are out-links from the document
      - Inlinks - The first URL is a document you crawled, and the remaining URLs are in-links to the document

# Implementation
I used [scrapy](https://scrapy.org/) framework in python to achieve the desired objective.
1. Politeness
    - To obey robots.txt, add the following line to settings.py
    ```
      ROBOTSTXT_OBEY = True
    ```
    - To enable 1s delay between crawling pages from same domain, add the following line to settings.py
    ```
      DOWNLOAD_DELAY = 1
    ```
2. Crawling Strategy
    - BFS algorithm, add the following line to settings.py
    ```
      DEPTH_PRIORITY = 1
      SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
      SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
    ```
3. [Rules](https://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.spiders.CrawlSpider.rules)
    - For [crawler spider](https://doc.scrapy.org/en/latest/topics/spiders.html#crawlspider) to work, you need to define the 
      - [seed url's](https://github.com/Karan-GM/webcrawler/blob/master/crawler/spiders/seed_url.py)
      - [rules](https://github.com/Karan-GM/webcrawler/blob/master/crawler/spiders/rules.py) - a single rule or list of rules to extract links from websites. You can define one rule for one website which will define the logic of extracting links from a website.

4. Avoiding topic degradation
    - When you start crawling, it is very easy to move away from the core topic, as all links extracted from a website not necessarily are relevant.
    - From all the links extracted from a website, you can filter the links based on [keywords](https://github.com/Karan-GM/webcrawler/blob/master/crawler/spiders/keywords.txt)
      search and setting priority accordingly. to do this you need to add a [callback](https://github.com/Karan-GM/webcrawler/blob/master/crawler/spiders/custom.py) to rules in which you will set priority
      ``` python
      def request_filtering(self, request):
        is_relavant = self.factory.keywords.is_link_relavant(request.url, request.meta['link_text'])
        if(is_relavant['answer'] == True):
            request.priority = is_relavant['priority']
            return request
        else:
            return None
      ```
 5. To know from which page the links was extracted and to set the depth parameter(wave number in BFS), we override _requests_to_follow(https://github.com/Karan-GM/webcrawler/blob/master/crawler/spiders/custom.py)
    ``` python
    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                r.meta['parent_url'] = response.url
                r.meta['depth'] = response.meta['depth'] + 1
                yield rule.process_request(r)
    ```
  6. To set parameters for seed urls, and to enable start url's as part of deduplication(by default they are not considered), you need to override start_requests(https://github.com/Karan-GM/webcrawler/blob/master/crawler/spiders/custom.py)
     ``` python
        def start_requests(self):
        ## Set Seed URl priority
        self.start_time = self.factory.summary.set_start_time()
        seed_url_priority = len(self.factory.keywords.keywords)+1
        for url in self.start_urls:
            request = Request(url, priority=seed_url_priority)
            request.meta['parent_url'] = None
            request.meta['depth'] = 0
            request.meta['link_text'] = None
            yield request
     ```
     
   7. To stop after crawling 10000 documents, you need to enable signal catching in the spider((https://github.com/Karan-GM/webcrawler/blob/master/crawler/spiders/custom.py))
   ``` python
       @classmethod
      def from_crawler(cls, crawler, *args, **kwargs):
          spider = super(CustomSpider, cls).from_crawler(crawler, *args, **kwargs)
          crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
          return spider
   ```
   
      and raise the signal when you hit that number from the callback functions
      
   ``` python
      if self.factory.summary.get_count() > self.total_documents:
            self.logger.info('Exiting, as we have got sufficient documents')
            raise CloseSpider('Exiting, as we have got sufficient documents')
   ```
   8. To output one xml to each webpage crawled, define [items](https://doc.scrapy.org/en/latest/topics/items.html) and enable [pipelines](https://doc.scrapy.org/en/latest/topics/item-pipeline.html) in scrapy
      and make use of inbuilt [feed exporters](https://doc.scrapy.org/en/latest/topics/feed-exports.html)
      - To enable pipline, add the following line to settings.py
        ``` python
            ITEM_PIPELINES = {
               'crawler.pipelines.CrawlerPipeline': 300,
            }
        ```
      - Pipelines with feed exports [implementation](https://github.com/Karan-GM/webcrawler/blob/master/crawler/pipelines.py)
      
# setup
1. Clone the repository
	  - git clone https://github.com/Karan-GM/webcrawler.git
2. Cd into the directory
	  - cd webcrawler
3. Install Virtual environment tool
	  - pip install virtualenv
4. Create an virtual environment
	  - virtualenv webcrawler_env
5. Activate the virtual environment
	  - source webcrawler_env/bin/activate
6. Install the libraries from requirements file
	  - pip install -r requirements.txt
7. cd crawler/spiders
8. Create data and pickle folders for output dump
	  - mkdir data
	  - mkdir pickle
8. To start the program
    - scrapy crawl custom
