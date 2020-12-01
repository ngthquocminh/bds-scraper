class CrawlHTML(object):
    """
    Crawl HTML of given links and also crawl all
    possible links which are not in given list
    @param queue is the provided list which is sent to queue
    @param result is list of all post links
    @param post_count is the number of post urls
    @param nonpost_count is the number of crawled non-post urls
    @param es is the ElasticSearch object
    """

    def __init__(self, given_list):
        pass

    def set_connection(self, url):
        """
        Return Beautifulsoup object
        """
        pass

    def check_if_url_is_post(self, url):
        """
        Check whether an url is post url (the last level url) or not
        """
        pass

    def check_url(self, url):
        """
        Check whether an url is valid or not
        """
        pass

    def get_html(self, url):
        """
        Get HTML (page source) of a given url
        """
        pass

    def main(self):
        """
        Set driver
        Step 1: Start with a queue of urls, retreive the first one
        Step 2: Check this url is valid or not
        Step 3: Set connection and retreive html of this url
        Step 4: Extract all urls from the content of the origin url
        Step 5: Check every urls which have already extracted,
        - Case 1: if this url is post url, check if it exist in result or not and add to this list
        - Case 2: It is not post url, check if it exists in queue or not, add to queue
        Step 6: Delete origin url and all checked urls
        Step 7: Check queue is empty or not come back to Step 1
        """
        pass

    def save_tocsv(self):
        """
        Save to csv, but it is not recommended
        """
        pass

    def save_to_elasticsearch(self, _type, url, html):
        pass
