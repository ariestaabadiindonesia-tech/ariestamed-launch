import os
import openai
from typing import Dict, List, Any
from datetime import datetime
import json

class AIContentGenerator:
    """AI-powered content generation service using OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        openai.api_key = self.api_key
    
    def generate(self, product: Dict, content_type: str, platform: str, 
                 tone: str = 'professional', length: str = 'medium') -> Dict[str, Any]:
        """
        Generate content for a product
        
        Args:
            product: Product information dict
            content_type: Type of content (caption, post, story, video_desc)
            platform: Target platform (youtube, instagram, facebook, tiktok)
            tone: Writing tone (professional, casual, humorous, emotional)
            length: Content length (short, medium, long)
        
        Returns:
            Dict with generated content
        """
        
        # Build product description
        product_desc = self._build_product_description(product)
        
        # Get platform-specific guidelines
        platform_guidelines = self._get_platform_guidelines(platform, content_type)
        
        # Build prompt
        prompt = self._build_prompt(
            product_desc, content_type, platform, tone, length, platform_guidelines
        )
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional social media content creator and marketing expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse response
        content = response['choices'][0]['message']['content']
        return self._parse_generated_content(content, platform)
    
    def generate_variations(self, content: str, platforms: List[str], 
                          num_variations: int = 3) -> Dict[str, List[str]]:
        """
        Generate content variations for different platforms
        
        Args:
            content: Original content text
            platforms: List of target platforms
            num_variations: Number of variations per platform
        
        Returns:
            Dict with variations per platform
        """
        
        variations = {}
        
        for platform in platforms:
            platform_guidelines = self._get_platform_guidelines(platform)
            
            prompt = f"""
            Take this content and adapt it for {platform} following these guidelines:
            {platform_guidelines}
            
            Original content:
            {content}
            
            Generate {num_variations} variations that:
            1. Maintain the core message
            2. Use platform-specific best practices
            3. Include relevant hashtags
            4. Add platform-specific formatting
            
            Format your response as JSON with this structure:
            {{
                "variations": [
                    {{
                        "text": "variation text here",
                        "hashtags": ["#tag1", "#tag2"]
                    }}
                ]
            }}
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media content expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content_text = response['choices'][0]['message']['content']
            try:
                parsed = json.loads(content_text)
                variations[platform] = parsed['variations']
            except:
                variations[platform] = [{"text": content_text, "hashtags": []}]
        
        return variations
    
    def optimize_for_platform(self, content: str, platform: str) -> Dict[str, Any]:
        """
        Optimize content for a specific platform
        
        Args:
            content: Original content
            platform: Target platform
        
        Returns:
            Optimized content with platform recommendations
        """
        
        guidelines = self._get_platform_guidelines(platform)
        
        prompt = f"""
        Optimize this content for {platform}:
        
        {content}
        
        Guidelines:
        {guidelines}
        
        Provide:
        1. Optimized text
        2. Recommended hashtags (max 5)
        3. Best posting time (hour)
        4. Recommended media type
        5. Call-to-action suggestion
        
        Format as JSON.
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a social media optimization expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        try:
            return json.loads(response['choices'][0]['message']['content'])
        except:
            return {"optimized_text": response['choices'][0]['message']['content']}
    
    def _build_product_description(self, product: Dict) -> str:
        """Build a comprehensive product description from product dict"""
        desc = f"""
        Product: {product.get('name', '')}
        Description: {product.get('description', '')}
        Category: {product.get('category', '')}
        Price: ${product.get('price', 0)}
        Target Audience: {product.get('target_audience', '')}
        
        Key Features:
        """
        
        features = product.get('features', [])
        if isinstance(features, list):
            for feature in features:
                desc += f"\n- {feature}"
        
        desc += "\n\nKey Benefits:\n"
        benefits = product.get('benefits', [])
        if isinstance(benefits, list):
            for benefit in benefits:
                desc += f"\n- {benefit}"
        
        return desc
    
    def _get_platform_guidelines(self, platform: str, content_type: str = None) -> str:
        """
        Get platform-specific content guidelines
        """
        guidelines = {
            'youtube': """
            - Video descriptions should be 200-5000 characters
            - Include timestamps for longer videos
            - Use first 50 characters wisely (visible in search)
            - Include CTA at beginning and end
            - Add links to playlist and related content
            - Best hashtags: 3-5 relevant tags
            """,
            'instagram': """
            - Captions: 125-150 characters work best (but can go up to 2200)
            - Use 3-5 relevant hashtags
            - Include emoji for visual interest
            - First line should hook the reader
            - CTA should be clear (Link in bio, DM us, etc)
            - Post at peak hours: 11am-1pm, 7pm-9pm
            """,
            'facebook': """
            - Posts should be 40-80 characters for best engagement
            - Use line breaks for readability
            - Include 5-10 relevant hashtags
            - Encourage interaction (ask questions)
            - Link posts perform better than image posts
            - Best time: Tue-Fri 1pm-3pm
            """,
            'tiktok': """
            - Captions: 150 characters max (with urgency)
            - Use trendy hashtags (#FYP, #ForYou)
            - Add 3-5 hashtags related to content
            - Emoji increase engagement
            - Hook viewers in first 3 seconds
            - Call-to-action critical
            - Best times: 6am-10am, 7pm-11pm
            """
        }
        
        return guidelines.get(platform, "")
    
    def _build_prompt(self, product_desc: str, content_type: str, platform: str,
                     tone: str, length: str, guidelines: str) -> str:
        """
        Build the prompt for OpenAI
        """
        
        length_guidance = {
            'short': 'Keep it brief (50-100 words)',
            'medium': 'Aim for 100-200 words',
            'long': 'Create comprehensive content (200+ words)'
        }
        
        prompt = f"""
        Create a {content_type} for {platform} with a {tone} tone.
        
        Product Information:
        {product_desc}
        
        Platform Guidelines:
        {guidelines}
        
        Requirements:
        - {length_guidance.get(length, length_guidance['medium'])}
        - Tone: {tone}
        - Platform: {platform}
        - Content Type: {content_type}
        - Make it engaging and conversion-focused
        - Include a clear call-to-action
        
        Format your response as JSON with this structure:
        {{
            "title": "Content title/heading",
            "text": "Main content text",
            "hashtags": ["#tag1", "#tag2", "#tag3"],
            "cta": "Call to action",
            "emojis": ["emoji1", "emoji2"]
        }}
        """
        
        return prompt
    
    def _parse_generated_content(self, content: str, platform: str) -> Dict[str, Any]:
        """
        Parse generated content from AI response
        """
        try:
            # Try to extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback to simple parsing
        return {
            "title": "Generated Content",
            "text": content,
            "hashtags": [],
            "cta": "Learn more and get started today!",
            "emojis": []
        }
