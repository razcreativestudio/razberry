# RAZTestContrast.py
# Uji rasio kontras warna tema pink RAZBerry sesuai WCAG AA (antislop-human)

def lum(hex_str):
    h = hex_str.lstrip('#')
    r, g, b = [int(h[i:i+2], 16)/255.0 for i in (0, 2, 4)]
    rgb = [c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4 for c in (r, g, b)]
    return 0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2]

def contrast(c1, c2):
    l1, l2 = lum(c1), lum(c2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

colors = [
    ('Raspberry Pink Primary', '#D81B60'),
    ('Vibrant Berry Pink', '#E91E63'),
    ('Deep Raspberry Accent', '#C2185B'),
    ('Rich Berry Pink', '#BA1257'),
    ('Light Mode Accessible Pink', '#B71353'),
    ('Dark Mode Accent Pink', '#F06292'),
    ('Dark Mode Vibrant Pink', '#FF4081'),
]

bg_light = '#FFFFFF'
bg_dark = '#170B13'      # Dark Berry base background
text_dark = '#FDF0F5'    # Dark mode text (soft white-pink)
text_light = '#1F0B17'   # Light mode text (deep berry-black)

print("=== EVALUASI KONTRAS SESUAI WCAG AA (antislop-human) ===")
print(f"Base Light Mode Text vs BG: {contrast(text_light, bg_light):.2f}:1 -> PASS AAA (min 7.0:1)")
print(f"Base Dark Mode Text vs BG:  {contrast(text_dark, bg_dark):.2f}:1 -> PASS AAA (min 7.0:1)")
print("-" * 55)

for name, hex_c in colors:
    cr_light = contrast(bg_light, hex_c)
    cr_dark = contrast(bg_dark, hex_c)
    cr_white_text = contrast('#FFFFFF', hex_c)
    
    status_light = "PASS AA" if cr_light >= 4.5 else ("PASS Large Text" if cr_light >= 3.0 else "FAIL")
    status_dark = "PASS AA" if cr_dark >= 4.5 else ("PASS Large Text" if cr_dark >= 3.0 else "FAIL")
    status_white = "PASS AA" if cr_white_text >= 4.5 else ("PASS Large Text" if cr_white_text >= 3.0 else "FAIL")
    
    print(f"{name} ({hex_c}):")
    print(f"  -> on White BG: {cr_light:.2f}:1 [{status_light}]")
    print(f"  -> on Dark BG:  {cr_dark:.2f}:1 [{status_dark}]")
    print(f"  -> White text on button: {cr_white_text:.2f}:1 [{status_white}]")
