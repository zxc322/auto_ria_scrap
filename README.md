# autoRiaScrap

### How to use
    docker-compose up --build


### Done. Script will be runing while `next_page` button is on page

You can change start url and docker mode (default=True) in main.py:
    
```
asyncio.get_event_loop().run_until_complete(Fetcher(start_url=start_url, docker_mode=docker_mode).run())
```

###### Check data on `localhost:5050`
