import time
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
load_dotenv()
print("🔑 OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

import folium
from dotenv import load_dotenv

# optional: load .env file in project root
load_dotenv()

# If you want AI, set OPENAI_API_KEY in env (or .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Import openai only if API key present (avoid error if not installed)
if OPENAI_API_KEY:
  import openai
openai.api_key = OPENAI_API_KEY



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Sample points (fallback)
DESTINATIONS = [
    {"name": "Sapa - Ruộng bậc thang", "lat": 22.3400, "lon": 103.8442,
     "img": ":https://www.google.com/url?sa=i&url=https%3A%2F%2Fbaovinhlong.com.vn%2Fphong-su-ky-su%2F201910%2Fky-vi-ruong-bac-thang-sa-pa-2971557%2F&psig=AOvVaw23EKfdLmU43C9tZr0Z_XNL&ust=1760603286334000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCJDI_MTkpZADFQAAAAAdAAAAABAE",
     "desc": "Ngắm ruộng bậc thang tuyệt đẹp, khám phá văn hóa người H’Mông."},
    {"name": "Fansipan - Nóc nhà Đông Dương", "lat": 22.2956, "lon": 103.7768,
     "img": "https://bvhttdl.gov.vn/kham-pha-mua-may-dep-nhat-nam-tren-noc-nha-dong-duong-20241115113924526.htm",
     "desc": "Chinh phục đỉnh Fansipan hoặc đi cáp treo ngắm mây trời."},
    {"name": "Mộc Châu - Đồi chè", "lat": 21.6175, "lon": 104.7417,
     "img": "https://plo.vn/moc-chau-dep-ngo-ngang-voi-nhung-doi-che-xanh-bat-ngan-post741566.html",
     "desc": "Thưởng thức trà xanh, check-in đồi chè, và khám phá bản làng yên bình."},
    {"name": "Mai Châu - Bản Lác", "lat": 20.7396, "lon": 105.2376,
     "img": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Mai_Chau_valley.jpg",
     "desc": "Khám phá nhà sàn, ẩm thực và văn hóa người Thái."},
    {"name": "Điện Biên - Đồi A1", "lat": 21.3860, "lon": 103.0190,
     "img": "https://upload.wikimedia.org/wikipedia/commons/1/13/Dien_Bien_Phu_Memorial.jpg",
     "desc": "Tham quan đồi A1, hầm Đờ Cát, tìm hiểu lịch sử Điện Biên Phủ."},
]

def generate_map_html(points, fname_prefix="map"):
    """Tạo folium map lưu vào static/, trả về đường dẫn relative để nhúng iframe"""
    # Center map on average coords
    avg_lat = sum(p['lat'] for p in points) / len(points)
    avg_lon = sum(p['lon'] for p in points) / len(points)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=8)
    for i, p in enumerate(points, start=1):
        folium.Marker(
            [p['lat'], p['lon']],
            popup=f"{i}. {p.get('name')}",
            tooltip=p.get('name')
        ).add_to(m)
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"{fname_prefix}_{ts}.html"
    out_path = os.path.join("static", "maps")
    os.makedirs(out_path, exist_ok=True)
    fullpath = os.path.join(out_path, fname)
    m.save(fullpath)
    return f"/static/maps/{fname}"

def call_openai_generate(location, days, pref):
    """Gọi OpenAI để yêu cầu trả về JSON itinerary. Nếu lỗi trả None."""
    if not OPENAI_API_KEY:
        return None

    prompt = f"""
Bạn là một trợ lý du lịch. Sinh một lịch trình du lịch cho vùng Tây Bắc Việt Nam.
Yêu cầu xuất ra **CHỈ** JSON theo định dạng: một mảng các objects.
Mỗi object có: name (tên địa điểm), lat (vĩ độ số), lon (kinh độ số), desc (mô tả ngắn), img (link ảnh).
Các items sao cho phù hợp cho {days} ngày, ưu tiên chủ đề: {pref}.
Trả ra JSON hợp lệ (không giải thích).
"""
    try:
        # ChatCompletion
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            max_tokens=800,
            temperature=0.8,
            timeout=30
        )
        text = resp["choices"][0]["message"]["content"].strip()
        # Tr attempt to parse JSON — model instructed to return JSON only
        # Some models may wrap with ``` so try to extract JSON block
        # find first { or [
        start = text.find('[')
        if start != -1:
            text = text[start:]
        # ensure valid JSON
        data = json.loads(text)
        # Basic validation: list of dicts with lat/lon
        if isinstance(data, list) and all(('name' in d and 'lat' in d and 'lon' in d) for d in data):
            return data
    except Exception as e:
        print("OpenAI generate error:", e)
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/plan", methods=["GET","POST"])
def plan():
    if request.method == "POST":
        # Form-based submission (safer)
        days = int(request.form.get("days", 3))
        pref = request.form.get("pref", "khám phá thiên nhiên")
        use_ai = request.form.get("use_ai") == "on"
    else:
        # GET fallback for quick testing: /plan?days=3
        days = int(request.args.get("days", 3))
        pref = request.args.get("pref", "khám phá thiên nhiên")
        use_ai = request.args.get("use_ai", "false").lower() == "true"

    points = None
    if use_ai:
        points = call_openai_generate("Tây Bắc Việt Nam", days, pref)

    # fallback if AI missing or failed
    if not points:
        # pick first `days` entries from DESTINATIONS (or random)
        chosen = random.sample(DESTINATIONS, min(days, len(DESTINATIONS)))
        # convert to expected keys
        points = [{"name": d["name"], "lat": d["lat"], "lon": d["lon"], "desc": d.get("desc",""), "img": d.get("img","")} for d in chosen]

    # create folium map and get url
    map_url = generate_map_html(points, fname_prefix="tbn_map")
    return render_template("plan.html", plan=points, map_url=map_url, days=days, used_ai=use_ai)
# ---------------- AI Chat Route ----------------
from flask import jsonify
from openai import OpenAI

@app.route("/chat")
def chat_page():
    """Trang giao diện chat AI"""
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask_ai():
    """API hỏi đáp du lịch bằng AI"""
    if not OPENAI_API_KEY:
        return jsonify({"error": "Chưa cấu hình OpenAI API key"}), 400

    data = request.get_json()
    question = data.get("question", "")
    if not question.strip():
        return jsonify({"error": "Câu hỏi trống"}), 400

    try:
        # ✅ Dùng cú pháp mới của openai>=1.0
        client = OpenAI(api_key=OPENAI_API_KEY)

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là hướng dẫn viên du lịch vùng Tây Bắc Việt Nam, nói chuyện thân thiện, gợi ý du lịch hấp dẫn."},
                {"role": "user", "content": question}
            ],
            temperature=0.8,
            max_tokens=400,
        )

        answer = resp.choices[0].message.content.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        print("AI error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # debug True helpful while developing
    app.run(debug=True)
