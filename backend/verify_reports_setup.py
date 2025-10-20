"""
Verify PDF Reports Setup
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def verify_setup():
    print("=" * 60)
    print("PDF REPORTS SETUP VERIFICATION")
    print("=" * 60)
    
    # 1. Check reportlab
    print("\n1. Checking reportlab installation...")
    try:
        import reportlab
        print(f"   ✅ reportlab installed (version {reportlab.Version})")
    except ImportError:
        print("   ❌ reportlab NOT installed - run: pip install reportlab")
        return
    
    # 2. Check database views
    print("\n2. Checking database views...")
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'brightbuy')
        )
        
        cursor = conn.cursor()
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        
        expected_views = [
            'quarterly_sales_report',
            'top_selling_products',
            'category_order_summary',
            'customer_order_payment_summary',
            'customer_summary_statistics'
        ]
        
        found_views = [v[0] for v in views]
        
        print(f"   ✅ Found {len(found_views)} views:")
        for view in found_views:
            status = "✅" if view in expected_views else "⚠️"
            print(f"      {status} {view}")
        
        missing = set(expected_views) - set(found_views)
        if missing:
            print(f"\n   ❌ Missing views: {', '.join(missing)}")
            print("   Run: python database/apply_report_views.py")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return
    
    # 3. Check reports module
    print("\n3. Checking reports module...")
    try:
        from app.routes import reports
        print("   ✅ Reports module loaded successfully")
    except Exception as e:
        print(f"   ❌ Error loading reports module: {e}")
        return
    
    # 4. Check routes registration
    print("\n4. Checking main.py configuration...")
    try:
        with open('app/main.py', 'r') as f:
            content = f.read()
            if 'from app.routes import reports' in content:
                print("   ✅ Reports import found in main.py")
            else:
                print("   ❌ Reports import missing in main.py")
            
            if 'app.include_router(reports.router)' in content:
                print("   ✅ Reports router registered in main.py")
            else:
                print("   ❌ Reports router not registered in main.py")
    except Exception as e:
        print(f"   ❌ Error checking main.py: {e}")
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    print("\n✅ Setup is complete! You can now:")
    print("   1. Start the server: python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8020")
    print("   2. Open: http://127.0.0.1:8020/docs")
    print("   3. Test the /reports endpoints")
    print("\n📚 Documentation:")
    print("   - PDF_REPORTS_DOCUMENTATION.md")
    print("   - REPORTS_QUICK_START.md")
    print("   - TEST_REPORTS_COMMANDS.md")

if __name__ == "__main__":
    verify_setup()
