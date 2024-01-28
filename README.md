# Words-API

This project was made for educational purposes. This API is hosted in [Vercel](https://vercel.com/).

## Endpoints

- Main URL: `words-api-zeta.vercel.app`

### Get a random word in Portuguese

#### Endpoint

- `/random`

#### Returns:

```
{
    "word": A random word,
    "uuid": An unique ID asssociated with the word
}
```

#### Possible errors:

```
500 - No words in the database
500 - DB Connection exception
```

### Find a word by uuid

#### Endpoint

- `/find_by_id/<string:id>`

#### Returns:

```
{
    "word": A specific word,
    "uuid": The uuid used in the search
}
```

#### Possible errors:

```
400 - Invalid UUID format
404 - The UUID isn't in the database
500 - DB Connection exception
```