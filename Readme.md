# Today Intel API Documentation

This repository contains the API documentation for the Today Intel app. 
The API is designed to provide various functionalities related to news, SEO analysis, NLP, videos, and more.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Request Examples](#request-examples)
- [Response Examples](#response-examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This API is the backend for the Today Intel app, providing endpoints for fetching news,
running SEO analysis, performing NLP tasks, and more. It adheres to the OpenAPI 3.1.0 specification.

## Getting Started

To get started with the Today Intel API, follow these steps:

1. Clone the repository.
2. Review the API documentation to understand available endpoints and their functionalities.
3. Set up the required dependencies.
4. Make requests to the API endpoints as needed.

For more details, refer to the [Terms of Service](https://todayintel.com/terms/) provided by [Stefan Laravel Developer](https://lzomedia.com).

## API Endpoints

- **POST /feed/reader:** Fetch news feed.
- **POST /feed/finder:** Find relevant feeds.
- **POST /run/scrapper:** Run a web scraper.
- **POST /jobs:** Searches fo jobs.
- **GET /google/trending:** Get trending Google searches.
- **POST /google/news/search:** Search Google News.
- **POST /google/news/topic:** Get news on a specific topic.
- **POST /seo/analyze:** Analyze SEO for a given link.
- **POST /seo/lighthouse:** Run Lighthouse SEO analysis.
- **POST /nlp/article:** Perform NLP analysis on an article.
- **POST /videos/youtube:** Search for videos on YouTube.
- **GET /:** Root endpoint.

For detailed information on request and response formats, refer to the OpenAPI specification in the `openapi.yaml` file.

## Request Examples

### Fetch News Feed
```json
{
  "link": "https://example.com/feed"
}
```

### Run SEO Analysis
```json
{
  "link": "https://example.com",
  "format": "json|html"
}
```
### Perform NLP Analysis
```json
{
  "link": "https://example.com/article"
}
```
## Response Examples

### Successful Response

```json
{
  "data": "..."
}
```

### Validation Error

  ```json
  {
  "detail": [
    {
      "loc": [],
      "msg": "Validation error message",
      "type": "error_type"
    }
  ]
}
  ```
