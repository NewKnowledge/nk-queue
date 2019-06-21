# nk-queue client
Package for managing a variety of generic queue types including list queue / sorted queue and pub-sub messaging.

## Usage
The package exposes two methods for acquiring a queue instance: 'get_queue' and 'get_pub_sub_client'

get_queue:
```
def get_queue(
    queue_type,
    queue_name,
    host=HOST,
    port=PORT,
    auth_token=None,
    ssl=False,
    iterator_timeout=0,
):
```

**queue_type**: ['list', 'sorted'] (Any other option will throw an exception.

**queue_name**: Any non-null string value.  If the queue already exists, any future operatiosn will occurr against it. Otherwise a new queue is created.

**host/port/auth_token/ssl**: Connection properties, currently redis is the underlying infrastructure for this package. See config.py for defaults.

**iterator_timeout**: When a queue iterator is acquired, the timeout (in seconds) determines how long the iterator waits until a StopIteration() is raised.
1. 0 blocks indefinitley and is the default behavior.

get_queue:
```
def get_pub_sub_client(
    client_type, host, publisher_channels, subscription_channel, **kwargs
):
```

**client_type**: ['kafka'] (Any other option will throw an exception.

**host**: Pub-sub host to be used. As kafka is the only implementation currently, the kafka brokers will be passed in.

**publisher_channels**: Channels (Topcis) to publish to.

**subscription_channel**: Channels (Topcis) to subscribe / consume from.  Reading from the subscribed channel is a blocking call.

### List Queue - Implemented as a left to right FIFO queue.
Basic list queue usage see **test_list_queue.py** for further usage details.
Repositories consuming this package also show some higher level usage patterns:
1. https://github.com/NewKnowledge/tasking-common
2. https://github.com/NewKnowledge/task-polling-service
```
from nk_queue import get_queue

queue_name = "test_queue"

list_queue = get_queue(
    "list", queue_name, QUEUE_SERVER, QUEUE_PORT, QUEUE_AUTH_TOKEN, QUEUE_SSL, iterator_timeout=iterator_timeout
)

# Initializes connection to queue host.
list_queue.initialize()

# Write operations supported
queue_item = "queue item", "{"key": "value"}", 123  // Strings, integers, json etc.
list_queue.put(queue_item)
list_queue.remove_item(queue_item)

# Read operations supported
item = list_queue.get()
all_queue_items = list_queue.list_all()

# Transaction support 
list_queue.begin_transaction()
list_queue.put(queue_item)
list_queue.commit_transaction() / list_queue.abort_transaction()

# Iterator support ( See above for blocking / non-blocking configuration)
for message in list_queue:
    ...

```

### Scheduling Queue - Implemented as a sorted set.
Basic sorted queue usage see **test_test_scheduling_queue.py** for further usage details.
Repositories consuming this package also show some higher level usage patterns:
1. https://github.com/NewKnowledge/tasking-common
2. https://github.com/NewKnowledge/task-polling-service
```
from nk_queue import get_queue

queue_name = "test_queue"

schedule_queue = get_queue(
    "sorted", queue_name, QUEUE_SERVER, QUEUE_PORT, QUEUE_AUTH_TOKEN, QUEUE_SSL, iterator_timeout=iterator_timeout
)

# Initializes connection to queue host.
schedule_queue.initialize()

# Write operations supported
queue_item = "queue item", "{"key": "value"}", 123  // Strings, integers, json etc.
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

# Timestamp serves as a "score" and calls to "get_scheduled_items" will return queue items with a timestamp
#less than the current timestamp
schedule_queue.scheduled_item(timestamp, queue_item)
schedule_queue.remove_item(queue_item)

# Read operations supported
items = schedule_queue.get_scheduled_items()
all_queue_items = schedule_queue.list_all()

# Transaction support 
schedule_queue.begin_transaction()
schedule_queue.schedule_item(queue_item)
schedule_queue.commit_transaction() / list_queue.abort_transaction()
```

## Run Tests
```
docker-compose -f docker-compose-test.yml up --build
```

## TODO
1. Document exposed methods on all of the queue types
2. Further negative testing
3. Redis pub-sub client