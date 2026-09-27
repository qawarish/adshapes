# Builds curtain.svg. Pass a logo file path as argv[1] to place it behind the curtain.
import sys, base64, mimetypes
NAVY, GREY, WHITE = "#103b5e", "#e0e0e0", "#ffffff"
logo = sys.argv[1] if len(sys.argv) > 1 else None

curtain = ("M470,480 L1578,480 L1584,1262 "
           "C1500,1250 1384,1212 1304,1170 C1284,1160 1268,1152 1256,1152 "
           "C1236,1162 1192,1262 1122,1360 C1072,1432 1020,1468 960,1480 "
           "C890,1494 830,1478 760,1492 C690,1506 620,1480 550,1494 "
           "C520,1500 490,1494 466,1488 Z")

# fold lines: (path, width) — gather toward the lifted hem near the nib
folds = [
 ("M548,486 C560,720 526,1000 548,1240 C556,1350 540,1430 552,1490", 3.2),
 ("M636,486 C650,600 672,720 662,860", 2.4),
 ("M716,486 C700,740 740,1020 718,1250 C708,1360 726,1430 720,1488", 3.4),
 ("M818,486 C840,680 806,880 828,1080 C842,1230 824,1380 834,1482", 2.8),
 ("M902,486 C894,570 912,650 902,740", 2.2),
 ("M972,486 C990,730 950,960 984,1170 C1000,1280 1000,1380 990,1470", 3.2),
 ("M1060,486 C1074,720 1070,920 1100,1090 C1120,1200 1150,1270 1170,1300", 3.0),
 ("M1148,486 C1156,640 1144,760 1160,880", 2.2),
 ("M1214,486 C1232,720 1212,920 1236,1040 C1246,1100 1252,1130 1254,1146", 3.4),
 ("M1320,486 C1340,700 1330,900 1306,1030 C1292,1100 1274,1130 1264,1148", 2.8),
 ("M1430,486 C1416,680 1444,880 1420,1010 C1400,1100 1330,1140 1276,1156", 3.0),
 ("M1512,486 C1526,720 1504,960 1522,1110 C1532,1190 1556,1230 1578,1254", 2.6),
]

# pen drawn along +x with nib tip at origin, then rotated into place
pen = f"""
<g transform="translate(1262,1160) rotate(66.5)" stroke-linejoin="round">
 <g fill="{NAVY}" stroke="{GREY}" stroke-width="7" paint-order="stroke">
  <path d="M0,0 C18,-3 44,-10 72,-12 L72,12 C44,10 18,3 0,0 Z"/>
  <path d="M70,-13 L150,-16 C152,-16 153,-15 153,-13 L153,13 C153,15 152,16 150,16 L70,13 Z"/>
  <path d="M154,-17 L500,-17 C514,-17 522,-9 522,0 C522,9 514,17 500,17 L154,17 Z"/>
  <path d="M332,-18 L336,-27 L488,-27 C494,-27 496,-24 494,-20 L490,-18 Z"/>
 </g>
 <g fill="none" stroke="{WHITE}" stroke-width="2.4" stroke-linecap="round">
  <path d="M10,0 L50,0"/><circle cx="55" cy="0" r="3.4"/>
  <path d="M72,-11 L72,11"/><path d="M300,-16 L300,16"/><path d="M308,-16 L308,16"/>
  <path d="M342,-23 L484,-23"/>
 </g>
 <circle cx="338" cy="-24" r="6" fill="{NAVY}" stroke="{GREY}" stroke-width="4" paint-order="stroke"/>
</g>"""

# small curl of hem draped over the nib tip, drawn in front of the pen
curl = (f'<g transform="translate(-34,-82)"><path d="M1262,1236 C1276,1206 1302,1196 1322,1206 C1330,1214 1326,1230 1312,1238 '
        f'C1296,1246 1276,1246 1262,1236 Z" fill="{NAVY}" stroke="{GREY}" stroke-width="6" paint-order="stroke"/>'
        f'<path d="M1272,1232 C1286,1214 1304,1210 1316,1216" fill="none" stroke="{WHITE}" stroke-width="2.4" stroke-linecap="round"/></g>')

logo_el = ""
if logo:
    data = base64.b64encode(open(logo, "rb").read()).decode()
    mime = mimetypes.guess_type(logo)[0] or "image/png"
    # box sits behind the lifted hem; only its lower-left corner shows through the opening
    logo_el = f'<image href="data:{mime};base64,{data}" x="1090" y="960" width="460" height="460" preserveAspectRatio="xMidYMid meet"/>'

fold_el = "".join(f'<path d="{d}" stroke-width="{w}"/>' for d, w in folds)
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="2048" viewBox="0 0 2048 2048">
<rect width="2048" height="2048" fill="{GREY}"/>
{logo_el}
<path d="{curtain}" fill="{NAVY}"/>
<g fill="none" stroke="{WHITE}" stroke-linecap="round">{fold_el}</g>
{pen}
{curl}
</svg>"""
open("curtain.svg", "w").write(svg)
