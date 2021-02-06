## Development

Clone repository

```bash
$ git clone https://github.com/missing-pet/server.git
```

Change directory

```bash
$ cd server/
```

Create the following files from templates

```
.env
app/conf/credentials.py
app/conf/local_settings.py
```

Build docker image

```bash
$ docker-compose up --build
```
