import news_api_client as client

def basic_test():
    news = client.getNewsFromSources()
    print (news)
    assert len(news) > 0




if __name__ == "__main__":
    basic_test()