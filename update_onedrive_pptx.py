import os, sys
import win32com.client

def main():
    src_path = os.path.abspath(r"C:\GitHub\l-data-seT---ML\Comprehensive_Viva_Crop_Fertilizer_ML.pptx")
    target_path = os.path.abspath(r"C:\Users\ROSHNI\OneDrive\Documents\GitHub\l-data-seT---ML\Comprehensive_Viva_Crop_Fertilizer_ML.pptx")
    
    print(f"[INFO] Source file: {src_path}")
    print(f"[INFO] Target file: {target_path}")
    
    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    try:
        # Open target presentation
        # WithWindow=False (0)
        pres = ppt_app.Presentations.Open(target_path, 0, 0, 0)
        print(f"[INFO] Opened target presentation. Initial slide count: {pres.Slides.Count}")
        
        # 1. Replace Slide 27:
        # Insert after slide 26 (becomes slide 27)
        # Old slide 27 shifts to slide 28
        pres.Slides.InsertFromFile(src_path, 26, 27, 27)
        print(f"[INFO] Inserted new slide 27. Slide count is now: {pres.Slides.Count}")
        pres.Slides(28).Delete()
        print(f"[INFO] Deleted old slide 27 (was at index 28). Slide count is now: {pres.Slides.Count}")
        
        # 2. Replace Slide 30:
        # Insert after slide 29 (becomes slide 30)
        # Old slide 30 shifts to slide 31
        pres.Slides.InsertFromFile(src_path, 29, 30, 30)
        print(f"[INFO] Inserted new slide 30. Slide count is now: {pres.Slides.Count}")
        pres.Slides(31).Delete()
        print(f"[INFO] Deleted old slide 30 (was at index 31). Slide count is now: {pres.Slides.Count}")
        
        # Save presentation
        pres.Save()
        print("[SUCCESS] Target presentation saved successfully via PowerPoint COM!")
        pres.Close()
    finally:
        ppt_app.Quit()

if __name__ == "__main__":
    main()
