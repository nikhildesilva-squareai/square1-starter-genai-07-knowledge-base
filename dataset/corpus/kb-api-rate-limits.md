---
id: kb-api-rate-limits
title: API rate limits
updated: 2026-01-30
tags: [api, limits, developers]
---

# API rate limits

The Northwind Cloud API enforces per-organisation rate limits. Free and Team organisations are limited to 60 requests per minute; Business organisations are limited to 600 requests per minute. When you exceed the limit the API returns HTTP 429 with a Retry-After header. Use exponential backoff and honour Retry-After to recover gracefully.
