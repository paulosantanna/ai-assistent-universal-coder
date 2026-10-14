# Frame and copy

`FrameStage` builds one frame per ranked video. The phrase uses the sentiment palette in the creative module. The source is fitted inside the frame. It is not cropped into a new shot.

`CopyStage` writes one description and up to five tags per publish network. Tags are tied to that video and platform-specific.

## Description & Tag Generation Per Platform

### TikTok (max 5 tags)
- **Description**: Sentiment-aware caption from creative palette
- **Tags**: Up to 5 TikTok-optimized hashtags
- **Format**: `#tag1 #tag2 #tag3 #tag4 #tag5`
- **Learning**: Tag performance tracked (usage frequency, engagement correlation)
- **Best practices**: Mix trending + niche + brand tags; rotate periodically to prevent fatigue

### Instagram Reels (max 5 tags)
- **Description**: Platform-appropriate caption (longer-form allowed)
- **Tags**: Up to 5 Instagram-optimized hashtags
- **Format**: `#tag1 #tag2 #tag3 #tag4 #tag5`
- **Learning**: Tag performance tracked within Instagram algorithm context
- **Best practices**: 3-5 tags optimal; first tag often most important for discovery; include brand-specific tags
- **Note**: Instagram may not clickable hashtags in Reels description same as feed posts

### YouTube Shorts (unlimited tags, but typically 3-5)
- **Description**: Must include `#Shorts` for Shorts classification
- **Tags**: Up to 15 recommended, 3-5 typically used for clarity
- **Format**: `#tag1 #tag2 #tag3 #Shorts` (must include `#Shorts`)
- **Learning**: Tag performance tracked via YouTube Analytics
- **Best practices**: `#Shorts` mandatory in first 3 lines of description; mix broad + specific tags; include misspellings/common variations for discovery

## Frame Generation Details

### One Frame Per Video
- **Rule**: Exactly one frame per ranked video
- **Purpose**: Thumbnail/preview image for posting metadata
- **Fitting**: Source video fitted inside frame; not cropped into new shot
- **Learning**: Frame selection quality evaluated (retention correlation, click-through rate)

### Sentiment Palette
- Creative module provides sentiment palette for description generation
- Palette adapted per platform tone (TikTok: casual/trending, Instagram: polished, YouTube: informative)
- Sentiment affects: word choice, emoji usage, caption length, call-to-action style
- Learning: Sentiment-combination correlation with performance metrics

### CopyStage Output Per Network

| Field | TikTok | Instagram | YouTube Shorts |
|-------|--------|-----------|----------------|
| **Max tags** | 5 | 5 | 3-5 (unlimited but typical) |
| **Description length** | Short, casual | Medium, polished | Medium, must include `#Shorts` |
| **Hashtag format** | `#tag1 #tag2 ...` | `#tag1 #tag2 ...` | `#tag1 #tag2 #Shorts` |
| **CTA included** | Often (e.g., "Watch this!") | Sometimes | Often (e.g., "Subscribe for more") |
| **Emoji usage** | High | Medium | Medium |
| **Learning tracked** | Tag performance, emoji correlation | Tag performance, hashtag discovery | Tag performance, `#Shorts` impact |

### ReviewStage & Gate System

`ReviewStage` and the stage gates record a verdict per piece: pass, revise, or fail.

- **Pass**: Description and tags acceptable as-is; proceed to publishing
- **Revise**: Minor adjustments needed (tag rotation, description tweak); re-evaluate before publishing
- **Fail**: Major issues (wrong platform, inappropriate content, missing requirements); stop and revise fundamentally

**A blocking gate stops the run.** Do not add a second caption or frame path.

### On-the-Desktop File Access

- Classified file can be downloaded when the video is selected
- Publishing still composes the final file at post time (not pre-rendered)
- Learning: Downloadable files enable manual review of frame quality and copy decisions

### Learning Integration Points

1. **Frame Selection Learning**: Which frames perform better (retention, CTR) fed back to improve frame generation
2. **Copy Learning**: Which description/tag combinations perform better per platform fed to improve CopyStage
3. **Sentiment Learning**: Which sentiment palettes perform better per platform fed to improve FrameStage
4. **Tag Learning**: Tag performance metrics (usage, engagement, discovery) stored per video for future pipeline runs
5. **Platform Adaptation**: Learning which platform combinations perform best (e.g., TikTok first, then cross-post to IG/YouTube)
