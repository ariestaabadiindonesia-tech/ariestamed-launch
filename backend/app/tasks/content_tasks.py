from celery import shared_task
from app import db
from app.models import Content, Product
from app.services.ai_service import AIContentGenerator
import logging

logger = logging.getLogger(__name__)

ai_generator = AIContentGenerator()

@shared_task(bind=True)
def generate_content_ai(self, product_id, content_type, platform, tone='professional', length='medium'):
    """Generate content using AI based on product info"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return {"status": "error", "message": "Product not found"}
        
        # Prepare product context
        product_context = {
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": product.price,
            "features": product.features,
            "benefits": product.key_benefits,
            "target_audience": product.target_audience
        }
        
        # Generate content
        generated_content = ai_generator.generate(
            product=product_context,
            content_type=content_type,
            platform=platform,
            tone=tone,
            length=length
        )
        
        # Create content record
        content = Content(
            product_id=product_id,
            title=generated_content['title'],
            text=generated_content['text'],
            content_type=content_type,
            platform=platform,
            hashtags=generated_content.get('hashtags', []),
            call_to_action=generated_content.get('cta', ''),
            ai_generated=True,
            status='draft'
        )
        
        db.session.add(content)
        db.session.commit()
        
        logger.info(f"Generated AI content for product {product_id}: {content.id}")
        return {
            "status": "success",
            "content_id": content.id,
            "content": generated_content
        }
    except Exception as exc:
        logger.error(f"Error generating AI content: {str(exc)}")
        return {"status": "error", "message": str(exc)}

@shared_task(bind=True)
def generate_content_variations(self, content_id, num_variations=3):
    """Generate variations of existing content for different platforms"""
    try:
        content = Content.query.get(content_id)
        if not content:
            return {"status": "error", "message": "Content not found"}
        
        variations = ai_generator.generate_variations(
            content=content.text,
            platforms=['instagram', 'facebook', 'tiktok', 'youtube'],
            num_variations=num_variations
        )
        
        created_contents = []
        for platform, variant_text in variations.items():
            variant_content = Content(
                product_id=content.product_id,
                title=content.title,
                text=variant_text['text'],
                content_type=content.content_type,
                platform=platform,
                hashtags=variant_text.get('hashtags', content.hashtags),
                call_to_action=content.call_to_action,
                ai_generated=True,
                status='draft'
            )
            db.session.add(variant_content)
            created_contents.append(variant_content.id)
        
        db.session.commit()
        
        logger.info(f"Generated {len(created_contents)} content variations")
        return {"status": "success", "content_ids": created_contents}
    except Exception as exc:
        logger.error(f"Error generating content variations: {str(exc)}")
        return {"status": "error", "message": str(exc)}
