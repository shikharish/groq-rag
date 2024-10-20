Simple RAG pipeline using [Groq](https://groq.com/) and [llama-index](https://www.llamaindex.ai/)

- The database used here is just a bunch of scraped MetaKGP-Wiki pages. (`links.json` has the list of links to be scraped. `n_links` defined in `main.py` allows the first `n_links` to be scraped only. Currently set to 1 because the process is a bit slow.)

- Requires Python3.9+

- To run locally: 
```shell
$ pip3 install -r requirements.txt
$ python3 main.py
```

