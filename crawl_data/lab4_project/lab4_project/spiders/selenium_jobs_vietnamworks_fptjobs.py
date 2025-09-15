import scrapy
class JobSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["vietnamworks.com", "fptjobs.com"]
    start_urls = [
        # VietnamWorks IT Software listing (stable route)
        "https://www.vietnamworks.com/tim-viec-lam/tim-tat-ca-viec-lam",
        # FPTJobs listing root
        "https://fptjobs.com/tuyen-dung"
    ]

    def start_requests(self):
        # Force Selenium on listings with scroll + wait to load dynamic links
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"selenium": True, "selenium_wait": 4, "selenium_scroll": 3}
            )

    def parse(self, response):
        # Collect all anchors then filter by pattern; works even if classes change
        hrefs = set([h.strip() for h in response.css("a::attr(href)").getall() if h.strip()])

        if "vietnamworks" in response.url:
            # VietnamWorks detail links vary; accept common forms
            domain_links = [h if h.startswith("http") else response.urljoin(h) for h in hrefs]
            job_links = [h for h in domain_links if "vietnamworks.com" in h and ("/job/" in h or "/viec-lam/" in h or "/jobs/" in h)]
            if not job_links:
                # Fallback: render listing with Selenium once
                yield response.request.replace(callback=self.parse_listing_selenium, meta={"selenium": True, "selenium_wait": 4, "selenium_scroll": 3})
                return
            for link in job_links:
                yield response.follow(link, callback=self.parse_vnw, meta={"selenium": True})
            # pagination: look for next page by rel or button text
            next_href = response.css("a[rel='next']::attr(href)").get() or response.xpath("//a[contains(., 'Next') or contains(., 'Sau') or contains(., '›')]/@href").get()
            if next_href:
                yield response.follow(next_href, callback=self.parse)

        elif "fptjobs" in response.url:
            # Prefer the overlay anchor links rendered in cards
            overlay_links = response.css("a.link-overlay::attr(href)").getall()
            if overlay_links:
                job_links = overlay_links
            else:
                # Fallback: pattern like /some-title-23273
                job_links = [h for h in hrefs if h.startswith("/") and h.count("-")>=1 and h.split("-")[-1].isdigit() and "Error" not in h]
            if not job_links:
                yield response.request.replace(callback=self.parse_listing_selenium, meta={"selenium": True, "selenium_wait": 4, "selenium_scroll": 3})
                return
            for link in job_links:
                yield response.follow(link, callback=self.parse_fpt, meta={"selenium": True})
            next_href = response.css("a[rel='next']::attr(href)").get() or response.xpath("//a[contains(., 'Sau') or contains(., 'Next') or contains(., '›')]/@href").get()
            if next_href:
                yield response.follow(next_href, callback=self.parse)

    def parse_listing_selenium(self, response):
        # Same as parse(), but this response is rendered by Selenium
        hrefs = set([h.strip() for h in response.css("a::attr(href)").getall() if h.strip()])

        if "vietnamworks" in response.url:
            job_links = [h for h in hrefs if "/job/" in h]
            for link in job_links:
                yield response.follow(link, callback=self.parse_vnw, meta={"selenium": True})
            next_href = response.css("a[rel='next']::attr(href)").get() or response.xpath("//a[contains(., 'Next') or contains(., 'Sau') or contains(., '›')]/@href").get()
            if next_href:
                yield response.follow(next_href, callback=self.parse, meta={})

        elif "fptjobs" in response.url:
            job_links = [h for h in hrefs if "/viec-lam/" in h and "Error" not in h]
            for link in job_links:
                yield response.follow(link, callback=self.parse_fpt, meta={"selenium": True})
            next_href = response.css("a[rel='next']::attr(href)").get() or response.xpath("//a[contains(., 'Sau') or contains(., 'Next') or contains(., '›')]/@href").get()
            if next_href:
                yield response.follow(next_href, callback=self.parse, meta={})

    def parse_vnw(self, response):
        # Title: prefer meta tag, then h1, fallback to first heading
        title = (response.xpath("//meta[@property='og:title']/@content").get(default="") or
                response.css("h1::text").get(default="") or 
                response.xpath("(//h1|//h2)[1]/text()").get(default="") or
                response.xpath("//title/text()").get(default="")).strip()
        
        # Company: try multiple selectors
        company = (response.css(".employer a::text").get(default="") or
                  response.xpath("//meta[@property='og:site_name']/@content").get(default="") or
                  response.xpath("//*[contains(@class, 'company') or contains(@class, 'employer')]//a/text()").get(default="")).strip()
        
        # Location: try multiple selectors
        location = (", ".join([t.strip() for t in response.css(".svg-icon-location ~ span::text").getall() if t.strip()]) or
                   ", ".join([t.strip() for t in response.xpath("//*[contains(@class, 'location')]//text()").getall() if t.strip()]) or
                   response.xpath("//*[contains(text(), 'Địa điểm') or contains(text(), 'Location')]/following::*[1]/text()").get(default="")).strip()
        
        # Salary: try multiple selectors
        salary = (response.css("span.salary::text").get(default="") or
                 response.xpath("//*[contains(@class, 'salary')]//text()").get(default="") or
                 response.xpath("//*[contains(text(), 'Mức lương') or contains(text(), 'Salary')]/following::*[1]/text()").get(default="") or
                 response.xpath("//span[contains(., '$') or contains(., 'VND') or contains(., 'USD')]/text()").get(default="")).strip()
        
        # Deadline: try multiple selectors
        deadline = (response.xpath("//span[contains(., 'Hạn nộp')]/text()").get(default="") or
                   response.xpath("//*[contains(text(), 'Deadline') or contains(text(), 'Hạn nộp')]/following::*[1]/text()").get(default="") or
                   response.xpath("//*[contains(@class, 'deadline') or contains(@class, 'expire')]//text()").get(default="")).strip()
        
        # Description: try multiple selectors
        description = (response.xpath("//meta[@property='og:description']/@content").get(default="") or
                      " ".join([t.strip() for t in response.css(".job-description *::text").getall() if t.strip()]) or
                      " ".join([t.strip() for t in response.xpath("//section[contains(., 'Mô tả') or contains(., 'Description')]//text()").getall() if t.strip()]) or
                      " ".join([t.strip() for t in response.xpath("//*[contains(@class, 'description') or contains(@class, 'content')]//text()").getall() if t.strip()])).strip()

        yield {
            "site": "Vietnamworks",
            "url": response.url,
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "deadline": deadline,
            "description": description
        }

    def parse_fpt(self, response):
        # Get title from meta tag or h1
        title = (response.xpath("//meta[@property='og:title']/@content").get(default="") or 
                response.css("h1::text").get(default="") or 
                response.xpath("//title/text()").get(default="")).strip()
        
        # Get company from meta or specific selectors
        company = (response.xpath("//meta[@property='og:site_name']/@content").get(default="") or
                  response.css(".company-title a::text").get(default="") or
                  response.xpath("//a[contains(@href, 'company')]/text()").get(default="")).strip()
        
        # Get location from multiple possible selectors
        location = (response.css(".card-location::text").get(default="") or
                   response.xpath("//span[contains(@class, 'card-location')]/text()").get(default="") or
                   ", ".join([t.strip() for t in response.css(".job-location span::text").getall() if t.strip()])).strip()
        
        # Get salary - look for salary-related elements
        salary = (response.xpath("//span[contains(@class, 'salary-icon')]/following-sibling::*[1]/text()").get(default="") or
                 response.xpath("//*[contains(text(), 'Mức lương')]/following::*[1]/text()").get(default="") or
                 response.xpath("//*[contains(., 'VND') or contains(., '$') or contains(., 'USD')]/text()").get(default="")).strip()
        
        # Get deadline
        deadline = (response.xpath("//span[contains(text(), 'Hạn nộp CV')]/following::*[1]/text()").get(default="") or
                   response.xpath("//*[contains(text(), 'Hạn nộp') or contains(text(), 'Deadline')]/following::*[1]/text()").get(default="") or
                   response.css(".expire-date::text").get(default="")).strip()
        
        # Get description from meta or content areas
        description = (response.xpath("//meta[@property='og:description']/@content").get(default="") or
                      " ".join([t.strip() for t in response.css(".job-description *::text").getall() if t.strip()]) or
                      " ".join([t.strip() for t in response.xpath("//section[contains(., 'Mô tả') or contains(., 'Description')]//text()").getall() if t.strip()])).strip()

        yield {
            "site": "FPTJobs",
            "url": response.url,
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "deadline": deadline,
            "description": description
        }
