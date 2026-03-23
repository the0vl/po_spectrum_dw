{{
    config(
        materialized='view',
    )
}}

with source as (
    select * from {{ source('raw_reddit_posts', 'stg_reddit_posts') }}
),

reddit_posts as (
    select
        id,
        title,
        selftext,
        score,
        num_comments,
        created_utc,
        created_at,
        subreddit,
        author,
        url,
        permalink,
        keyword,
        is_self,
        over_18,
        processed_at,
        source_file
    from source
)

select * from reddit_posts
