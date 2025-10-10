from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.product import Product
from app.models.category import Category
from app.models.variant import Variant, VariantAttributeValue, VariantAttribute
from app.schemas.product import ProductOut, ProductCreate
from app.schemas.variant import ProductWithVariantsOut, VariantOut, VariantAttributeOut

router = APIRouter(prefix="/products", tags=["Products"])

# Get all products with optional category filter
@router.get("/", response_model=List[ProductOut])
def get_products(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    category_name: Optional[str] = Query(None, description="Filter by category name"),
    db: Session = Depends(get_db)
):
    """
    Get all products, optionally filtered by category
    """
    try:
        print(f"🔍 get_products called with: category_id={category_id}, category_name={repr(category_name)}")
        query = db.query(Product)
        
        # Filter by category_id if provided
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        # Filter by category_name if provided
        elif category_name:
            # Debug: show all categories
            all_cats = db.query(Category).all()
            print(f"📋 Available categories: {[c.category_name for c in all_cats]}")
            
            category = db.query(Category).filter(Category.category_name == category_name).first()
            if category:
                print(f"✅ Found category: {repr(category.category_name)} (ID: {category.category_id})")
                query = query.filter(Product.category_id == category.category_id)
            else:
                print(f"❌ Category {repr(category_name)} not found in database")
                return []  # Return empty list if category not found
        
        products = query.all()
        print(f"📦 Returning {len(products)} products")
        return products
    
    except Exception as e:
        print(f"❌ Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Get a single product by ID
@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a specific product by ID
    """
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Create a new product (for future use)
@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product
    """
    try:
        # Check if category exists
        category = db.query(Category).filter(Category.category_id == product.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
        
        new_product = Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        return new_product
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Get product with all variants and their attributes
@router.get("/{product_id}/variants/", response_model=ProductWithVariantsOut)
def get_product_with_variants(product_id: int, db: Session = Depends(get_db)):
    """
    Get a product with all its variants and variant attributes
    """
    try:
        # Get product
        product = db.query(Product).filter(Product.product_id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get all variants for this product
        variants = db.query(Variant).filter(Variant.product_id == product_id).all()
        
        # Build response with variants and their attributes
        product_data = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "category_id": product.category_id,
            "description": product.description,
            "category": {
                "category_id": product.category.category_id,
                "category_name": product.category.category_name
            } if product.category else None,
            "variants": []
        }
        
        # Process each variant
        for variant in variants:
            # Get all attribute values for this variant
            attr_values = (
                db.query(VariantAttributeValue, VariantAttribute)
                .join(VariantAttribute, VariantAttributeValue.attribute_id == VariantAttribute.attribute_id)
                .filter(VariantAttributeValue.variant_id == variant.variant_id)
                .all()
            )
            
            # Build attributes list
            attributes = [
                {
                    "attribute_name": attr.attribute_name,
                    "value": attr_val.value
                }
                for attr_val, attr in attr_values
            ]
            
            # Add variant to list
            product_data["variants"].append({
                "variant_id": variant.variant_id,
                "variant_name": variant.variant_name,
                "product_id": variant.product_id,
                "price": variant.price,
                "quantity": variant.quantity,
                "SKU": variant.SKU,
                "attributes": attributes
            })
        
        return product_data
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching product with variants: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
