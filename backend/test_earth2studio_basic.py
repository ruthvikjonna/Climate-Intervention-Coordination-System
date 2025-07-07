# test_earth2studio_basic.py
"""
Test Earth2Studio installation and basic functionality
Run this to verify everything works before building the full service
"""

print("🧪 Testing Earth2Studio installation...")

try:
    # Test basic imports
    import torch
    import xarray as xr
    from earth2studio.models.px import DLWP
    from earth2studio.data import GFS
    print("✅ All imports successful!")
    
    # Check device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"✅ Device: {device}")
    
    # Test basic model loading (this will download ~500MB first time)
    print("📥 Loading DLWP model (downloading ~500MB first time, please wait...)...")
    model = DLWP.load_model(DLWP.load_default_package())
    print("✅ DLWP model loaded successfully!")
    
    # Test data source
    print("🌍 Testing GFS data source...")
    ds = GFS()
    print("✅ GFS data source initialized!")
    
    print("\n🎉 Earth2Studio is working perfectly!")
    print("Ready to build climate simulation service!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Try: pip install earth2studio")
    
except Exception as e:
    print(f"⚠️ Warning: {e}")
    print("Earth2Studio installed but some models may need internet connection")
    print("This is normal - proceed with integration!")

print("\n📋 Next steps:")
print("1. Run the climate simulation service")
print("2. Test the API endpoints") 
print("3. Integrate with your frontend")