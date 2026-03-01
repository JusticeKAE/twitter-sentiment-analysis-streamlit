# Project Challenges and Solutions  

## Twitter Sentiment Analysis Project  

---

## Overview  

This document outlines the technical challenges encountered during the development of the Twitter Sentiment Analysis application and the solutions implemented to overcome them.

---

# Challenge 1: Twitter Data Fetching Limitations  

## Initial Approach  

The original plan was to implement two main features:

1. **Single Tweet Analysis** – Users input individual tweets for sentiment analysis.  
2. **User-based Analysis** – Users input a Twitter username to fetch and analyze their recent tweets.

---

## Problems Encountered  

### Ntscraper Limitations  

When using the `ntscraper` library (a web scraping tool for Twitter), several issues were encountered:

- Rate limiting from Twitter’s servers  
- Inconsistent data retrieval  
- Frequent blocking of scraping attempts  
- Limited number of tweets that could be fetched  
- No guarantee of data availability  

---

### Twitter API Restrictions  

An attempt was made to switch to the official Twitter API v2, but the following challenges arose:

- **Free Tier**
  - Extremely limited access  
  - Allowed posting tweets but not fetching them  

- **Basic Tier**
  - Required paid subscription (~$100/month)  
  - Needed for tweet fetching capabilities  

- **Academic Access**
  - Required institutional verification  
  - Limited to research institutions  

- **Enterprise Tier**
  - Prohibitively expensive for a personal project  

---

# Solution Implemented  

## CSV File Upload Alternative  

To overcome the data fetching limitations while maintaining project functionality:

### Added CSV Upload Functionality  

- Users can upload tweet data in CSV format  
- System processes multiple tweets at once  
- Enables batch sentiment analysis  

---

## Required CSV Format  

```csv
tweet_text
"This is my first tweet text"
"Another tweet example here"
"Multiple tweets can be analyzed at once"
```

---

## Benefits of This Approach

- ✓ **No API costs**
- ✓ **No rate limiting**
- ✓ **Works with any volume of data**
- ✓ **Users can collect tweets manually or via other tools**
- ✓ **Ideal for batch processing and testing**
- ✓ **Sustainable for long-term use**

---

# Challenge 2: Data Consistency

## Issue

When fetching tweets directly, there was no guarantee of:

- Tweet freshness
- Data format consistency
- Complete tweet metadata

## Solution

Using CSV upload gives users full control over:

- ✓ Which tweets to analyze
- ✓ Data format and quality
- ✓ Timeframe of tweets
- ✓ Data validation before upload

---

# Challenge 3: Scalability

## Issue

Direct API calls and scraping:

- Become slower with more requests
- Risk IP blocking
- Depend on external rate limits

## Solution

CSV processing enables:

- ✓ Batch processing of large datasets
- ✓ Offline analysis capability
- ✓ No server-side rate limiting
- ✓ Faster processing times

---

# Current Features (Post-Solution)

## Direct Text Input

- Enter individual tweets
- Instant sentiment analysis
- Quick sentiment checks

## CSV File Upload

- Upload multiple tweets at once
- Batch sentiment analysis
- Download results in CSV format

---

# Future Considerations

- Implement paid Twitter API tier (if budget permits)
- Integrate alternative social media APIs
- Add support for additional formats (JSON, Excel)

---

# Recommendations for Future Developers

If working on a similar project, consider:

## Budget Planning

If real-time Twitter data is required, allocate budget for API costs.

## Alternative Data Sources

- Pre-collected datasets (e.g., Kaggle)
- Academic Twitter access (if eligible)
- Other social media platforms with free APIs
- Synthetic data generation for testing

## Scraping Alternatives

If scraping:

- Use rotating proxies
- Respect rate limits
- Implement fallback mechanisms

## CSV Upload Advantage

The CSV upload feature provides:

- Greater flexibility
- Better batch testing capability
- Independence from external API restrictions

---

# Conclusion

Although the initial plan of direct Twitter integration faced significant challenges due to API costs and scraping limitations, implementing the CSV file upload functionality proved to be a **robust, scalable, and cost-effective alternative**.

This approach preserves the core functionality of sentiment analysis while giving users greater control over their data.

---

## Note

> ⚠️ **Important for Future Development**  
> If you're developing a similar project, carefully evaluate Twitter API costs and limitations before committing to integration. For development and testing phases, the CSV approach may be more practical and sustainable.
