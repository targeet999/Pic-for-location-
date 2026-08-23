import os
import time
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_full_metadata(image_path):
    print("\n[!] BYPASSING SECURITY...")
    time.sleep(1)
    
    image_path = image_path.strip().strip("'").strip('"')

    if not os.path.exists(image_path):
        print(f"[X] ERROR: File not found! Check path.")
        return

    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        if not exif_data:
            print("[!] WARNING: No EXIF/Metadata found in this image.")
            return

        print("[*] Data extracted. Decrypting...\n")
        time.sleep(0.5)
        
        device_info = {}
        basic_info = {}
        camera_settings = {}
        gps_info = {}

        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            
            if tag_name in ["Make", "Model", "Software"]:
                device_info[tag_name] = value
            elif tag_name in ["DateTime", "DateTimeOriginal", "ExifImageWidth", "ExifImageHeight"]:
                basic_info[tag_name] = value
            elif tag_name in ["ExposureTime", "FNumber", "ISOSpeedRatings", "FocalLength"]:
                camera_settings[tag_name] = value
            elif tag_name == "GPSInfo":
                for key in value:
                    sub_tag = GPSTAGS.get(key, key)
                    gps_info[sub_tag] = value[key]

        print("--- [ DEVICE DATA (PHONE/CAMERA) ] ---")
        if device_info:
            for k, v in device_info.items(): print(f"  > {k}: {v}")
        else:
            print("  > No device data found.")

        print("\n--- [ CAPTURE DETAILS ] ---")
        if basic_info:
            for k, v in basic_info.items(): print(f"  > {k}: {v}")
        else:
            print("  > No capture details found.")

        print("\n--- [ LENS SETTINGS ] ---")
        if camera_settings:
            for k, v in camera_settings.items(): print(f"  > {k}: {v}")
        else:
            print("  > No lens data found.")

        print("\n--- [ LOCATION (GPS) ] ---")
        if gps_info:
            def dms_to_decimal(dms, ref):
                degrees, minutes, seconds = float(dms[0]), float(dms[1]), float(dms[2])
                decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
                return -decimal if ref in ['S', 'W'] else decimal

            try:
                lat = dms_to_decimal(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
                lon = dms_to_decimal(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
                maps_link = f"https://www.google.com/maps?q={lat},{lon}"

                print("  [!] TARGET LOCATED!")
                print(f"  > Latitude  : {lat}")
                print(f"  > Longitude : {lon}")
                print(f"  > Maps Link : {maps_link}")
            except KeyError:
                print("  > Partial GPS data, cannot pinpoint.")
        else:
            print("  > Location data missing or GPS was OFF.")

        print("\n[!] ANALYSIS COMPLETE.")

    except Exception as e:
        print(f"[X] ERROR: {e}")

if __name__ == "__main__":
    print("""
    ██╗  ██╗██████╗ ██╗███████╗██╗  ██╗    ██████╗ ███████╗██╗   ██╗
    ██║ ██╔╝██╔══██╗██║██╔════╝██║  ██║    ██╔══██╗██╔════╝██║   ██║
    █████╔╝ ██████╔╝██║███████╗███████║    ██║  ██║█████╗  ██║   ██║
    ██╔═██╗ ██╔══██╗██║╚════██║██╔══██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║  ██╗██║  ██║██║███████║██║  ██║    ██████╔╝███████╗ ╚████╔╝ 
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝  ╚═══╝  
               [ OSINT METADATA SCANNER v2.0 ]
    """)
    
    photo_path = input("krish_dev@mainframe:~# Enter photo path: ")
    extract_full_metadata(photo_path)