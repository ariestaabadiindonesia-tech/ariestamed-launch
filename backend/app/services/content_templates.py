import yaml
import os

class ContentTemplates:
    """Content templates for different platforms and content types"""
    
    TEMPLATES = {
        'instagram': {
            'caption': """
🎯 [HOOK]

[VALUE PROP]
✨ Key benefits:
• {benefit_1}
• {benefit_2}
• {benefit_3}

💡 [CALL TO ACTION]

{hashtags}
            """,
            'story': """
{emoji} {main_text}

→ Tap to learn more!
            """,
            'reels': """
[ATTENTION GRABBER]

[MAIN MESSAGE]

[CTA] - Link in bio! {emoji}

{hashtags}
            """
        },
        'facebook': {
            'post': """
{emoji} {headline}

{description}

✅ Benefits:
→ {benefit_1}
→ {benefit_2}
→ {benefit_3}

{cta_button}

{hashtags}
            """,
            'ad': """
Attention {audience}! 👇

{pain_point}?

Try {product_name}:
{features_list}

[LEARN MORE] - Limited offer!
            """
        },
        'tiktok': {
            'caption': """
{hook} 🔥

{trend_element}

{cta} #FYP #ForYouPage
{hashtags}
            """,
            'trend': """
{trending_audio_desc}

[Text overlay]
{main_message}

{hashtags}
            """
        },
        'youtube': {
            'description': """
{product_name}

{intro_text}

✨ What You'll Get:
{features_list}

🔗 Resources & Links:
→ Website: {link}
→ {social_platform_1}: {social_link_1}
→ {social_platform_2}: {social_link_2}

⏰ Timestamps:
0:00 - Intro
{timestamps}

📌 Tags:
{hashtags}
            """
        }
    }
    
    @staticmethod
    def get_template(platform: str, content_type: str = None):
        """Get template for platform and content type"""
        if platform in ContentTemplates.TEMPLATES:
            templates = ContentTemplates.TEMPLATES[platform]
            if content_type and content_type in templates:
                return templates[content_type]
            # Return first available template for platform
            return next(iter(templates.values()))
        return None
    
    @staticmethod
    def render_template(platform: str, content_type: str, variables: dict) -> str:
        """Render template with variables"""
        template = ContentTemplates.get_template(platform, content_type)
        if not template:
            return ""
        
        # Replace variables
        rendered = template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))
        
        return rendered
