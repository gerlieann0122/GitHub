"""
Marketing Video Generator - Claude + Higgsfield Integration

This script generates marketing videos using Claude AI to create prompts
and Higgsfield API to generate the actual video content.
"""

import os
import json
import requests
from typing import Optional
import anthropic

# Initialize clients
HIGGSFIELD_API_KEY = os.getenv("HIGGSFIELD_API_KEY")
HIGGSFIELD_API_URL = "https://api.higgsfield.ai/v1"

# Supported video models
SUPPORTED_MODELS = {
    "seedance": "Seedance 2.0 - Best for cinematic marketing videos",
    "soul": "Soul 2.0 - Great for product showcases",
    "kling": "Kling 3.0 - Fast turnaround for social media",
}


def generate_marketing_prompt(
    product_name: str,
    product_description: str,
    target_audience: str,
    video_style: str = "cinematic",
    duration: str = "15-30 seconds",
) -> str:
    """
    Use Claude to generate a detailed video prompt for marketing content.
    
    Args:
        product_name: Name of the product
        product_description: Description of what the product does
        target_audience: Who this video is for
        video_style: Style of video (cinematic, energetic, minimal, professional)
        duration: Desired video length
    
    Returns:
        Generated video prompt ready for Higgsfield
    """
    client = anthropic.Anthropic()
    
    prompt = f"""You are a creative director for high-end marketing videos. 
    Generate a detailed, cinematic video prompt for Higgsfield AI that will be used 
    to create a marketing video.

    Product: {product_name}
    Description: {product_description}
    Target Audience: {target_audience}
    Style: {video_style}
    Duration: {duration}

    Create a vivid, production-ready prompt that includes:
    1. Scene composition and camera movements
    2. Visual elements and aesthetics
    3. Color palette and mood
    4. Text overlays or graphics descriptions
    5. Specific shots and transitions

    Make it detailed enough for AI video generation but concise enough to work well.
    Focus on what will resonate with the target audience."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    
    return message.content[0].text


def generate_video_with_higgsfield(
    prompt: str,
    model: str = "seedance",
    aspect_ratio: str = "16:9",
) -> Optional[dict]:
    """
    Send the prompt to Higgsfield API to generate the video.
    
    Args:
        prompt: The video generation prompt
        model: Video model to use (seedance, soul, kling)
        aspect_ratio: Video aspect ratio (16:9, 9:16, 1:1)
    
    Returns:
        API response with video generation details
    """
    if not HIGGSFIELD_API_KEY:
        print("⚠️  HIGGSFIELD_API_KEY not set. Returning mock response.")
        return mock_higgsfield_response(prompt, model)
    
    headers = {
        "Authorization": f"Bearer {HIGGSFIELD_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "prompt": prompt,
        "model": model,
        "aspect_ratio": aspect_ratio,
        "duration": 30,  # seconds
    }
    
    try:
        response = requests.post(
            f"{HIGGSFIELD_API_URL}/generate/video",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Higgsfield API error: {e}")
        return None


def mock_higgsfield_response(prompt: str, model: str) -> dict:
    """Return a mock response for testing without API key."""
    return {
        "status": "pending",
        "job_id": "job_marketing_123456",
        "model": model,
        "prompt": prompt[:100] + "...",
        "estimated_time": "2-5 minutes",
        "message": "Video generation queued. Check status with job_id.",
    }


def create_marketing_video(
    product_name: str,
    product_description: str,
    target_audience: str,
    video_style: str = "cinematic",
    model: str = "seedance",
) -> dict:
    """
    Complete workflow: Generate prompt with Claude, then create video with Higgsfield.
    
    Args:
        product_name: Product name
        product_description: What the product does
        target_audience: Target audience for the marketing video
        video_style: Visual style preference
        model: Higgsfield video model to use
    
    Returns:
        Dictionary with generation details
    """
    print(f"🎬 Creating marketing video for: {product_name}")
    print(f"   Target Audience: {target_audience}")
    print(f"   Style: {video_style}")
    
    # Step 1: Generate prompt with Claude
    print("\n📝 Step 1: Generating video prompt with Claude...")
    video_prompt = generate_marketing_prompt(
        product_name=product_name,
        product_description=product_description,
        target_audience=target_audience,
        video_style=video_style,
    )
    print(f"✅ Generated prompt:\n{video_prompt}\n")
    
    # Step 2: Send to Higgsfield for video generation
    print(f"🎥 Step 2: Submitting to Higgsfield ({model})...")
    result = generate_video_with_higgsfield(video_prompt, model=model)
    
    if result:
        print(f"✅ Video generation started!")
        print(f"   Job ID: {result.get('job_id')}")
        print(f"   Status: {result.get('status')}")
        print(f"   Estimated time: {result.get('estimated_time')}")
    else:
        print("❌ Failed to start video generation")
    
    return {
        "product_name": product_name,
        "video_prompt": video_prompt,
        "higgsfield_response": result,
        "model_used": model,
    }


def generate_upc_ad_variants(
    product_name: str,
    product_description: str,
    num_variants: int = 3,
) -> list:
    """
    Generate multiple marketing video variants for A/B testing.
    
    Args:
        product_name: Product name
        product_description: Product description
        num_variants: Number of variants to generate
    
    Returns:
        List of video generation jobs
    """
    client = anthropic.Anthropic()
    
    styles = ["cinematic", "energetic", "minimalist", "luxury", "playful"][:num_variants]
    audiences = ["Gen Z", "Professionals", "Families"][:num_variants]
    
    variants = []
    
    for i, (style, audience) in enumerate(zip(styles, audiences), 1):
        print(f"\n🎬 Generating variant {i}/{num_variants} ({style} for {audience})...")
        result = create_marketing_video(
            product_name=product_name,
            product_description=product_description,
            target_audience=audience,
            video_style=style,
            model="seedance",
        )
        variants.append(result)
    
    return variants


# Example usage
if __name__ == "__main__":
    # Example 1: Single marketing video
    print("=" * 60)
    print("MARKETING VIDEO GENERATOR")
    print("=" * 60)
    
    result = create_marketing_video(
        product_name="CloudSync Pro",
        product_description="Enterprise cloud storage solution with AI-powered organization",
        target_audience="Tech-savvy business professionals",
        video_style="cinematic",
        model="seedance",
    )
    
    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    
    # Example 2: Generate A/B testing variants (uncomment to use)
    # print("\n" + "=" * 60)
    # print("GENERATING A/B TEST VARIANTS")
    # print("=" * 60)
    # variants = generate_upc_ad_variants(
    #     product_name="CloudSync Pro",
    #     product_description="Enterprise cloud storage solution with AI-powered organization",
    #     num_variants=3,
    # )
    # print(json.dumps(variants, indent=2))
